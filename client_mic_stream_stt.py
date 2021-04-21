import pyaudio
import websocket
from halo import Halo

spinner = Halo(text='Microphone streaming STT with WebSocket: ', text_color='cyan', spinner='spin')
websocket = websocket.WebSocket()
websocket.connect('ws://0.0.0.0:8000/api/stt/mic')

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
sample_rate = 16000

pa = pyaudio.PyAudio()
stream = pa.open(format=sample_format,
                 channels=channels,
                 rate=sample_rate,
                 input=True,
                 frames_per_buffer=chunk)
stream.start_stream()
try:
    while True:
        data = stream.read(chunk)
        spinner.start()
        websocket.send_binary(data)
        result = websocket.recv()
        print(f' {result}')
except KeyboardInterrupt:
    websocket.close()
    stream.stop_stream()
    stream.close()
    pa.terminate()
    print()
    print('Microphone streaming is finished')
