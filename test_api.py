import requests
import json

def test_image_combiner():
    """Testa a API de combinação de imagens"""
    
    # URL da API local
    api_url = "http://localhost:5000/combine"
    
    # URLs de exemplo de imagens (você pode substituir por URLs reais)
    test_urls = [
        "https://picsum.photos/400/300?random=1",
        "https://picsum.photos/400/300?random=2",
        "https://picsum.photos/400/300?random=3",
        "https://picsum.photos/400/300?random=4"
    ]
    
    # Testa com diferentes quantidades de imagens
    test_cases = [
        {"name": "1 imagem", "urls": test_urls[:1]},
        {"name": "2 imagens", "urls": test_urls[:2]},
        {"name": "3 imagens", "urls": test_urls[:3]},
        {"name": "4 imagens", "urls": test_urls[:4]},
    ]
    
    for test_case in test_cases:
        print(f"\n--- Testando {test_case['name']} ---")
        
        payload = {"urls": test_case["urls"]}
        
        try:
            response = requests.post(
                api_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                # Salva a imagem resultante
                filename = f"combined_{len(test_case['urls'])}_images.jpg"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Sucesso! Imagem salva como: {filename}")
            else:
                print(f"❌ Erro {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Erro: Não foi possível conectar à API. Certifique-se de que o servidor está rodando.")
        except Exception as e:
            print(f"❌ Erro inesperado: {str(e)}")

def test_error_cases():
    """Testa casos de erro da API"""
    
    api_url = "http://localhost:5000/combine"
    
    print("\n=== Testando casos de erro ===")
    
    # Teste 1: Mais de 4 URLs
    print("\n--- Teste: Mais de 4 URLs ---")
    payload = {"urls": ["url1", "url2", "url3", "url4", "url5"]}
    response = requests.post(api_url, json=payload)
    print(f"Status: {response.status_code}, Response: {response.text}")
    
    # Teste 2: Lista vazia
    print("\n--- Teste: Lista vazia ---")
    payload = {"urls": []}
    response = requests.post(api_url, json=payload)
    print(f"Status: {response.status_code}, Response: {response.text}")
    
    # Teste 3: Sem parâmetro urls
    print("\n--- Teste: Sem parâmetro 'urls' ---")
    payload = {"images": ["url1"]}
    response = requests.post(api_url, json=payload)
    print(f"Status: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    print("🧪 Testando API de Combinação de Imagens")
    print("Certifique-se de que o servidor está rodando com: python app.py")
    
    # Testa casos normais
    test_image_combiner()
    
    # Testa casos de erro
    test_error_cases()
    
    print("\n✨ Testes concluídos!")
