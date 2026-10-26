"""Gera colagens 4:5 para o Instagram.

Layout (base 1080x1350, exportado em 2x = 2160x2700):
  - 1 foto grande (largura total, proporção 2:1)
  - 2 quadrados lado a lado
  - 3 horizontais iguais (4:3) lado a lado
A ordem das faixas é configurável por colagem.

Uso:
  python colagem.py config.json saida.jpg

config.json:
{
  "ordem": ["grande", "quadrados", "horizontais"],
  "espaco": 12, "fundo": "#ffffff",
  "grande": {"arquivo": "a.jpg", "foco": [0.5, 0.4]},
  "quadrados": [{"arquivo": "b.jpg"}, {"arquivo": "c.jpg", "foco": [0.5, 0.3]}],
  "horizontais": [{"arquivo": "d.jpg"}, {"arquivo": "e.jpg"}, {"arquivo": "f.jpg"}]
}
"foco" = ponto (x, y de 0 a 1) que deve ficar visível no recorte; padrão é o centro.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps

ESCALA = 2
W, H = 1080 * ESCALA, 1350 * ESCALA


def recortar(img, w, h, foco=(0.5, 0.5)):
    """Redimensiona e recorta a imagem para w x h mantendo o ponto de foco."""
    s = max(w / img.width, h / img.height)
    nw, nh = round(img.width * s), round(img.height * s)
    img = img.resize((nw, nh), Image.LANCZOS)
    fx, fy = foco
    x = min(max(round(fx * nw - w / 2), 0), nw - w)
    y = min(max(round(fy * nh - h / 2), 0), nh - h)
    return img.crop((x, y, x + w, y + h))


def carregar(spec, base):
    img = ImageOps.exif_transpose(Image.open(base / spec["arquivo"])).convert("RGB")
    return img, tuple(spec.get("foco", (0.5, 0.5)))


def faixa(n, g, altura_ratio):
    """Largura de cada célula numa faixa de n fotos e a altura pela proporção."""
    cw = (W - g * (n + 1)) / n
    return cw, cw / altura_ratio


def gerar(cfg, base):
    g = cfg.get("espaco", 12) * ESCALA
    fundo = cfg.get("fundo", "#ffffff")
    ordem = cfg.get("ordem", ["grande", "quadrados", "horizontais"])

    # Alturas: quadrados e horizontais têm proporção fixa; a grande ocupa o resto.
    alturas = {
        "quadrados": faixa(2, g, 1.0)[1],
        "horizontais": faixa(3, g, 4 / 3)[1],
    }
    alturas["grande"] = H - g * 4 - alturas["quadrados"] - alturas["horizontais"]

    canvas = Image.new("RGB", (W, H), fundo)
    y = g
    for nome in ordem:
        specs = cfg[nome] if isinstance(cfg[nome], list) else [cfg[nome]]
        n = len(specs)
        cw = (W - g * (n + 1)) / n
        ch = round(alturas[nome])
        for i, spec in enumerate(specs):
            x0 = round(g + i * (cw + g))
            x1 = round(g + (i + 1) * cw + i * g)
            img, foco = carregar(spec, base)
            canvas.paste(recortar(img, x1 - x0, ch, foco), (x0, round(y)))
        y += ch + g
    return canvas


if __name__ == "__main__":
    cfg_path, saida = Path(sys.argv[1]), sys.argv[2]
    cfg = json.loads(cfg_path.read_text())
    gerar(cfg, cfg_path.parent).save(saida, quality=95, subsampling=0)
    print("ok:", saida)
