import click_spinner
import websocket

websocket = websocket.WebSocket()
websocket.connect('ws://0.0.0.0:5000/api/stt/ws')

try:
    print('Performing speech-to-text with WebSocket...')
    with click_spinner.spinner():
        with open('audio/8455-210777-0068.wav', mode='rb') as file:
            websocket.send('{"power":1000, "paris":-1000}')
            audio = file.read()
            websocket.send_binary(audio)
            result = websocket.recv()
            print()
            print(result)
            websocket.close()
except Exception as ex:
    print(ex)
