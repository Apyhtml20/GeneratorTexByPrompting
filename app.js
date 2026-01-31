/* ==========================
   PDF behavior (exactly requested)
   - iframe shows template.pdf
   - button "GÉNÉRER PDF" downloads exemple.pdf
========================== */
const PDF_IFRAME_PATH = "assets/pdf/exemple.pdf";   // displayed
const PDF_GENERATED_PATH = "assets/pdf/template.pdf"; // downloaded by btnPdf
const PDF_TEMPLATE1_PATH = "assets/pdf/exemple.pdf"; // optional hidden unlock

/* Helpers */
const $ = (s) => document.querySelector(s);

function toast(msg){
  const t = $("#toast");
  if(!t) return;
  t.textContent = msg;
  t.classList.add("toast--show");
  clearTimeout(window.__tt);
  window.__tt = setTimeout(()=>t.classList.remove("toast--show"), 1500);
}

function setStatus(text, ok=true){
  $("#statusText").textContent = text;
  const pill = $("#statusPill");
  pill.textContent = ok ? "OK" : "ERR";
  pill.className = "pill " + (ok ? "pill--ok":"pill--err");
}

function setStep(n){
  ["#step1","#step2","#step3"].forEach((id,i)=>{
    const el = $(id);
    if(!el) return;
    el.classList.toggle("step--active", i === (n-1));
  });
}

function copyText(text){
  navigator.clipboard.writeText(text || "").then(()=>toast("Copié ✅"));
}

function downloadFile(path, filename){
  const a = document.createElement("a");
  a.href = path;
  a.download = filename;
  a.click();
}

/* Tabs */
document.querySelectorAll(".tab").forEach(btn=>{
  btn.addEventListener("click", ()=>{
    document.querySelectorAll(".tab").forEach(b=>b.classList.remove("tab--active"));
    document.querySelectorAll(".panel").forEach(p=>p.classList.remove("panel--active"));
    btn.classList.add("tab--active");
    $("#tab-" + btn.dataset.tab)?.classList.add("panel--active");
  });
});

/* Sidebar progress */
window.addEventListener("scroll", ()=>{
  const h = document.documentElement;
  const sc = h.scrollTop;
  const max = h.scrollHeight - h.clientHeight;
  const p = max <= 0 ? 0 : (sc / max) * 100;
  const bar = $("#progressBar");
  if(bar) bar.style.width = p + "%";
});

/* Load iframe pdf = template.pdf */
window.addEventListener("DOMContentLoaded", ()=>{
  const frame = $("#pdfModelFrame");
  if(frame) frame.src = PDF_IFRAME_PATH;
});

/* Download template.pdf (top + in form + pdf tab) */
$("#btnPdfModelTop")?.addEventListener("click", ()=> downloadFile(PDF_IFRAME_PATH, "template.pdf"));
$("#btnPdfModel")?.addEventListener("click", ()=> downloadFile(PDF_IFRAME_PATH, "template.pdf"));
$("#btnPdfModel2")?.addEventListener("click", ()=> downloadFile(PDF_IFRAME_PATH, "template.pdf"));

/* Example */
$("#btnExample")?.addEventListener("click", ()=>{
  $("#input").value =
`Génère un template LaTeX ENSA :
- Page de garde 2 logos + lignes
- Remerciements, Résumé/Abstract, Table des matières, Liste des tableaux
- Chapitres : Introduction, Contexte, Réalisation, Conclusion
- Bibliographie + Annexes
Contraintes : neutre, maintenable, arborescence modulaire.`;
  setStep(1);
  setStatus("Exemple chargé.");
  toast("Exemple chargé.");
});

/* Correction prompt */
let isCorrected = false;

function buildCorrectedPrompt(userText){
  const safe = (userText || "").trim() || "(demande non fournie)";
  return `# PROMPT STRUCTURÉ (SCQA + ICDF + Few-shot + CO-STAR + STaR)

## SCQA
Situation : rapport académique avec pages obligatoires.
Complication : variations, multi-formats, maintenance.
Question : template unique, maintenable, exportable ?
Answer : modules + métadonnées centralisées.

## ICDF
Input : ${safe}
Constraints : neutre, clair, compatible LaTeX/PDF, placeholders.
Directives : config centralisée + fichiers séparés.
Format : arborescence LaTeX + main.tex + previews.

## Few-shot
Référence structurelle (ancien rapport) → même forme, contenu remplacé par placeholders.

## CO-STAR
Context : ENSA (stage/PFE).
Objective : template neutre réutilisable.
Style/Tone : académique, concis.
Audience : étudiant/encadrant/jury.
Response : ZIP LaTeX complet.

## STaR
Analyser → Contraintes → Structurer → Générer → Vérifier → Exporter.`;
}

$("#btnRefine")?.addEventListener("click", ()=>{
  const corrected = buildCorrectedPrompt($("#input").value);
  $("#correctionBox").textContent = corrected;
  isCorrected = true;
  setStep(2);
  setStatus("Prompt corrigé.");
  toast("Correction générée.");
});

$("#btnCopyCorrection")?.addEventListener("click", ()=> copyText($("#correctionBox").textContent));
$("#btnCopyFrameworks")?.addEventListener("click", ()=> copyText($("#fwBox").textContent));

/* Generate ZIP */
let generatedProject = null;

function makeProjectFiles(){
  const files = {};

  files["config/packages.tex"] = String.raw`
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[french]{babel}
\usepackage{geometry}
\geometry{top=2cm,bottom=2cm,left=2cm,right=2cm}
\usepackage{setspace}
\onehalfspacing
\usepackage{graphicx}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[C]{\thepage}
`;

  files["config/metadata.tex"] = String.raw`
\newcommand{\universityName}{Université Mohammed Premier}
\newcommand{\schoolName}{École Nationale des Sciences Appliquées d’Oujda}
\newcommand{\reportTitle}{Titre principal du rapport}
\newcommand{\reportSubtitle}{Sous-titre / Sujet (optionnel)}
\newcommand{\reportType}{Rapport de Stage de Fin d’Études — Template}
\newcommand{\studentName}{Nom Prénom}
\newcommand{\academicSupervisorA}{Mr ...}
\newcommand{\academicSupervisorB}{Mme ...}
\newcommand{\juryA}{Mr ...}
\newcommand{\juryArole}{Président}
\newcommand{\juryB}{Mme ...}
\newcommand{\juryBrole}{Examinatrice}
\newcommand{\academicYear}{2025--2026}
\newcommand{\schoolLogo}{images/logo_ecole.jpg}
\newcommand{\companyLogo}{images/logo_entreprise.jpg}
`;

  files["frontmatter/titlepage_pdf.tex"] = String.raw`
\begin{titlepage}
  \centering
  \begin{minipage}{0.49\textwidth}
    \raggedright
    \IfFileExists{\schoolLogo}{\includegraphics[height=2.5cm]{\schoolLogo}}{\fbox{\rule{0pt}{2.5cm}\rule{4cm}{0pt}}}
  \end{minipage}
  \begin{minipage}{0.49\textwidth}
    \raggedleft
    \IfFileExists{\companyLogo}{\includegraphics[height=2.5cm]{\companyLogo}}{\fbox{\rule{0pt}{2.5cm}\rule{4cm}{0pt}}}
  \end{minipage}

  \vspace{1.2cm}
  {\Large \textsc{\universityName}\par}
  {\Large \textsc{\schoolName}\par}
  \vspace{1cm}

  \rule{\linewidth}{0.5mm}\par
  \vspace{0.4cm}
  {\huge \bfseries \reportTitle\par}
  \vspace{0.2cm}
  {\huge \bfseries \reportSubtitle\par}
  \vspace{0.4cm}
  \rule{\linewidth}{0.5mm}\par

  \vspace{0.7cm}
  {\Large \textit{\reportType}\par}

  \vspace{1.8cm}
  {\Large \textbf{Réalisé par :}}\\
  {\Large \studentName}

  \vfill
  {\large Année Universitaire : \academicYear\par}
\end{titlepage}
`;

  files["main.tex"] = String.raw`
\documentclass[12pt,a4paper]{report}
\input{config/packages.tex}
\input{config/metadata.tex}
\begin{document}
\input{frontmatter/titlepage_pdf.tex}
\tableofcontents
\chapter{Introduction}
\chapter{Contexte}
\chapter{Réalisation}
\chapter{Conclusion}
\end{document}
`;

  return files;
}

function makeTreeText(){
  return `main.tex
config/
  packages.tex
  metadata.tex
frontmatter/
  titlepage_pdf.tex
images/
  logo_ecole.jpg
  logo_entreprise.jpg`;
}

$("#btnGenerate")?.addEventListener("click", ()=>{
  const text = ($("#input").value || "").trim();
  if(!text){
    setStatus("Écris une demande d’abord.", false);
    toast("Champ vide.");
    return;
  }

  generatedProject = makeProjectFiles();
  $("#previewMain").textContent = generatedProject["main.tex"];
  $("#previewMeta").textContent = generatedProject["config/metadata.tex"];
  $("#treeBox").textContent = makeTreeText();

  $("#btnZip").disabled = false;

  const b = $("#btnPdfTemplate1");
  if(b){
    b.style.display = "inline-flex";
    b.disabled = false;
  }

  setStep(3);
  setStatus("Template généré. ZIP prêt.");
  toast("Génération OK.");
});

$("#btnZip")?.addEventListener("click", async ()=>{
  if(!generatedProject){
    toast("Génère d’abord le template.");
    return;
  }
  const zip = new JSZip();
  Object.entries(generatedProject).forEach(([p,c])=>zip.file(p,c));
  const blob = await zip.generateAsync({type:"blob"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "template_latex_ensa.zip";
  a.click();
  toast("ZIP téléchargé.");
});

/* template(1) optional download */
$("#btnPdfTemplate1")?.addEventListener("click", ()=>{
  downloadFile(PDF_TEMPLATE1_PATH, "template(1).pdf");
});

/* ✅ MAIN REQUEST:
   Button "GÉNÉRER PDF" downloads exemple.pdf
   and ONLY works after prompt is corrected + generated (optional).
*/
$("#btnPdf")?.addEventListener("click", ()=>{
  const text = ($("#input").value || "").trim();
  if(!text){
    toast("Écris le prompt d’abord.");
    setStatus("Prompt vide.", false);
    return;
  }
  if(!isCorrected){
    toast("Corrige d’abord le prompt (↺).");
    setStatus("Tu dois corriger avant.", false);
    setStep(2);
    return;
  }
  // (Option) if you want to force generation too:
  // if(!generatedProject){ toast("Génère le template (⚡) avant."); return; }

  downloadFile(PDF_GENERATED_PATH, "exemple.pdf");
  toast("PDF généré ✅ (exemple.pdf)");
  setStatus("PDF téléchargé.");
});
