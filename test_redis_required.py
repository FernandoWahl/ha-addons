#!/usr/bin/env python3
"""
Script para testar o comportamento de Redis obrigatório
"""

import subprocess
import os
import time
import sys

def test_redis_required_true():
    """Testa aplicação com Redis obrigatório (deve falhar se Redis não disponível)"""
    
    print("🧪 Testando Redis obrigatório = TRUE")
    print("=" * 50)
    
    # Define variáveis de ambiente para Redis obrigatório
    env = os.environ.copy()
    env.update({
        'ENABLE_CACHE': 'true',
        'REDIS_REQUIRED': 'true',
        'REDIS_HOST': 'localhost',
        'REDIS_PORT': '6379',
        'MAX_IMAGES': '4',
        'IMAGE_QUALITY': '85',
        'CELL_WIDTH': '400',
        'CELL_HEIGHT': '300',
        'TIMEOUT': '10',
        'CACHE_TTL': '600'
    })
    
    print("🔧 Configuração:")
    print("   - ENABLE_CACHE: true")
    print("   - REDIS_REQUIRED: true")
    print("   - REDIS_HOST: localhost")
    print("   - REDIS_PORT: 6379")
    print()
    
    try:
        print("🚀 Tentando iniciar aplicação...")
        
        # Tenta executar a aplicação
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            cwd='image-combiner',
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Aguarda um pouco para ver se a aplicação inicia ou falha
        time.sleep(3)
        
        # Verifica se o processo ainda está rodando
        if process.poll() is None:
            print("✅ Aplicação iniciou com sucesso (Redis disponível)")
            process.terminate()
            process.wait()
        else:
            # Processo terminou, vamos ver a saída
            stdout, stderr = process.communicate()
            print("❌ Aplicação falhou ao iniciar:")
            print("STDOUT:")
            print(stdout)
            print("STDERR:")
            print(stderr)
            
    except Exception as e:
        print(f"❌ Erro ao executar teste: {e}")

def test_redis_required_false():
    """Testa aplicação com Redis opcional (deve funcionar mesmo sem Redis)"""
    
    print("\n🧪 Testando Redis obrigatório = FALSE")
    print("=" * 50)
    
    # Define variáveis de ambiente para Redis opcional
    env = os.environ.copy()
    env.update({
        'ENABLE_CACHE': 'true',
        'REDIS_REQUIRED': 'false',
        'REDIS_HOST': 'localhost',
        'REDIS_PORT': '6379',
        'MAX_IMAGES': '4',
        'IMAGE_QUALITY': '85',
        'CELL_WIDTH': '400',
        'CELL_HEIGHT': '300',
        'TIMEOUT': '10',
        'CACHE_TTL': '600'
    })
    
    print("🔧 Configuração:")
    print("   - ENABLE_CACHE: true")
    print("   - REDIS_REQUIRED: false")
    print("   - REDIS_HOST: localhost")
    print("   - REDIS_PORT: 6379")
    print()
    
    try:
        print("🚀 Tentando iniciar aplicação...")
        
        # Tenta executar a aplicação
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            cwd='image-combiner',
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Aguarda um pouco para ver se a aplicação inicia
        time.sleep(3)
        
        # Verifica se o processo ainda está rodando
        if process.poll() is None:
            print("✅ Aplicação iniciou com sucesso (funcionando sem Redis)")
            process.terminate()
            process.wait()
        else:
            # Processo terminou, vamos ver a saída
            stdout, stderr = process.communicate()
            print("❌ Aplicação falhou inesperadamente:")
            print("STDOUT:")
            print(stdout)
            print("STDERR:")
            print(stderr)
            
    except Exception as e:
        print(f"❌ Erro ao executar teste: {e}")

def test_cache_disabled():
    """Testa aplicação com cache desabilitado (deve funcionar sempre)"""
    
    print("\n🧪 Testando Cache DESABILITADO")
    print("=" * 50)
    
    # Define variáveis de ambiente para cache desabilitado
    env = os.environ.copy()
    env.update({
        'ENABLE_CACHE': 'false',
        'REDIS_REQUIRED': 'true',  # Irrelevante quando cache está desabilitado
        'MAX_IMAGES': '4',
        'IMAGE_QUALITY': '85',
        'CELL_WIDTH': '400',
        'CELL_HEIGHT': '300',
        'TIMEOUT': '10'
    })
    
    print("🔧 Configuração:")
    print("   - ENABLE_CACHE: false")
    print("   - REDIS_REQUIRED: true (irrelevante)")
    print()
    
    try:
        print("🚀 Tentando iniciar aplicação...")
        
        # Tenta executar a aplicação
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            cwd='image-combiner',
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Aguarda um pouco para ver se a aplicação inicia
        time.sleep(3)
        
        # Verifica se o processo ainda está rodando
        if process.poll() is None:
            print("✅ Aplicação iniciou com sucesso (cache desabilitado)")
            process.terminate()
            process.wait()
        else:
            # Processo terminou, vamos ver a saída
            stdout, stderr = process.communicate()
            print("❌ Aplicação falhou inesperadamente:")
            print("STDOUT:")
            print(stdout)
            print("STDERR:")
            print(stderr)
            
    except Exception as e:
        print(f"❌ Erro ao executar teste: {e}")

def check_redis_status():
    """Verifica se Redis está rodando"""
    
    print("🔍 Verificando status do Redis...")
    
    try:
        # Tenta conectar no Redis
        import redis
        r = redis.Redis(host='localhost', port=6379, socket_connect_timeout=2)
        r.ping()
        print("✅ Redis está DISPONÍVEL em localhost:6379")
        return True
    except Exception as e:
        print(f"❌ Redis NÃO está disponível: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Teste de Redis Obrigatório - Image Combiner v1.1.1")
    print("Este teste demonstra o comportamento da aplicação com diferentes configurações de Redis")
    print()
    
    # Verifica status do Redis
    redis_available = check_redis_status()
    print()
    
    # Executa testes baseado na disponibilidade do Redis
    if redis_available:
        print("📋 Redis disponível - testando todos os cenários:")
        test_redis_required_true()
        test_redis_required_false() 
        test_cache_disabled()
    else:
        print("📋 Redis não disponível - testando cenários de falha:")
        print("⚠️ REDIS_REQUIRED=true deve FALHAR")
        test_redis_required_true()
        print("✅ REDIS_REQUIRED=false deve FUNCIONAR")
        test_redis_required_false()
        print("✅ CACHE desabilitado deve FUNCIONAR")
        test_cache_disabled()
    
    print("\n✨ Testes concluídos!")
    print()
    print("📋 Resumo dos comportamentos:")
    print("   🔴 ENABLE_CACHE=true + REDIS_REQUIRED=true + Redis indisponível = FALHA")
    print("   🟡 ENABLE_CACHE=true + REDIS_REQUIRED=false + Redis indisponível = FUNCIONA (sem cache)")
    print("   🟢 ENABLE_CACHE=false + qualquer REDIS_REQUIRED = FUNCIONA (sem cache)")
    print("   🟢 ENABLE_CACHE=true + REDIS_REQUIRED=true + Redis disponível = FUNCIONA (com cache)")

if __name__ == "__main__":
    main()
