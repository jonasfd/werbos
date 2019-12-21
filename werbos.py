import nltk
import re

from matplotlib.colors import rgb2hex
import matplotlib.pyplot as plt
from collections import Counter

nltk.download('stopwords')
nltk.download('punkt')


class TextPiece:
    
    def __init__(self, text: str, additional_stopwords: list=[]):
        stopwords = nltk.corpus.stopwords.words('portuguese')
        stopwords += additional_stopwords
        paragraphs = text.split("\n")
        # split the text by words        
        self.paragraph_tokens = [nltk.word_tokenize(i) for i in paragraphs]
        # remove punctuation
        pattern = re.compile('.*[A-Za-z].*')
        words = []
        for tokens in self.paragraph_tokens:
            w = [t.lower() for t in tokens if pattern.match(t) and t not in stopwords]
            words += w
        self.counter = Counter(words)
        
    def common_words(self, k:int = 10):
        return self.counter.most_common(k)
    
    def get_html(self, frequency_threshold=1):
        max_counter = max(self.counter.values())
        # set a colormap
        # cmap = autumn_r(linspace(0,1,max(max_counter, 5)))
        # cmap = ListedColormap(cmap[3:,:-1])
        cmap = plt.get_cmap('autumn_r')
        html_tokens = []
        for paragraph in self.paragraph_tokens:
            html_tokens.append('<p>')
            for t in paragraph:
                # for each token, set a color if it appears more than frequency_threshold in the text
                if t.lower() in self.counter and self.counter[t.lower()] > frequency_threshold:
                    relative_count = self.counter[t.lower()] / max_counter
                    color = rgb2hex(cmap(relative_count))
                    html_tokens.append(f'<font size=4 color={color}>{t}</font>')
                else:
                    html_tokens.append(t)
            html_tokens.append('</p>')
        html_string = ' '.join(html_tokens)
        return html_string