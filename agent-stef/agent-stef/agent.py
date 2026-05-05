import os
import json
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

# Charger la clé API
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Charger la Knowledge Base
def charger_knowledge_base(chemin):
    with open(chemin, "r", encoding="utf-8") as f:
        return f.read()

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

# Sauvegarder la conversation
def sauvegarder_conversation(historique):
    if not os.path.exists("conversations"):
        os.makedirs("conversations")
    
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"conversations/session_{horodatage}.json"
    
    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(historique, f, ensure_ascii=False, indent=2)
    
    print(f"\nConversation sauvegardée : {nom_fichier}")

# L'agent principal avec historique
def agent_stef(question, knowledge_base, historique):
    contexte = rechercher_contexte(question, knowledge_base)
    
    prompt_systeme = """Tu es un assistant expert de STEF, le leader européen 
    de la logistique du froid. Tu réponds aux questions des équipes métiers 
    en te basant uniquement sur les informations fournies dans le contexte.
    Tes réponses sont claires, précises et orientées vers l'action.
    Si la réponse n'est pas dans le contexte, dis-le honnêtement.
    Tu te souviens des échanges précédents dans la conversation."""
    
    # Construction des messages avec historique
    messages = [{"role": "system", "content": prompt_systeme}]
    
    # Ajouter le contexte uniquement au premier message utilisateur
    if len(historique) == 0:
        premier_message = f"""Contexte STEF :
{contexte}

Question : {question}

Réponds de façon claire et structurée en te basant sur le contexte fourni."""
        messages.append({"role": "user", "content": premier_message})
    else:
        # Ajouter tout l'historique
        for echange in historique:
            messages.append({"role": "user", "content": echange["question"]})
            messages.append({"role": "assistant", "content": echange["reponse"]})
        
        # Ajouter le contexte mis à jour + la nouvelle question
        nouveau_message = f"""Contexte supplémentaire si nécessaire :
{contexte}

Question : {question}"""
        messages.append({"role": "user", "content": nouveau_message})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=500,
        temperature=0.3
    )
    
    return response.choices[0].message.content

# Interface de conversation
def main():
    print("=" * 60)
    print("    AGENT IA STEF — Logistique du Froid")
    print("=" * 60)
    print("Posez vos questions sur STEF et la logistique du froid.")
    print("Tapez 'quitter' pour terminer et sauvegarder.\n")
    
    knowledge_base = charger_knowledge_base("knowledge_base/stef_data.txt")
    historique = []
    
    while True:
        question = input("Vous : ").strip()
        
        if question.lower() == "quitter":
            if historique:
                sauvegarder_conversation(historique)
            print("Au revoir !")
            break
            
        if not question:
            continue
        
        print("\nAgent STEF : ", end="", flush=True)
        reponse = agent_stef(question, knowledge_base, historique)
        print(reponse)
        print()
        
        # Sauvegarder dans l'historique
        historique.append({
            "question": question,
            "reponse": reponse,
            "horodatage": datetime.now().strftime("%H:%M:%S")
        })

if __name__ == "__main__":
    main()