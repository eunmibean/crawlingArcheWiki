from flask import Flask
from getRecipe import giveFinalRecipe


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/search/<keyword>')
def searchRecipe(keyword):
    final = giveFinalRecipe(keyword)
    return final
    #print(searchRecipe(keyword))

    



if __name__ == "__main__":
    app.run()
