from flask import Flask, render_template
from generate_poem import PoemGenerator
app = Flask(__name__)

generator = PoemGenerator(None)

@app.route("/")
def home():
    haiku = generator.generate_haiku()
    return render_template('index.html', haiku=haiku)

if __name__ == '__main__':
    app.run(debug=True)
