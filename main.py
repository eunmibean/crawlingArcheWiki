from flask import Flask, jsonify
from getRecipe import giveFinalRecipe
from flask_cors import CORS


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/search/<keyword>', methods=['GET'])
def searchRecipe(keyword):
    final = giveFinalRecipe(keyword)
    print(final)
    return jsonify(final)


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)

