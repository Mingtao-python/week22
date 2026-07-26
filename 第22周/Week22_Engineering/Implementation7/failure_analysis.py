def analyze_failure(query, retrieved, correct):
    if not retrieved:
        return "Retrieval failure: no documents retrieved."

    if correct not in retrieved:
        return "Retrieval failure: correct document not retrieved."

    return "LLM failure: misinterpreted context despite correct retrieval."


if __name__ == "__main__":
    print(analyze_failure("python", ["java info"], "python info"))
# :)