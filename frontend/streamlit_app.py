"""
frontend/streamlit_app.py
Interface do Sistema de Quimioinformática Inteligente.
TCC — Análise e Desenvolvimento de Sistemas
"""

import time
import requests
import streamlit as st

st.set_page_config(
    page_title            = "QuimioChat IA",
    page_icon             = "⚗️",
    layout                = "wide",
    initial_sidebar_state = "expanded",
)

API_URL = "http://127.0.0.1:8000"

# ──────────────────────────────────────────────────────────────────
# DESIGN SYSTEM
# ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset e base ── */
*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: #050a14;
    font-family: 'Inter', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111f 0%, #0a1628 100%);
    border-right: 1px solid rgba(99,179,237,0.12);
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] h3 { color: #e2e8f0 !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.08em; }

/* ── Tipografia global ── */
h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; color: #f0f6ff !important; }
p, span, label  { color: #94a3b8; }

/* ── Oculta decoração padrão Streamlit ── */
#MainMenu, footer { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
.block-container { padding-top: 1.5rem !important; }

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: rgba(15,23,42,0.95) !important;
    border: 1.5px solid rgba(99,179,237,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.65rem 1rem !important;
    transition: border-color 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(99,179,237,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.08) !important;
}
.stTextInput > div > div > input::placeholder { color: #475569 !important; }

/* ── Botão primário (Pesquisar) ── */
div[data-testid="stMainBlockContainer"] div[data-testid="stButton"]:first-of-type button,
.btn-primary button {
    background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.65rem 2rem !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.01em !important;
}
.stButton button {
    background: rgba(30,41,59,0.8) !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(99,179,237,0.15) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
.stButton button:hover {
    background: rgba(37,99,235,0.15) !important;
    border-color: rgba(99,179,237,0.4) !important;
    color: #93c5fd !important;
    transform: translateY(-1px) !important;
}

/* ── Card genérico ── */
.qc-card {
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(99,179,237,0.12);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(12px);
}
.qc-card-ai     { border-top: 3px solid #7c3aed; }
.qc-card-pc     { border-top: 3px solid #0ea5e9; }
.qc-card-match  { border-top: 3px solid #10b981; }
.qc-card-perf   { border-top: 3px solid #f59e0b; }

/* ── Badge de fonte ── */
.qc-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
}
.qc-badge-ai  { background: rgba(124,58,237,0.15); color: #a78bfa; border: 1px solid rgba(124,58,237,0.3); }
.qc-badge-pc  { background: rgba(14,165,233,0.12); color: #38bdf8; border: 1px solid rgba(14,165,233,0.3); }

/* ── Label de campo ── */
.qc-label {
    font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.08em; color: #475569; margin-bottom: 4px;
}

/* ── Valor de campo ── */
.qc-value {
    font-size: 1rem; font-weight: 500; color: #e2e8f0;
    word-break: break-word;
}
.qc-value.mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem; color: #7dd3fc; background: rgba(7,17,31,0.7);
    border: 1px solid rgba(99,179,237,0.12);
    border-radius: 6px; padding: 6px 10px;
    word-break: break-all;
}

/* ── Pill de tempo ── */
.qc-time {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 600;
    background: rgba(245,158,11,0.1); color: #fbbf24;
    border: 1px solid rgba(245,158,11,0.2);
}

/* ── Separador ── */
hr { border: none; border-top: 1px solid rgba(99,179,237,0.1) !important; margin: 1.5rem 0 !important; }

/* ── Exemplo rápido ── */
.ex-btn button {
    background: rgba(37,99,235,0.08) !important;
    color: #60a5fa !important;
    border: 1px solid rgba(37,99,235,0.25) !important;
    border-radius: 20px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 4px 14px !important;
}
.ex-btn button:hover {
    background: rgba(37,99,235,0.2) !important;
    border-color: rgba(37,99,235,0.5) !important;
    color: #93c5fd !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab"] {
    color: #64748b !important; font-weight: 500 !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: #60a5fa !important; border-bottom-color: #2563eb !important;
}

/* ── Métricas Streamlit ── */
[data-testid="stMetric"] label { color: #64748b !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-size: 1.4rem !important; font-weight: 700 !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #2563eb !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(15,23,42,0.6) !important;
    border: 1px solid rgba(99,179,237,0.1) !important;
    border-radius: 10px !important;
}

/* ── Alertas ── */
[data-testid="stAlert"] { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# MAPEAMENTO DE ERROS HTTP → MENSAGENS AMIGÁVEIS
# ──────────────────────────────────────────────────────────────────
_HTTP_ERRORS = {
    400: "Dados inválidos. Verifique as informações e tente novamente.",
    401: "Usuário ou senha incorretos.",
    403: "Você não tem permissão para realizar esta ação.",
    404: "Recurso não encontrado.",
    409: "Este e-mail já está cadastrado.",
    422: "Os dados enviados são inválidos. Verifique e tente novamente.",
    429: "Muitas tentativas. Aguarde um momento e tente novamente.",
    500: "Ocorreu um erro interno. Tente novamente em alguns instantes.",
    502: "Serviço temporariamente indisponível.",
    503: "Serviço temporariamente indisponível.",
}

def _friendly_error(status_code: int, detail: str | list = "") -> str:
    """Converte status HTTP em mensagem legível para o usuário."""
    if status_code in _HTTP_ERRORS:
        return _HTTP_ERRORS[status_code]
    
    if isinstance(detail, list):
        return "Preencha as informações corretamente."

    if detail and not any(x in str(detail).lower() for x in ["traceback", "exception", "stack", "http"]):
        return str(detail)
    return "Algo deu errado. Tente novamente."


# ──────────────────────────────────────────────────────────────────
# CHAMADAS À API
# ──────────────────────────────────────────────────────────────────

def api_post(endpoint: str, data: dict, token: str = None) -> dict | None:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        resp = requests.post(f"{API_URL}{endpoint}", json=data, headers=headers, timeout=180)
        if resp.status_code in (200, 201):
            return resp.json()
        try:
            detail = resp.json().get("detail", "")
        except Exception:
            detail = ""
        st.error(f"⚠️ {_friendly_error(resp.status_code, detail)}")
        return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Não foi possível conectar ao servidor. Verifique se o backend está em execução.")
        return None
    except requests.exceptions.Timeout:
        st.error("⚠️ A consulta demorou muito. Verifique sua conexão e tente novamente.")
        return None


def api_get(endpoint: str, token: str, params: dict = None) -> dict | list | None:
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(f"{API_URL}{endpoint}", headers=headers, params=params, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        try:
            detail = resp.json().get("detail", "")
        except Exception:
            detail = ""
        st.error(f"⚠️ {_friendly_error(resp.status_code, detail)}")
        return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Não foi possível conectar ao servidor.")
        return None


def get_molecule_image_url(smiles: str) -> str | None:
    if not smiles:
        return None
    encoded = requests.utils.quote(smiles)
    return f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{encoded}/PNG"


# ──────────────────────────────────────────────────────────────────
# ESTADO DA SESSÃO
# ──────────────────────────────────────────────────────────────────

def init_session():
    defaults = {
        "token":        None,
        "user":         None,
        "last_result":  None,
        "page":         "login",
        "mol_input":    "",
        "auto_search":  False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ──────────────────────────────────────────────────────────────────
# TELA: LOGIN / REGISTRO
# ──────────────────────────────────────────────────────────────────

def show_auth_page():
    # Centraliza verticalmente com espaço
    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        # Logotipo e branding
        st.markdown("""
        <div style='text-align:center; margin-bottom:2rem;'>
            <div style='font-size:56px; line-height:1; margin-bottom:0.5rem;'>⚗️</div>
            <div style='font-size:2rem; font-weight:800; letter-spacing:-0.02em;
                        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #38bdf8 100%);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                QuimioChat IA
            </div>
            <div style='color:#475569; font-size:0.88rem; margin-top:6px;'>
                Sistema de Quimioinformática Inteligente
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_reg = st.tabs(["  Entrar  ", "  Criar conta  "])

        with tab_login:
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            with st.form("form_login", clear_on_submit=False):
                email    = st.text_input("E-mail", placeholder="seu@email.com")
                senha    = st.text_input("Senha",  placeholder="••••••••", type="password")
                entrar   = st.form_submit_button("Entrar", use_container_width=True)

            if entrar:
                if not email or not senha:
                    st.warning("Preencha e-mail e senha para continuar.")
                else:
                    with st.spinner("Verificando credenciais..."):
                        result = api_post("/auth/login", {"email": email, "senha": senha})
                    if result:
                        st.session_state.token = result["access_token"]
                        st.session_state.user  = result["user"]
                        st.session_state.page  = "home"
                        st.success(f"Bem-vindo, **{result['user']['nome']}**! 👋")
                        time.sleep(0.6)
                        st.rerun()

        with tab_reg:
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            with st.form("form_register", clear_on_submit=True):
                nome     = st.text_input("Nome completo", placeholder="João Silva")
                email_r  = st.text_input("E-mail",         placeholder="joao@email.com")
                senha_r  = st.text_input("Senha",           placeholder="Mínimo 6 caracteres", type="password")
                criar    = st.form_submit_button("Criar conta", use_container_width=True)

            if criar:
                if not nome or not email_r or not senha_r:
                    st.warning("Preencha todos os campos.")
                elif len(senha_r) < 6:
                    st.warning("A senha precisa ter pelo menos 6 caracteres.")
                else:
                    with st.spinner("Criando sua conta..."):
                        result = api_post("/auth/register", {"nome": nome, "email": email_r, "senha": senha_r})
                    if result:
                        st.success("Conta criada com sucesso! Acesse a aba **Entrar** para fazer login.")

    st.markdown("""
    <div style='text-align:center; margin-top:4rem; color:#1e293b; font-size:0.75rem;'>
        TCC — Análise e Desenvolvimento de Sistemas
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────

def show_sidebar():
    with st.sidebar:
        user_name = st.session_state.user.get("nome", "Usuário") if st.session_state.user else "Usuário"
        st.markdown(f"""
        <div style='padding:1rem 0 1.2rem; border-bottom:1px solid rgba(99,179,237,0.1); margin-bottom:1rem; text-align:center;'>
            <div style='font-size:32px;'>⚗️</div>
            <div style='font-weight:700; color:#e2e8f0; font-size:1.05rem; margin-top:4px;'>QuimioChat IA</div>
            <div style='color:#475569; font-size:0.78rem; margin-top:2px;'>{user_name}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Menu")
        if st.button("🔬  Pesquisar Molécula", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
        if st.button("📋  Histórico",          use_container_width=True):
            st.session_state.page = "history"
            st.rerun()
        if st.button("🗂️  Banco de Moléculas", use_container_width=True):
            st.session_state.page = "molecules"
            st.rerun()

        st.markdown("---")

        # Status dos serviços — sem expor detalhes técnicos
        st.markdown("### Serviços")
        try:
            health        = requests.get(f"{API_URL}/health", timeout=4).json()
            api_ok        = health.get("api")    == "online"
            ollama_ok     = health.get("ollama") == "online"
        except Exception:
            api_ok = ollama_ok = False

        st.markdown(
            f"{'🟢' if api_ok    else '🔴'} **API** &nbsp;&nbsp;"
            f"{'🟢' if ollama_ok else '🟡'} **IA (Gemma2)**",
            unsafe_allow_html=True,
        )
        if not ollama_ok:
            st.caption("IA offline — execute `ollama serve`")

        st.markdown("---")
        if st.button("🚪  Sair", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()


# ──────────────────────────────────────────────────────────────────
# COMPONENTES VISUAIS
# ──────────────────────────────────────────────────────────────────

def _field(label: str, value: str, mono: bool = False):
    """Renderiza um campo label+valor no estilo do design system."""
    css_class = "qc-value mono" if mono else "qc-value"
    display   = value if value else "—"
    st.markdown(
        f"<div class='qc-label'>{label}</div>"
        f"<div class='{css_class}'>{display}</div>",
        unsafe_allow_html=True,
    )

def _time_pill(ms: int | None) -> str:
    if ms is None:
        return "<span class='qc-time'>—</span>"
    return f"<span class='qc-time'>⏱ {ms} ms</span>"


# ──────────────────────────────────────────────────────────────────
# PÁGINA: PESQUISA
# ──────────────────────────────────────────────────────────────────

def _run_search(mol_name: str):
    """Executa a pesquisa e armazena o resultado na sessão."""
    if not mol_name.strip():
        st.warning("⚠️ Digite o nome de uma molécula para pesquisar.")
        return

    progress_messages = [
        "🔬 Analisando estrutura molecular...",
        "🤖 Consultando modelo de IA Gemma2...",
        "🌐 Consultando base científica PubChem...",
        "📊 Comparando resultados das fontes...",
    ]

    with st.status(progress_messages[0], expanded=False) as status:
        # Atualiza o texto do spinner progressivamente enquanto aguarda
        import threading

        def _cycle_messages():
            for msg in progress_messages[1:]:
                time.sleep(5)
                try:
                    status.update(label=msg)
                except Exception:
                    break

        t = threading.Thread(target=_cycle_messages, daemon=True)
        t.start()

        result = api_post(
            "/molecules/search",
            {"molecule_name": mol_name.strip()},
            token=st.session_state.token,
        )
        status.update(label="✅ Pesquisa concluída!", state="complete")

    if result:
        st.session_state.last_result = result
        st.session_state.mol_input   = ""
        st.session_state.auto_search = False


def show_search_page():
    # ── Cabeçalho da página ──
    st.markdown("""
    <div style='margin-bottom:1.5rem;'>
        <h1 style='font-size:1.8rem; font-weight:800; margin:0; letter-spacing:-0.02em;'>
            🔬 Pesquisa Molecular
        </h1>
        <p style='color:#475569; margin-top:4px; font-size:0.92rem;'>
            Consulta simultânea ao modelo de IA Gemma2 e ao banco de dados científico PubChem.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Exemplos rápidos ──
    st.markdown("<div style='color:#94a3b8; font-size:0.8rem; margin-bottom:6px;'>EXEMPLOS RÁPIDOS</div>",
                unsafe_allow_html=True)
    exemplos = ["Aspirina", "Cafeína", "Glicose", "Dopamina", "Ibuprofeno", "Paracetamol", "Etanol", "Metanol", "Acetona", "Ácido Acético"]
    
    # Renderizar em 2 linhas de 5 colunas
    for row in range(0, 10, 5):
        ex_cols = st.columns(5)
        for i in range(5):
            idx = row + i
            if idx < len(exemplos):
                ex = exemplos[idx]
                with ex_cols[i]:
                    st.markdown("<div class='ex-btn'>", unsafe_allow_html=True)
                    if st.button(ex, key=f"ex_{idx}", use_container_width=True):
                        st.session_state.mol_input  = ex
                        st.session_state.auto_search = True
                    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    # ── Campo de busca ──
    # Usar on_change + Enter: o form_submit_button captura tanto Enter quanto clique
    with st.form("form_search", clear_on_submit=False):
        col_inp, col_btn = st.columns([5, 1])
        with col_inp:
            mol_name = st.text_input(
                "Molécula",
                value       = st.session_state.mol_input,
                placeholder = "Ex: Aspirina, Cafeína, Ácido acetilsalicílico...",
                label_visibility = "collapsed",
            )
        with col_btn:
            pesquisar = st.form_submit_button("🔍 Buscar", use_container_width=True)

    # Executa ao clicar no botão OU ao pressionar Enter (form_submit_button captura ambos)
    if pesquisar and mol_name:
        st.session_state.auto_search = False
        _run_search(mol_name)

    # Executa automaticamente ao clicar em exemplo rápido
    if st.session_state.auto_search and st.session_state.mol_input:
        _run_search(st.session_state.mol_input)

    # ── Resultado ──
    if st.session_state.last_result:
        show_search_result(st.session_state.last_result)


def show_search_result(result: dict):
    mol = result.get("molecule", "")
    ai  = result.get("ai",      {}) or {}
    pc  = result.get("pubchem", {}) or {}

    ai_name   = ai.get("name")   or ""
    ai_smiles = ai.get("smiles") or ""
    ai_time   = ai.get("time_ms")

    pc_cid     = pc.get("cid")
    pc_comum   = pc.get("nome_comum") or ""
    pc_iupac   = pc.get("nome_iupac") or ""
    pc_smiles  = pc.get("smiles_canonico") or ""
    pc_formula = pc.get("formula") or ""
    pc_massa   = pc.get("massa") or ""
    pc_time    = pc.get("time_ms")

    st.markdown("---")
    st.markdown(f"""
    <h2 style='font-size:1.3rem; font-weight:700; margin-bottom:1rem;'>
        Resultados para: <span style='color:#60a5fa;'>{mol}</span>
    </h2>
    """, unsafe_allow_html=True)

    # ── Duas colunas: PubChem | IA ──
    col_pc, col_ai = st.columns(2, gap="medium")

    with col_pc:
        st.markdown("""
        <div class='qc-card qc-card-pc'>
            <span class='qc-badge qc-badge-pc'>🔬 PubChem (Oficial)</span>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            if pc_cid:
                st.markdown(
                    f"<div class='qc-label'>CID PUBCHEM</div>"
                    f"<div class='qc-value'>"
                    f"<a href='https://pubchem.ncbi.nlm.nih.gov/compound/{pc_cid}' "
                    f"target='_blank' style='color:#38bdf8; text-decoration:none;'>#{pc_cid} ↗</a>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            _field("Nome Pesquisado", mol)
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            _field("Nome Oficial (PubChem)", pc_comum or "Não encontrado")
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            _field("Nome IUPAC", pc_iupac or "—")
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            _field("SMILES Oficial", pc_smiles or "Não disponível", mono=True)
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            
            c_f, c_m = st.columns(2)
            with c_f: _field("Fórmula Molecular", pc_formula or "—")
            with c_m: _field("Massa Molecular", f"{pc_massa} g/mol" if pc_massa else "—")
            
            st.markdown(
                f"<div style='margin-top:0.6rem;'>{_time_pill(pc_time)}</div>",
                unsafe_allow_html=True,
            )

        if pc_cid:
            img_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{pc_cid}/PNG"
            st.markdown("<div style='margin-top:0.8rem; color:#64748b; font-size:0.78rem;'>ESTRUTURA 2D OFICIAL</div>",
                        unsafe_allow_html=True)
            try:
                st.image(img_url, width=240)
            except Exception:
                st.caption("Imagem da estrutura não disponível.")

        if not pc_cid and not pc_smiles:
            st.info("Molécula não encontrada no PubChem.")

    with col_ai:
        st.markdown("""
        <div class='qc-card qc-card-ai'>
            <span class='qc-badge qc-badge-ai'>🤖 Gemma2 (IA Local)</span>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            _field("Tradução / Nome", ai_name or "Não identificado")
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            _field("SMILES Gerado", ai_smiles or "Não gerado", mono=True)
            st.markdown(
                f"<div style='margin-top:0.6rem;'>{_time_pill(ai_time)}</div>",
                unsafe_allow_html=True,
            )

        if ai_smiles:
            img_url = get_molecule_image_url(ai_smiles)
            if img_url:
                st.markdown("<div style='margin-top:0.8rem; color:#64748b; font-size:0.78rem;'>ESTRUTURA 2D GERADA</div>",
                            unsafe_allow_html=True)
                try:
                    st.image(img_url, width=240)
                except Exception:
                    st.caption("Imagem da estrutura não disponível.")

        if not ai_name and not ai_smiles:
            st.info("A IA não retornou dados. Verifique se o Ollama está em execução.")

    # ── Painel de desempenho ──
    st.markdown("---")
    st.markdown("""
    <div class='qc-card qc-card-perf'>
        <span style='font-size:0.78rem; font-weight:700; text-transform:uppercase;
                     letter-spacing:0.08em; color:#f59e0b;'>⚡ Comparativo de Desempenho</span>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🤖 Tempo IA",      f"{ai_time or '—'} ms" if ai_time else "—")
    with c2:
        st.metric("🔬 Tempo PubChem", f"{pc_time or '—'} ms" if pc_time else "—")
    with c3:
        st.metric("IA · Nome",        "✅ Obtido" if ai_name else "❌ Ausente")
    with c4:
        st.metric("PubChem · Nome",   "✅ Obtido" if (pc_comum or pc_iupac) else "❌ Ausente")

    # Comparação de SMILES
    if ai_smiles and pc_smiles:
        if ai_smiles.strip() == pc_smiles.strip():
            st.success("✅ Os SMILES retornados pela IA e pelo PubChem são **idênticos**.")
        else:
            st.info("ℹ️ Os SMILES diferem entre as fontes — representações equivalentes podem variar em notação.")
    elif ai_smiles or pc_smiles:
        st.caption("Comparação de SMILES indisponível — apenas uma fonte retornou dados.")


# ──────────────────────────────────────────────────────────────────
# PÁGINA: HISTÓRICO
# ──────────────────────────────────────────────────────────────────

def show_history_page():
    st.markdown("""
    <h1 style='font-size:1.8rem; font-weight:800; margin-bottom:0.3rem;'>📋 Histórico de Pesquisas</h1>
    <p style='color:#475569; font-size:0.92rem; margin-bottom:1.5rem;'>
        Suas consultas mais recentes, da mais nova para a mais antiga.
    </p>
    """, unsafe_allow_html=True)

    with st.spinner("Carregando histórico..."):
        history = api_get("/search/history", token=st.session_state.token, params={"limit": 50})

    if history is None:
        return
    if not history:
        st.info("Você ainda não realizou nenhuma pesquisa. Use a página de Pesquisa Molecular para começar.")
        return

    st.caption(f"{len(history)} pesquisa(s) registrada(s)")
    st.markdown("---")

    for i, item in enumerate(history):
        mol_name    = item.get("molecule") or "Molécula desconhecida"
        search_time = (item.get("search_time") or "")[:16].replace("T", " às ")
        label       = f"⚗️  {mol_name}   ·   {search_time}"

        with st.expander(label, expanded=(i == 0)):
            c1, c2 = st.columns(2, gap="medium")
            with c1:
                st.markdown("<span class='qc-badge qc-badge-ai'>🤖 IA — Gemma2</span>", unsafe_allow_html=True)
                st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
                _field("Nome Químico", item.get("ai_name") or "—")
                st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
                _field("SMILES",       item.get("ai_smiles") or "—", mono=True)
                st.markdown(
                    f"<div style='margin-top:0.4rem;'>{_time_pill(item.get('ai_time_ms'))}</div>",
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown("<span class='qc-badge qc-badge-pc'>🔬 PubChem</span>", unsafe_allow_html=True)
                st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
                _field("Nome Químico", item.get("pubchem_name") or "—")
                st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
                _field("SMILES",       item.get("pubchem_smiles") or "—", mono=True)
                st.markdown(
                    f"<div style='margin-top:0.4rem;'>{_time_pill(item.get('pubchem_time_ms'))}</div>",
                    unsafe_allow_html=True,
                )
            st.markdown(
                f"<div style='margin-top:0.5rem; color:#334155; font-size:0.75rem;'>"
                f"Tempo total: {item.get('response_time_ms') or '—'} ms  ·  ID #{item.get('id')}"
                f"</div>",
                unsafe_allow_html=True,
            )


# ──────────────────────────────────────────────────────────────────
# PÁGINA: BANCO DE MOLÉCULAS
# ──────────────────────────────────────────────────────────────────

def show_molecules_page():
    st.markdown("""
    <h1 style='font-size:1.8rem; font-weight:800; margin-bottom:0.3rem;'>🗂️ Banco de Moléculas</h1>
    <p style='color:#475569; font-size:0.92rem; margin-bottom:1.5rem;'>
        Todas as moléculas catalogadas pelo sistema até o momento.
    </p>
    """, unsafe_allow_html=True)

    with st.spinner("Carregando moléculas..."):
        molecules = api_get("/molecules", token=st.session_state.token, params={"limit": 100})

    if molecules is None:
        return
    if not molecules:
        st.info("Nenhuma molécula cadastrada ainda. Realize uma pesquisa para popular o banco.")
        return

    filtro = st.text_input("🔍 Filtrar", placeholder="Nome da molécula...")
    if filtro:
        molecules = [m for m in molecules if filtro.lower() in (m.get("nome_original") or "").lower()]

    st.caption(f"{len(molecules)} molécula(s) encontrada(s)")
    st.markdown("---")

    for i in range(0, len(molecules), 3):
        cols = st.columns(3, gap="medium")
        for j, mol in enumerate(molecules[i:i + 3]):
            with cols[j]:
                nome_orig = mol.get("nome_original") or "—"
                nome_quim = mol.get("nome_quimico")  or "—"
                smiles    = mol.get("smiles")

                st.markdown(f"""
                <div class='qc-card'>
                    <div style='font-weight:700; font-size:1rem; color:#e2e8f0; margin-bottom:0.6rem;'>
                        ⚗️ {nome_orig}
                    </div>
                """, unsafe_allow_html=True)

                if smiles:
                    img_url = get_molecule_image_url(smiles)
                    if img_url:
                        try:
                            st.image(img_url, width=160)
                        except Exception:
                            pass

                _field("Nome Químico", nome_quim)
                st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
                _field("SMILES", smiles or "—", mono=True)
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# ROTEADOR PRINCIPAL
# ──────────────────────────────────────────────────────────────────

def main():
    init_session()

    if not st.session_state.token:
        show_auth_page()
        return

    show_sidebar()

    page = st.session_state.get("page", "home")
    if page == "home":
        show_search_page()
    elif page == "history":
        show_history_page()
    elif page == "molecules":
        show_molecules_page()


if __name__ == "__main__":
    main()
