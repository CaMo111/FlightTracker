from flask import Flask
'''
app = Flask(__name__)

@app.route('/')
def main():
    return 'Hello main!'

if __name__ == '__main__':
    app.run()
'''
def create_app():
    app = Flask(__name__)
    return app

app = create_app()

@app.route("/")
def index():
    return "success"

if __name__ == "__main__":
    app.run()