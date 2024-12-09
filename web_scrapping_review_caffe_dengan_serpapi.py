# -*- coding: utf-8 -*-
"""Web Scrapping Review Caffe dengan SerpAPI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jOb8UIzWzs_c81uAYM70l4EKFpxNuP4n

instal Modul Python Google Search Results
"""

!pip install google-search-results
from serpapi import GoogleSearch  # Make sure this line is present to import GoogleSearch
from urllib.parse import *

"""Import Library"""

from serpapi import GoogleSearch
from urllib.parse import *

"""Scrapping Local Results
mengambil data 10 objek (Caffe) yang memiliki ≥ 100 reviews
"""

params = {
  "engine": "google_maps",
  "q": "caffe", # objek yang dicari
  "ll": "@-6.5481531,106.4878679,10z", #koordinat tempat sekitar
  "type": "search",
  "api_key": "203da87ec763566500b2c5e502840dc8ba9d27efcf8ecc53c8f9cef4af34ce5d"
}
search = GoogleSearch(params)

lIdx = 0 # indeks yang ditampilkan dari data
lSum = 7 # Batas jumlah data yang ditampilkan
local_results = []

while lIdx  <= lSum:
  results = search.get_dict()

  # Periksa apakah API mengembalikan error
  if 'error' in results:
    print(f"Error API: {results['error']}")
    break # Keluar dari loop jika ada error

  # Periksa apakah kunci 'local_results' ada dalam respons
  if 'local_results' in results:
    for Result in results["local_results"]:
      # The if statement should be indented within the for loop
      if lIdx <= lSum:

        # Use the get method with a default value to safely access the 'reviews' key
        reviews = Result.get("reviews", 0)

        #seleksi data (jangan ambil data jika jumlah review < 50 )
        if reviews < 50:  # Check the reviews variable now
          lIdx += 1
          continue

        # Append data sesuai dengan batas jumlah yang sudah ditentukan
        local_results.append({'Nama': Result["title"],
                             'data_id': Result["data_id"],
                             'total_reviews': reviews}); # Use the reviews variable

  #menghilangkan pagination pada web, sehingga data yang terambil bisa banyak
  if "next" in results.get("serpapi_pagination", {}):
    # Akan mengubah parameter dari 'GoogleSearch()' dengan isi parameter dari halaman selanjutnya
    search.params_dict.update(dict(parse_qsl(urlsplit(results.get("serpapi_pagination").get("next")).query)))

  else:
    break

for LR in local_results:
  print(LR)

"""Scrapping Reviews
Mengambil 100 data dari masing-masing objek (Caffe) sesuai dengan jumlah index yang diinginkan
"""

data = {'Caffe_name':[],
        'name':[],
        'rating':[],
        'review':[]}

for LR in local_results:

  params = {
    "engine": "google_maps_reviews",
    "data_id": "",
    "api_key": "203da87ec763566500b2c5e502840dc8ba9d27efcf8ecc53c8f9cef4af34ce5d" #Fixed: This line was causing the indentation error. It's now aligned correctly and the previous incorrect content is removed.
  }

  params["data_id"] = LR['data_id']

  search = GoogleSearch(params)

  lIdx = 0 # Angka indeks dari data
  lSum = 30 # Batas jumlah data yang ditampilkan

  while lIdx <= lSum:
    results = search.get_dict()

    for Result in results["reviews"]:
      lIdx += 1

      if lIdx <= lSum:
        # Append data sesuai dengan batas jumlah yang sudah ditentukan
        data['Caffe_name'].append(LR['Nama']);
        data['name'].append(Result["user"]["name"]);
        data['rating'].append(Result["rating"]);
        data['review'].append(Result.get("snippet", ""));

    #menghilangkan pagination pada web, sehingga data yang terambil bisa banyak
    if "next" in results.get("serpapi_pagination", {}):
      # Akan mengubah parameter dari 'GoogleSearch()' dengan isi parameter dari halaman selanjutnya
      search.params_dict.update(dict(parse_qsl(urlsplit(results.get("serpapi_pagination").get("next")).query)))

    else:
      break

review_original = data['review']

"""Export Data Scrapping"""

import pandas as pd
import os

dfScrap = pd.DataFrame(data)

# Create the directory if it doesn't exist
os.makedirs('File CSV', exist_ok=True)

dfScrap.to_csv('File CSV/reviewCaffeBogor.csv', index = False)

"""2. Tahap Case Folding

Import Library
"""

import re
import string

"""Proses Listing"""

import re
import string

review_clean = []  # Initialize review_clean as an empty list

for review in review_original:
    # Remove Unicode
    review_test = re.sub(r'[^\x00-\x7F]+', ' ', review)
    # Remove Mentions
    review_test = re.sub(r'@\w+', '', review_test)
    # Lowercase the document
    review_test = review_test.lower()
    # Remove punctuations
    review_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', review_test)
    # Remove the numbers
    review_test = re.sub(r'[0-9]', '', review_test)
    # Remove the doubled space
    review_test = re.sub(r'\s{2,}', ' ', review_test)

    review_clean.append(review_test) # Now you can append to review_clean

"""3. Tahap Tokenizing

Import Library
"""

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize

"""Proses Listing"""

import nltk

# Download the necessary data for the Punkt Sentence Tokenizer
nltk.download('punkt')
nltk.download('punkt_tab')

from nltk.tokenize import sent_tokenize, word_tokenize

review_tokenized = []

for review in review_clean:
    review_tokenized.append(word_tokenize(review))

"""4. Tahap Filtering (Stopword Removal)

Import Library
"""

from nltk.corpus import stopwords
nltk.download('stopwords')

"""Proses Listing"""

review_filtered = []
listStopword =  set(stopwords.words('english'))

for review in review_tokenized:

  review_each_filtered = []

  for r in review:
    if r not in listStopword:
        review_each_filtered.append(r)

  review_filtered.append(review_each_filtered)

"""5. Tahap Stemming

menggunakan algoritma SnowballStemmer
"""

from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("english")

review_stemmed = []

for review in review_filtered:

  review_each_stemmed = []

  for r in review:
    review_each_stemmed.append(stemmer.stem(r))

  review_stemmed.append(review_each_stemmed)

"""6. Export Hasil ke CSV

Import Library & Proses Listing
"""

import pandas as pd

data_preprocessed = data
data_preprocessed['review'] = review_stemmed


df = pd.DataFrame(data_preprocessed)
df

df.to_csv('File CSV/reviewCaffeBogor_setelah_preprocessing.csv', index=False)

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
sns.set_style("whitegrid")

#set warning
import warnings
warnings.filterwarnings('ignore')


pd.pandas.set_option('display.max_columns', None)

filename = "./File CSV/reviewCaffeBogor.csv"
df = pd.read_csv(filename, encoding = 'latin-1')
df.head()

df.drop(columns = ['Caffe_name', 'name'], inplace = True)
df.columns = ['rating', 'review']
df.head()

import string
import re

def clean_text(text):
    # Check if 'text' is a list
    if isinstance(text, list):
        # If it is, join its elements into a single string
        text = ' '.join(text)
    # Ensure text is a string (handle potential NaN or other non-string types)
    text = str(text)  # Convert to string to handle non-string values
    # Then, proceed with the rest of the cleaning
    return re.sub('[^a-zA-Z]', ' ', text).lower()

df['cleaned_text'] = df['review'].apply(lambda x: clean_text(x)) # Changed 'Review' to 'review'
df['label'] = df['rating'].map({1.0:0, 2.0:0, 3.0:0, 4.0:1, 5.0:1})

def count_punct(text):
    # Ensure text is a string
    text = str(text) # Handle potential non-string types like float
    count = sum([1 for char in text if char in string.punctuation])
    # Avoid division by zero if text is empty after removing spaces
    if len(text) - text.count(" ") == 0:
        return 0
    return round(count/(len(text) - text.count(" ")), 3)*100

df['review_len'] = df['review'].apply(lambda x: len(str(x)) - str(x).count(" ")) # Convert to string to handle non-string
df['punct'] = df['review'].apply(lambda x: count_punct(x))
df.head()

def tokenize_text(text):
    tokenized_text = text.split()
    return tokenized_text
df['tokens'] = df['cleaned_text'].apply(lambda x: tokenize_text(x))
df.head()

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
all_stopwords = stopwords.words('english')
all_stopwords.remove('not')

import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
def lemmatize_text(token_list):
    return " ".join([lemmatizer.lemmatize(token) for token in token_list if not token in set(all_stopwords)])

lemmatizer = nltk.stem.WordNetLemmatizer()
df['lemmatized_review'] = df['tokens'].apply(lambda x: lemmatize_text(x))
df.head()

#Shape of the dataset, and breakdown of the classes
print(f"Input data has {len(df)} rows and {len(df.columns)} columns")
print(f"rating 1.0 = {len(df[df['rating']==1.0])} rows")
print(f"rating 2.0 = {len(df[df['rating']==2.0])} rows")
print(f"rating 3.0 = {len(df[df['rating']==3.0])} rows")
print(f"rating 4.0 = {len(df[df['rating']==4.0])} rows")
print(f"rating 5.0 = {len(df[df['rating']==5.0])} rows")

# Missing values in the dataset
print(f"Number of null in label: { df['rating'].isnull().sum() }")
print(f"Number of null in text: { df['review'].isnull().sum()}")
sns.countplot(x='rating', data=df);

from wordcloud import WordCloud

df_negative = df[ (df['rating']==1.0) | (df['rating']==2.0) | (df['rating']==3.0)]
df_positive = df[ (df['rating']==4.0) | (df['rating']==5.0)]
#convert to list
negative_list=df_negative['lemmatized_review'].tolist()
positive_list= df_positive['lemmatized_review'].tolist()

filtered_negative = ("").join(str(negative_list)) #convert the list into a string of spam
filtered_negative = filtered_negative.lower()

filtered_positive = ("").join(str(positive_list)) #convert the list into a string of ham
filtered_positive = filtered_positive.lower()

wordcloud = WordCloud(max_font_size = 160, margin=0, background_color = "white", colormap="Greens").generate(filtered_positive)
plt.figure(figsize=[10,10])
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.title("Positive Reviews Word Cloud")
plt.show()

wordcloud = WordCloud(max_font_size = 160, margin=0, background_color = "white", colormap="Reds").generate(filtered_negative)
plt.figure(figsize=[10,10])
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.title("Negative Reviews Word Cloud")
plt.show()

X = df[['lemmatized_review', 'review_len', 'punct']]
y = df['label']
print(X.shape)
print(y.shape)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_df = 0.5, min_df = 2) # ignore terms that occur in more than 50% documents and the ones that occur in less than 2
tfidf_train = tfidf.fit_transform(X_train['lemmatized_review'])
tfidf_test = tfidf.transform(X_test['lemmatized_review'])

X_train_vect = pd.concat([X_train[['review_len', 'punct']].reset_index(drop=True),
           pd.DataFrame(tfidf_train.toarray())], axis=1)
X_test_vect = pd.concat([X_test[['review_len', 'punct']].reset_index(drop=True),
           pd.DataFrame(tfidf_test.toarray())], axis=1)
X_train_vect.head()

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

from sklearn.naive_bayes import MultinomialNB
classifier = MultinomialNB()
classifier.fit(X_train_vect, y_train)
naive_bayes_pred = classifier.predict(X_test_vect)

# Classification Report
print(classification_report(y_test, naive_bayes_pred))

# Confusion Matrix
class_label = ["negative", "positive"]
df_cm = pd.DataFrame(confusion_matrix(y_test, naive_bayes_pred), index=class_label, columns=class_label)
sns.heatmap(df_cm, annot=True, fmt='d')
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators=150)
classifier.fit(X_train_vect, y_train)
random_forest_pred = classifier.predict(X_test_vect)

# Classification report
print(classification_report(y_test, random_forest_pred))

# Confusion Matrix
class_label = ["negative", "positive"]
df_cm = pd.DataFrame(confusion_matrix(y_test, random_forest_pred), index=class_label, columns=class_label)
sns.heatmap(df_cm, annot=True, fmt='d')
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(X_train_vect, y_train)
log_reg_pred = classifier.predict(X_test_vect)
# Classification report
print(classification_report(y_test, log_reg_pred))

# Confusion Matrix
class_label = ["negative", "positive"]
df_cm = pd.DataFrame(confusion_matrix(y_test, log_reg_pred), index=class_label, columns=class_label)
sns.heatmap(df_cm, annot=True, fmt='d')
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()

from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train_vect, y_train)
svm_pred = classifier.predict(X_test_vect)
# Classification report
print(classification_report(y_test, svm_pred))

# Confusion Matrix
class_label = ["negative", "positive"]
df_cm = pd.DataFrame(confusion_matrix(y_test, svm_pred), index=class_label, columns=class_label)
sns.heatmap(df_cm, annot=True, fmt='d')
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()

from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors = 5)
classifier.fit(X_train_vect, y_train)
knn_pred = classifier.predict(X_test_vect)

# Classification report
print(classification_report(y_test, knn_pred))

# Confusion Matrix
class_label = ["negative", "positive"]
df_cm = pd.DataFrame(confusion_matrix(y_test, knn_pred), index=class_label, columns=class_label)
sns.heatmap(df_cm, annot=True, fmt='d')
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()

from sklearn.ensemble import ExtraTreesClassifier
classifier = ExtraTreesClassifier(n_estimators=150, random_state=50)
classifier.fit(X_train_vect, y_train)
extra_trees_pred = classifier.predict(X_test_vect)

# Classification report
print(classification_report(y_test, extra_trees_pred))

# Confusion Matrix
class_label = ["negative", "positive"]
df_cm = pd.DataFrame(confusion_matrix(y_test, extra_trees_pred), index=class_label, columns=class_label)
sns.heatmap(df_cm, annot=True, fmt='d')
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()

from sklearn.model_selection import cross_val_score

models = [
          MultinomialNB(),
          LogisticRegression(),
          RandomForestClassifier(n_estimators = 150),
          SVC(kernel = 'linear'),
          KNeighborsClassifier(n_neighbors = 5),
          ExtraTreesClassifier(n_estimators=150, random_state=50)
         ]
names = ["Naive Bayes", "Logistic Regression", "Random Forest", "SVM", "KNN", "Extra Trees"]
for model, name in zip(models, names):
    print(name)
    for score in ["accuracy", "precision", "recall", "f1"]:
        print(f" {score} - {cross_val_score(model, X_train_vect, y_train, scoring=score, cv=10).mean()} ")
    print()

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X_cv = cv.fit_transform(df['lemmatized_review']) # Fit the Data
y_cv = df['label']

from sklearn.model_selection import train_test_split
X_train_cv, X_test_cv, y_train_cv, y_test_cv = train_test_split(X_cv, y_cv, test_size=0.3, random_state=42)

#Naive Bayes Classifier
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()

clf.fit(X_train_cv, y_train_cv)
clf.score(X_test_cv, y_test_cv)

data = ["Bad", "Good", "I hate the service, it's really bad", "The nurse is so kind"]
vect = cv.transform(data).toarray()

my_prediction = clf.predict(vect)
print(my_prediction)

from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 10)
# from sklearn.ensemble import ExtraTreesClassifier
# classifier = ExtraTreesClassifier(n_estimators=150, random_state=50)

classifier.fit(tfidf_train, y_train)
classifier.score(tfidf_test, y_test)

data = ["Bad", "Good", "I hate the service, it's really bad", "The nurse is so kind"]
vect = tfidf.transform(data).toarray()

my_pred = classifier.predict(vect)
print(my_pred)