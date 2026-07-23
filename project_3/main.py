from src.data import courses
from src.vectorizer import create_vectors
from src.recommender import recommend
from src.utils import display

print("="*50)
print("DECODELABS PROJECT 3")
print("AI RECOMMENDATION LOGIC")
print("="*50)

print("\nAvailable Interests:")

print("""
1. Python
2. AI
3. Machine Learning
4. Cloud
5. Automation
6. Security
7. Web Development
""")

user_input = input(
    "\nEnter Interests: "
)

course_tags = [
    item["tags"]
    for item in courses
]

vectorizer, vectors = create_vectors(
    course_tags
)

results = recommend(
    user_input,
    courses,
    vectorizer,
    vectors
)

display(
    results[:5]
)