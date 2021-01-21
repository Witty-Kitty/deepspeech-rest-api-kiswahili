import ffmpeg


def normalize_audio_input(audio):
    output, err = ffmpeg.input('pipe:0').output('pipe:1', f='WAV', acodec='pcm_s16le', ac=1, ar='16k', loglevel='error',
                                                hide_banner=None).run(input=audio, capture_stdout=True,
                                                                      capture_stderr=True)
    if err:
        raise Exception(err)
    return output
