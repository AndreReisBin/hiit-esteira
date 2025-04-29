import streamlit as st
import time

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="HIIT Corrida na Esteira",
    page_icon="🏃‍♂️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS ESTILO PERSONALIZADO
st.markdown("""
<style>
    .stButton>button {
        font-size: 24px !important;
        padding: 18px 36px !important;
        border-radius: 50px !important;
    }
    .btn-principal {
        font-size: 24px !important;
        padding: 18px 36px !important;
        border-radius: 50px !important;
    }
    .btn-cancelar {
        background-color: #cccccc !important;
        color: #333333 !important;
        font-size: 14px !important;
        border-radius: 30px !important;
        padding: 6px 18px !important;
        margin-top: 6px;
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

# INICIALIZAÇÃO DE VARIÁVEIS
if "treino_iniciado" not in st.session_state:
    st.session_state.treino_iniciado = False
if "repeticoes_restantes" not in st.session_state:
    st.session_state.repeticoes_restantes = 0
if "fase" not in st.session_state:
    st.session_state.fase = "corrida"
if "cronometro_ativo" not in st.session_state:
    st.session_state.cronometro_ativo = False
if "botoes_bloqueados" not in st.session_state:
    st.session_state.botoes_bloqueados = False

# TOCAR BIP
def tocar_bip():
    bip_html = """
    <audio autoplay>
      <source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg">
    </audio>
    """
    st.markdown(bip_html, unsafe_allow_html=True)

# TELA INICIAL
if not st.session_state.treino_iniciado:
    repeticoes = st.number_input("Número de repetições:", min_value=1, step=1, value=5)
    tempo_corrida = st.number_input("Tempo de corrida (segundos):", min_value=1, step=1, value=30)
    tempo_descanso = st.number_input("Tempo de descanso (segundos):", min_value=1, step=1, value=30)

    col_botao = st.columns(3)
    with col_botao[1]:
        iniciar_click = st.button("🟢 Iniciar", disabled=st.session_state.treino_iniciado)

        if iniciar_click:
            st.session_state.treino_iniciado = True
            st.session_state.repeticoes_restantes = repeticoes
            st.session_state.tempo_corrida = tempo_corrida
            st.session_state.tempo_descanso = tempo_descanso
            st.session_state.fase = "corrida"
            st.session_state.cronometro_ativo = False
            st.rerun()

    st.markdown("---")
    st.caption("Desenvolvido por [AndreReisBin](https://github.com/AndreReisBin) — Treine forte e com segurança! 💪")

# TELA DE TREINO
if st.session_state.treino_iniciado:

    st.header(f"Repetições restantes: {st.session_state.repeticoes_restantes}")
    
    placeholder_status = st.empty()
    placeholder_timer = st.empty()

    colunas = st.columns(3)
    with colunas[1]:
        iniciar_btn = st.button(
            "🏃‍♂️ Correr" if st.session_state.fase == "corrida" else "⏸️ Descansar",
            disabled=st.session_state.cronometro_ativo or st.session_state.botoes_bloqueados,
            key="acao"
        )
        cancelar_btn = st.button("❌ Cancelar", key="cancelar", disabled=st.session_state.cronometro_ativo)

        st.markdown("""
            <script>
            const botoes = window.parent.document.querySelectorAll('button');
            botoes.forEach(btn => {
                if (btn.innerText === '❌ Cancelar') {
                    btn.classList.add('btn-cancelar');
                }
                if (btn.innerText.includes('Correr') || btn.innerText.includes('Descansar')) {
                    btn.classList.add('btn-principal');
                }
            });
            </script>
        """, unsafe_allow_html=True)

    if iniciar_btn and not st.session_state.cronometro_ativo:
        st.session_state.cronometro_ativo = True
        st.session_state.botoes_bloqueados = True
        tempo = st.session_state.tempo_corrida if st.session_state.fase == "corrida" else st.session_state.tempo_descanso
        label = "Correndo..." if st.session_state.fase == "corrida" else "Descansando..."

        with placeholder_status.container():
            st.subheader(label)

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
        st.session_state.botoes_bloqueados = False

        if st.session_state.repeticoes_restantes == 0:
            st.balloons()
            st.success("🏆 Treino finalizado!")
            st.session_state.treino_iniciado = False

        st.rerun()

    if cancelar_btn:
        st.session_state.clear()
        st.rerun()
