import wave
from io import BytesIO
from pathlib import Path

import ffmpeg
import numpy as np
from deepspeech import Metadata
from deepspeech import Model
from sanic.log import logger


def normalize_audio_input(audio):
    output, err = ffmpeg.input('pipe:0').output('pipe:1', f='WAV', acodec='pcm_s16le', ac=1, ar='16k', loglevel='error',
                                                hide_banner=None).run(input=audio, capture_stdout=True,
                                                                      capture_stderr=True)
    if err:
        raise Exception(err)
    return output


class SpeechToTextEngine:
    """ Class to perform speech-to-text transcription and related functionality """

    def __init__(self, scorer='deepspeech_model.scorer') -> None:
        """ Initializing the DeepSpeech model """
        self.model = Model(model_path=Path(__file__).parents[2].joinpath('deepspeech_model.pbmm').absolute().as_posix())
        self.model.enableExternalScorer(
            scorer_path=Path(__file__).parents[2].joinpath(scorer).absolute().as_posix())

    def run(self, audio) -> str:
        """ Receives the audio,  normalizes it and is sent to the model to be transcribed. Returns the result of the
        transcribe audio in string format."""

        normalized_audio = normalize_audio_input(audio)
        audio_streams = BytesIO(normalized_audio)
        with wave.Wave_read(audio_streams) as wav:
            audio_streams = np.frombuffer(wav.readframes(wav.getnframes()), np.int16)
        results = self.model.stt(audio_buffer=audio_streams)
        return results

    def run_with_metadata(self, audio) -> Metadata:
        normalized_audio = normalize_audio_input(audio)
        audio_streams = BytesIO(normalized_audio)
        with wave.Wave_read(audio_streams) as wav:
            audio_streams = np.frombuffer(wav.readframes(wav.getnframes()), np.int16)
        results = self.model.sttWithMetadata(audio_buffer=audio_streams)
        return results

    def add_hot_words(self, data) -> list:
        """ Receives data in form of hot-words and boosts, adds them to the language model and return the list of the
        added hot-words """

        all_hot_words = []
        try:
            logger.info('----------------------------------------------------')
            for hot_word in data:
                # Change all the characters of the hot-word to lower case
                word = hot_word.lower()

                # Get numeric value of the boost
                boost = float(data.get(hot_word))

                # Adding the hot-word and its boost to the language model
                self.model.addHotWord(hot_word, boost)

                # Printing on the prompt the activity
                logger.info(f"`{word}` hot-word with boost `{boost}` was added.")
                all_hot_words.append(word)
            return all_hot_words
        except RuntimeError:
            return []

    def erase_hot_word(self, hot_words) -> None:
        try:
            for hot_word in hot_words:
                self.model.eraseHotWord(hot_word)
                logger.info(f"`{hot_word}` hot-word is erased.")
            logger.info('----------------------------------------------------')
        except RuntimeError:
            return

    def clear_hot_words(self) -> str:
        try:
            self.model.clearHotWords()
            return f"All hot-words were erased."
        except RuntimeError:
            return f"No more hot-words are left."

    def sample_rate(self):
        return self.model.sampleRate()
