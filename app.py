import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.probability import FreqDist
import heapq
from flask import Flask, render_template, request
import random

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__, template_folder='C:\\Users\\A-222\\Desktop\\Castillo Files\\templates')

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

def paraphrase_text(text):
    words = word_tokenize(text.lower())
    paraphrased_words = []
    for word in words:
        if word not in stopwords.words("english") and len(word) > 2:
            synonyms = get_synonyms(word)
            if synonyms:
                paraphrased_words.append(random.choice(synonyms).replace("_", " "))
            else:
                paraphrased_words.append(word)
        else:
            paraphrased_words.append(word)
    return ' '.join(paraphrased_words)

def summarize_and_paraphrase(text, num_sentences=2):
    summarized_text = ""
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize words
    words = word_tokenize(text.lower())

    # Filter out stopwords
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word not in stop_words]

    # Calculate word frequency
    word_freq = FreqDist(filtered_words)

    # Rank sentences based on word frequency
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                if len(sentence.split(' ')) < 30:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_freq[word]
                    else:
                        sentence_scores[sentence] += word_freq[word]

    # Select top sentences based on scores
    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summarized_text += ' '.join(summary_sentences)
    
    # Paraphrase the summarized text
    paraphrased_text = paraphrase_text(summarized_text)
    
    return paraphrased_text

@app.route('/')
def index():
    return render_template('sample.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form['inputText']
    summarized_text = summarize_and_paraphrase(text)
    return summarized_text

if __name__ == '__main__':
    app.run(debug=True)
