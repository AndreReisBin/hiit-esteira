import streamlit as st
import time

# CONFIGURAÇÕES DE PÁGINA
st.set_page_config(
    page_title="HIIT Corrida na Esteira",
    page_icon="🏃‍♂️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS ESTILIZADO
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 12px 24px;
        border-radius: 50px;
        border: none;
        font-size: 20px;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    .stMetric {
        font-size: 24px;
    }
    .css-18e3th9 {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h1, h2, h3 {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏃‍♂️ Treino HIIT na Esteira com Som")

# INICIALIZAÇÃO DE ESTADOS
if "treino_iniciado" not in st.session_state:
    st.session_state.treino_iniciado = False
if "repeticoes_restantes" not in st.session_state:
    st.session_state.repeticoes_restantes = 0
if "fase" not in st.session_state:
    st.session_state.fase = "corrida"  # "corrida" ou "descanso"
if "cronometro_ativo" not in st.session_state:
    st.session_state.cronometro_ativo = False

# FUNÇÃO PARA TOCAR BIP
def tocar_bip():
    bip_html = """
    <audio autoplay>
      <source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg">
    </audio>
    """
    st.markdown(bip_html, unsafe_allow_html=True)

# ENTRADA DO USUÁRIO
if not st.session_state.treino_iniciado:
    repeticoes = st.number_input("Número de repetições:", min_value=1, step=1, value=5)
    tempo_corrida = st.number_input("Tempo de corrida (segundos):", min_value=1, step=1, value=30)
    tempo_descanso = st.number_input("Tempo de descanso (segundos):", min_value=1, step=1, value=30)

    if st.button("🟢 Iniciar"):
        st.session_state.treino_iniciado = True
        st.session_state.repeticoes_restantes = repeticoes
        st.session_state.tempo_corrida = tempo_corrida
        st.session_state.tempo_descanso = tempo_descanso
        st.session_state.fase = "corrida"
        st.session_state.cronometro_ativo = False

# INTERFACE DO TREINO
if st.session_state.treino_iniciado:

    st.header(f"Repetições restantes: {st.session_state.repeticoes_restantes}")
    
    placeholder_status = st.empty()
    placeholder_timer = st.empty()

    col1, col2 = st.columns(2)
    with col1:
        iniciar_btn = st.button(
            "🏃‍♂️ Correr" if st.session_state.fase == "corrida" else "⏸️ Descansar",
            disabled=st.session_state.cronometro_ativo
        )
    with col2:
        cancelar_btn = st.button("❌ Cancelar")

    if iniciar_btn and not st.session_state.cronometro_ativo:
        st.session_state.cronometro_ativo = True
        tempo = st.session_state.tempo_corrida if st.session_state.fase == "corrida" else st.session_state.tempo_descanso
        label = "Correndo..." if st.session_state.fase == "corrida" else "Descansando..."

        with placeholder_status.container():
            st.subheader(label)

        with placeholder_timer.container():
            for t in range(tempo, 0, -1):
                placeholder_timer.metric(label="Tempo restante:", value=f"{t} segundos")
                time.sleep(1)
            placeholder_timer.metric(label="Tempo restante:", value="0 segundos")


        tocar_bip()

        if st.session_state.fase == "corrida":
            st.session_state.fase = "descanso"
        else:
            st.session_state.repeticoes_restantes -= 1
            st.session_state.fase = "corrida"

        st.session_state.cronometro_ativo = False

        if st.session_state.repeticoes_restantes == 0:
            st.balloons()
            st.success("🏆 Treino finalizado!")
            st.session_state.treino_iniciado = False

        st.rerun()

    if cancelar_btn:
        st.session_state.clear()
        st.rerun()
st.markdown("---")
st.caption("Desenvolvido por [AndreReisBin](https://github.com/AndreReisBin) — Treine forte e com segurança! 💪")
