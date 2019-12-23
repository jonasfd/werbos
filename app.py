import os
from flask import Flask, render_template, request

from werbos import TextPiece

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


@app.route('/conta_palavras', methods=['GET', 'POST'])
def conta_palavras():
    errors = []
    results = {}
    words = []
    frequencies = []
    if request.method == "POST":
        # get text from the box
        try:
            text = request.form['text']
            piece = TextPiece(text)
            # get top-k words
            common_words = piece.common_words(k=10)
            words, frequencies = [i for i, _ in common_words], [j for _, j in common_words]
            # get colored HTML
            results = piece.get_html()
        except Exception as ex:
            errors.append(
                "Desculpe. Não foi possível processar o texto informado."  # + str(ex)
            )
    return render_template('conta_palavras.html', errors=errors, results=results, words=words, frequencies=frequencies)


if __name__ == '__main__':
    app.run()
