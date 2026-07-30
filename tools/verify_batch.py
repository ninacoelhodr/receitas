from pathlib import Path
idx = Path("index.html").read_text(encoding="utf-8")
print("links", idx.count('href="./receitas/'))
print("has musse", "Musse de guaran" in idx)
p = Path("receitas/frutos-do-mar/talharim-com-vongole.html").read_text(encoding="utf-8")
assert "dish-photo" in p and "source-photo" not in p
print("sample ok")
print("recipes", len(list(Path("receitas").rglob("*.html"))))
print("images", len(list(Path("imagens").glob("*.jpg"))))
print("pending", len(list(Path("entradas/pending").glob("*.jpg"))))
print("processadas", len(list(Path("entradas/processadas").glob("*.jpg"))))
