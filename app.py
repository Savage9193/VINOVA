from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get-config', methods=['GET'])
def get_config():
    config = {
        "screenshot_interval": 15,
        "capture_screenshots": True,
        "screenshot_blurred": False
    }
    return jsonify(config)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
