import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Charger la Knowledge Base
def charger_knowledge_base(chemin):
    with open(chemin, "r", encoding="utf-8") as f:
        return f.read()

KNOWLEDGE_BASE = charger_knowledge_base("knowledge_base/stef_data.txt")

# Rechercher les passages pertinents
def rechercher_contexte(question, knowledge_base):
    question_lower = question.lower()
    sections = knowledge_base.split("===")
    contexte_pertinent = []
    for section in sections:
        section = section.strip()
        if any(mot in section.lower() for mot in question_lower.split()):
            contexte_pertinent.append(section)
    if not contexte_pertinent:
        return knowledge_base[:1500]
    return "\n\n".join(contexte_pertinent[:3])

# L'agent principal
def agent_stef(question, historique):
    contexte = rechercher_contexte(question, KNOWLEDGE_BASE)
    
    prompt_systeme = """Tu es un assistant expert de STEF, le leader européen 
    de la logistique du froid. Tu réponds aux questions des équipes métiers 
    en te basant uniquement sur les informations fournies dans le contexte.
    Tes réponses sont claires, précises et orientées vers l'action.
    Si la réponse n'est pas dans le contexte, dis-le honnêtement.
    Tu te souviens des échanges précédents dans la conversation."""
    
    messages = [{"role": "system", "content": prompt_systeme}]
    
    if len(historique) == 0:
        premier_message = f"""Contexte STEF :
{contexte}

Question : {question}"""
        messages.append({"role": "user", "content": premier_message})
    else:
        for echange in historique:
            messages.append({"role": "user", "content": echange["question"]})
            messages.append({"role": "assistant", "content": echange["reponse"]})
        messages.append({"role": "user", "content": f"Contexte supplémentaire :\n{contexte}\n\nQuestion : {question}"})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=500,
        temperature=0.3
    )
    
    return response.choices[0].message.content

# Sauvegarder la conversation
def sauvegarder_conversation(historique):
    if not os.path.exists("conversations"):
        os.makedirs("conversations")
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"conversations/session_{horodatage}.json"
    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(historique, f, ensure_ascii=False, indent=2)

# Routes Flask
@app.route("/")
def index():
    session["historique"] = []
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "").strip()
    
    if not question:
        return jsonify({"erreur": "Question vide"}), 400
    
    historique = session.get("historique", [])
    reponse = agent_stef(question, historique)
    
    historique.append({
        "question": question,
        "reponse": reponse,
        "horodatage": datetime.now().strftime("%H:%M:%S")
    })
    session["historique"] = historique
    
    return jsonify({"reponse": reponse})

@app.route("/sauvegarder", methods=["POST"])
def sauvegarder():
    historique = session.get("historique", [])
    if historique:
        sauvegarder_conversation(historique)
        return jsonify({"message": "Conversation sauvegardée"})
    return jsonify({"message": "Aucune conversation à sauvegarder"})

@app.route("/reinitialiser", methods=["POST"])
def reinitialiser():
    session["historique"] = []
    return jsonify({"message": "Conversation réinitialisée"})

if __name__ == "__main__":
    app.run(debug=True)