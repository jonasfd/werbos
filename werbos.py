import nltk
import re

from numpy import linspace
from matplotlib.colors import rgb2hex # , ListedColormap, LinearSegmentedColormap
# from matplotlib.cm import autumn_r
import matplotlib.pyplot as plt
from collections import Counter

nltk.download('stopwords')
nltk.download('punkt')

class TextPiece():
    
    def __init__(self, text: str, additional_stopwords: list=[]):
        stopwords = nltk.corpus.stopwords.words('portuguese')
        stopwords += additional_stopwords
        # split the text by words        
        self.tokens = nltk.word_tokenize(text)
        # remove punctuation
        pattern = re.compile('.*[A-Za-z].*')
        self.words = [w.lower() for w in self.tokens if pattern.match(w) and w not in stopwords]
        self.counter = Counter(self.words)
        
    def common_words(self, k:int = 10):
        return self.counter.most_common(k)
    
    def get_html(self, frequency_threshold=1):
        max_counter = max(self.counter.values())
        # set a colormap
        # cmap = autumn_r(linspace(0,1,max(max_counter, 5)))
        # cmap = ListedColormap(cmap[3:,:-1])
        cmap = plt.get_cmap('autumn_r')
        html_tokens = []
        for t in self.tokens:
            # for each token, set a color if it appears more than frequency_threshold in the text
            if t.lower() in self.counter and self.counter[t.lower()] > frequency_threshold:
                relative_count = self.counter[t.lower()] / max_counter
                color = rgb2hex(cmap(relative_count))
                html_tokens.append(f'<font size=4 color={color}>{t}</font>')
            else:
                html_tokens.append(t)
        html_string = ' '.join(html_tokens)
        return html_string