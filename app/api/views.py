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
from app.responses import Response

stt_engine = SpeechToTextEngine()
executor = ThreadPoolExecutor()


@app_bp.route('')
async def index(request):
    return response.text('DeepSpeech RW API says Hello')


# HTTP route for the API
@api_bp.route('/v1/http', methods=['GET', 'POST'])
async def speech_to_text_http(request):
    current_app = request.app
    speech = request.files.get('speech')
    if not speech:
        raise InvalidUsage('Speech audio not provided')
    inference_start = perf_counter()
    text = await current_app.loop.run_in_executor(executor, lambda: stt_engine.run(speech.body))
    inference_end = perf_counter() - inference_start
    logger.info('-----------------------------------------------------------------')
    logger.info(json.dumps(Response(text, inference_end).__dict__))
    logger.info('-----------------------------------------------------------------')
    return sanic_json(Response(text, inference_end).__dict__)


# WebSocket route for the API
async def speech_to_text_websocket(request, websocket):
    current_app = request.app
    while True:
        try:
            speech = await websocket.recv()
            inference_start = perf_counter()
            text = await current_app.loop.run_in_executor(executor, lambda: stt_engine.run(speech))
            inference_end = perf_counter() - inference_start
            await websocket.send(json.dumps(Response(text, inference_end).__dict__))
            logger.warning(f'Received {request.method} request at {request.path}')
        except Exception as ex:
            logger.warning(f'{request.method} request failure at {request.path}. Exception is: {str(ex)}')
            await websocket.send(json.dumps(Response('Speech audio not provided').__dict__))
        await websocket.close()


api_bp.add_websocket_route(speech_to_text_websocket, '/v1/ws')
