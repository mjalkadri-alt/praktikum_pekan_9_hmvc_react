"""Render source code snippets as dark editor-style images for the report."""
import os
import re
from pygments import lex
from pygments.lexers import PhpLexer, TypeScriptLexer, JsonLexer, MarkdownLexer
from pygments.token import Token
from PIL import Image, ImageDraw, ImageFont

ASSETS = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ASSETS, "code")
os.makedirs(OUT, exist_ok=True)

FONT = ImageFont.truetype("consola.ttf", 26)
FONT_BOLD = ImageFont.truetype("consolab.ttf", 26)
NUMFONT = ImageFont.truetype("consola.ttf", 24)

LINE_H = 38
CW = FONT.getlength("M")
PAD_L = 96
PAD_R = 34
PAD_T = 78
PAD_B = 34

COLORS = {
    "bg": (40, 44, 52),
    "bar": (33, 37, 43),
    "border": (56, 61, 71),
    "num": (99, 106, 120),
    "text": (220, 223, 228),
    "kw": (198, 120, 221),
    "str": (152, 195, 121),
    "com": (128, 137, 150),
    "num_lit": (209, 154, 102),
    "fn": (97, 175, 239),
    "type": (229, 192, 123),
    "tag": (224, 108, 117),
    "attr": (209, 154, 102),
    "var": (224, 108, 117),
}

KW_PHP = {"use", "namespace", "class", "extends", "return", "public", "private", "protected",
          "function", "new", "if", "else", "fn", "static", "null", "true", "false", "array",
          "match", "foreach", "as", "in", "const"}
KW_TS = {"import", "from", "export", "default", "function", "const", "let", "return", "if",
         "else", "await", "async", "type", "interface", "true", "false", "null", "undefined",
         "new", "void"}


def style_for(tok, text, lang):
    """Map a pygments token to (colour, bold)."""
    if tok in Token.Comment or tok in Token.Comment.Single or tok in Token.Comment.Multiline:
        return COLORS["com"], False
    if tok in Token.Literal.String or tok in Token.Literal.String.Double or tok in Token.Literal.String.Single \
            or tok in Token.Literal.String.Interpol:
        return COLORS["str"], False
    if tok in Token.Literal.Number:
        return COLORS["num_lit"], False
    if tok in Token.Name.Builtin:
        return COLORS["fn"], False
    if tok in Token.Name.Function or tok in Token.Name.Function.Magic:
        return COLORS["fn"], False
    if tok in Token.Name.Class or tok in Token.Name.Namespace:
        return COLORS["type"], True
    if tok in Token.Name.Variable:
        return COLORS["var"], False
    if tok in Token.Name.Attribute:
        return COLORS["attr"], False
    if tok in Token.Name.Tag:
        return COLORS["tag"], False
    if tok in Token.Punctuation:
        return COLORS["text"], False
    s = text.strip()
    if s in (KW_PHP | KW_TS):
        return COLORS["kw"], False
    if s.startswith("<") and s.endswith(">"):
        return COLORS["tag"], False
    return COLORS["text"], False


def wrap_token_lines(line, lang):
    """Return list of (indent, [(text, colour, bold)]) with soft-wrapped continuation lines."""
    lexer = {"php": PhpLexer(startinline=False), "ts": TypeScriptLexer(),
             "json": JsonLexer(), "md": MarkdownLexer()}[lang]
    tokens = list(lex(line + "\n", lexer))
    stripped = line.lstrip(" ")
    indent = len(line) - len(stripped)
    cols = 0
    out = []
    cur = []
    for tok, text in tokens:
        text = text.replace("\n", "")
        if not text:
            continue
        colour, bold = style_for(tok, text, lang)
        while text:
            room = int((1400 - 40 - PAD_L) // CW) - cols
            if len(text) <= room:
                cur.append((text, colour, bold))
                cols += len(text)
                text = ""
            else:
                cont_indent_room = room - 12
                if cont_indent_room <= 4:
                    out.append(cur)
                    cur = [(" " * 4, COLORS["text"], False)]
                    cols = 4
                    continue
                cur.append((text[:cont_indent_room], colour, bold))
                out.append(cur)
                cur = [(" " * 4, COLORS["text"], False)]
                cols = 4
                text = text[cont_indent_room:]
    out.append(cur)
    return indent, out


def render(name, code, lang, width=None, start_line=1):
    lines = code.rstrip("\n").split("\n")
    rendered = []
    for ln in lines:
        indent, wrapped = wrap_token_lines(ln, lang)
        for i, seg in enumerate(wrapped):
            rendered.append((indent, seg, i == 0))

    max_cols = 0
    for indent, seg, first in rendered:
        cols = sum(len(t) for t, _, _ in seg) + (indent if first else 0)
        max_cols = max(max_cols, cols)

    width = width or int(PAD_L + max_cols * CW + PAD_R)
    width = max(1120, min(width, 1400))
    height = PAD_T + len(rendered) * LINE_H + PAD_B

    img = Image.new("RGB", (width, height), COLORS["bg"])
    d = ImageDraw.Draw(img)

    # title bar + traffic lights
    d.rectangle([0, 0, width, 54], fill=COLORS["bar"])
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([26 + i * 34, 18, 44 + i * 34, 36], fill=c)
    d.rectangle([0, 54, width, height], outline=COLORS["border"], width=2)

    y = PAD_T - 10
    for idx, (indent, seg, first) in enumerate(rendered):
        if first:
            num = str(start_line + idx)
            tw = NUMFONT.getlength(num)
            d.text((PAD_L - 22 - tw, y + 4), num, font=NUMFONT, fill=COLORS["num"])
        x = PAD_L + (indent if first else 0) * CW
        for text, colour, bold in seg:
            d.text((x, y), text, font=(FONT_BOLD if bold else FONT), fill=colour)
            x += FONT.getlength(text)
        y += LINE_H

    path = os.path.join(OUT, name + ".png")
    if height > 2700:
        f = 2700 / height
        img = img.resize((int(width * f), 2700), Image.LANCZOS)
    img.save(path)
    return path, img.size[0], img.size[1]
