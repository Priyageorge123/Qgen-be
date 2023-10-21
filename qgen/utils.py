import re
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import numpy as np
import tensorflow_hub as hub
import numpy as np
from pathlib import Path

nltk.download('all')

BASE_DIR = Path(__file__).resolve().parent
filename=str(BASE_DIR)+'/my_model.h5'
lemmatizer=WordNetLemmatizer()
stopwords = nltk.corpus.stopwords.words('english')
embed = hub.load("https://tfhub.dev/google/Wiki-words-250/2")

def get_word2vec_enc(Questions):
    encoded_Questions = []
    for Question in Questions:
        tokens = Question.split(" ")
        word2vec_embedding = embed(tokens)
        encoded_Questions.append(word2vec_embedding)
    return encoded_Questions

def get_padded_encoded_Question(encoded_reviews):
    max_length=22
    padded_reviews_encoding = []
    for enc_review in encoded_reviews:
        zero_padding_cnt = max_length - enc_review.shape[0]
        pad = np.zeros((1, 250))
        for i in range(zero_padding_cnt):
            enc_review = np.concatenate((pad, enc_review), axis=0)
        padded_reviews_encoding.append(enc_review)
    return padded_reviews_encoding

encoder = LabelEncoder()

new_model = tf.keras.models.load_model(filename)

def getLevel(question):
    encoder=LabelEncoder()
    Y = np.array(["Evaluation","Knowledge","Comprehension","Synthesis","Analysis","Application"])
    encoder = encoder.fit(Y)
    Question = [question]
    qarr=[]
    for i in Question:
      sentence=re.sub(r'[^\w\s]','',i)
      words=nltk.word_tokenize(sentence)
      sample=[]
      nouns=[]
      pos=nltk.pos_tag(words)
      pos=[(w,p) for (w,p) in pos if not w in stopwords]
      pos=[(w,p) for (w,p) in pos if not p in nouns ]
      for (word,p) in pos:
        sample.append(lemmatizer.lemmatize(word))
      qarr.append(" ".join(sample))
    encoded_Question = get_word2vec_enc(qarr)
    padded_encoded_Question = get_padded_encoded_Question(encoded_Question)
    X = np.array(padded_encoded_Question)
    predictions = new_model.predict(X)
    predictions=(encoder.inverse_transform(np.argmax(predictions,axis=1)))
    return predictions[0]