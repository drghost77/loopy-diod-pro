def get_frame(intent: str) -> dict:
    if intent == "behavior":
        return {
            "type": "Analyse comportementale",
            "axes": ["motivations", "freins", "intérêts", "biais possibles"]
        }

    if intent == "strategy":
        return {
            "type": "Analyse stratégique",
            "axes": ["objectifs", "ressources", "options", "risques"]
        }

    if intent == "causal":
        return {
            "type": "Analyse causale",
            "axes": ["causes directes", "causes indirectes", "conséquences court terme", "conséquences long terme"]
        }

    return {
        "type": "Analyse générale",
        "axes": ["faits observables", "hypothèses", "implications"]
    }