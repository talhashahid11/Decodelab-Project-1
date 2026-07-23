def display(results):

    print("\nTop Recommendations:\n")

    for item, score in results:

        print(
            f"{item['name']} "
            f"({score:.2f})"
        )