#!/usr/bin/env python3
"""
Script para diagnosticar problemas de conexão Redis
"""

import redis
import socket
import json
import os
from redis.exceptions import ConnectionError as RedisConnectionError

def test_redis_connection(host, port, password=None):
    """Testa conexão Redis com diagnósticos detalhados"""
    
    print(f"🔍 Testando conexão Redis: {host}:{port}")
    print("=" * 50)
    
    # 1. Teste de resolução DNS
    print(f"1️⃣ Testando resolução DNS para '{host}'...")
    try:
        ip = socket.gethostbyname(host)
        print(f"✅ DNS resolvido: {host} → {ip}")
    except socket.gaierror as e:
        print(f"❌ Erro de DNS: {e}")
        return False
    
    # 2. Teste de conectividade TCP
    print(f"\n2️⃣ Testando conectividade TCP para {host}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Porta {port} está aberta em {host}")
        else:
            print(f"❌ Porta {port} está fechada ou inacessível em {host}")
            return False
    except Exception as e:
        print(f"❌ Erro de conectividade TCP: {e}")
        return False
    
    # 3. Teste de conexão Redis
    print(f"\n3️⃣ Testando conexão Redis...")
    try:
        r = redis.Redis(
            host=host,
            port=port,
            password=password if password else None,
            socket_connect_timeout=5,
            socket_timeout=5,
            decode_responses=False
        )
        
        # Testa ping
        response = r.ping()
        print(f"✅ Redis PING: {response}")
        
        # Testa info
        info = r.info()
        print(f"✅ Redis versão: {info.get('redis_version', 'N/A')}")
        print(f"✅ Redis modo: {info.get('redis_mode', 'N/A')}")
        print(f"✅ Clientes conectados: {info.get('connected_clients', 'N/A')}")
        
        return True
        
    except RedisConnectionError as e:
        print(f"❌ Erro de conexão Redis: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_configuration_loading():
    """Testa como a configuração está sendo carregada"""
    
    print(f"\n🔧 Testando carregamento de configuração...")
    print("=" * 50)
    
    # Verifica arquivo de opções do HA
    options_file = '/data/options.json'
    if os.path.exists(options_file):
        try:
            with open(options_file, 'r') as f:
                config = json.load(f)
            print(f"✅ Arquivo de opções encontrado: {options_file}")
            print(f"📋 Configuração Redis:")
            print(f"   - redis_host: '{config.get('redis_host', 'N/A')}'")
            print(f"   - redis_port: {config.get('redis_port', 'N/A')}")
            print(f"   - enable_cache: {config.get('enable_cache', 'N/A')}")
            print(f"   - redis_required: {config.get('redis_required', 'N/A')}")
            
            return config
        except Exception as e:
            print(f"❌ Erro ao ler {options_file}: {e}")
    else:
        print(f"⚠️ Arquivo {options_file} não encontrado")
    
    # Verifica variáveis de ambiente
    print(f"\n📋 Variáveis de ambiente:")
    env_vars = ['REDIS_HOST', 'REDIS_PORT', 'ENABLE_CACHE', 'REDIS_REQUIRED']
    for var in env_vars:
        value = os.getenv(var, 'N/A')
        print(f"   - {var}: '{value}'")
    
    return None

def simulate_app_config_loading():
    """Simula como a aplicação carrega a configuração"""
    
    print(f"\n🔄 Simulando carregamento de configuração da aplicação...")
    print("=" * 50)
    
    # Replica a lógica do app.py
    config = {}
    
    # Tenta ler do arquivo de opções do Home Assistant
    options_file = '/data/options.json'
    
    if os.path.exists(options_file):
        try:
            with open(options_file, 'r') as f:
                config = json.load(f)
            print(f"📋 Configuração carregada do Home Assistant")
        except Exception as e:
            print(f"⚠️ Erro ao ler options file: {e}")
    else:
        print(f"📋 Configuração carregada de variáveis de ambiente")
        config = {
            'redis_host': os.getenv('REDIS_HOST', 'localhost'),
            'redis_port': int(os.getenv('REDIS_PORT', 6379)),
            'redis_password': os.getenv('REDIS_PASSWORD', ''),
            'enable_cache': os.getenv('ENABLE_CACHE', 'true').lower() == 'true',
            'redis_required': os.getenv('REDIS_REQUIRED', 'true').lower() == 'true'
        }
    
    # Extrai configurações Redis
    redis_host = config.get('redis_host', 'localhost')
    redis_port = config.get('redis_port', 6379)
    redis_password = config.get('redis_password', '')
    
    print(f"🔧 Configuração final:")
    print(f"   - Host: '{redis_host}' (tipo: {type(redis_host)})")
    print(f"   - Port: {redis_port} (tipo: {type(redis_port)})")
    print(f"   - Password: {'***' if redis_password else '(vazio)'}")
    
    return redis_host, redis_port, redis_password

def main():
    """Função principal"""
    print("🚀 Diagnóstico de Conexão Redis - Image Combiner v1.1.2")
    print("Este script ajuda a diagnosticar problemas de conexão Redis")
    print()
    
    # 1. Testa carregamento de configuração
    config = test_configuration_loading()
    
    # 2. Simula carregamento da aplicação
    redis_host, redis_port, redis_password = simulate_app_config_loading()
    
    # 3. Verifica se os valores estão corretos
    print(f"\n⚠️ DIAGNÓSTICO DO PROBLEMA:")
    if not redis_host or redis_host in ['', 'localhost', '127.0.0.1']:
        print(f"❌ PROBLEMA ENCONTRADO: redis_host está vazio ou localhost")
        print(f"   Valor atual: '{redis_host}'")
        print(f"   Configure o IP correto do seu servidor Redis")
    
    if redis_port == 0 or not redis_port:
        print(f"❌ PROBLEMA ENCONTRADO: redis_port está 0 ou vazio")
        print(f"   Valor atual: {redis_port}")
        print(f"   Esperado: 6379")
    
    # 4. Testa com valores corretos (exemplo)
    print(f"\n🧪 Testando com valores de exemplo...")
    test_redis_connection('redis-server', 6379)
    
    # 5. Testa com valores da configuração atual
    if redis_host and redis_port:
        print(f"\n🧪 Testando com configuração atual...")
        test_redis_connection(redis_host, redis_port, redis_password)
    
    print(f"\n💡 SOLUÇÕES SUGERIDAS:")
    print(f"1. Verifique se redis_host está configurado corretamente")
    print(f"2. Verifique se redis_port está configurado como 6379")
    print(f"3. Reinicie o addon após alterar as configurações")
    print(f"4. Verifique se o Redis está rodando no host/porta configurados")
    print(f"5. Teste conectividade: telnet <redis_host> 6379")

if __name__ == "__main__":
    main()
