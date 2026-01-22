def detect_intent(question: str) -> str:
    q = question.lower()

    if any(word in q for word in ["comportement", "attitude", "réaction"]):
        return "behavior"
    if any(word in q for word in ["stratégie", "business", "décision", "choisir"]):
        return "strategy"
    if any(word in q for word in ["pourquoi", "cause", "conséquence"]):
        return "causal"

    return "general"