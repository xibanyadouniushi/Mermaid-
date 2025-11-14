from flask import Flask, render_template, jsonify, request
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/export', methods=['POST'])
def export_image():
    try:
        data = request.json
        image_data = data.get('image').split(',')[1]
        return jsonify({
            'status': 'success',
            'image': image_data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.errorhandler(Exception)
def handle_errors(e):
    return jsonify({
        'error': str(e),
        'error_type': 'mermaid_syntax_error'
    }), 500

from werkzeug.serving import make_server
import threading

class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('localhost', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

if __name__ == '__main__':
    server = ServerThread(app)
    server.start()
    print("服务已启动，输入'停止'以关闭服务...")
    while True:
        user_input = input()
        if user_input.strip() == '停止':
            server.shutdown()
            server.join()
            print("服务已成功关闭。")
            break