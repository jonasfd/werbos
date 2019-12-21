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
    if request.method == "POST":
        # get text from the box
        try:
            text = request.form['text']
            piece = TextPiece(text)
            results = piece.get_html()
            # print(results)
        except Exception as ex:
            errors.append(
                "Desculpe. Não foi possível processar o texto informado. " + str(ex)
            )
    return render_template('conta_palavras.html', errors=errors, results=results)


if __name__ == '__main__':
    app.run()
