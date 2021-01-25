import json
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

from sanic import response
from sanic.exceptions import InvalidUsage
from sanic.log import logger
from sanic.response import json as sanic_json

from app import app_bp
from app.api import api_bp
from app.api.engine import SpeechToTextEngine
from app.responses import SttResponse, HotWordResponse

stt_engine = SpeechToTextEngine()
executor = ThreadPoolExecutor()


@app_bp.route('')
async def index(request):
    return response.text('DeepSpeech REST API says Hello')


# HTTP route for speech to text
@api_bp.route('/v1/stt/http/', methods=['GET', 'POST'])
async def speech_to_text_http(request):
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
async def speech_to_text_websocket(request, websocket):
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


api_bp.add_websocket_route(speech_to_text_websocket, '/v1/stt/ws/')


# Route for adding a hot word
@api_bp.route('/v1/hw/add/', methods=['POST', ])
async def add_hot_word(request):
    data = request.args or request.json
    keys = data.keys()
    hw = list(keys)[0]
    boost = data.get(hw)
    results = stt_engine.add_hot_word(hw, float(boost))
    return sanic_json(HotWordResponse(results).__dict__)


# Route for erasing a hot word
@api_bp.route('/v1/hw/delete/', methods=['GET'])
async def delete_hot_word(request):
    keys = request.args.keys() or request.json.keys()
    hw = list(keys)[0]
    results = stt_engine.erase_hot_word(hw)
    return sanic_json(HotWordResponse(results).__dict__)
