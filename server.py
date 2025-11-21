from flask import Flask, render_template, request, jsonify, send_from_directory, Response
import os
from pathlib import Path
from flask_socketio import SocketIO, emit
import threading
from harness import fuzzBinary
import globalVar
import json, time, threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

binaries = Path('created_binaries/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configure')
def configure():
    names = [binary.name for binary in binaries.iterdir()]
    return render_template('configure.html', binaries=names)

@app.route('/fuzz')
def fuzz():
    return render_template('fuzz.html')

@app.route('/static/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/', filename)

@app.route("/stats")
def show_statistics():
    return render_template("stats.html")

@app.route('/events')
def events():
    def stream():
        while True:
            data = json.dumps(globalVar.status)
            yield f"data: {data}\n\n"
            time.sleep(0.2)  # 5 updates per second
    return Response(stream(), mimetype='text/event-stream')


@app.route('/api/start-fuzzing', methods=['POST'])
def start_fuzzing():
    data = request.json
    runtime = data.get('runtime', 60) * 1000
    timeout = data.get('timeout', 3)

    binary = Path(f"created_binaries/{data.get('binary', '')}")
    sample_input = Path(f'example_inputs/{binary.name}.txt')
    globalVar.init()
    fuzzing_thread = threading.Thread(target=fuzzBinary, 
                                      args=(binary, sample_input, timeout, runtime, True))
    fuzzing_thread.start()
    
    return jsonify({
        'status': 'success',
        'message': f'Started fuzzing {binary} for {runtime} seconds'
    })

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)
