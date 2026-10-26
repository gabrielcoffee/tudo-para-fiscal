"""Gera colagens 4:5 para o Instagram com 3 fotos cada (exportado em 2160x2700).

Layouts (a 1a foto da lista ocupa a 1a caixa, e assim por diante):
  "3h":           3 faixas horizontais iguais
  "grande-cima":  grande em cima + 2 quadrados embaixo
  "grande-baixo": 2 quadrados em cima + grande embaixo
  "faixa-topo":   faixa larga em cima + 2 retratos embaixo
  "tall-esq":     retrato alto à esquerda + 2 fotos empilhadas à direita
  "tall-dir":     2 fotos empilhadas à esquerda + retrato alto à direita
  "faixa-base":   2 retratos em cima + faixa larga embaixo
  "video-esq":    caixa 9:16 (vídeo) + foto embaixo + retrato alto à direita
  "video-dir":    o mesmo, espelhado (vídeo no canto superior direito)

Uso: python colagem.py config.json saida.jpg

config.json:
{
  "layout": "grande-cima", "espaco": 12, "fundo": "#ffffff",
  "fotos": [
    {"arquivo": "a.jpg", "foco": [0.5, 0.3]},
    {"placeholder": "FOTO PENDENTE"},
    {"buraco": true}
  ]
}
"foco" = ponto (x, y de 0 a 1) que fica no centro do recorte (padrão: centro).
"placeholder" = caixa cinza com texto; "buraco" = área reservada para o vídeo
(sai cinza no .jpg e transparente em um .png extra).
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ESCALA = 2
BW, BH = 1080, 1350  # base do layout; o arquivo sai multiplicado por ESCALA


def caixas(layout, g):
    iw, ih = BW - 2 * g, BH - 2 * g
    q = (iw - g) // 2
    if layout == "3h":
        h = (BH - 4 * g) // 3
        return [(g, g + i * (h + g), iw, h) for i in range(3)]
    if layout in ("grande-cima", "grande-baixo"):
        gh = BH - 3 * g - q
        if layout == "grande-cima":
            return [(g, g, iw, gh), (g, 2 * g + gh, q, q), (2 * g + q, 2 * g + gh, q, q)]
        return [(g, 2 * g + q, iw, gh), (g, g, q, q), (2 * g + q, g, q, q)]
    if layout == "faixa-topo":
        fh = 470
        bh = BH - 3 * g - fh
        return [(g, g, iw, fh), (g, 2 * g + fh, q, bh), (2 * g + q, 2 * g + fh, q, bh)]
    if layout in ("tall-esq", "tall-dir"):
        sh = (ih - g) // 2
        if layout == "tall-esq":
            tw, sw = 620, iw - 620 - g
            return [(g, g, tw, ih), (2 * g + tw, g, sw, sh), (2 * g + tw, 2 * g + sh, sw, sh)]
        lw, rw = 640, iw - 640 - g
        return [(g, g, lw, sh), (g, 2 * g + sh, lw, sh), (2 * g + lw, g, rw, ih)]
    if layout == "faixa-base":
        fh = 470
        bh = BH - 3 * g - fh
        return [(g, 2 * g + bh, iw, fh), (g, g, q, bh), (2 * g + q, g, q, bh)]
    if layout in ("video-esq", "video-dir"):
        vw, vh = 506, 900  # 9:16
        lh, tw = BH - 3 * g - vh, iw - vw - g
        if layout == "video-esq":
            return [(g, g, vw, vh), (g, 2 * g + vh, vw, lh), (2 * g + vw, g, tw, ih)]
        return [(g + tw + g, g, vw, vh), (g + tw + g, 2 * g + vh, vw, lh), (g, g, tw, ih)]
    raise ValueError(layout)


def recortar(img, w, h, foco=(0.5, 0.5)):
    """Redimensiona e recorta a imagem para w x h mantendo o ponto de foco."""
    s = max(w / img.width, h / img.height)
    nw, nh = round(img.width * s), round(img.height * s)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = min(max(round(foco[0] * nw - w / 2), 0), nw - w)
    y = min(max(round(foco[1] * nh - h / 2), 0), nh - h)
    return img.crop((x, y, x + w, y + h))


def gerar(cfg, base):
    g = cfg.get("espaco", 12)
    canvas = Image.new("RGB", (BW * ESCALA, BH * ESCALA), cfg.get("fundo", "#ffffff"))
    buracos = []
    for spec, caixa in zip(cfg["fotos"], caixas(cfg["layout"], g)):
        x, y, w, h = (v * ESCALA for v in caixa)
        if "arquivo" in spec:
            img = ImageOps.exif_transpose(Image.open(base / spec["arquivo"])).convert("RGB")
            canvas.paste(recortar(img, w, h, tuple(spec.get("foco", (0.5, 0.5)))), (x, y))
            continue
        d = ImageDraw.Draw(canvas)
        d.rectangle((x, y, x + w - 1, y + h - 1), fill="#d9d9d9")
        texto = spec.get("placeholder", "VIDEO 9:16")
        fonte = ImageFont.load_default(size=48 * ESCALA)
        d.text((x + w / 2, y + h / 2), texto, fill="#7a7a7a", font=fonte, anchor="mm")
        if spec.get("buraco"):
            buracos.append((x, y, w, h))
    return canvas, buracos


if __name__ == "__main__":
    cfg_path, saida = Path(sys.argv[1]), Path(sys.argv[2])
    cfg = json.loads(cfg_path.read_text())
    img, buracos = gerar(cfg, cfg_path.parent)
    img.save(saida, quality=95, subsampling=0)
    print("ok:", saida)
    if buracos:
        png = img.convert("RGBA")
        for x, y, w, h in buracos:
            png.paste((0, 0, 0, 0), (x, y, x + w, y + h))
            print(f"área do vídeo (px): x={x} y={y} largura={w} altura={h}")
        png.save(saida.with_suffix(".png"))
