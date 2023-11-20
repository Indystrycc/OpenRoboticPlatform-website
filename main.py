from flask import Flask

from website import create_app

app: Flask = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5004)
