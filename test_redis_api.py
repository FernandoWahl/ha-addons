#!/usr/bin/env python3
"""
Script para testar a API Image Combiner com funcionalidades Redis
"""

import requests
import json
import time

def test_cache_functionality():
    """Testa as funcionalidades de cache Redis"""
    
    api_url = "http://localhost:5000"
    
    # URLs de teste
    test_urls = [
        "https://picsum.photos/400/300?random=1",
        "https://picsum.photos/400/300?random=2"
    ]
    
    print("🧪 Testando funcionalidades de cache Redis")
    print("=" * 50)
    
    # 1. Verificar status inicial do cache
    print("\n1️⃣ Verificando status do cache...")
    try:
        response = requests.get(f"{api_url}/cache/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Cache status: {stats}")
        else:
            print(f"❌ Erro ao obter stats: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return
    
    # 2. Primeira requisição (deve ser MISS)
    print("\n2️⃣ Primeira requisição (Cache MISS esperado)...")
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{api_url}/combine",
            json={"urls": test_urls},
            headers={"Content-Type": "application/json"}
        )
        
        first_request_time = time.time() - start_time
        
        if response.status_code == 200:
            with open("test_first_request.jpg", "wb") as f:
                f.write(response.content)
            print(f"✅ Primeira requisição: {first_request_time:.2f}s")
            print(f"📁 Imagem salva: test_first_request.jpg")
        else:
            print(f"❌ Erro na primeira requisição: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Erro na primeira requisição: {e}")
        return
    
    # 3. Segunda requisição (deve ser HIT)
    print("\n3️⃣ Segunda requisição (Cache HIT esperado)...")
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{api_url}/combine",
            json={"urls": test_urls},
            headers={"Content-Type": "application/json"}
        )
        
        second_request_time = time.time() - start_time
        
        if response.status_code == 200:
            with open("test_second_request.jpg", "wb") as f:
                f.write(response.content)
            print(f"✅ Segunda requisição: {second_request_time:.2f}s")
            print(f"📁 Imagem salva: test_second_request.jpg")
            
            # Calcula melhoria de performance
            if first_request_time > 0:
                improvement = ((first_request_time - second_request_time) / first_request_time) * 100
                print(f"🚀 Melhoria de performance: {improvement:.1f}%")
        else:
            print(f"❌ Erro na segunda requisição: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na segunda requisição: {e}")
    
    # 4. Verificar stats após requisições
    print("\n4️⃣ Verificando stats após requisições...")
    try:
        response = requests.get(f"{api_url}/cache/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Cache stats atualizadas: {stats}")
        else:
            print(f"❌ Erro ao obter stats: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 5. Testar diferentes configurações (deve gerar nova chave)
    print("\n5️⃣ Testando com URLs diferentes...")
    different_urls = [
        "https://picsum.photos/400/300?random=3",
        "https://picsum.photos/400/300?random=4"
    ]
    
    try:
        response = requests.post(
            f"{api_url}/combine",
            json={"urls": different_urls},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            with open("test_different_urls.jpg", "wb") as f:
                f.write(response.content)
            print(f"✅ URLs diferentes processadas")
            print(f"📁 Imagem salva: test_different_urls.jpg")
        else:
            print(f"❌ Erro com URLs diferentes: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 6. Limpar cache
    print("\n6️⃣ Limpando cache...")
    try:
        response = requests.post(f"{api_url}/cache/clear")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Cache limpo: {result}")
        else:
            print(f"❌ Erro ao limpar cache: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 7. Verificar stats finais
    print("\n7️⃣ Verificando stats finais...")
    try:
        response = requests.get(f"{api_url}/cache/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Stats finais: {stats}")
        else:
            print(f"❌ Erro ao obter stats: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_health_endpoint():
    """Testa o endpoint de health com informações de cache"""
    
    print("\n🏥 Testando endpoint de health...")
    
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Health check: {health}")
        else:
            print(f"❌ Erro no health check: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_home_endpoint():
    """Testa o endpoint home com novas informações"""
    
    print("\n🏠 Testando endpoint home...")
    
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            home = response.json()
            print(f"✅ Home endpoint: {json.dumps(home, indent=2)}")
        else:
            print(f"❌ Erro no home endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    """Função principal"""
    print("🚀 Teste completo da API Image Combiner com Redis")
    print("Certifique-se de que:")
    print("1. O servidor está rodando: python app.py")
    print("2. Redis está disponível (ou cache desabilitado)")
    print()
    
    # Testa funcionalidades de cache
    test_cache_functionality()
    
    # Testa outros endpoints
    test_health_endpoint()
    test_home_endpoint()
    
    print("\n✨ Testes concluídos!")
    print("📁 Arquivos gerados:")
    print("   - test_first_request.jpg")
    print("   - test_second_request.jpg") 
    print("   - test_different_urls.jpg")

if __name__ == "__main__":
    main()
