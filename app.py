from flask import Flask, render_template, redirect
from generate_poem import PoemGenerator
app = Flask(__name__)

generator = PoemGenerator(None)


@app.route("/")
def home():
    return redirect('http://git.hallada.net/nlp/')


@app.route("/nlp/buzzfeed_haiku_generator/")
def buzzfeed_haiku_generator():
    haiku = generator.generate_haiku()
    return render_template('buzzfeed-haiku-generator.html', haiku=haiku)

if __name__ == '__main__':
    app.run(debug=True)
