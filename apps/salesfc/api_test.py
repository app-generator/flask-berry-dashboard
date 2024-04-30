from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def entry_point():
    return 'Test API call!'

@app.route('/post', methods=["POST"])
def testpost():
     input_json = request.get_json(force=True) 
     dictToReturn = {'text':input_json['text']}
     return jsonify(dictToReturn)
