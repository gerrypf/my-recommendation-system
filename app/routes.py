from flask import render_template, request
from app import app
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

# Membaca dataset dan memastikan semua nilai di kolom keywords adalah string
dataset_path = 'dataset.csv'
dataset = pd.read_csv(dataset_path, delimiter=',')
dataset['keywords'] = dataset['keywords'].astype(str)
corpus = dataset['keywords'].tolist()
subjects = dataset['subject'].tolist()
sks_values = dataset['sks'].tolist()

# Fit TF-IDF Vectorizer pada corpus
tfidf_vectorizer = TfidfVectorizer()
tfidf_corpus_matrix = tfidf_vectorizer.fit_transform(corpus)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    uploaded_file = request.files['pdf']
    file_path = os.path.join('uploaded_pdfs', uploaded_file.filename)
    uploaded_file.save(file_path)

    # Baca PDF dan ekstraksi teks
    reader = PyPDF2.PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Tokenisasi teks
    tokens = word_tokenize(text.lower())
    text = ' '.join(tokens)

    # TF-IDF Vectorization
    tfidf_matrix = tfidf_vectorizer.transform([text])

    # Cosine Similarity
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_corpus_matrix)

    # Hasil dalam bentuk persentase
    similarities = [(subjects[i], sks_values[i], round(cosine_similarities[0][i] * 100, 2)) for i in range(len(subjects))]
    sorted_similarities = sorted(similarities, key=lambda x: x[2], reverse=True)

    # Rekomendasi mata kuliah berdasarkan similarity tertinggi dengan total SKS tidak lebih dari 20
    recommended_subjects = []
    total_sks = 0
    for subject, sks, similarity in sorted_similarities:
        if total_sks + sks <= 20:
            recommended_subjects.append((subject, sks, similarity))
            total_sks += sks

    return render_template('index.html', 
                           similarities=sorted_similarities, 
                           file_name=uploaded_file.filename,
                           recommended_subjects=recommended_subjects,
                           enumerate=enumerate)
