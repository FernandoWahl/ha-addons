#!/usr/bin/env python3
"""
Script para testar configuração do Home Assistant
"""

import json
import os
import tempfile
import shutil
import subprocess
import sys
import time

def create_ha_config(redis_host="192.168.68.120", redis_port=6379):
    """Cria configuração simulada do Home Assistant"""
    
    config = {
        "max_images": 4,
        "image_quality": 85,
        "cell_width": 400,
        "cell_height": 300,
        "timeout": 10,
        "redis_host": redis_host,
        "redis_port": redis_port,
        "redis_password": "",
        "cache_ttl": 600,
        "enable_cache": True,
        "redis_required": True
    }
    
    # Cria diretório /data se não existir
    data_dir = '/tmp/test_ha_data'
    os.makedirs(data_dir, exist_ok=True)
    
    # Escreve arquivo de configuração
    options_file = os.path.join(data_dir, 'options.json')
    with open(options_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"📝 Configuração HA criada em {options_file}:")
    print(json.dumps(config, indent=2))
    
    return options_file, config

def test_app_with_ha_config():
    """Testa a aplicação com configuração do HA"""
    
    print("🧪 Testando aplicação com configuração do Home Assistant")
    print("=" * 60)
    
    # Cria configuração de teste
    options_file, config = create_ha_config()
    
    # Modifica temporariamente o app.py para usar o arquivo de teste
    app_file = 'image-combiner/app.py'
    backup_file = 'image-combiner/app.py.backup'
    
    try:
        # Faz backup do arquivo original
        shutil.copy(app_file, backup_file)
        
        # Lê o arquivo original
        with open(app_file, 'r') as f:
            content = f.read()
        
        # Substitui o caminho do arquivo de opções
        modified_content = content.replace(
            "options_file = '/data/options.json'",
            f"options_file = '{options_file}'"
        )
        
        # Escreve o arquivo modificado
        with open(app_file, 'w') as f:
            f.write(modified_content)
        
        print(f"✅ Arquivo app.py modificado para usar {options_file}")
        
        # Executa a aplicação por alguns segundos para ver os logs
        print(f"\n🚀 Iniciando aplicação...")
        
        env = os.environ.copy()
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            cwd='image-combiner',
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Aguarda alguns segundos
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Aplicação iniciou com sucesso!")
            process.terminate()
            stdout, stderr = process.communicate()
        else:
            stdout, stderr = process.communicate()
            print("❌ Aplicação falhou ao iniciar")
        
        print(f"\n📋 LOGS DA APLICAÇÃO:")
        print("STDOUT:")
        print(stdout)
        if stderr:
            print("STDERR:")
            print(stderr)
        
    finally:
        # Restaura o arquivo original
        if os.path.exists(backup_file):
            shutil.move(backup_file, app_file)
            print(f"\n✅ Arquivo app.py restaurado")
        
        # Remove arquivos temporários
        if os.path.exists(options_file):
            os.remove(options_file)
        if os.path.exists('/tmp/test_ha_data'):
            shutil.rmtree('/tmp/test_ha_data')

def test_config_variations():
    """Testa diferentes variações de configuração"""
    
    print("\n🔄 Testando variações de configuração...")
    print("=" * 50)
    
    variations = [
        {
            "name": "Redis IP correto",
            "config": {"redis_host": "192.168.68.120", "redis_port": 6379}
        },
        {
            "name": "Redis localhost",
            "config": {"redis_host": "localhost", "redis_port": 6379}
        },
        {
            "name": "Redis host vazio",
            "config": {"redis_host": "", "redis_port": 6379}
        },
        {
            "name": "Redis porta inválida",
            "config": {"redis_host": "192.168.68.120", "redis_port": 0}
        }
    ]
    
    for variation in variations:
        print(f"\n🧪 Testando: {variation['name']}")
        
        # Simula carregamento de configuração
        config = {
            "max_images": 4,
            "image_quality": 85,
            "cell_width": 400,
            "cell_height": 300,
            "timeout": 10,
            "redis_password": "",
            "cache_ttl": 600,
            "enable_cache": True,
            "redis_required": False,  # Para não falhar nos testes
            **variation['config']
        }
        
        redis_host = config.get('redis_host', 'localhost')
        redis_port = config.get('redis_port', 6379)
        
        # Validação (replica a lógica do app.py)
        if not redis_host or redis_host == '':
            redis_host = 'localhost'
            print(f"⚠️ redis_host vazio, usando padrão: localhost")
        
        if not isinstance(redis_port, int) or redis_port <= 0:
            redis_port = 6379
            print(f"⚠️ redis_port inválido, usando padrão: 6379")
        
        print(f"📊 Resultado:")
        print(f"   - Host final: '{redis_host}'")
        print(f"   - Port final: {redis_port}")
        
        # Testa conexão se for um endereço válido
        if redis_host == "192.168.68.120":
            try:
                import redis
                r = redis.Redis(host=redis_host, port=redis_port, socket_connect_timeout=2)
                r.ping()
                print(f"   - Conexão: ✅ Sucesso")
            except Exception as e:
                print(f"   - Conexão: ❌ Falha - {e}")

def main():
    """Função principal"""
    print("🚀 Teste de Configuração Home Assistant - Image Combiner v1.1.1")
    print("Este script testa como a aplicação carrega configurações do HA")
    print()
    
    # Testa variações de configuração
    test_config_variations()
    
    # Testa aplicação com configuração real
    test_app_with_ha_config()
    
    print("\n✨ Testes concluídos!")
    print("\n💡 PRÓXIMOS PASSOS:")
    print("1. Verifique se redis_host está configurado como '192.168.68.120' no HA")
    print("2. Verifique se redis_port está configurado como 6379 no HA")
    print("3. Reinicie o addon após alterar as configurações")
    print("4. Verifique os logs de inicialização do addon")

if __name__ == "__main__":
    main()
