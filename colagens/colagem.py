"""Gera colagens 4:5 para o Instagram com 3 fotos cada (exportado em 2160x2700).

Layouts:
  "grande-2q": 1 foto grande + 2 quadrados lado a lado (grande em cima ou embaixo)
  "3h":        3 fotos horizontais iguais, empilhadas

Uso: python colagem.py config.json saida.jpg

config.json:
{
  "layout": "grande-2q", "grande_em_cima": true,
  "espaco": 12, "fundo": "#ffffff",
  "fotos": [{"arquivo": "a.jpg", "foco": [0.5, 0.3]}, {...}, {...}]
}
Em "grande-2q" a 1a foto é a grande. "foco" = ponto (x, y de 0 a 1) que deve
ficar no centro do recorte (padrão: centro da foto).
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


def celulas(layout, g, em_cima):
    """Retorna as caixas (x, y, w, h) de cada foto, na ordem de config['fotos']."""
    if layout == "3h":
        h = (H - 4 * g) // 3
        return [(g, g + i * (h + g), W - 2 * g, h) for i in range(3)]
    q = (W - 3 * g) // 2
    gh = H - 3 * g - q
    if em_cima:
        return [(g, g, W - 2 * g, gh), (g, 2 * g + gh, q, q), (2 * g + q, 2 * g + gh, q, q)]
    return [(g, 2 * g + q, W - 2 * g, gh), (g, g, q, q), (2 * g + q, g, q, q)]


def gerar(cfg, base):
    g = cfg.get("espaco", 12) * ESCALA
    canvas = Image.new("RGB", (W, H), cfg.get("fundo", "#ffffff"))
    caixas = celulas(cfg["layout"], g, cfg.get("grande_em_cima", True))
    for spec, (x, y, w, h) in zip(cfg["fotos"], caixas):
        img = ImageOps.exif_transpose(Image.open(base / spec["arquivo"])).convert("RGB")
        canvas.paste(recortar(img, w, h, tuple(spec.get("foco", (0.5, 0.5)))), (x, y))
    return canvas


if __name__ == "__main__":
    cfg_path, saida = Path(sys.argv[1]), sys.argv[2]
    cfg = json.loads(cfg_path.read_text())
    gerar(cfg, cfg_path.parent).save(saida, quality=95, subsampling=0)
    print("ok:", saida)
