# 🚛 Agent IA STEF — Logistique du Froid

> Prototype d'agent conversationnel RAG appliqué à la logistique du froid.  
> Développé dans le cadre d'une candidature à l'alternance chez **STEF**, leader européen du transport et de la logistique du froid.

---

## 🎯 Objectif

Ce projet démontre comment un agent IA peut rendre les données opérationnelles d'une entreprise logistique **accessibles en langage naturel** à n'importe quel collaborateur — sans formation technique.

Un employé STEF peut poser des questions comme :
- *"Quelle est la température réglementaire pour transporter des surgelés ?"*
- *"Quels sont nos KPI principaux ?"*
- *"Comment l'IA peut optimiser nos tournées de livraison ?"*

Et obtenir une réponse précise, contextuelle et instantanée.

---

## 🏗️ Architecture — Le principe RAG

```
Question utilisateur
        ↓
Recherche dans la Knowledge Base STEF
(données opérationnelles, KPI, réglementation...)
        ↓
Contexte pertinent extrait
        ↓
LLM (Llama 3.3 via Groq) génère la réponse
en se basant uniquement sur ce contexte
        ↓
Réponse affichée dans l'interface web
```

**RAG = Retrieval Augmented Generation**  
Le LLM ne répond pas depuis sa mémoire générale — il s'appuie sur les données réelles de l'entreprise. Résultat : des réponses fiables, précises et auditables.

---

## ✨ Fonctionnalités

- **Interface web moderne** — chat intuitif accessible depuis le navigateur
- **Mémoire de conversation** — l'agent se souvient des échanges précédents dans la session
- **Recherche contextuelle** — sélection intelligente des passages pertinents dans la Knowledge Base
- **Sauvegarde automatique** — chaque session est exportée en JSON horodaté
- **Questions suggérées** — accès rapide aux questions fréquentes
- **Nouvelle session** — réinitialisation en un clic

---

## 🛠️ Stack technique

| Composant | Technologie |
|---|---|
| Backend | Python 3.13 + Flask |
| LLM | Llama 3.3 70B via API Groq |
| RAG | Implémentation custom Python |
| Frontend | HTML5 / CSS3 / JavaScript vanilla |
| Gestion des secrets | python-dotenv |
| Environnement | venv isolé |

---

## 🚀 Installation et lancement

### Prérequis
- Python 3.10+
- Un compte Groq (gratuit) : [console.groq.com](https://console.groq.com)

### 1. Cloner le repo

```bash
git clone https://github.com/TON_USERNAME/agent-ia-stef.git
cd agent-ia-stef
```

### 2. Créer et activer l'environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate.bat

# Mac / Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la clé API

Crée un fichier `.env` à la racine (voir `.env.example`) :

```
GROQ_API_KEY=ta-clé-groq-ici
```

### 5. Lancer l'application

```bash
python app.py
```

Ouvre ton navigateur sur **http://localhost:5000**

---

## 📁 Structure du projet

```
agent-ia-stef/
│
├── knowledge_base/
│   └── stef_data.txt        # Base de connaissance STEF
│
├── templates/
│   └── index.html           # Interface web
│
├── conversations/           # Sessions sauvegardées (auto-généré)
│
├── app.py                   # Serveur Flask + agent RAG
├── agent.py                 # Agent en mode terminal
├── requirements.txt         # Dépendances
├── .env.example             # Template configuration
├── .gitignore               # Fichiers exclus de Git
└── README.md
```

---

## 💡 Lien avec les enjeux STEF

Ce prototype répond directement aux 3 piliers digitaux de STEF :

**Pilier 1 — IA Appliquée**  
Un modèle simple, interprétable et à fort impact opérationnel. Les équipes terrain obtiennent des réponses basées sur de vraies données, pas des généralités.

**Pilier 2 — Automatisation**  
La sauvegarde automatique des conversations et la recherche contextuelle automatisent des tâches qui se faisaient manuellement (chercher dans des docs, interroger un expert...).

**Pilier 3 — Low Code**  
L'interface web est conçue pour être utilisée sans aucune compétence technique. N'importe quel opérateur, commercial ou manager peut l'utiliser.

---

## 🔮 Évolutions envisagées

- Connexion aux données réelles STEF (ERP, capteurs IoT, tickets incidents)
- Ajout d'un module de prédiction de demande (Machine Learning)
- Déploiement cloud pour un accès multi-sites
- Intégration d'un système de feedback utilisateur
- Support multilingue pour les équipes européennes

---

## 👤 Auteur

**KINHOU Déo-Gracias**  
Futur élève-ingénieur — CESI Lyon (2026-2029)  
[linkedin.com/in/deograciaskinhou](https://linkedin.com/in/deograciaskinhou)  
[dkinhou.github.io/monportfolio](https://dkinhou.github.io/monportfolio)

---

*Prototype développé en autonomie dans le cadre d'une candidature à l'alternance chez STEF — Mai 2026*