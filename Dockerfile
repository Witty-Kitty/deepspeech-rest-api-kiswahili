FROM python:3.8 as build

# make explicit workdir
RUN mkdir /WORKDIR
WORKDIR /WORKDIR
# create a virtual environment for the project
RUN python -m venv venv
# Updating PATH environment variable by adding the virtual environment
ENV PATH=/WORKDIR/venv/bin/:$PATH
ADD requirements.txt requirements.txt
RUN python -m pip install -U pip==21.0.0 wheel
RUN python -m pip install -r requirements.txt

# cURL deepspeech models to /workdir
RUN curl -L https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm -o deepspeech_model.pbmm
RUN curl -L https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer -o deepspeech_model.scorer

FROM python:3.8

# Adding more dependencies and removing unwanted files
RUN apt-get update \
 && apt-get install --no-install-recommends -y ffmpeg \
 && rm -rf /var/lib/apt/lists/* \
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

ENV DATABASE_URI=postgresql://forrest:gump@localhost/forrest
ENV SANIC_FORWARDED_SECRET=foo
ENV SECRET_KEY=foo

ENV SANIC_HOST=0.0.0.0
ENV SANIC_PORT=8000
EXPOSE 8000

CMD python -m run
