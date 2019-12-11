import os
from flask import Flask, render_template, request

from werbos import TextPiece

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
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
    return render_template('index.html', errors=errors, results=results)


if __name__ == '__main__':
    app.run()
