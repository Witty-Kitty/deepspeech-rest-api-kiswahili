import wave
from io import BytesIO
from pathlib import Path

import numpy as np
from deepspeech import Model

from app.helpers import normalize_audio_input


class SpeechToTextEngine:
    """ Class to perform speech-to-text transcription and related functionality """

    def __init__(self):
        """ Initializing the DeepSpeech model """
        self.model = Model(model_path=Path(__file__).parents[2].joinpath('deepspeech_model.pbmm').absolute().as_posix())

    def run(self, audio):
        """

        :param audio:
        :return:
        """
        normalized_audio = normalize_audio_input(audio)
        audio_streams = BytesIO(normalized_audio)
        with wave.Wave_read(audio_streams) as wav:
            audio_streams = np.frombuffer(wav.readframes(wav.getnframes()), np.int16)
        results = self.model.stt(audio_buffer=audio_streams)
        return results

    def run_with_metadata(self, audio):
        """

        :param audio:
        :return:
        """
        normalized_audio = normalize_audio_input(audio)
        audio_streams = BytesIO(normalized_audio)
        with wave.Wave_read(audio_streams) as wav:
            audio_streams = np.frombuffer(wav.readframes(wav.getnframes()), np.int16)
        results = self.model.sttWithMetadata(audio_buffer=audio_streams)
        return results
