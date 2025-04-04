
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Índice de Risco Assistencial Hospitalar", layout="centered")
st.title("💉 Índice de Risco Assistencial Hospitalar (IRAH)")
st.markdown("Preencha os campos abaixo para calcular o risco assistencial do paciente.")

# Entradas do usuário
atendimento = st.text_input("Código do Atendimento")
fugulin = st.number_input("Pontuação da Escala Fugulin", min_value=0, max_value=100, step=1)
asg = st.selectbox("Classificação da ASG", ["", "Bem nutrido (ASG A)", "Moderadamente desnutrido (ASG B)", "Gravemente desnutrido (ASG C)"])
mrc = st.number_input("Pontuação da Escala MRC (0 a 60)", min_value=0, max_value=60, step=1)
triagem = st.number_input("Pontuação da Triagem de Alta", min_value=0, max_value=20, step=1)
charlson = st.number_input("Índice de Charlson", min_value=0, max_value=50, step=1)

# Normalizações
if fugulin == 0:
    fugulin_norm = 0
elif fugulin < 17:
    fugulin_norm = 0
elif 18 <= fugulin <= 22:
    fugulin_norm = 0.14
elif 23 <= fugulin <= 34:
    fugulin_norm = 0.43
elif fugulin > 34:
    fugulin_norm = 1

asg_map = {
    "": 0,
    "Bem nutrido (ASG A)": 0,
    "Moderadamente desnutrido (ASG B)": 0.5,
    "Gravemente desnutrido (ASG C)": 1
}
asg_norm = asg_map.get(asg, 0)
mrc_norm = 1 if mrc <= 35 else 0
triagem_norm = 1 if triagem >= 10 else 0
charlson_norm = 1 if charlson >= 6 else (charlson / 6) * 0.75 if charlson else 0

# Cálculo do IRAH
irah = round((fugulin_norm + asg_norm + mrc_norm + triagem_norm + charlson_norm) / 5, 2)
risco = "Baixo Risco" if irah <= 0.3 else "Risco Moderado" if irah <= 0.59 else "Alto Risco"

# Resultado
st.markdown("---")
st.subheader("Resultado do IRAH")
st.metric("Pontuação do IRAH", f"{irah}")
st.success(f"Classificação: {risco}")

# Rodapé
st.markdown("<small>Este é um protótipo clínico-educacional. Sempre utilize o julgamento clínico profissional junto à ferramenta.</small>", unsafe_allow_html=True)
