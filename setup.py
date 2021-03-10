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
        'deepspeech==0.9.3',
        'environs',
        'ffmpeg-python',
        'numpy',
        'psycopg2',
        'requests',
        'sanic',
        'sanic-jwt',
        'sanic-validation',
        'sqlalchemy',
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
