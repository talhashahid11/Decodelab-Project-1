from sklearn.feature_extraction.text import TfidfVectorizer

def create_vectors(data):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        data
    )

    return (
        vectorizer,
        vectors
    )