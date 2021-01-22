FROM python:3.8 as build

# Installing Python dependencies and creating a virtual environment for the project
RUN pip install -U pip virtualenv \
 && virtualenv -p `which python3` /venv/

# Updating PATH environment variable by adding the virtual environment
ENV PATH=/venv/bin/:$PATH

# Copying the project dependecies and installing them
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

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

COPY --from=build --chown=api:api /venv/ /venv/
ENV PATH=/venv/bin/:$PATH

ADD --chown=api:api app/ app/

# Copying the model and other needed .py files
ADD deepspeech_model.pbmm deepspeech_model.pbmm
ADD factory.py factory.py
ADD run.py run.py
ADD config.py config.py


WORKDIR .

EXPOSE 8000

CMD python -m run
