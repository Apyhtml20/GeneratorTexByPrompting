# template_data.py

SYSTEM_PROMPT = r"""
4 – LE INPUT DONNÉ AU CHATBOT

PROMPT

RÔLE :
Tu es un expert en rédaction académique et en LaTeX, spécialisé dans la conception
de rapports de stage et de projets de fin d’études d’écoles d’ingénieurs,
conformes aux normes universitaires en vigueur (ENSA / écoles d’ingénieurs francophones).
Tu maîtrises la structuration documentaire académique, la modularité LaTeX
et la compatibilité Pandoc pour l’export multi-formats (PDF, DOCX, PPTX).

OBJECTIF :
Générer un template LaTeX modulaire, maintenable et professionnel de rapport de stage,
permettant, à partir d’une source LaTeX unique, de produire automatiquement :
- un PDF académique,
- un document Word (.docx),
- une présentation PowerPoint (.pptx),
sans duplication ni réécriture du contenu.

CONTEXTE (SCQA – Situation & Complication) :
Les rapports de stage d’ingénieur présentent :
- des exigences académiques strictes (pages obligatoires, chapitres normés, bibliographie),
- des variations selon les filières, départements et établissements,
- des formats de sortie multiples (PDF, Word, PowerPoint),
ce qui rend la rédaction, l’évolution et la maintenance des documents
complexes, répétitives et sujettes aux incohérences.

QUESTION (SCQA) :
Comment concevoir un template unique, structuré et maintenable,
capable de s’adapter automatiquement à plusieurs formats de sortie
tout en respectant les normes académiques,
sans réécriture du contenu ?

RÉPONSE ATTENDUE (SCQA – Answer) :
En concevant une architecture LaTeX modulaire, basée sur :
- des fichiers séparés,
- des métadonnées centralisées,
- des sections clairement balisées,
entièrement compatible avec Pandoc pour l’export multi-formats.

ENTRÉES (Input – ICDF) :
Le template doit accepter les paramètres suivants :
- Titre du projet,
- Nom et prénom de l’étudiant,
- Filière et établissement,
- Année universitaire,
- Encadrants (académique et professionnel),
- Langue principale (français).

Ces paramètres doivent être centralisés et facilement modifiables.

CONTRAINTES (Constraints – ICDF) :
- Compatibilité totale avec Pandoc (PDF / DOCX / PPTX),
- Respect de la structure académique standard des rapports de stage,
- Aucune dépendance à des packages LaTeX non standards,
- Mise en forme sobre et académique (pas de couleurs excessives),
- Séparation stricte entre contenu, configuration et mise en forme.

DIRECTIVES (Directives – ICDF) :
1. Proposer une architecture de fichiers LaTeX claire et hiérarchisée
   (ex. main.tex, config/, frontmatter/, chapters/, backmatter/).
2. Centraliser toutes les informations variables dans un fichier de métadonnées unique.
3. Prévoir explicitement :
   - page de garde,
   - remerciements,
   - résumés (français + anglais),
   - table des matières,
   - chapitres principaux,
   - bibliographie,
   - annexes.
4. Ajouter des commentaires pédagogiques expliquant le rôle de chaque fichier.
5. Préparer le template pour une conversion simple, reproductible et maintenable
   avec Pandoc vers Word et PowerPoint.

ÉTAPE APRÈS LA RÉDACTION DU PROMPT (FEW-SHOTS) :
Après la conception du prompt principal, une étape complémentaire de few-shot prompting
a été mise en œuvre afin d’orienter le modèle vers des propositions cohérentes avec
les standards académiques des projets de fin d’études d’ingénieur.

Dans cette phase, des extraits de rapports de PFE réalisés par des lauréats
des promotions précédentes ont été fournis à titre d’exemples.
Ces documents n’ont pas été utilisés comme source de contenu à reproduire,
mais comme références structurelles et thématiques, permettant de mieux comprendre :
- le niveau académique attendu,
- la nature des sujets validés précédemment,
- le périmètre technique généralement accepté pour un PFE.

À l’issue de cette étape, le modèle a suggéré le sujet :
« Conception et Développement d’une Architecture Microservices ».

Ce sujet a été retenu à titre illustratif et utilisé de manière volontairement minimaliste
dans le cadre du template LaTeX développé.
L’objectif n’était pas de traiter le domaine des microservices en profondeur,
mais de disposer d’un exemple réaliste, technique et conforme aux attentes d’un PFE,
afin de :
- valider la structure du template,
- tester la cohérence des sections générées,
- illustrer le fonctionnement du prompt conçu.

Ainsi, le sujet constitue un support démonstratif,
indépendant du contenu technique final,
permettant d’évaluer la capacité du template à accueillir
n’importe quel thème de rapport ou de PFE.
"""

TEMPLATE_RESULT = {
    "project_name": "rapport-stage-ingenieur",
    "topic_example": "Conception et Développement d’une Architecture Microservices",
    "files": [
        {
            "path": "main.tex",
            "content": r"""\documentclass[12pt,a4paper]{report}

\input{config/packages}
\input{config/metadata}

\begin{document}

% --- Frontmatter ---
\input{frontmatter/titlepage_pdf}
\pagenumbering{roman}
\input{frontmatter/remerciements}
\input{frontmatter/resume}
\tableofcontents
\listoffigures
\listoftables

% --- Mainmatter ---
\cleardoublepage
\pagenumbering{arabic}
\input{chapters/01_introduction}
\input{chapters/02_contexte}
\input{chapters/03_realisation}
\input{chapters/04_conclusion}

% --- Backmatter ---
\cleardoublepage
\bibliographystyle{plain}
\bibliography{references}

\appendix
\input{backmatter/annexes}

\end{document}
"""
        },
        {
            "path": "references.bib",
            "content": r"""@book{newman2015building,
  title={Building Microservices},
  author={Newman, Sam},
  year={2015},
  publisher={O'Reilly Media}
}
"""
        },
        {
            "path": "config/metadata.tex",
            "content": r"""\newcommand{\ReportTitle}{Conception et Développement d’une Architecture Microservices}
\newcommand{\StudentName}{NOM Prénom}
\newcommand{\School}{École Nationale des Sciences Appliquées}
\newcommand{\Department}{Génie Informatique}
\newcommand{\AcademicYear}{2025--2026}
\newcommand{\SupervisorAcademic}{Pr. Nom Encadrant}
\newcommand{\SupervisorCompany}{Mme/Mr. Nom Encadrant}
"""
        },
        {
            "path": "config/packages.tex",
            "content": r"""\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{geometry}
\geometry{top=3cm,bottom=3cm,left=4.5cm,right=2cm}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{setspace}
\onehalfspacing
"""
        },
        {
            "path": "frontmatter/titlepage_pdf.tex",
            "content": r"""\begin{titlepage}
\centering
{\Large \School \par}
\vspace{0.5cm}
{\large \Department \par}
\vspace{1.5cm}
{\Huge \bfseries \ReportTitle \par}
\vspace{1.5cm}
{\Large Rapport de Stage \par}
\vfill
{\large Réalisé par : \StudentName \par}
\vspace{0.5cm}
{\large Encadré par : \SupervisorAcademic \par}
{\large Encadrant entreprise : \SupervisorCompany \par}
\vspace{1cm}
{\large Année universitaire : \AcademicYear \par}
\end{titlepage}
"""
        },
        {
            "path": "frontmatter/remerciements.tex",
            "content": r"""\chapter*{Remerciements}
\addcontentsline{toc}{chapter}{Remerciements}
Votre texte de remerciements ici.
"""
        },
        {
            "path": "frontmatter/resume.tex",
            "content": r"""\chapter*{Résumé}
\addcontentsline{toc}{chapter}{Résumé}
Résumé en français (200--250 mots maximum).

\bigskip
\textbf{Mots-clés :} microservices, architecture, API, conteneurs, DevOps.

\chapter*{Abstract}
\addcontentsline{toc}{chapter}{Abstract}
English abstract (200--250 words).

\bigskip
\textbf{Keywords:} microservices, architecture, API, containers, DevOps.
"""
        },
        {
            "path": "chapters/01_introduction.tex",
            "content": r"""\chapter{Introduction}
Contexte, problématique, objectifs, plan du rapport.
"""
        },
        {
            "path": "chapters/02_contexte.tex",
            "content": r"""\chapter{Contexte et état de l’art}
Présentation de l’entreprise, du besoin, et synthèse bibliographique.
"""
        },
        {
            "path": "chapters/03_realisation.tex",
            "content": r"""\chapter{Réalisation}
Architecture, conception, implémentation, tests, résultats.
"""
        },
        {
            "path": "chapters/04_conclusion.tex",
            "content": r"""\chapter{Conclusion et perspectives}
Bilan, limites, perspectives.
"""
        },
        {
            "path": "backmatter/annexes.tex",
            "content": r"""\chapter{Annexes}
Ajouter vos annexes ici (captures, tableaux, extraits, etc.).
"""
        },
    ],
    "build": {
        "pdf": "pdflatex main.tex (x2) puis bibtex puis pdflatex (x2)",
        "pandoc_docx": "pandoc main.tex -o rapport.docx",
        "pandoc_pptx": "pandoc main.tex -t pptx -o soutenance.pptx"
    },
    "comments": [
        "Mode démonstration : résultat simulé (sans appel API).",
        "Le framework SCQA + ICDF est affiché comme prompt utilisé.",
        "Le sujet ‘Architecture Microservices’ est un exemple minimaliste pour valider le template."
    ]
}
