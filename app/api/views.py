import json
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

from sanic import response
from sanic.exceptions import InvalidUsage
from sanic.log import logger
from sanic.response import json as sanic_json, HTTPResponse
from sanic_jwt import protected

from app import app_bp
from app.api import api_bp
from app.api.engine import SpeechToTextEngine
from app.responses import SttResponse

stt_engine = SpeechToTextEngine()
executor = ThreadPoolExecutor()


@app_bp.route('')
async def index(request):
    return response.text('DeepSpeech REST API says Hello')


@api_bp.route('/stt/http', methods=['POST'])
@protected()
async def transcribe_with_http(request) -> HTTPResponse:
    """ Transcription route using HTTP. """

    current_app = request.app

    # The audio to be transcribed
    audio = request.files.get('audio')

    # The hot-words with their boosts to be used for transcribing the audio
    data = request.form

    all_hot_words = []
    if data:
        all_hot_words = stt_engine.add_hot_words(data)
    if not audio:
        raise InvalidUsage('Audio not provided')
    inference_start = perf_counter()

    # Running the transcription
    text = await current_app.loop.run_in_executor(executor, lambda: stt_engine.run(audio.body))
    inference_end = perf_counter() - inference_start

    # Logging on the prompt the outcome of the transcription process
    logger.info('----------------------------------------------------------------------------')
    logger.info(json.dumps(SttResponse(text, inference_end).__dict__))
    logger.info('----------------------------------------------------------------------------')

    # Explicitly erasing a hot-word from the language model (even though they are removed when the request is done)
    stt_engine.erase_hot_word(all_hot_words)
    return sanic_json(SttResponse(text, inference_end).__dict__)


async def transcribe_with_ws(request, websocket) -> None:
    """ Transcription route using a WebSocket. """

    all_hot_words = []
    current_app = request.app
    while True:
        try:
            data = await websocket.recv()
            if isinstance(data, str):
                data = json.loads(data)

                if data:
                    all_hot_words = stt_engine.add_hot_words(data)
                continue
            if isinstance(data, bytes):
                inference_start = perf_counter()
                text = await current_app.loop.run_in_executor(executor, lambda: stt_engine.run(data))
                inference_end = perf_counter() - inference_start
                await websocket.send(json.dumps(SttResponse(text, inference_end).__dict__))
                logger.warning(f'Received {request.method} request at {request.path}')
                stt_engine.erase_hot_word(all_hot_words)
        except Exception as ex:
            logger.warning(f'{request.method} request failure at {request.path}. Exception is: {str(ex)}')
            await websocket.send(json.dumps(SttResponse('Audio not provided').__dict__))
        await websocket.close()


api_bp.add_websocket_route(transcribe_with_ws, '/stt/ws')
