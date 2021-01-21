from factory import create_app

app = create_app()

if __name__ == "__main__":
    HOST, PORT, DEBUG = app.config['HOST'], app.config['PORT'], app.config['DEBUG']
    app.run(host=HOST, port=PORT, debug=DEBUG)
