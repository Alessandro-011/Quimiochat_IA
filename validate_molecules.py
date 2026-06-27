import requests
import time

URL_REGISTER = "http://127.0.0.1:8000/auth/register"
URL_LOGIN    = "http://127.0.0.1:8000/auth/login"
URL_SEARCH   = "http://127.0.0.1:8000/molecules/search"

MOLECULAS = [
    "Aspirina", "Cafeína", "Glicose", "Dopamina", "Ibuprofeno",
    "Paracetamol", "Etanol", "Metanol", "Acetona", "Ácido Acético"
]

def run():
    print("=== INICIANDO VALIDAÇÃO DO PUBCHEM ===")
    
    # 1. Criar user
    email = f"validador_{int(time.time())}@teste.com"
    requests.post(URL_REGISTER, json={"nome": "Validador", "email": email, "senha": "senha_forte_123"})
    
    # 2. Login
    res = requests.post(URL_LOGIN, json={"email": email, "senha": "senha_forte_123"})
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Pesquisar
    for m in MOLECULAS:
        print(f"\n🧪 Pesquisando: {m}")
        resp = requests.post(URL_SEARCH, json={"molecule_name": m}, headers=headers)
        if resp.status_code == 200:
            data = resp.json()["pubchem"]
            cid = data.get("cid")
            comum = data.get("nome_comum")
            iupac = data.get("nome_iupac")
            c_smiles = data.get("smiles_canonico")
            i_smiles = data.get("smiles_isomerico")
            print(f"   [CID]      {cid}")
            print(f"   [Comum]    {comum}")
            print(f"   [IUPAC]    {iupac}")
            print(f"   [SMILES_C] {c_smiles}")
            print(f"   [SMILES_I] {i_smiles}")
        else:
            print(f"   ERRO: {resp.text}")

if __name__ == "__main__":
    run()
