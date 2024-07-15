from flask import Flask, request, jsonify, render_template
from .utils import query_llm_llamafile
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    
    # Use your LLM pipeline here to generate the response
    answer = query_llm_llamafile(question)

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
