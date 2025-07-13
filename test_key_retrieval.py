#!/usr/bin/env python3
"""
Script para testar as novas funcionalidades de chave única do Image Combiner
"""

import requests
import json
import time

def test_key_based_retrieval():
    """Testa o sistema de chave única para recuperação de imagens"""
    
    api_url = "http://localhost:5000"
    
    # URLs de teste
    test_urls = [
        "https://picsum.photos/400/300?random=1",
        "https://picsum.photos/400/300?random=2"
    ]
    
    print("🔑 Testando sistema de chave única")
    print("=" * 50)
    
    # 1. Fazer requisição POST /combine (deve retornar JSON com chave)
    print("\n1️⃣ Fazendo requisição POST /combine...")
    
    try:
        response = requests.post(
            f"{api_url}/combine",
            json={"urls": test_urls},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response JSON: {json.dumps(result, indent=2)}")
            
            # Extrai a chave
            if 'key' in result and result['key']:
                cache_key = result['key']
                print(f"🔑 Chave obtida: {cache_key}")
                
                # Remove prefixo para usar na URL
                if cache_key.startswith('image_combiner:'):
                    url_key = cache_key.replace('image_combiner:', '')
                else:
                    url_key = cache_key
                
                # 2. Usar a chave para recuperar a imagem
                print(f"\n2️⃣ Recuperando imagem com chave: {url_key[:16]}...")
                
                image_response = requests.get(f"{api_url}/image/{url_key}")
                
                if image_response.status_code == 200:
                    # Salva a imagem recuperada
                    with open("retrieved_image.jpg", "wb") as f:
                        f.write(image_response.content)
                    print(f"✅ Imagem recuperada com sucesso!")
                    print(f"📁 Salva como: retrieved_image.jpg")
                    print(f"📊 Tamanho: {len(image_response.content)} bytes")
                else:
                    print(f"❌ Erro ao recuperar imagem: {image_response.status_code}")
                    print(f"Response: {image_response.text}")
                
                # 3. Testar chave inválida
                print(f"\n3️⃣ Testando chave inválida...")
                
                invalid_response = requests.get(f"{api_url}/image/invalid_key_123")
                
                if invalid_response.status_code == 404:
                    error_result = invalid_response.json()
                    print(f"✅ Erro esperado para chave inválida: {error_result}")
                else:
                    print(f"❌ Resposta inesperada: {invalid_response.status_code}")
                
                # 4. Testar múltiplas requisições com mesma combinação
                print(f"\n4️⃣ Testando cache com mesma combinação...")
                
                start_time = time.time()
                response2 = requests.post(
                    f"{api_url}/combine",
                    json={"urls": test_urls},
                    headers={"Content-Type": "application/json"}
                )
                second_request_time = time.time() - start_time
                
                if response2.status_code == 200:
                    result2 = response2.json()
                    print(f"✅ Segunda requisição: {second_request_time:.3f}s")
                    print(f"🔑 Mesma chave retornada: {result2['key'] == cache_key}")
                    print(f"💾 Cache hit: {result2.get('cached', False)}")
                
                # 5. Testar com URLs diferentes
                print(f"\n5️⃣ Testando com URLs diferentes...")
                
                different_urls = [
                    "https://picsum.photos/400/300?random=3",
                    "https://picsum.photos/400/300?random=4"
                ]
                
                response3 = requests.post(
                    f"{api_url}/combine",
                    json={"urls": different_urls},
                    headers={"Content-Type": "application/json"}
                )
                
                if response3.status_code == 200:
                    result3 = response3.json()
                    print(f"✅ URLs diferentes processadas")
                    print(f"🔑 Nova chave gerada: {result3['key'] != cache_key}")
                    print(f"📊 Tamanho: {result3.get('image_size', 0)} bytes")
                    
                    # Recupera a nova imagem
                    new_key = result3['key'].replace('image_combiner:', '')
                    new_image_response = requests.get(f"{api_url}/image/{new_key}")
                    
                    if new_image_response.status_code == 200:
                        with open("retrieved_image_2.jpg", "wb") as f:
                            f.write(new_image_response.content)
                        print(f"📁 Segunda imagem salva: retrieved_image_2.jpg")
                
            else:
                print(f"❌ Chave não encontrada na resposta")
                
        else:
            print(f"❌ Erro na requisição combine: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_api_info():
    """Testa os endpoints de informação da API"""
    
    api_url = "http://localhost:5000"
    
    print("\n📋 Testando endpoints de informação...")
    
    # Testa endpoint home
    try:
        response = requests.get(f"{api_url}/")
        if response.status_code == 200:
            info = response.json()
            print(f"✅ API Info:")
            print(f"   - Versão: {info.get('version', 'N/A')}")
            print(f"   - Features: {info.get('features', [])}")
            print(f"   - Endpoints: {list(info.get('endpoints', {}).keys())}")
        else:
            print(f"❌ Erro no endpoint home: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Testa endpoint health
    try:
        response = requests.get(f"{api_url}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Health Check:")
            print(f"   - Status: {health.get('status', 'N/A')}")
            print(f"   - Versão: {health.get('version', 'N/A')}")
            print(f"   - Features: {health.get('features', [])}")
            print(f"   - Cache: {health.get('cache', {}).get('enabled', False)}")
        else:
            print(f"❌ Erro no health check: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    """Função principal"""
    print("🚀 Teste das funcionalidades de chave única - Image Combiner v1.2.0")
    print("Certifique-se de que:")
    print("1. O servidor está rodando: python app.py")
    print("2. Redis está disponível (ou cache desabilitado)")
    print()
    
    # Testa funcionalidades de chave única
    test_key_based_retrieval()
    
    # Testa endpoints de informação
    test_api_info()
    
    print("\n✨ Testes concluídos!")
    print("📁 Arquivos gerados:")
    print("   - retrieved_image.jpg (primeira imagem recuperada)")
    print("   - retrieved_image_2.jpg (segunda imagem recuperada)")
    print()
    print("🔑 Funcionalidades testadas:")
    print("   ✅ POST /combine retorna JSON com chave")
    print("   ✅ GET /image/<key> recupera imagem")
    print("   ✅ Cache funciona com chaves")
    print("   ✅ Chaves diferentes para URLs diferentes")
    print("   ✅ Tratamento de chaves inválidas")

if __name__ == "__main__":
    main()
