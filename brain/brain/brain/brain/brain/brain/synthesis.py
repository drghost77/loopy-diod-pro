def synthesize(question: str, frame: dict, analysis: dict, critique: dict) -> str:
    response = []
    response.append(f"Problème analysé : {question}\n")
    response.append(f"Cadre utilisé : {frame['type']}\n")

    response.append("Analyse structurée :")
    for k, v in analysis.items():
        response.append(f"- {k.capitalize()} : {v}")

    response.append("\nEsprit critique :")
    response.append(f"- Hypothèses : {critique['hypotheses_non_verifiees']}")
    response.append(f"- Biais possibles : {', '.join(critique['biais_probables'])}")
    response.append(f"- Limites : {critique['manques']}")

    return "\n".join(response)