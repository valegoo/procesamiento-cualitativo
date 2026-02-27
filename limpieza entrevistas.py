import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """Eres un asistente especializado en procesamiento cualitativo de entrevistas.
Tu tarea es ayudar a analizar, limpiar y codificar entrevistas de investigación cualitativa.
Puedes ayudar con:
- Limpieza y corrección de transcripciones
- Identificación de temas y categorías
- Codificación de fragmentos relevantes
- Análisis de patrones y narrativas
Responde siempre en español."""

st.set_page_config(page_title="Chatbot Entrevistas", page_icon="💬")
st.title("Procesamiento Cualitativo de Entrevistas")
st.caption("Asistente GPT-4 para análisis de entrevistas")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("Escribe tu mensaje o pega un fragmento de entrevista..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Procesando..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages,
                temperature=0.3,
            )
            reply = response.choices[0].message.content
            st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
