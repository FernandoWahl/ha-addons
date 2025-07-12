#!/usr/bin/env python3
"""
Script para gerar ícones para o Image Combiner Home Assistant Addon
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size=(128, 128), filename="icon.png"):
    """Cria um ícone para o addon"""
    
    # Cria uma nova imagem com fundo gradiente azul
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fundo com gradiente azul
    for y in range(size[1]):
        alpha = int(255 * (1 - y / size[1] * 0.3))
        color = (41, 128, 185, alpha)  # Azul Home Assistant
        draw.line([(0, y), (size[0], y)], fill=color)
    
    # Desenha 4 quadrados representando as imagens
    margin = size[0] // 8
    square_size = (size[0] - 3 * margin) // 2
    
    # Posições dos quadrados (2x2)
    positions = [
        (margin, margin),  # Top-left
        (margin + square_size + margin//2, margin),  # Top-right
        (margin, margin + square_size + margin//2),  # Bottom-left
        (margin + square_size + margin//2, margin + square_size + margin//2)  # Bottom-right
    ]
    
    # Cores para os quadrados
    colors = [
        (52, 152, 219, 200),   # Azul claro
        (46, 204, 113, 200),   # Verde
        (241, 196, 15, 200),   # Amarelo
        (231, 76, 60, 200)     # Vermelho
    ]
    
    # Desenha os quadrados
    for i, (pos, color) in enumerate(zip(positions, colors)):
        x, y = pos
        # Quadrado com bordas arredondadas
        draw.rounded_rectangle(
            [x, y, x + square_size, y + square_size],
            radius=8,
            fill=color,
            outline=(255, 255, 255, 150),
            width=2
        )
        
        # Adiciona um símbolo de imagem (retângulo menor)
        inner_margin = square_size // 4
        draw.rounded_rectangle(
            [x + inner_margin, y + inner_margin, 
             x + square_size - inner_margin, y + square_size - inner_margin],
            radius=4,
            fill=(255, 255, 255, 100)
        )
    
    # Adiciona seta de combinação no centro
    center_x, center_y = size[0] // 2, size[1] // 2
    arrow_size = 12
    
    # Desenha seta apontando para baixo e direita (combinação)
    arrow_points = [
        (center_x - arrow_size//2, center_y - arrow_size//2),
        (center_x + arrow_size//2, center_y),
        (center_x - arrow_size//2, center_y + arrow_size//2)
    ]
    draw.polygon(arrow_points, fill=(255, 255, 255, 220))
    
    # Salva o ícone
    img.save(filename, 'PNG')
    print(f"✅ Ícone criado: {filename}")

def create_logo(size=(256, 256), filename="logo.png"):
    """Cria um logo maior para o addon"""
    
    # Cria uma nova imagem com fundo transparente
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fundo circular com gradiente
    center = (size[0] // 2, size[1] // 2)
    radius = min(size) // 2 - 10
    
    # Desenha círculo de fundo
    draw.ellipse(
        [center[0] - radius, center[1] - radius,
         center[0] + radius, center[1] + radius],
        fill=(41, 128, 185, 200),
        outline=(255, 255, 255, 100),
        width=4
    )
    
    # Desenha 4 imagens em grid
    margin = size[0] // 6
    square_size = (size[0] - 4 * margin) // 2
    
    positions = [
        (margin, margin),
        (margin + square_size + margin, margin),
        (margin, margin + square_size + margin),
        (margin + square_size + margin, margin + square_size + margin)
    ]
    
    colors = [
        (52, 152, 219, 220),   # Azul
        (46, 204, 113, 220),   # Verde
        (241, 196, 15, 220),   # Amarelo
        (231, 76, 60, 220)     # Vermelho
    ]
    
    # Desenha as "imagens"
    for pos, color in zip(positions, colors):
        x, y = pos
        draw.rounded_rectangle(
            [x, y, x + square_size, y + square_size],
            radius=12,
            fill=color,
            outline=(255, 255, 255, 180),
            width=3
        )
        
        # Adiciona detalhes internos
        inner_margin = square_size // 5
        draw.rounded_rectangle(
            [x + inner_margin, y + inner_margin,
             x + square_size - inner_margin, y + square_size - inner_margin],
            radius=6,
            fill=(255, 255, 255, 120)
        )
        
        # Adiciona um "ponto" representando uma foto
        dot_size = 8
        dot_x = x + square_size - inner_margin - dot_size
        dot_y = y + inner_margin
        draw.ellipse(
            [dot_x, dot_y, dot_x + dot_size, dot_y + dot_size],
            fill=(255, 255, 255, 200)
        )
    
    # Adiciona símbolo de combinação no centro
    center_x, center_y = size[0] // 2, size[1] // 2
    
    # Desenha setas convergindo
    arrow_size = 20
    line_width = 4
    
    # Setas apontando para o centro
    arrows = [
        # De cima-esquerda para centro
        [(margin + square_size//2, margin + square_size//2), (center_x - 10, center_y - 10)],
        # De cima-direita para centro
        [(margin + square_size + margin + square_size//2, margin + square_size//2), (center_x + 10, center_y - 10)],
        # De baixo-esquerda para centro
        [(margin + square_size//2, margin + square_size + margin + square_size//2), (center_x - 10, center_y + 10)],
        # De baixo-direita para centro
        [(margin + square_size + margin + square_size//2, margin + square_size + margin + square_size//2), (center_x + 10, center_y + 10)]
    ]
    
    for start, end in arrows:
        draw.line([start, end], fill=(255, 255, 255, 200), width=line_width)
    
    # Círculo central
    center_radius = 15
    draw.ellipse(
        [center_x - center_radius, center_y - center_radius,
         center_x + center_radius, center_y + center_radius],
        fill=(255, 255, 255, 240),
        outline=(41, 128, 185, 255),
        width=3
    )
    
    # Salva o logo
    img.save(filename, 'PNG')
    print(f"✅ Logo criado: {filename}")

def main():
    """Função principal"""
    print("🎨 Gerando ícones para o Image Combiner Addon...")
    
    # Cria os diretórios se não existirem
    addon_dir = "image-combiner"
    if not os.path.exists(addon_dir):
        os.makedirs(addon_dir)
    
    # Gera os ícones
    create_icon(size=(128, 128), filename=f"{addon_dir}/icon.png")
    create_logo(size=(256, 256), filename=f"{addon_dir}/logo.png")
    
    print("✨ Ícones gerados com sucesso!")
    print(f"📁 Arquivos salvos em: {addon_dir}/")
    print("   - icon.png (128x128) - Ícone do addon")
    print("   - logo.png (256x256) - Logo do addon")

if __name__ == "__main__":
    main()
