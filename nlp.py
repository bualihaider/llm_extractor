import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk import pos_tag, word_tokenize

# Ensure resources are downloaded
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)
nltk.download('stopwords', quiet=True)

def extract_keywords(text: str):
    words = word_tokenize(text.lower())
    words = [w for w in words if w.isalpha() and w not in stopwords.words("english")]
    tagged = pos_tag(words)
    nouns = [w for w, pos in tagged if pos.startswith("NN")]
    common = [w for w, _ in Counter(nouns).most_common(3)]
    return common
