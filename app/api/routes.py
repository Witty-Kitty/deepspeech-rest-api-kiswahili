import json
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

import numpy as np
from sanic import response, Sanic
from sanic.exceptions import InvalidUsage
from sanic.log import logger
from sanic.request import Request
from sanic.response import json as sanic_json, HTTPResponse
from sanic_jwt import protected
from websocket import WebSocketConnectionClosedException

from app import app_bp
from app.api import api_bp
from app.api.engine import SpeechToTextEngine
from app.responses import SttResponse

sanic_app = Sanic.get_app(name='DeepSpeech REST API')

stt_engine = SpeechToTextEngine()
executor = ThreadPoolExecutor()


@app_bp.route('')
async def index(request: Request) -> HTTPResponse:
    return response.html('<h1>DeepSpeech REST API says Hello &#128075;&#127998;</h1>')


@api_bp.route('/stt/http', methods=['POST'])
@protected()
async def transcribe_audio_http(request: Request) -> HTTPResponse:
    """ Audio file transcription route using HTTP. """

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
    text = await sanic_app.loop.run_in_executor(executor, lambda: stt_engine.run(audio.body))
    inference_end = perf_counter() - inference_start

    # Logging on the prompt the outcome of the transcription process
    logger.info('----------------------------------------------------------------------------')
    logger.info(json.dumps(SttResponse(text, inference_end).__dict__))
    logger.info('----------------------------------------------------------------------------')

    # Explicitly erasing a hot-word from the language model (even though they are removed when the request is done)
    stt_engine.erase_hot_word(all_hot_words)
    return sanic_json(SttResponse(text, inference_end).__dict__)


async def transcribe_audio_ws(request, websocket) -> None:
    """ Audio file transcription route using a WebSocket. """

    all_hot_words = []
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
                text = await sanic_app.loop.run_in_executor(executor, lambda: stt_engine.run(data))
                inference_end = perf_counter() - inference_start
                await websocket.send(json.dumps(SttResponse(text, inference_end).__dict__))
                logger.warning(f'Received {request.method} request at {request.path}')
                stt_engine.erase_hot_word(all_hot_words)
        except WebSocketConnectionClosedException as wex:
            logger.warning(f'Exception is: {str(wex)}')
            await websocket.send(json.dumps(SttResponse('Websocket connection closed').__dict__))
        except Exception as ex:
            logger.warning(f'{request.method} request failure at {request.path}. Exception is: {str(ex)}')
            await websocket.send(json.dumps(SttResponse('Audio not provided').__dict__))
        await websocket.close()


api_bp.add_websocket_route(transcribe_audio_ws, '/stt/ws')


async def transcribe_mic_stream(request, websocket):
    """ Speech input transcription from microphone using WebSocket."""

    stream = stt_engine.deep_stream()
    while True:
        data = await websocket.recv()
        frames = stt_engine.frame_generator(audio=data)
        if isinstance(data, bytes):
            for frame in frames:
                stream.feedAudioContent(np.frombuffer(frame.bytes, np.int16))
                text = stream.intermediateDecode()
                await websocket.send(text)
        else:
            pass


api_bp.add_websocket_route(transcribe_mic_stream, '/stt/mic')
