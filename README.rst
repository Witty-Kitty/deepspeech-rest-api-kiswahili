DeepSpeech REST API
===================

.. start-badges

.. list-table::
    :widths: 15 85
    :stub-columns: 1

    * - Build
      - | |Open| |Coverage|
    * - Docs
      - | |Documentation|
    * - Package
      - | |PyPI version|

.. |Documentation| image:: https://img.shields.io/badge/user%20guide-sanic-ff0068
   :target: https://sanicframework.org/en/
.. |PyPI version| image:: https://img.shields.io/pypi/pyversions/google-cloud-speech.svg
   :target: https://img.shields.io/pypi/pyversions/google-cloud-speech.svg
.. |Open| image:: https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/
    :target: https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/
.. |Coverage| image:: https://codecov.io/gh/fabricekwizera/deepspeech-rest-api/branch/master/graph/badge.svg?token=RWBRSCLNN4
      :target: https://codecov.io/gh/fabricekwizera/deepspeech-rest-api


.. end-badges

This REST API is built on top of Mozilla's `DeepSpeech`_. It is written based on `examples`_  provided by Mozilla. It accepts HTTP methods such as GET and POST as well as WebSocket. To perform transcription using HTTP methods is
appropriate for relatively short audio files while the WebSocket can be used even for longer audio recordings.

.. _DeepSpeech: https://github.com/mozilla/DeepSpeech
.. _examples: https://github.com/mozilla/DeepSpeech-examples


Getting started
~~~~~~~~~~~~~~~

Below instructions are for Unix/OS X, they will have to be changed to be able to run the code on Windows.

1. Clone the repository to your local machine and change directory to ``deepspeech-rest-api``

.. code-block:: console

    $ git clone https://github.com/fabricekwizera/deepspeech-rest-api.git
    $ cd deepspeech-rest-api


2. Create a virtual environment and activate it (assuming that it is installed your machine)
and install the project in editable mode (locally).

.. code-block:: console

    $ python -m venv venv
    $ source venv/bin/activate
    $ python -m pip install -U pip==21.0.0 wheel
    $ python -m pip install --editable .


3. Download the model and the scorer. For English model and scorer, follow below links

.. code-block:: console

    $ wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm \
        -O deepspeech_model.pbmm
    $ wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer \
        -O deepspeech_model.scorer


For other languages, you can place the two files in the current working directory under the names ``deepspeech_model.pbmm`` for the
model and ``deepspeech_model.scorer`` for the scorer.

4. Migrations are done using `Alembic`_

.. _Alembic: https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment

Below steps can be followed to make the migrations up and running. The choice of the RDBMS lies with the developer,
here I will use `PostgresSQL`_

.. _PostgresSQL: https://www.postgresql.org/

- With use of a valid username and password, create a database to hold all the relationships.
- Update the line ``driver://user:pass@localhost/dbname`` in the file ``.env`` with the valid driver name, username and password.
  Driver is ``postgresql`` in this case.
- Initialize the migrations with

.. code-block:: console

    $ alembic init migrations

- Alembic creates an ``alembic.ini`` file into the current directory and a ``migrations`` directory. The .ini file needs
  to be changed at the line ``sqlalchemy.url = driver://user:pass@localhost/dbname`` with the values from the .env file.
- Change directory to migrations directory and update ``env.py`` file by import ``Base`` from models and updating the metadata.

.. code-block:: python

    from logging.config import fileConfig

    from sqlalchemy import engine_from_config
    from sqlalchemy import pool

    from alembic import context
    from app.models import Base

    # this is the Alembic Config object, which provides
    # access to the values within the .ini file in use.
    config = context.config

    # Interpret the config file for Python logging.
    # This line sets up loggers basically.
    fileConfig(config.config_file_name)

    # add your model's MetaData object here
    # for 'autogenerate' support
    # from myapp import mymodel
    # target_metadata = mymodel.Base.metadata
    target_metadata = Base.metadata

- Create migration script and apply it to database

.. code-block:: console

    $ alembic revision -m "Create users table" --autogenerate
    $ alembic upgrade head

After this last step, the ``users`` table should be created in the database.


5. Running the server

.. code-block:: console


    $ python run.py


Usage
~~~~~

Register a new user and request a new `JWT`_ token to access the API

.. _JWT: https://jwt.io/
.. code-block:: console

    $ curl -X POST \
    http://0.0.0.0:8000/api/v1/users \
    -H 'Content-Type: application/json' \
    -d '{
    "username": "forrestgump",
    "email": "fgump@yourdomain.com",
    "password": "yourpassword"
    }'

API response

.. code-block:: json

    {
      "message": "User forrestgump is successfully created."
    }


To generate a JWT token to access the API

.. code-block:: console

    $ curl -X POST \
    http://0.0.0.0:8000/api/v1/token \
    -H 'Content-Type: application/json' \
    -d '{
    "username": "forrestgump",
    "password": "yourpassword"
    }'


If both steps are done correctly, you should get a token in below format

.. code-block:: json

    {
        "access_token": "JWT_token"
    }


With this ``JWT_token``, you have access to different endpoints of the API.


Performing STT (Speech-To-Text)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

STT with audio files
^^^^^^^^^^^^^^^^^^^^

Change directory to ``audio`` and use the WAV files provided for testing.

``Note the usage of hot-words and their boosts in the request.``

- STT the HTTP way


.. code-block:: console

    cURL

    $ curl -X POST \
    http://0.0.0.0:8000/api/v1/stt/http \
    -H 'Authorization: Bearer JWT_token' \
    -F 'audio=@8455-210777-0068.wav' \
    -F 'paris=-1000' \
    -F 'power=1000' \
    -F 'parents=-1000'


.. code-block:: python

    python

    import requests

    jwt_token = 'JWT_token'
    headers = {'Authorization': 'Bearer ' + jwt_token}
    url = 'http://0.0.0.0:8000/api/v1/stt/http'
    hot_words = {'paris': -1000, 'power': 1000, 'parents': -1000}
    audio_filename = 'audio/8455-210777-0068.wav'
    audio = [('audio', open(audio_filename, 'rb'))]
    response = requests.post(url, data=hot_words, files=audio, headers=headers)
    print(response.json())



- STT the WebSocket way (simple test)

WebSockets don't support ``curl``. To take advantage of this feature, you will have to write a web app to send request to the endpoint ``ws://0.0.0.0:8000/api/v1/stt/ws`` (in case the server is running at ``0.0.0.0:8000``).

 
Below command can be used to check if the WebSocket is running.

.. code-block:: console

    $ python client_audio_file_stt.py

In the both cases (HTTP and WebSocket), you should get a result in below format.

.. code-block:: json

    {
      "message": "experience proves this",
      "time": 1.4718825020026998
    }

STT with speech from microphone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Below command can be used to stream speech using the WebSocket on the endpoint ``ws://0.0.0.0:8000/api/v1/stt/mic``. Also in this case, the web app well need to implement
something similar (or far better) to the one in below code.

.. code-block:: console

    $ python client_mic_stream_stt.py

Now you can stream speech to your server and see the result in the client's shell. The implementation of VAD (Voice Activity Detection) will be released pretty soon.


License
^^^^^^^

Licensed under the `Mozilla Public License 2.0`_

.. _Mozilla Public License 2.0: LICENSE
