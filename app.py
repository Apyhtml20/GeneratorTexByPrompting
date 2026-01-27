import io
import zipfile
from flask import Flask, render_template, request, jsonify, send_file
from template_data import SYSTEM_PROMPT, TEMPLATE_RESULT

app = Flask(__name__)

def refine_prompt(user_message: str) -> str:
    """
    Transforme un prompt brut en prompt structuré SCQA + ICDF (style académique).
    Sans API : c'est une 'correction' par règles simples.
    """
    cleaned = user_message.strip()
    if not cleaned:
        cleaned = "Générer un template LaTeX pour rapport de stage."

    # On détecte quelques intentions
    wants_pdf = "pdf" in cleaned.lower()
    wants_word = "word" in cleaned.lower() or "docx" in cleaned.lower()
    wants_ppt = "ppt" in cleaned.lower() or "powerpoint" in cleaned.lower() or "pptx" in cleaned.lower()

    outputs = []
    if wants_pdf: outputs.append("PDF")
    if wants_word: outputs.append("DOCX")
    if wants_ppt: outputs.append("PPTX")
    if not outputs: outputs = ["PDF", "DOCX", "PPTX"]

    output_str = " / ".join(outputs)

    return f"""RÔLE :
Tu es un expert en rédaction académique et en LaTeX spécialisé dans les rapports de stage d’écoles d’ingénieurs, compatible Pandoc.

OBJECTIF :
Générer un template LaTeX modulaire (sans contenu technique) permettant de produire : {output_str}, à partir d’une source unique.

CONTEXTE (SCQA) :
Les rapports exigent une structure normée, des pages obligatoires et une maintenance fiable.

QUESTION (SCQA) :
Comment produire un template unique, maintenable, réutilisable et exportable sans réécriture ?

RÉPONSE ATTENDUE (SCQA) :
Architecture LaTeX modulaire, fichiers séparés, métadonnées centralisées, sections balisées compatibles Pandoc.

ENTRÉES (ICDF) :
Titre du rapport, étudiant, filière, année, encadrants, établissement.

CONTRAINTES (ICDF) :
Sobriété académique, packages standards, séparation contenu/forme, compatible Pandoc.

DIRECTIVES (ICDF) :
Page de garde, remerciements, résumés FR/EN, table des matières, chapitres, bibliographie, annexes.
Ajouter des commentaires pédagogiques dans les fichiers.
"""

def generate_neutral_template() -> dict:
    """
    Retourne une copie du TEMPLATE_RESULT en mode neutre :
    pas de sujet microservices, pas de contenu technique.
    """
    data = dict(TEMPLATE_RESULT)

    data["topic_example"] = "Rapport de stage (template neutre)"

    for f in data["files"]:
        if f["path"] == "config/metadata.tex":
            f["content"] = f["content"].replace(
                "Conception et Développement d’une Architecture Microservices",
                "Rapport de stage"
            )
        # Option : neutraliser le contenu des chapitres
        if f["path"].startswith("chapters/"):
            f["content"] = f["content"].replace(
                "Architecture, conception, implémentation, tests, résultats.",
                "Contenu à compléter par l’étudiant."
            )

    return data

@app.route("/api/refine", methods=["POST"])
def refine():
    msg = request.json.get("message", "")
    refined = refine_prompt(msg)
    return jsonify({"ok": True, "refined_prompt": refined})

def simulate_llm(user_message: str) -> dict:
    refined = refine_prompt(user_message)
    neutral = generate_neutral_template()

    return {
        "prompt_used": refined.strip(),    # on affiche le prompt corrigé (framework)
        "user_message": user_message,
        "result": neutral
    }


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "")
    payload = simulate_llm(msg)
    return jsonify({"ok": True, "data": payload})

@app.route("/api/zip", methods=["POST"])
def zip_project():
    result = request.json.get("result")
    mem = io.BytesIO()

    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as z:
        for f in result["files"]:
            z.writestr(f["path"], f["content"])

    mem.seek(0)
    return send_file(
        mem,
        mimetype="application/zip",
        as_attachment=True,
        download_name="template_latex_rapport_stage.zip"
    )

if __name__ == "__main__":
    app.run(debug=False)
