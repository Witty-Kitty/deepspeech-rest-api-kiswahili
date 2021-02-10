import websocket

websocket = websocket.WebSocket()
websocket.connect('ws://0.0.0.0:8000/api/stt/ws')

try:
    with open('2830-3980-0043.wav', mode='rb') as file:
        audio = file.read()
        websocket.send_binary(audio)
        result = websocket.recv()
        print(result)
        websocket.close()
except Exception as ex:
    print(ex)
