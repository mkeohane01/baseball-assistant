from flask import request, jsonify, render_template, Blueprint
from src.llm_pipelining import answer_baseball_question

app = Blueprint('app', __name__)
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    print(question)
    # Use your LLM pipeline here to generate the response
    answer = answer_baseball_question(question)
    print(answer)
    return jsonify({'answer': answer})
