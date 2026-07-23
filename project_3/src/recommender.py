from sklearn.metrics.pairwise import cosine_similarity

def recommend(
        user_input,
        courses,
        vectorizer,
        vectors
):

    user_vector = vectorizer.transform(
        [user_input]
    )

    scores = cosine_similarity(
        user_vector,
        vectors
    )

    scores = scores.flatten()

    ranked = sorted(
        zip(
            courses,
            scores
        ),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked