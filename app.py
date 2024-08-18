from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/v1/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command')
    # Placeholder: Handle command here
    return jsonify({"response": f"Aiden Lumi received: {command}"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
