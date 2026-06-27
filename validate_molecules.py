import requests
import time
import sys

API_URL = "http://127.0.0.1:8000"

def run_tests():
    print("🚀 Iniciando Teste de Moléculas na API QuimioChat...")
    
    # Register/Login to get token
    email = f"test_{int(time.time())}@test.com"
    res = requests.post(f"{API_URL}/auth/register", json={"nome": "Tester", "email": email, "senha": "senha_forte_123"})
    
    login = requests.post(f"{API_URL}/auth/login", json={"email": email, "senha": "senha_forte_123"})
    if login.status_code != 200:
        print("❌ Erro no login!")
        sys.exit(1)
        
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    molecules = ["Aspirina", "Cafeína", "Glicose", "Dopamina", "Paracetamol", "Ibuprofeno", "Acetona", "Etanol"]
    
    success_count = 0
    for mol in molecules:
        print(f"\n🧪 Testando: {mol}...")
        resp = requests.post(f"{API_URL}/molecules/search", json={"molecule_name": mol}, headers=headers, timeout=60)
        
        if resp.status_code != 200:
            print(f"❌ Erro! Code {resp.status_code}: {resp.text}")
            continue
            
        data = resp.json()
        pc = data.get("pubchem", {})
        ai = data.get("ai", {})
        
        cid = pc.get("cid")
        nome_comum = pc.get("nome_comum")
        smiles_c = pc.get("smiles_canonico")
        
        if cid and nome_comum and smiles_c:
            print(f"✅ SUCESSO | CID: {cid} | Nome: {nome_comum} | SMILES: {smiles_c}")
            success_count += 1
        else:
            print(f"⚠️ AVISO | Algum campo vazio! CID: {cid} | Nome: {nome_comum} | SMILES: {smiles_c}")
            
    print(f"\n📊 Resultado Final: {success_count}/{len(molecules)} sucessos ({(success_count/len(molecules))*100:.1f}%)")

if __name__ == "__main__":
    run_tests()
