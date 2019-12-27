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
    quality_vector = []
    if request.method == "POST":
        # get text from the box
        try:
            text = request.form['text']
            stopwords = request.form['stopwords']
            if stopwords is not None and stopwords != '':
                stopwords = [i.strip().lower() for i in stopwords.split(',')]
            else:
                stopwords = []
            piece = TextPiece(text, additional_stopwords=stopwords)
            # get top-k words
            common_words = piece.common_words(k=10)
            words, frequencies = [i for i, _ in common_words], [j for _, j in common_words]
            quality_vector = piece.get_text_quality()
            # get colored HTML
            results = piece.get_html()
        except Exception as ex:
            errors.append(
                "Desculpe. Não foi possível processar o texto informado."  # + str(ex)
            )
    return render_template('conta_palavras.html',
                           errors=errors,
                           results=results,
                           words=words,
                           frequencies=frequencies,
                           quality=quality_vector)


if __name__ == '__main__':
    app.run()
