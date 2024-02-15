from flask import Flask, render_template
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
    return render_template("index.html")

if __name__ == "__main__":
    app.run()