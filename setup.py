from setuptools import setup, find_packages

setup(
    name='DeepSpeech REST API',
    version='0.0.1',
    description='A REST API to facilitate the usage of Mozilla DeepSpeech',
    long_description='file: README.md',
    author='Fabrice Kwizera',
    author_email='fabrice@mozillafoundation.org',
    url='https://github.com/fabricekwizera/deepspeech-rest-api',
    package=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platform='any',
    install_requires=[
        'alembic',
        'aredis',
        'deepspeech-tflite==0.9.3',
        'environs',
        'ffmpeg-python',
        'halo',
        'numpy',
        'psycopg2',
        'pyaudio',
        'requests',
        'sanic==18.12.0',
        'sanic-cors==0.10.0.post3',
        'sanic-jwt',
        'sanic-validation==0.5.1',
        'scipy',
        'sqlalchemy',
        'webrtcvad',
        'websocket-client',
        'werkzeug'
    ],
    classifiers=[
        'Framework :: Sanic',
        'Programming Language :: Python :: 3.8',
        'Environment :: Application Programming Interface',
        'Topic :: Software Development',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ]
)
