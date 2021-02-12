import json
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

from sanic import response
from sanic.exceptions import InvalidUsage
from sanic.log import logger
from sanic.response import json as sanic_json
from sanic.views import HTTPMethodView
from sanic_jwt import protected

from app.api import api_bp
from app.api.engine import SpeechToTextEngine
from app.responses import SttResponse, HotWordResponse

stt_engine = SpeechToTextEngine()
executor = ThreadPoolExecutor()


@api_bp.route('')
async def index(request):
    return response.text('DeepSpeech REST API says Hello')


class HotWordView(HTTPMethodView):
    """ Implementation of create and delete of hot words with usage of Class-Based views """
    decorators = [protected()]

    async def post(self, request):
        """ Implementation of create of a hot word. """
        try:
            data = request.args or request.json
            keys = data.keys()
            word = list(keys)[0]
            if word:
                boost = data.get(word)
                results = stt_engine.add_hot_word(word, float(boost))
                return sanic_json(HotWordResponse(results).__dict__)
            else:
                return sanic_json(HotWordResponse('Forgot to provide the hot-word?').__dict__)
        except AttributeError:
            return sanic_json(HotWordResponse('Forgot to provide the hot-word?').__dict__)

    async def delete(self, request):
        """ Implementation of delete of a hot word. """
        try:
            keys = request.args.keys() or request.json.keys()
            word = list(keys)[0]
            results = stt_engine.erase_hot_word(word)
            return sanic_json(HotWordResponse(results).__dict__)
        except AttributeError:
            return sanic_json(HotWordResponse('The boost of hot-word is missing.').__dict__)


api_bp.add_route(HotWordView.as_view(), '/hw')


# Route for erasing all hot words
@api_bp.route('/hw/delete/', methods=['DELETE'])
@protected()
async def delete_all_hot_words(request):
    results = stt_engine.clear_hot_words()
    return sanic_json(HotWordResponse(results).__dict__)


# HTTP route for speech to text
@api_bp.route('/stt/http', methods=['GET', 'POST'])
@protected()
async def transcribe_with_http(request):
    current_app = request.app
    speech = request.files.get('speech')
    if not speech:
        raise InvalidUsage('Speech audio not provided')
    inference_start = perf_counter()
    text = await current_app.loop.run_in_executor(executor, lambda: stt_engine.run(speech.body))
    inference_end = perf_counter() - inference_start
    logger.info('-----------------------------------------------------------------')
    logger.info(json.dumps(SttResponse(text, inference_end).__dict__))
    logger.info('-----------------------------------------------------------------')
    return sanic_json(SttResponse(text, inference_end).__dict__)


# WebSocket route for speech to text
async def transcribe_with_ws(request, websocket):
    current_app = request.app
    while True:
        try:
            speech = await websocket.recv()
            inference_start = perf_counter()
            text = await current_app.loop.run_in_executor(executor, lambda: stt_engine.run(speech))
            inference_end = perf_counter() - inference_start
            await websocket.send(json.dumps(SttResponse(text, inference_end).__dict__))
            logger.warning(f'Received {request.method} request at {request.path}')
        except Exception as ex:
            logger.warning(f'{request.method} request failure at {request.path}. Exception is: {str(ex)}')
            await websocket.send(json.dumps(SttResponse('Speech audio not provided').__dict__))
        await websocket.close()


api_bp.add_websocket_route(transcribe_with_ws, '/stt/ws')
