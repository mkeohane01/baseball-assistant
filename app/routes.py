from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    print(data)
    # Use your LLM pipeline here to generate the response
    answer = "This is a placeholder answer to your question: " + question

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
