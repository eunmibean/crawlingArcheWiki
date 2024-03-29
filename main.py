from flask import Flask, jsonify
from getRecipe import retrieve_recipe
from flask_cors import CORS


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/search/<keyword>', methods=['GET'])
def search_recipe(keyword):
    recipe = retrieve_recipe(keyword)
    return jsonify(recipe)

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)

