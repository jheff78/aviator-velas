import streamlit as st
import requests

# 🔐 Login simples com senha vinda do secrets.toml
def login():
    st.title("🔐 Login")
    password = st.text_input("Digite a senha:", type="password")
    if password != st.secrets["password"]:
        st.stop()

def obter_velas_da_api():
    try:
        url = "https://aviator-api-bz4x.onrender.com/velas"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, "❌ Erro ao buscar velas da API."
    except Exception as e:
        return None, f"❌ Erro de conexão: {e}"


# 🚀 Analisador de Velas
def analisar_velas(velas_raw):
    try:
        # Remover o 'x', espaços e converter para float
        velas = [float(v.strip().replace('x', '')) for v in velas_raw.split(',')]
        
        if len(velas) != 20:
            return None, "⚠️ Você precisa inserir exatamente 20 velas."

        acima_10x = [v for v in velas if v > 10]
        prob = len(acima_10x) / len(velas) * 100
        return prob, None
    except Exception as e:
        return None, f"❌ Erro ao processar os dados: {e}"

# --- EXECUÇÃO ---
login()

st.title("🎯 Analisador de Velas – H2Bet Manual")
st.markdown("Cole abaixo as **últimas 20 velas** separadas por vírgula (exemplo: `1.2x, 10.5x, 3.4x ...`)")

entrada = st.text_input("📊 Digite as 20 velas:")

if entrada:
    probabilidade, erro = analisar_velas(entrada)
    if erro:
        st.error(erro)
    else:
        st.success(f"✅ Probabilidade de sair vela maior que 10x: **{probabilidade:.2f}%**")
