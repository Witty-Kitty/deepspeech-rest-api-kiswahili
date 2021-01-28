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
        self.model.enableExternalScorer(
            scorer_path=Path(__file__).parents[2].joinpath('deepspeech_model.scorer').absolute().as_posix())

    def run(self, audio):
        """
        Based on https://github.com/zelo/deepspeech-rest-api/blob/master/stt/engine.py
        """
        normalized_audio = normalize_audio_input(audio)
        audio_streams = BytesIO(normalized_audio)
        with wave.Wave_read(audio_streams) as wav:
            audio_streams = np.frombuffer(wav.readframes(wav.getnframes()), np.int16)
        results = self.model.stt(audio_buffer=audio_streams)
        return results

    def run_with_metadata(self, audio):
        normalized_audio = normalize_audio_input(audio)
        audio_streams = BytesIO(normalized_audio)
        with wave.Wave_read(audio_streams) as wav:
            audio_streams = np.frombuffer(wav.readframes(wav.getnframes()), np.int16)
        results = self.model.sttWithMetadata(audio_buffer=audio_streams)
        return results

    def add_hot_word(self, word, boost):
        try:
            self.model.addHotWord(word, boost)
            return f"'{word}' hot-word with boost '{boost}' was added."
        except RuntimeError:
            return f"Hot-word was already added."

    def erase_hot_word(self, word):
        try:
            self.model.eraseHotWord(word)
            return f"'{word}' hot-word is erased."
        except RuntimeError:
            return f"That hot-word can't be found."

    def clear_hot_words(self):
        try:
            self.model.clearHotWords()
            return f"All hot-words were erased."
        except RuntimeError:
            return f"No more hot-words are left."

    def sample_rate(self):
        return self.model.sampleRate()
