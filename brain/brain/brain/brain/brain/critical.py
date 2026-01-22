from .knowledge_base import BIAS

def critical_review(question: str) -> dict:
    return {
        "hypotheses_non_verifiees": "Les informations sont partielles ou implicites.",
        "biais_probables": BIAS[:2],
        "manques": "Données contextuelles supplémentaires nécessaires pour conclure avec certitude."
    }