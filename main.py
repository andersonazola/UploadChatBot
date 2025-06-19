# titulo
# input do chat
# a cada mensagem enviada:
    # mostra a mensagem que o usuario enviou no chat
    # enviar essa mensagem para a IA responder

#streamlit  permitirá criar o site de forma simples usando apenas Python. Ela cuida automaticamente da parte visual (front-end) e do funcionamento da página (back-end).

#outras ferramentas em python para criação de sites: flask, django, fastapi.

import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
modelo = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.write("## Chatbot do Andin com IA") # markdown
st.write(" Este é um chatbot com Inteligencia artficial, Aproveite!")

#session_state = memoria do streamlit
if not "lista_mensagens" in st.session_state:
    st.session_state["lista_mensagens"]=[]

# exibir o historico de mensagens
for mensagem in st.session_state["lista_mensagens"]:
    role = mensagem["role"]
    content = mensagem["content"]
    st.chat_message(role).write(content)

mensagem_usuario = st.chat_input("Escreva sua mensagem")

# para as mensagens do usuario ficarem a direita e do assistante a esquerda.
st.markdown("""
    <style>
        .st-emotion-cache-1c7y2kd { flex-direction: row-reverse; text-align: right; }
        .st-emotion-cache-4oy321 { text-align: left; }
    </style>
""", unsafe_allow_html=True)
       
                         
if mensagem_usuario:
    #user -> ser humano
    #assistant -> Inteligencia artificial
    st.chat_message("user").write(mensagem_usuario)
    mensagem = {"role": "user", "content":mensagem_usuario}
    st.session_state["lista_mensagens"].append(mensagem)

    # resposta da IA
    resposta_modelo = modelo.chat.completions.create(
        messages=st.session_state["lista_mensagens"],
        model="gpt-4o"
    )
    resposta_ia = resposta_modelo.choices[0].message.content

    # exibir resposta da IA na tela
    st.chat_message('assistant').write(resposta_ia)
    mensagem_ia = {"role":"assistant", "content": resposta_ia}
    st.session_state["lista_mensagens"].append(mensagem_ia)

# Para limitar o histórico de mensagens para até 10.
if len(st.session_state["lista_mensagens"]) > 10: 
    st.session_state["lista_mensagens"] = st.session_state["lista_mensagens"][-10:]
