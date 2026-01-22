def analyze(question: str, frame: dict) -> dict:
    analysis = {}

    for axis in frame["axes"]:
        analysis[axis] = f"Éléments possibles liés à '{axis}' en lien avec la question."

    return analysis