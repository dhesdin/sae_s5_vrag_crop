import json


# WARNING : IT NOT DEPENDS OF SCHEMAS.PY BE CAREFUL TO REPRODUCIBILITY
_EXPECTED_JSON_SHAPE = json.dumps(
    {
        "main_subject": "<string, sujet principal de l'image>",
        "background": "<string, arrière-plan et contexte général>",
        "detected_objects": [
            {
                "label": "<string, nom de l'objet>",
                "color": "<string ou null, couleur dominante>",
                "position": "<string, position relative, ex: 'en haut à gauche', 'centre'>",
                "state": "<string ou null, état notable, ex: 'ouvert', 'cassé'>",
                "bounding_box": {
                    "x": "<number>",
                    "y": "<number>",
                    "width": "<number>",
                    "height": "<number>",
                },
            }
        ],
    },
    ensure_ascii=False, # to avoid escaping non-ASCII characters
    indent=2, # \n and two indent per lines
)

# Examples of valid JSON extractions from images
_JSON_EXAMPLE = json.dumps(
    {
        "main_subject": "un vélo rouge appuyé contre un mur",
        "background": "rue pavée en ville, façade d'immeuble en pierre, fin de journée",
        "detected_objects": [
            {
                "label": "vélo",
                "color": "rouge",
                "position": "centre",
                "state": "à l'arrêt",
                "bounding_box": {"x": 120, "y": 80, "width": 300, "height": 220},
            },
            {
                "label": "panneau de signalisation",
                "color": "bleu",
                "position": "en haut à droite",
                "state": None,
                "bounding_box": None,
            },
            {
                "label": "poubelle",
                "color": "vert",
                "position": "en bas à gauche",
                "state": "fermée",
                "bounding_box": None,
            },
        ],
    },
    ensure_ascii=False, # to avoid escaping non-ASCII characters
    indent=2, # \n and two indent per lines
)


def build_extraction_prompt() -> str:
    """
    Build the prompt for extracting structured information from an image.

    Returns:
        str: The prompt string to be used with the VLM.
    """
    return (
        "CONTEXTE : Tu es un modèle de vision par ordinateur capable d'extraire "
        "des informations structurées à partir d'images.\n"
        "INSTRUCTIONS : Décompose l'image en JSON structuré avec main_subject, "
        "background, detected_objects (label, color, position, state).\n"
        f"FORME DU JSON ATTENDU :\n{_EXPECTED_JSON_SHAPE}\n"
        f"EXEMPLE SUR UNE IMAGE :\n{_JSON_EXAMPLE}\n"
        "RÉPONSE FINALE : ta réponse doit contenir uniquement un objet JSON "
        "valide respectant la forme ci-dessus. Aucun texte avant ou après, "
        "aucun bloc de code Markdown (pas de ```). Toute information "
        "manquante doit valoir null.\n"
    )