import logging

from gtts import gTTS

from config.settings.celery import app


@app.task
def add(x, y):
    print('add')
    return x + y


@app.task
def audio_file_save(text, file_path):
    logging.info('audio_file_save processing...')
    tts = gTTS(text, lang='ko')
    tts.save(str(file_path))
    return f'success audio file - {file_path}'
