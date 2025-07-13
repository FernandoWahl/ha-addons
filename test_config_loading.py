#!/usr/bin/env python3
"""
Script para testar a leitura de configurações do Home Assistant
"""

import requests
import json
import os
import tempfile

def create_test_options_file():
    """Cria um arquivo de opções de teste"""
    
    test_config = {
        "max_images": 3,
        "image_quality": 90,
        "cell_width": 500,
        "cell_height": 400,
        "timeout": 15,
        "redis_host": "test-redis-host",
        "redis_port": 6380,
        "redis_password": "test-password",
        "cache_ttl": 300,
        "enable_cache": True,
        "redis_required": False
    }
    
    # Cria diretório /data se não existir
    os.makedirs('/tmp/test_data', exist_ok=True)
    
    # Escreve arquivo de configuração de teste
    with open('/tmp/test_data/options.json', 'w') as f:
        json.dump(test_config, f, indent=2)
    
    print("📝 Arquivo de teste criado em /tmp/test_data/options.json:")
    print(json.dumps(test_config, indent=2))
    
    return test_config

def test_config_endpoint():
    """Testa o endpoint /config"""
    
    api_url = "http://localhost:5000"
    
    print("\n🔧 Testando endpoint /config...")
    
    try:
        response = requests.get(f"{api_url}/config")
        
        if response.status_code == 200:
            config_data = response.json()
            print("✅ Configuração atual:")
            print(json.dumps(config_data, indent=2))
            
            # Verifica se as configurações estão corretas
            redis_settings = config_data.get('redis_settings', {})
            print(f"\n🔍 Verificação Redis:")
            print(f"   - Host: {redis_settings.get('host')}")
            print(f"   - Port: {redis_settings.get('port')}")
            print(f"   - Password set: {redis_settings.get('password_set')}")
            print(f"   - Cache enabled: {redis_settings.get('enable_cache')}")
            print(f"   - Redis required: {redis_settings.get('redis_required')}")
            
        else:
            print(f"❌ Erro no endpoint /config: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_health_endpoint():
    """Testa o endpoint /health"""
    
    api_url = "http://localhost:5000"
    
    print("\n🏥 Testando endpoint /health...")
    
    try:
        response = requests.get(f"{api_url}/health")
        
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health check:")
            print(f"   - Status: {health_data.get('status')}")
            print(f"   - Version: {health_data.get('version')}")
            print(f"   - Cache enabled: {health_data.get('cache', {}).get('enabled')}")
            
        else:
            print(f"❌ Erro no health check: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_home_endpoint():
    """Testa o endpoint home"""
    
    api_url = "http://localhost:5000"
    
    print("\n🏠 Testando endpoint home...")
    
    try:
        response = requests.get(f"{api_url}/")
        
        if response.status_code == 200:
            home_data = response.json()
            print("✅ API Info:")
            print(f"   - Service: {home_data.get('service')}")
            print(f"   - Version: {home_data.get('version')}")
            print(f"   - Features: {home_data.get('features')}")
            print(f"   - Endpoints: {list(home_data.get('endpoints', {}).keys())}")
            
        else:
            print(f"❌ Erro no endpoint home: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def check_server_status():
    """Verifica se o servidor está rodando"""
    
    api_url = "http://localhost:5000"
    
    try:
        response = requests.get(f"{api_url}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def main():
    """Função principal"""
    print("🧪 Teste de Leitura de Configurações - Image Combiner v1.1.2")
    print("=" * 60)
    
    # Verifica se servidor está rodando
    if not check_server_status():
        print("❌ Servidor não está rodando em localhost:5000")
        print("💡 Inicie o servidor com: cd image-combiner && python app.py")
        return
    
    print("✅ Servidor está rodando")
    
    # Cria arquivo de configuração de teste
    test_config = create_test_options_file()
    
    # Testa endpoints
    test_config_endpoint()
    test_health_endpoint()
    test_home_endpoint()
    
    print("\n✨ Testes concluídos!")
    print("\n📋 Para testar com Home Assistant:")
    print("1. Altere as configurações no addon")
    print("2. Reinicie o addon")
    print("3. Verifique os logs de inicialização")
    print("4. Acesse GET /config para ver configuração atual")
    
    print("\n🔧 Endpoints úteis para debug:")
    print("   - GET /config - Configuração atual")
    print("   - GET /health - Status do sistema")
    print("   - GET /cache/stats - Estatísticas do cache")

if __name__ == "__main__":
    main()
