FROM python:3.8 as build

# make explicit workdir
RUN mkdir /WORKDIR
WORKDIR /WORKDIR
# create a virtual environment for the project
RUN python -m venv venv
# Updating PATH environment variable by adding the virtual environment
ENV PATH=/WORKDIR/venv/bin/:$PATH
ADD requirements.txt requirements.txt
RUN apt-get update 
RUN apt-get install portaudio19-dev -y 
RUN apt-get install python3-pyaudio libatlas-base-dev libatlas-doc liblapack-doc libasound2-plugins alsa-utils libasound2-doc portaudio19-doc -y 
RUN python -m pip install -r requirements.txt --use-pep517 
RUN python -m pip install -U pip

# cURL deepspeech models to /workdir
RUN curl -L https://coqui.gateway.scarf.sh/swahili/coqui/v8.0/model.tflite -o deepspeech_model.tflite
RUN curl -L https://coqui.gateway.scarf.sh/swahili/coqui/v8.0/large-vocabulary.scorer -o deepspeech_model.scorer

FROM python:3.8

# Adding more dependencies and removing unwanted files
RUN apt-get update \
 && apt-get install --no-install-recommends -y ffmpeg \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get update \
 && apt-get install portaudio19-dev -y \
 && apt-get install python3-pyaudio libatlas-base-dev libatlas-doc liblapack-doc libasound2-plugins alsa-utils libasound2-doc portaudio19-doc -y \
 && apt-get clean

# User management
RUN groupadd --gid=1000 api \
 && useradd --uid=1000 --gid=1000 --system api
USER api
COPY --from=build --chown=api:api /WORKDIR /WORKDIR
ENV PATH=/WORKDIR/venv/bin/:$PATH
WORKDIR /WORKDIR
ADD run.py run.py
ADD config.py config.py
ADD --chown=api:api app/ app/

ENV SANIC_DEBUG=True
ENV SANIC_ENV=prod
ENV SANIC_TESTING=True

ENV DATABASE_URI=postgresql://postgres@172.31.0.0
ENV SANIC_FORWARDED_SECRET=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2NzYwODUyMTEuNjI5ODgxfQ.eXM-ygEbc0WPEzqbYsZxp5RNj6DC4l4_eI-JLWwDcpU
ENV SECRET_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2NzYwODUyMTEuNjI5ODgxfQ.eXM-ygEbc0WPEzqbYsZxp5RNj6DC4l4_eI-JLWwDcpU

ENV SANIC_HOST=0.0.0.0
ENV SANIC_PORT=8000
EXPOSE 8000

CMD python -m run
