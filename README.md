# DeepSpeech REST API

[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![Python 3.6](https://upload.wikimedia.org/wikipedia/commons/a/a5/Blue_Python_3.8_Shield_Badge.svg)](https://www.python.org/downloads/release/python-380/)

---

This REST API is built on top of Mozilla's [DeepSpeech](https://github.com/mozilla/DeepSpeech). It is written based on
[examples](https://github.com/mozilla/DeepSpeech-examples) provided by Mozilla.

It accepts HTTP methods such as GET and POST as well as WebSocket. To perform transcription using HTTP methods is
appropriate for relatively short audio files while the WebSocket can be used even for longer audio recordings.


----

## Project setup

- 1. Clone the repository to your local machine and change directory to _deepspeech-rest-api_

```shell
git clone https://github.com/fabricekwizera/deepspeech-rest-api.git && cd deepspeech-rest-api 
```

- 2. Create a virtual environment and activate it (assuming that it is installed your machine)
and install the project in editable mode (locally).

```shell
 virtualenv -p python3 venv && source venv/bin/activate && pip install --editable .
```

- 3. Download the model and the scorer. For English model and scorer, follow below links

```shell
wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.1/deepspeech-0.9.1-models.pbmm -O deepspeech_model.pbmm
wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.1/deepspeech-0.9.1-models.scorer -O deepspeech_model.scorer
```

For other languages, you can place them in the current working directory under the names _deepspeech_model.pbmm_ for the
model and _deepspeech_model.scorer_ for the scorer.

- 4. Migrations are done using [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment)

- 5. Running the server 
```shell
python3 run.py
```
## Usage

----

#### Register a new user and request a new token to access the API

```shell
curl -X POST -H "Content-Type: application/json" -d '{"username": "forrestgump", "email": "fgump@yourdomain.com", "password": "yourpassword"}' http://0.0.0.0:8000/users
```

to get a token 

```shell
curl -H "Content-Type: application/json" -d '{"username": "forrestgump", "password": "yourpassword"}' http://localhost:8000/auth
```

If both steps are done correctly, you should get a token in below format

```shell
{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MTI5MDkxNTZ9.HbmcCwm1CM3sQMV5D8_EueyuIYuAAC0Z9baH0-k35Ws"}
```

With this token, you have access to different endpoints of the API.

#### Sending STT (speech-to-text) requests to server

- STT the HTTP way
```shell
curl -X POST -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MTI5MDkxNTZ9.HbmcCwm1CM3sQMV5D8_EueyuIYuAAC0Z9baH0-k35Ws" -F "speech=@2830-3980-0043.wav" http://0.0.0.0:8000/api/stt/http
```

- STT the WebSocket way (simple test)

WebSockets don't support _curl_. To take advantage of this feature, you will have to write a web app to send request to <span style="color:yellow">_ws://0.0.0.0:8000/api/stt/ws_</span>
```shell
python3 test_websocket.py
```

```shell
{"message": "experience proves this", "time": 1.4718825020026998}
```

#### Hot-words

- Add a hot-word

```shell
curl -X POST -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MTI5MDkxNTZ9.HbmcCwm1CM3sQMV5D8_EueyuIYuAAC0Z9baH0-k35Ws" -d '{"football": 1.56}' http://0.0.0.0:8000/api/hw/
```

Output

```shell
{"message":" 'football' hot-word with boost '1.56' was added."}
```

- Erase a hot-word

```shell
curl -X DELETE -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MTI5MDkxNTZ9.HbmcCwm1CM3sQMV5D8_EueyuIYuAAC0Z9baH0-k35Ws" -d '{"football": ""}' http://0.0.0.0:8000/api/hw/
```

Output

```shell
{"message":" 'football' hot-word was erased."}
```

- Erase all hot-words

```shell
curl -X DELETE -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MTI5MDkxNTZ9.HbmcCwm1CM3sQMV5D8_EueyuIYuAAC0Z9baH0-k35Ws" http://0.0.0.0:8000/api/hw/delete/
```

Output

```shell
{"message":"All hot-words were erased."}
```