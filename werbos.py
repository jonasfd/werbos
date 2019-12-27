import nltk
import re
import matplotlib.pyplot as plt

from matplotlib.colors import rgb2hex
from collections import Counter

nltk.download('stopwords')
nltk.download('punkt')


class TextPiece:
    """
    A class to analyze a piece of text and get it colored based on word frequency.
    """

    def __init__(self, text: str, additional_stopwords: list = []):
        # setup list of stopwords
        stopwords = nltk.corpus.stopwords.words('portuguese')
        stopwords += additional_stopwords
        # break the text into paragraphs
        paragraphs = text.split("\n")
        # split the text by words        
        self.paragraph_tokens = [nltk.word_tokenize(i) for i in paragraphs]
        # remove punctuation and stopwords
        pattern = re.compile('.*[A-Za-z].*')
        # will store only the relevant words for each paragraph
        self.relevant_words = []
        for tokens in self.paragraph_tokens:
            w = [t.lower() for t in tokens if pattern.match(t) and t.lower() not in stopwords]
            self.relevant_words.append(w)
        # do the counting
        self.counter = Counter([i for j in self.relevant_words for i in j])

    def common_words(self, k: int = 10):
        return self.counter.most_common(k)

    def get_html(self, frequency_threshold=1):
        max_counter = max(self.counter.values())
        rel_counter = {k: v/max_counter for k, v in self.counter.items()}
        # set a colormap
        cmap = plt.get_cmap('autumn_r')
        html_tokens = []
        for idx, paragraph in enumerate(self.paragraph_tokens):
            html_tokens.append(f'<p><font size=4 color="#3e95cd"><b> [ §{idx} ] </b></font>')
            for t in paragraph:
                # for each token, set a color if it appears more than frequency_threshold in the text
                if t.lower() in rel_counter \
                        and rel_counter[t.lower()] > frequency_threshold/max_counter:
                    color = rgb2hex(cmap(rel_counter[t.lower()]))
                    html_tokens.append(f'<font size=4 color={color}>{t}</font>')
                else:
                    html_tokens.append(t)
            html_tokens.append('</p>')
        html_string = ' '.join(html_tokens)
        return html_string

    def _get_paragraph_quality(self, paragraph):
        if len(paragraph) > 0:
            sum_frequencies = sum([self.counter[t] for t in paragraph])
            return len(paragraph)/sum_frequencies
        else:
            return 0

    def get_text_quality(self):
        quality_vector = [round(self._get_paragraph_quality(p)*10, 2) for p in self.relevant_words]
        return quality_vector
