from flask import Flask, render_template

# Server static through nginx in future
app = Flask(__name__, template_folder="client", static_folder="client")


@app.route('/')
def index():
    return render_template('index.html')
