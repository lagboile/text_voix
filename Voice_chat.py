import streamlit as st
import speech_recognition as sr
import nltk
from nltk.chat.util import Chat, reflections
import re

pairs = [
    [
        r"bonjour|salut|coucou",
        ["Bonjour ! Comment puis-je vous aider ?", "Salut ! Que puis-je faire pour vous ?"]
    ],
    [
        r"comment ca va ?",
        ["Je vais bien, merci ! Et vous ?", "Tout va bien, et de votre côté ?"]
    ],
    [
        r"je vais bien aussi ",
        ["cool alors et bienvenue !"]
    ],
    [
        r"quel est votre nom ?",
        ["Je suis un chatbot simple. Vous pouvez m'appeler Chatbot !"]
    ],
    [
        r"quel pays est le plus doux au monde ?",
        ["la cote d'ivoire "]
    ],
    [
        r"quel est le meilleur plat du monde?",
        ["le garba !"]
    ],
    [
        r"quit",
        ["Au revoir ! À bientôt."]
    ]
]

chatbot = Chat(pairs, reflections)

def transcribe_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Parlez maintenant...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="fr-FR")
            st.write(f"Vous avez dit : {text}")
            return text
        except sr.UnknownValueError:
            st.error("Désolé, je n'ai pas compris ce que vous avez dit.")
        except sr.RequestError:
            st.error("Erreur lors de la requête à l'API de reconnaissance vocale.")
    return None

def chatbot_response(user_input):
    user_input = user_input.lower().strip()
    user_input = re.sub(r'[^\w\s]', '', user_input)

    if user_input.lower() == "quit":
        return "Au revoir ! À bientôt."
    return chatbot.respond(user_input)

def main():
    st.title("Chatbot à Commande Vocale")
    st.write("Parlez ou tapez votre message ci-dessous.")

    input_type = st.radio("Choisissez le mode d'entrée :", ("Texte", "Voix"))

    user_input = None

    if input_type == "Texte":
        user_input = st.text_input("Tapez votre message :")

    elif input_type == "Voix":
        if st.button("Démarrer l'enregistrement vocal"):
            user_input = transcribe_speech()

    if user_input:
        response = chatbot_response(user_input)
        if response:
            st.write(f"Chatbot : {response}")
        else :
            st.write("Chatbot: je ne comprends pas.pouvez vous reformuler ")

if __name__ == "__main__":
    main()