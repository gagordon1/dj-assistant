from flask import Flask, send_from_directory
app = Flask(__name__)
PORT=8000

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
if __name__ == "__main__":
    app.run(debug=True, port=PORT)
