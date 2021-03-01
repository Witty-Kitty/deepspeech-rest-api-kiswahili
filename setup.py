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
        'sanic==20.12.1',
        'sanic-jwt==1.6.0',
        'environs==9.3.1',
        'sqlalchemy==1.3.23',
        'werkzeug==1.0.1',
        'sanic-validation==0.5.1',
        'psycopg2',
        'ffmpeg-python==0.2.0',
        'numpy',
        'deepspeech==0.9.3',
        'alembic==1.5.4',
        'aredis==1.1.8',
        'requests==2.25.1'
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
