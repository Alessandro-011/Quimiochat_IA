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

*, *::before, *::after { box-sizing: border-box; }

.stApp { background: #050a14; font-family: 'Inter', sans-serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111f 0%, #0a1628 100%);
    border-right: 1px solid rgba(99,179,237,0.12);
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] h3 { color: #e2e8f0 !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.08em; }

h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; color: #f0f6ff !important; }
p, span, label  { color: #94a3b8; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
.block-container { padding-top: 1.5rem !important; }

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
.qc-card-perf   { border-top: 3px solid #f59e0b; }

.qc-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
}
.qc-badge-ai  { background: rgba(124,58,237,0.15); color: #a78bfa; border: 1px solid rgba(124,58,237,0.3); }
.qc-badge-pc  { background: rgba(14,165,233,0.12); color: #38bdf8; border: 1px solid rgba(14,165,233,0.3); }

.qc-label {
    font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.08em; color: #475569; margin-bottom: 4px;
}
.qc-value {
    font-size: 1rem; font-weight: 500; color: #e2e8f0; word-break: break-word;
}
.qc-value.mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem; color: #7dd3fc; background: rgba(7,17,31,0.7);
    border: 1px solid rgba(99,179,237,0.12); border-radius: 6px; padding: 6px 10px;
    word-break: break-all;
}
.qc-time {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 600;
    background: rgba(245,158,11,0.1); color: #fbbf24; border: 1px solid rgba(245,158,11,0.2);
}

hr { border: none; border-top: 1px solid rgba(99,179,237,0.1) !important; margin: 1.5rem 0 !important; }

.ex-btn button {
    background: rgba(37,99,235,0.08) !important;
    color: #60a5fa !important;
    border: 1px solid rgba(37,99,235,0.25) !important;
    border-radius: 20px !important;
    font-size: 0.82rem !important; font-weight: 500 !important;
    padding: 4px 14px !important;
}
.ex-btn button:hover {
    background: rgba(37,99,235,0.2) !important; border-color: rgba(37,99,235,0.5) !important; color: #93c5fd !important;
}
</style>
""", unsafe_allow_html=True)


_HTTP_ERRORS = {
    400: "Dados inválidos. Verifique as informações e tente novamente.",
    401: "Usuário ou senha incorretos.",
    403: "Você não tem permissão para realizar esta ação.",
    404: "Recurso não encontrado.",
    409: "Este e-mail já está cadastrado.",
    500: "Ocorreu um erro interno. Tente novamente em alguns instantes.",
}

def _friendly_error(status_code: int, detail: str = "") -> str:
    if status_code in _HTTP_ERRORS:
        return _HTTP_ERRORS[status_code]
    if detail and not any(x in detail.lower() for x in ["traceback", "exception", "http"]):
        return detail
    return "Algo deu errado. Tente novamente."


def api_post(endpoint: str, data: dict, token: str = None) -> dict | None:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        resp = requests.post(f"{API_URL}{endpoint}", json=data, headers=headers, timeout=180)
        if resp.status_code in (200, 201):
            return resp.json()
        st.error(f"⚠️ {_friendly_error(resp.status_code, resp.json().get('detail', ''))}")
        return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Não foi possível conectar ao servidor.")
        return None


def api_get(endpoint: str, token: str, params: dict = None) -> dict | list | None:
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(f"{API_URL}{endpoint}", headers=headers, params=params, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        st.error(f"⚠️ {_friendly_error(resp.status_code)}")
        return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Não foi possível conectar ao servidor.")
        return None


def get_molecule_image_url(smiles: str) -> str | None:
    if not smiles: return None
    encoded = requests.utils.quote(smiles)
    return f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{encoded}/PNG"


def init_session():
    defaults = {"token": None, "user": None, "last_result": None, "page": "login", "mol_input": "", "auto_search": False}
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def show_auth_page():
    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
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

        t1, t2 = st.tabs(["  Entrar  ", "  Criar conta  "])
        with t1:
            with st.form("f1"):
                email = st.text_input("E-mail")
                senha = st.text_input("Senha", type="password")
                if st.form_submit_button("Entrar", use_container_width=True):
                    res = api_post("/auth/login", {"email": email, "senha": senha})
                    if res:
                        st.session_state.update({"token": res["access_token"], "user": res["user"], "page": "home"})
                        st.rerun()

        with t2:
            with st.form("f2"):
                nome = st.text_input("Nome")
                email_r = st.text_input("E-mail")
                senha_r = st.text_input("Senha", type="password")
                if st.form_submit_button("Criar conta", use_container_width=True):
                    res = api_post("/auth/register", {"nome": nome, "email": email_r, "senha": senha_r})
                    if res: st.success("Conta criada! Volte à aba Entrar.")


def show_sidebar():
    with st.sidebar:
        user_name = st.session_state.user.get("nome", "Usuário") if st.session_state.user else "Usuário"
        st.markdown(f"""
        <div style='padding:1rem 0 1.2rem; border-bottom:1px solid rgba(99,179,237,0.1); margin-bottom:1rem; text-align:center;'>
            <div style='font-size:32px;'>⚗️</div>
            <div style='font-weight:700; color:#e2e8f0; font-size:1.05rem;'>QuimioChat IA</div>
            <div style='color:#475569; font-size:0.78rem;'>{user_name}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔬  Pesquisar Molécula", use_container_width=True): st.session_state.page = "home"; st.rerun()
        if st.button("📋  Histórico", use_container_width=True): st.session_state.page = "history"; st.rerun()
        if st.button("🗂️  Banco", use_container_width=True): st.session_state.page = "molecules"; st.rerun()
        
        st.markdown("---")
        if st.button("🚪  Sair", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()


def _field(label: str, value: str, mono: bool = False, info: str = None):
    css = "qc-value mono" if mono else "qc-value"
    val = value if value else "Não disponível"
    lbl = f"{label} <span title='{info}' style='cursor:help;color:#64748b'>ℹ️</span>" if info else label
    st.markdown(f"<div class='qc-label'>{lbl}</div><div class='{css}'>{val}</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

def _time_pill(ms: int | None) -> str:
    return f"<span class='qc-time'>⏱ {ms} ms</span>" if ms else ""


def _run_search(mol_name: str):
    if not mol_name.strip(): return
    with st.status("🔬 Buscando dados da molécula... (A IA atua como fallback para o PubChem)", expanded=False):
        res = api_post("/molecules/search", {"molecule_name": mol_name.strip()}, token=st.session_state.token)
    if res:
        st.session_state.update({"last_result": res, "mol_input": "", "auto_search": False})


def show_search_page():
    st.markdown("""
    <div style='margin-bottom:1.5rem;'>
        <h1 style='font-size:1.8rem; font-weight:800; margin:0;'>🔬 Pesquisa Molecular (IA + PubChem)</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='color:#94a3b8; font-size:0.8rem; margin-bottom:6px;'>TESTE RÁPIDO:</div>", unsafe_allow_html=True)
    exemplos = ["Aspirina", "Cafeína", "Glicose", "Dopamina", "Ibuprofeno", "Paracetamol", "Etanol", "Metanol", "Acetona", "Ácido Acético"]
    ex_cols = st.columns(5)
    for i, ex in enumerate(exemplos):
        with ex_cols[i % 5]:
            st.markdown("<div class='ex-btn'>", unsafe_allow_html=True)
            if st.button(ex, key=f"ex_{i}"):
                st.session_state.update({"mol_input": ex, "auto_search": True})
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    with st.form("form_search", clear_on_submit=False):
        c1, c2 = st.columns([5, 1])
        with c1:
            mol_name = st.text_input("Molécula", value=st.session_state.mol_input, label_visibility="collapsed")
        with c2:
            pesquisar = st.form_submit_button("🔍 Buscar", use_container_width=True)

    if pesquisar and mol_name:
        st.session_state.auto_search = False
        _run_search(mol_name)
    if st.session_state.auto_search and st.session_state.mol_input:
        _run_search(st.session_state.mol_input)

    if st.session_state.last_result:
        show_search_result(st.session_state.last_result)


def show_search_result(result: dict):
    mol = result.get("molecule", "")
    ai  = result.get("ai", {}) or {}
    pc  = result.get("pubchem", {}) or {}

    # Lógica de fallback para exibição no frontend (sempre mostra o melhor dado disponível)
    pc_cid = pc.get("cid")
    
    # Se PubChem não tiver nome comum, usa IUPAC. Se ambos vazios, usa o nome que a IA sugeriu.
    pc_comum = pc.get("nome_comum") or pc.get("nome_iupac") or ai.get("name")
    pc_iupac = pc.get("nome_iupac") or ai.get("name")
    
    # Sempre tenta o Canonical, depois o Isomeric
    pc_smiles = pc.get("smiles_canonico") or pc.get("smiles_isomerico")

    st.markdown("---")
    st.markdown(f"<h2 style='font-size:1.3rem; margin-bottom:1rem;'>Resultado: <span style='color:#60a5fa;'>{mol}</span></h2>", unsafe_allow_html=True)

    col_pc, col_ai = st.columns(2, gap="medium")

    # 1) PUBCHEM CARD (Com todos os fallbacks científicos aplicados)
    with col_pc:
        st.markdown("<div class='qc-card qc-card-pc'><span class='qc-badge qc-badge-pc'>🔬 PubChem (Oficial)</span><br><br>", unsafe_allow_html=True)
        if pc_cid:
            st.markdown(f"<div class='qc-label'>CID</div><div class='qc-value'><a href='https://pubchem.ncbi.nlm.nih.gov/compound/{pc_cid}' target='_blank' style='color:#38bdf8'>#{pc_cid} ↗</a></div><br>", unsafe_allow_html=True)
        
        _field("Nome Pesquisado", mol)
        _field("Nome Oficial (PubChem)", pc_comum)
        _field("Nome IUPAC", pc_iupac)
        
        smiles_info = "CanonicalSMILES (fallback IsomericSMILES)" if pc.get("smiles_canonico") else "IsomericSMILES"
        _field("SMILES Oficial", pc_smiles, mono=True, info=smiles_info)
        
        sub1, sub2 = st.columns(2)
        with sub1: _field("Fórmula Molecular", pc.get("formula") or "—")
        with sub2: _field("Massa Molecular", pc.get("massa") or "—")
        
        st.markdown(_time_pill(pc.get("time_ms")), unsafe_allow_html=True)
        
        if pc_cid:
            st.image(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{pc_cid}/PNG", width=220)
        elif pc_smiles:
            st.image(get_molecule_image_url(pc_smiles), width=220)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # 2) IA CARD
    with col_ai:
        st.markdown("<div class='qc-card qc-card-ai'><span class='qc-badge qc-badge-ai'>🤖 Gemma2 (IA Local)</span><br><br>", unsafe_allow_html=True)
        _field("Tradução / Nome", ai.get("name"))
        _field("SMILES Gerado", ai.get("smiles"), mono=True)
        st.markdown(_time_pill(ai.get("time_ms")), unsafe_allow_html=True)
        
        if ai.get("smiles"):
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            try:
                st.image(get_molecule_image_url(ai.get("smiles")), width=220)
            except: pass
        st.markdown("</div>", unsafe_allow_html=True)


def show_history_page():
    st.markdown("<h1>📋 Histórico</h1>", unsafe_allow_html=True)
    history = api_get("/search/history", token=st.session_state.token, params={"limit": 50})
    if not history:
        st.info("Nenhuma pesquisa realizada.")
        return

    for i, h in enumerate(history):
        lbl = f"⚗️ {h.get('molecule')} · {(h.get('search_time') or '')[:16].replace('T', ' às ')}"
        with st.expander(lbl, expanded=(i==0)):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**PubChem**")
                st.write(f"CID: {h.get('pubchem_cid') or '—'}")
                st.write(f"Nome: {h.get('pubchem_nome_comum') or h.get('pubchem_nome_iupac') or '—'}")
                st.write(f"SMILES: `{h.get('pubchem_smiles_canonico') or h.get('pubchem_smiles_isomerico') or '—'}`")
            with c2:
                st.markdown("**Gemma2 (IA)**")
                st.write(f"Nome: {h.get('ai_name') or '—'}")
                st.write(f"SMILES: `{h.get('ai_smiles') or '—'}`")

def show_molecules_page():
    st.markdown("<h1>🗂️ Banco de Moléculas</h1>", unsafe_allow_html=True)
    mols = api_get("/molecules", token=st.session_state.token, params={"limit": 100})
    if not mols:
        st.info("Banco vazio.")
        return
    for mol in mols:
        st.markdown(f"**{mol.get('nome_original')}** → {mol.get('nome_quimico')} | `{mol.get('smiles')}`")

if __name__ == "__main__":
    init_session()
    if not st.session_state.token: show_auth_page()
    else:
        show_sidebar()
        if st.session_state.page == "home": show_search_page()
        elif st.session_state.page == "history": show_history_page()
        elif st.session_state.page == "molecules": show_molecules_page()
