import os
import json
import hashlib
from pathlib import Path
from datetime import datetime


# ============================================================
# Função para gerar o hash SHA256 de um arquivo (até 2 MB)
# ============================================================
def gerar_sha256(caminho):
    try:
        tamanho = os.path.getsize(caminho)
        if tamanho > 2_000_000:  # pula arquivos grandes
            return None

        sha = hashlib.sha256()
        with open(caminho, "rb") as f:
            for bloco in iter(lambda: f.read(4096), b""):
                sha.update(bloco)

        return sha.hexdigest()
    except Exception:
        return None


# ============================================================
# Função para coletar metadados de um único item
# ============================================================
def coletar_info(caminho: Path):
    try:
        stat = caminho.stat()
        info = {
            "path": str(caminho),
            "name": caminho.name,
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        }

        if caminho.is_dir():
            info["type"] = "directory"
            info["ext"] = None
            info["size"] = None
            info["sha256"] = None
        else:
            info["type"] = "file"
            info["ext"] = caminho.suffix
            info["size"] = stat.st_size
            info["sha256"] = gerar_sha256(caminho)

        return info

    except Exception:
        return {
            "path": str(caminho),
            "error": "Não foi possível ler este item."
        }


# ============================================================
# Função principal: varrer diretório e gerar JSON
# ============================================================
def escanear_projeto(raiz="."):
    raiz = Path(raiz).resolve()
    logs_dir = raiz / "src" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    destino_json = logs_dir / "proj.json"

    itens = []

    for root, dirs, files in os.walk(raiz):
        # Ignora a pasta de logs para não escanear ela mesma
        if "logs" in root:
            continue

        for nome in dirs:
            p = Path(root) / nome
            itens.append(coletar_info(p))

        for nome in files:
            p = Path(root) / nome
            # Evita capturar o próprio JSON
            if p.name == "proj.json":
                continue
            itens.append(coletar_info(p))

    estrutura = {
        "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "root": str(raiz),
        "items": itens
    }

    with open(destino_json, "w", encoding="utf-8") as f:
        json.dump(estrutura, f, indent=4, ensure_ascii=False)

    print(f"[OK] Arquivo gerado em: {destino_json}")


if __name__ == "__main__":
    escanear_projeto()
