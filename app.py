import os
import io
import zipfile
from flask import Flask, render_template, request, jsonify, send_file

# -----------------------------------------------------------------------------
# Flask app
# -----------------------------------------------------------------------------
app = Flask(__name__)

# -----------------------------------------------------------------------------
# Prompt Engineering: Correction (SCQA + ICDF) - sans API (démo pédagogique)
# -----------------------------------------------------------------------------
def refine_prompt(user_message: str) -> str:
    cleaned = (user_message or "").strip()
    if not cleaned:
        cleaned = "Générer un template LaTeX de rapport de stage."

    # Détection simple (optionnelle) de formats demandés
    low = cleaned.lower()
    outputs = []
    if "pdf" in low:
        outputs.append("PDF")
    if "word" in low or "docx" in low:
        outputs.append("DOCX")
    if "ppt" in low or "powerpoint" in low or "pptx" in low:
        outputs.append("PPTX")
    if not outputs:
        outputs = ["PDF", "DOCX", "PPTX"]

    output_str = " / ".join(outputs)

    return f"""
RÔLE
Tu es un expert en rédaction académique et en LaTeX spécialisé dans les rapports de stage
d’écoles d’ingénieurs. Tu produis des templates sobres, maintenables et compatibles Pandoc.

OBJECTIF
Générer un template LaTeX modulaire et neutre (sans contenu technique, sans sujet),
permettant de produire : {output_str} à partir d’une seule source.

CONTEXTE (SCQA)
- Situation : rapports de stage académiques avec pages et sections obligatoires.
- Complication : variations selon filières + multi-formats + maintenance difficile.
- Question : comment concevoir un template unique, maintenable et exportable ?
- Answer : architecture LaTeX modulaire, métadonnées centralisées, sections balisées.

ENTRÉES (ICDF)
- Titre du rapport (neutre)
- Nom et prénom de l’étudiant
- Établissement / filière
- Année universitaire
- Encadrant académique + encadrant entreprise
- Langue principale (FR) + résumé EN

CONTRAINTES (ICDF)
- Template neutre : aucun contenu technique, pas de sujet imposé.
- Sobriété académique (pas de design excessif).
- Séparation stricte contenu / mise en forme.
- Packages LaTeX standards uniquement.
- Compatibilité Pandoc pour DOCX/PPTX.

DIRECTIVES (ICDF)
1) Proposer une arborescence claire : main.tex, config/, frontmatter/, chapters/, backmatter/.
2) Centraliser les informations variables dans config/metadata.tex.
3) Inclure : page de garde, remerciements, résumés FR/EN, table des matières,
   chapitres, bibliographie (BibTeX), annexes.
4) Ajouter des commentaires pédagogiques dans les fichiers.
5) Fournir des commandes de compilation PDF et de conversion Pandoc.

DEMANDE UTILISATEUR (BRUTE)
{cleaned}
""".strip()


# -----------------------------------------------------------------------------
# Template LaTeX neutre (sans sujet) - résultat structuré renvoyé au front
# -----------------------------------------------------------------------------
def generate_neutral_template() -> dict:
    project_name = "rapport-stage-ingenieur"

    files = [
        # ---------------- config ----------------
        {
            "path": "config/metadata.tex",
            "content": r"""\newcommand{\ReportTitle}{Rapport de stage}
\newcommand{\StudentName}{Nom Prénom}
\newcommand{\SchoolName}{École / Université}
\newcommand{\Department}{Filière / Département}
\newcommand{\AcademicYear}{2025/2026}
\newcommand{\SupervisorAcademic}{Encadrant académique}
\newcommand{\SupervisorCompany}{Encadrant entreprise}
"""
        },
        {
            "path": "config/packages.tex",
            "content": r"""% Packages standards (sobres, compatibles)
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{lmodern}
\usepackage{geometry}
\geometry{margin=2.5cm}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{setspace}
\onehalfspacing

% Bibliographie
\usepackage[numbers]{natbib}
"""
        },

        # ---------------- frontmatter ----------------
        {
            "path": "frontmatter/titlepage_pdf.tex",
            "content": r"""% Page de garde (PDF)
\begin{titlepage}
\centering
\vspace*{2cm}

{\Large \SchoolName \par}
\vspace{1cm}
{\large \Department \par}
\vspace{2cm}

{\LARGE \textbf{\ReportTitle} \par}
\vspace{2cm}

{\large Étudiant : \StudentName \par}
\vspace{1cm}

{\large Encadrant académique : \SupervisorAcademic \par}
{\large Encadrant entreprise : \SupervisorCompany \par}

\vfill
{\large Année universitaire : \AcademicYear \par}
\end{titlepage}
"""
        },
        {
            "path": "frontmatter/remerciements.tex",
            "content": r"""% Remerciements (texte à compléter)
\chapter*{Remerciements}
\addcontentsline{toc}{chapter}{Remerciements}

Texte à compléter par l'étudiant.
"""
        },
        {
            "path": "frontmatter/resume.tex",
            "content": r"""% Résumés FR + EN
\chapter*{Résumé}
\addcontentsline{toc}{chapter}{Résumé}

Résumé en français (à compléter).

\bigskip
\noindent\textbf{Mots-clés :} mot1, mot2, mot3

\chapter*{Abstract}
\addcontentsline{toc}{chapter}{Abstract}

Abstract in English (to complete).

\bigskip
\noindent\textbf{Keywords:} key1, key2, key3
"""
        },

        # ---------------- chapters ----------------
        {
            "path": "chapters/01_introduction.tex",
            "content": r"""\chapter{Introduction}
Contenu à compléter par l'étudiant.
"""
        },
        {
            "path": "chapters/02_contexte.tex",
            "content": r"""\chapter{Contexte et objectifs}
Contenu à compléter par l'étudiant.
"""
        },
        {
            "path": "chapters/03_realisation.tex",
            "content": r"""\chapter{Réalisation}
Contenu à compléter par l'étudiant.
"""
        },
        {
            "path": "chapters/04_conclusion.tex",
            "content": r"""\chapter{Conclusion}
Contenu à compléter par l'étudiant.
"""
        },

        # ---------------- backmatter ----------------
        {
            "path": "backmatter/annexes.tex",
            "content": r"""\appendix
\chapter{Annexes}
Contenu à compléter par l'étudiant.
"""
        },

        # ---------------- bibliography ----------------
        {
            "path": "references.bib",
            "content": r"""@book{latexcompanion,
  title     = {The LaTeX Companion},
  author    = {Frank Mittelbach and Michel Goossens},
  year      = {2004},
  publisher = {Addison-Wesley}
}
"""
        },

        # ---------------- main ----------------
        {
            "path": "main.tex",
            "content": r"""\documentclass[12pt,a4paper]{report}

% Charger config
\input{config/packages}
\input{config/metadata}

\begin{document}

% Page de garde (PDF)
\input{frontmatter/titlepage_pdf}

% Pages liminaires
\input{frontmatter/remerciements}
\input{frontmatter/resume}

% Table des matières
\tableofcontents
\listoffigures
\listoftables
\clearpage

% Chapitres
\input{chapters/01_introduction}
\input{chapters/02_contexte}
\input{chapters/03_realisation}
\input{chapters/04_conclusion}

% Bibliographie
\bibliographystyle{plainnat}
\bibliography{references}

% Annexes
\input{backmatter/annexes}

\end{document}
"""
        },
        # ---------------- build notes ----------------
        {
            "path": "README_BUILD.txt",
            "content": """Commandes utiles

1) Compilation PDF (local):
   pdflatex main.tex
   bibtex main
   pdflatex main.tex
   pdflatex main.tex

2) Conversion Pandoc vers DOCX:
   pandoc main.tex -o rapport.docx

3) Conversion Pandoc vers PPTX (présentation):
   pandoc main.tex -t pptx -o presentation.pptx
"""
        }
    ]

    return {
        "project_name": project_name,
        "topic_example": "Rapport de stage (template neutre)",
        "files": files,
        "build": {
            "pdf": "pdflatex main.tex",
            "pandoc_docx": "pandoc main.tex -o rapport.docx",
            "pandoc_pptx": "pandoc main.tex -t pptx -o presentation.pptx"
        }
    }


# -----------------------------------------------------------------------------
# API Routes
# -----------------------------------------------------------------------------
@app.route("/")
def home():
    # index.html doit être dans templates/
    return render_template("index.html")


@app.route("/api/refine", methods=["POST"])
def api_refine():
    try:
        msg = (request.json or {}).get("message", "")
        refined = refine_prompt(msg)
        return jsonify({"ok": True, "refined_prompt": refined})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        msg = (request.json or {}).get("message", "")
        refined = refine_prompt(msg)
        neutral = generate_neutral_template()
        payload = {
            "prompt_used": refined,
            "user_message": msg,
            "result": neutral
        }
        return jsonify({"ok": True, "data": payload})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/zip", methods=["POST"])
def api_zip():
    try:
        result = (request.json or {}).get("result")
        if not result or "files" not in result:
            return jsonify({"ok": False, "error": "Résultat manquant"}), 400

        mem = io.BytesIO()
        with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as z:
            for f in result["files"]:
                z.writestr(f["path"], f["content"])
        mem.seek(0)

        name = result.get("project_name", "rapport-stage-ingenieur")
        return send_file(
            mem,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"{name}.zip"
        )
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# -----------------------------------------------------------------------------
# Run locally / Railway
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
