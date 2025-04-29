# ESTILO FINAL DOS BOTÕES
st.markdown("""
    <style>
    .btn-principal {
        background-color: #4CAF50 !important;
        color: white !important;
        font-size: 24px !important;
        padding: 18px 36px !important;
        border-radius: 50px !important;
    }
    .btn-principal:hover {
        background-color: #45a049 !important;
    }
    .btn-cancelar {
        background-color: #eeeeee !important;
        color: #555 !important;
        font-size: 12px !important;
        padding: 6px 16px !important;
        border-radius: 30px !important;
        margin-top: 6px;
    }
    </style>
""", unsafe_allow_html=True)

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
