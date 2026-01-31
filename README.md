# 📄 Template Studies Generator (LaTeX)

**Template Studies Generator** est un projet académique qui combine  
👉 **Prompt Engineering**,  
👉 **Frameworks de prompting**,  
👉 et **génération automatique de templates LaTeX**  

afin d’aider les étudiants à produire rapidement des **rapports académiques bien structurés**, sans se soucier de la mise en forme LaTeX.

---

## 🎯 Objectifs pédagogiques

- Appliquer les concepts du **Prompt Engineering**
- Utiliser des **frameworks de prompting** pour guider la génération
- Corriger et améliorer automatiquement les prompts mal formulés
- Générer des **templates LaTeX standards**, propres et académiques
- Séparer clairement :
  - **la structure du document**
  - **le contenu scientifique**

---

## 🧠 Prompt Engineering & Frameworks utilisés

Le projet repose sur une **méthodologie structurée de rédaction de prompts**, inspirée des frameworks étudiés en cours.

### 🔹 Frameworks intégrés

- **CRISP Prompting**
  - Context
  - Role
  - Instructions
  - Structure
  - Parameters

- **Template-based Prompting**
  - Prompts prédéfinis et réutilisables
  - Normalisation des entrées utilisateur

- **Chain of Thought (simplifié)**
  - Analyse du prompt
  - Correction logique
  - Génération structurée du template

---

## ✍️ Correction et amélioration des prompts

Le système est capable de :

- Détecter les prompts :
  - vagues
  - incomplets
  - mal structurés
- Reformuler automatiquement le prompt
- Adapter le prompt à un **format académique LaTeX**
- Ignorer le contenu scientifique pour ne produire que :
  - la structure
  - les sections
  - les environnements LaTeX

👉 Objectif : **aider l’étudiant à apprendre à bien formuler un prompt**

---

## 🧩 Fonctionnalités principales

- Génération automatique de :
  - Page de garde
  - Table des matières
  - Listes des figures et tableaux
  - Sections académiques standards :
    - Introduction
    - Problématique
    - Méthodologie
    - Résultats
    - Discussion
    - Conclusion
- Correction du prompt utilisateur
- Génération d’un **template LaTeX propre et compilable**
- Interface simple et pédagogique

---

## 🛠️ Technologies utilisées

- **LaTeX**
- **HTML5**
- **CSS3**
- **JavaScript (DOM & logique de prompting)**
- (Optionnel) Génération PDF côté navigateur

---

## 📁 Structure du projet

```text
TemplateStudiesGeneratorTex/
│
├── index.html        # Interface utilisateur
├── style.css         # Design de l'application
├── script.js         # Prompting + génération LaTeX
├── templates/        # Templates LaTeX génériques
│   └── report.tex
├── assets/           # Logos, images
├── README.md
