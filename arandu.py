#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arandu — CLI do palácio de memória (sabedoria em guarani).

Desenho: Markdown + Git = fonte da verdade.
         .palace/cache.sqlite = índice DERIVADO (FTS5), jamais versionado,
         sempre re-gerável:  python arandu.py build   (zero migrations)

Comandos:
  build             varre as salas e (re)constrói o índice descartável
  find <query>      busca com ranking (FTS5; fallback LIKE)
  wake              gera .palace/wake-up.md (L0 identidade + L1 essential story)
  save              salva um bloco novo na sala certa (valida o contrato)
  stats             contagem por sala/status
  audit             saúde do palácio: YAML inválido, duplicatas, staleness
  graph             grafo de links [[...]] e blocos órfãos
  rooms             lista as salas

Zero dependências externas (Python stdlib only). Local. Nuvem: nenhuma.
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PALACE = ROOT / ".palace"
CACHE = PALACE / "cache.sqlite"
WAKE = PALACE / "wake-up.md"

INDEX_VERSION = 1          # sobe = rebuild total (nunca há migration)
WAKE_BUDGET = 3200         # orçamento L1 em caracteres (mempalace-compatible)
STALE_HOT_DAYS = 90        # bloco hot sem atualização há N dias
STALE_UNREAD_DAYS = 30     # ref unread sem absorção há N dias
BIG_BLOCK_CHARS = 2000     # bloco grande demais (1 ideia = 1 bloco!)

ROOM_RE = re.compile(r"^\d\d-"            )
SKIP_DIRS = {"00-reception"}               # mapa/protocolo, não são blocos
FIELD_RE = re.compile(r"^\s*([A-Za-z_][\w-]*)\s*:\s*(.*)$")
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
REQUIRED = ("id", "room", "status", "entry", "updated")

CLI_TAG = " [CLI]"                       # marca blocos criados pela CLI


# ---------------------------------------------------------------- parsing

def rooms() -> list[Path]:
    out = []
    for p in sorted(ROOT.iterdir()):
        if p.is_dir() and ROOM_RE.match(p.name) and p.name not in SKIP_DIRS:
            out.append(p)
    return out


def slugify(text: str) -> str:
    t = unicodedata.normalize("NFKD", text.encode("ascii", "ignore").decode())
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).lower()
    return t.strip("-")[:48] or "bloco"


def parse_list(value: str) -> list[str]:
    v = value.strip()
    if not v.startswith("["):
        return [p.strip() for p in re.split(r"[,;]", v) if p.strip()]
    inner = v.strip("[]")
    return [p.strip().strip("'\"") for p in inner.split(",") if p.strip()]


def scan_files() -> list[tuple[Path, list[dict]]]:
    """Retorna [(arquivo, [blocos])] de todas as salas."""
    corpus = []
    for room in rooms():
        for md in sorted(room.rglob("*.md")):
            rel = md.relative_to(room).as_posix()
            if md.name == "SKILL.md" or rel.startswith("skills/"):
                continue                       # arquivo guardado na biblioteca, não é bloco
            try:
                text = md.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            corpus.append((md, blocks_of(text)))
    return corpus


def blocks_of(text: str) -> list[dict]:
    """Extrai blocos --- YAML --- + conteúdo até o próximo --- (ou EOF)."""
    out, lines, n, i = [], text.splitlines(), len(text.splitlines()), 0
    while i < n:
        if lines[i].strip() == "---":
            j = i + 1
            meta = {}
            while j < n and lines[j].strip() != "---":
                m = FIELD_RE.match(lines[j])
                if m:
                    meta[m.group(1).lower().replace("-", "_")] = m.group(2).strip()
                j += 1
            if j < n:                                # frontmatter fechado
                k = j + 1                            # conteúdo até o próximo --- (o próximo opener)
                while k < n and lines[k].strip() != "---":
                    k += 1
                if meta:                             # fence vazio = separador decorativo: pula só ele
                    meta["__content"] = "\n".join(lines[j + 1:k]).strip()
                    out.append(meta)
                    i = k
                else:
                    i = j + 1
                continue
        i += 1
    return out


def load_blocks() -> list[dict]:
    blocks = []
    for path, blist in scan_files():
        room = path.parent.name if path.parent.name not in SKIP_DIRS else ""
        for b in blist:
            b["_file"] = str(path.relative_to(ROOT))
            b["_room"] = b.get("room") or room
            blocks.append(b)
    return blocks


def block_valid(b: dict) -> bool:
    return all(b.get(k) for k in REQUIRED) and "__content" in b


def content_of(b: dict) -> str:
    return b.get("__content", "").strip()


def tags_of(b: dict) -> list[str]:
    return parse_list(b.get("tags", ""))


def first_line(b: dict) -> str:
    for line in content_of(b).splitlines():
        if line.strip():
            return line.strip().lstrip("# ").strip()
    return "(vazio)"


# ---------------------------------------------------------------- índice

def fts_available() -> bool:
    try:
        con = sqlite3.connect(":memory:")
        try:
            con.execute("CREATE VIRTUAL TABLE t USING fts5(x)")
            return True
        except sqlite3.Error:
            return False
        finally:
            con.close()
    except sqlite3.Error:
        return False


def cmd_build(_args) -> None:
    PALACE.mkdir(exist_ok=True)
    if CACHE.exists():
        CACHE.unlink()
    con = sqlite3.connect(CACHE)
    cur = con.cursor()
    cur.execute("CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT)")
    cur.execute("INSERT INTO meta VALUES ('index_version', ?)", (str(INDEX_VERSION),))
    cur.execute("INSERT INTO meta VALUES ('built_at', ?)", (datetime.now().isoformat(timespec="seconds"),))
    cur.execute(
        "CREATE TABLE memory (id TEXT PRIMARY KEY, room TEXT, file TEXT, "
        "status TEXT, type TEXT, tags TEXT, entry TEXT, updated TEXT, source TEXT, content TEXT)"
    )
    use_fts = fts_available()
    if use_fts:
        cur.execute("CREATE VIRTUAL TABLE fts USING fts5(id UNINDEXED, content, tags)")
    cur.execute("CREATE TABLE edges (src TEXT, dst TEXT)")

    blocks = load_blocks()
    seen, n_ok, n_bad, dupes = {}, 0, 0, []
    for b in blocks:
        if not block_valid(b):
            if b:  # fence solta (yaml incompleto) vira ruído; audit mostra
                n_bad += 1
            continue
        bid = b["id"]
        if bid in seen:
            dupes.append(bid)
            continue
        seen[bid] = True
        cur.execute(
            "INSERT INTO memory VALUES (?,?,?,?,?,?,?,?,?,?)",
            (bid, b["_room"], b["_file"], b.get("status"), b.get("type"),
             " ".join(tags_of(b)), b.get("entry"), b.get("updated"),
             b.get("source", ""), content_of(b)),
        )
        if use_fts:
            body = (b["id"] + " " + content_of(b))
            cur.execute("INSERT INTO fts (id, content, tags) VALUES (?,?,?)",
                        (bid, body, " ".join(tags_of(b))))
        for target in LINK_RE.findall(content_of(b)):
            cur.execute("INSERT INTO edges VALUES (?,?)", (bid, target.strip()))
        n_ok += 1
    con.commit()
    n_edges = cur.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
    con.close()
    engine = "FTS5" if use_fts else "LIKE-fallback"
    print(f"[build v{INDEX_VERSION}] blocos ok={n_ok}  invalidos/ustriados={n_bad}  dup_id={len(dupes)}  links={n_edges}  motor={engine}")
    print(f"  cache: {CACHE.relative_to(ROOT)}  (derivado — .gitignore, re-geravel com build)")
    for d in sorted(set(dupes)):
        print(f"  ! id duplicado: {d}")


def cmd_find(args) -> None:
    q = args.query
    limit = args.limit
    if not CACHE.exists():
        cmd_find_build_if_needed()
    con = sqlite3.connect(CACHE)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if fts_available():
        try:
            rows = cur.execute(
                "SELECT m.id, m.room, m.status, m.tags, m.file, "
                "snippet(fts, 1, '»', '«', '…', 12) AS snip "
                "FROM fts JOIN memory m ON m.id = fts.id "
                "WHERE fts MATCH ? ORDER BY bm25(fts) LIMIT ?",
                (q, limit),
            ).fetchall()
        except sqlite3.Error:
            rows = like_rows(cur, q, limit)
    else:
        rows = like_rows(cur, q, limit)
    con.close()
    if not rows:
        print(f"nada para: {q!r}")
        return
    print(f"{len(rows)} resultado(s) para {q!r}:\n")
    for r in rows:
        print(f"[{r['id']}]  sala={r['room']}  status={r['status']}  tags={r['tags']}")
        print(f"    file: {r['file']}")
        print(f'    "{r["snip"]}"')
        print()


def like_rows(cur, q, limit):
    like = f"%{q}%"
    return cur.execute(
        "SELECT id, room, status, tags, file, substr(content,1,160) AS snip "
        "FROM memory WHERE content LIKE ? OR tags LIKE ? OR id LIKE ? LIMIT ?",
        (like, like, like, limit),
    ).fetchall()


def cmd_find_build_if_needed() -> None:
    print("[find] cache ausente — construindo índice primeiro…")
    cmd_build(None)


# ---------------------------------------------------------------- wake

def cmd_wake(_args) -> None:
    blocks = [b for b in load_blocks() if block_valid(b)]

    # L0 — identidade
    ident = None
    for b in blocks:
        if b["_file"].replace("\\", "/").startswith("10-person/who-i-am") and str(b.get("id", "")).startswith("pref-identidade"):
            ident = b
            break
    if ident is None:                                   # fallback: primeiro bloco de fato
        ident = next((b for b in blocks if b["_room"] == "10-person"), None)
    l0 = f"L0 IDENTIDADE: {first_line(ident)}" if ident else "L0 IDENTIDADE: (bloco de identidade ausente)"
    used = len(l0)

    # L1 — essential story: hot primeiro, depois os mais atualizados
    eligible = sorted(
        [b for b in blocks if b.get("status") in ("hot", "active")],
        key=lambda b: (0 if b.get("status") == "hot" else 1, str(b.get("updated", ""))),
        reverse=True,
    )
    story: dict[str, list[str]] = {}
    for b in eligible:
        line = f"- {first_line(b)}  ({b.get('id')})"
        if used + len(line) > WAKE_BUDGET:
            break
        story.setdefault(b["_room"], []).append(line)
        used += len(line)

    lines = [
        f"arandu wake-up — gerado {datetime.now():%Y-%m-%d %H:%M} (derivado, ver via `python arandu.py wake`)",
        "",
        l0,
        "",
        "L1 ESSENTIAL STORY:",
    ]
    if story:
        for room in sorted(story):
            lines.append(f"  [{room}]")
            lines.extend(f"  {ln}" for ln in story[room])
    else:
        lines.append("  (nenhum bloco hot/active ainda)")
    lines += ["", f"L2/L3: sob demanda — `python arandu.py find \"<termo>\"`. "
                  f"Orçamento usado: ~{used}/{WAKE_BUDGET} chars."]
    text = "\n".join(lines)
    PALACE.mkdir(exist_ok=True)
    WAKE.write_text(text + "\n", encoding="utf-8")
    print(text)
    print(f"\n(written: {WAKE.relative_to(ROOT)})")


# ---------------------------------------------------------------- save

TYPE_PREFIX = {"inspiration": "ref", "leitura": "ref", "ferramenta": "ref", "repo": "ref",
               "ideia": "ideia", "decisao": "fato", "preference": "pref", "skill": "skill",
               "projeto": "proj"}


def cmd_save(args) -> None:
    today = date.today().isoformat()
    title = args.title or (args.text.splitlines()[0][:60] if args.text else "memoria")
    prefix = TYPE_PREFIX.get(args.type, "fato")
    bid = f"{prefix}-{slugify(title)}"

    target = Path(args.file) if args.file else ROOT / args.room / f"{slugify(title)}.md"
    target.parent.mkdir(parents=True, exist_ok=True)

    tags = ", ".join(t.strip() for t in args.tags.split(",") if t.strip()) if args.tags else "geral"
    fence_open, fence_close = "---", "---"
    block = [
        fence_open,
        f"id: {bid}",
        f"room: {args.room}",
        f"tags: [{tags}]",
        f"type: {args.type}",
        "status: hot" if args.type in ("decisao", "preference") else "status: active",
        f"entry: {today}",
        f"updated: {today}",
        f"source: {args.source}" if args.source else "source: \"\"",
        fence_close,
        "",
        (args.text or args.title or "").strip(),
    ]
    marker = f"id: {bid}\n"
    existing = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""
    if marker in existing:
        print(f"! dedupe: bloco '{bid}' ja existe em {target.relative_to(ROOT)} — nada gravado (verifique/edite)")
        return
    text = "\n".join(block) + "\n"
    with target.open("a", encoding="utf-8", newline="\n") as fh:
        if existing and not existing.endswith("\n"):
            fh.write("\n")
        if existing:
            fh.write("\n")
        fh.write(text)
    print(f"salvo: {target.relative_to(ROOT)}  (id={bid}{CLI_TAG})")
    print("proximo passo:  git add -A && git commit -m 'palace: add %s'" % bid)


# ---------------------------------------------------------------- stats/audit

def cmd_stats(_args) -> None:
    blocks = [b for b in load_blocks() if block_valid(b)]
    by_room: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for b in blocks:
        by_room[b["_room"]] = by_room.get(b["_room"], 0) + 1
        by_status[b.get("status", "?")] = by_status.get(b.get("status", "?"), 0) + 1
    print(f"total: {len(blocks)} blocos")
    print("por sala:")
    for room in sorted(by_room):
        print(f"  {room:<16} {by_room[room]}")
    print("por status:")
    for s in sorted(by_status):
        print(f"  {s:<12} {by_status[s]}")


def cmd_audit(_args) -> None:
    blocks = load_blocks()
    problems: dict[str, list[str]] = {"invalid": [], "stale_hot": [], "stale_unread": [], "big": []}
    ids = {}
    for b in blocks:
        path = b["_file"]
        if b and not block_valid(b):
            problems["invalid"].append(f"{path} — frontmatter incompleto (faltam {', '.join(k for k in REQUIRED if not b.get(k))})")
            continue
        if not b:
            continue
        bid = b.get("id", "?")
        if bid in ids:
            problems["invalid"].append(f"{path} — id duplicado: {bid} (primeiro em {ids[bid]})")
        ids[bid] = path
        today = date.today()
        try:
            updated = date.fromisoformat(str(b.get("updated", ""))[:10])
        except ValueError:
            problems["invalid"].append(f"{path} — updated fora do formato ISO: {b.get('updated')}")
            continue
        age = (today - updated).days
        if b.get("status") == "hot" and age > STALE_HOT_DAYS:
            problems["stale_hot"].append(f"{bid} (updated há {age}d, file {path})")
        if str(b.get("status")) == "unread" and age > STALE_UNREAD_DAYS:
            problems["stale_unread"].append(f"{bid} (unread há {age}d — absorver ou archivar: {path})")
        if len(content_of(b)) > BIG_BLOCK_CHARS:
            problems["big"].append(f"{bid} — {len(content_of(b))} chars (> {BIG_BLOCK_CHARS}) — dividir em blocos menores")

    if blocks and not any(block_valid(b) for b in blocks):
        print("atenção: nenhum bloco válido encontrado — palácio vazio ou protocolo fora do formato.")
    total = 0
    for k in ("invalid", "stale_hot", "stale_unread", "big"):
        items = problems[k]
        title = {"invalid": "YAML/contrato", "stale_hot": f"hot estagnado (>{STALE_HOT_DAYS}d)",
                 "stale_unread": f"unread parado (>{STALE_UNREAD_DAYS}d)", "big": f"blocos gigantes (>{BIG_BLOCK_CHARS} chars)"}[k]
        print(f"\n== {title}: {len(items)}")
        for item in items:
            print(f"  - {item}")
            total += 1
    print(f"\naudit: {total} problema(s) em {len([b for b in blocks if b])} blocos escaneados.")


# ---------------------------------------------------------------- graph

def cmd_graph(_args) -> None:
    blocks = [b for b in load_blocks() if block_valid(b)]
    ids = {b["id"] for b in blocks}
    edges = [(b["id"], t.strip()) for b in blocks
             for t in LINK_RE.findall(content_of(b))]
    broken = [(s, t) for s, t in edges if t not in ids]
    print(f"graph: {len(blocks)} blocos, {len(edges)} links")
    for s, t in edges:
        flag = f"  (! dest inexistente)" if t not in ids else ""
        print(f"  {s} -> {t}{flag}")
    dangling = sorted(ids - {s for s, _ in edges} - {t for _, t in edges if t in ids})
    if dangling:
        print(f"\norfaos (sem link entra/sai): {', '.join(dangling)}")
    if broken:
        print(f"\n{len(broken)} link(s) quebrado(s) — corrigir nomes")


# ---------------------------------------------------------------- rooms

def cmd_rooms(_args) -> None:
    for room in rooms():
        n = sum(len(blocks_of(p.read_text(encoding='utf-8', errors='replace')))
                for p in room.rglob('*.md'))
        print(f"{room.name:<16} {n:>3} blocos")


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(prog="arandu", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build",  help="(re)constrói o índice descartável").set_defaults(fn=cmd_build)
    p = sub.add_parser("find", help="busca com ranking")
    p.add_argument("query"); p.add_argument("--limit", type=int, default=5); p.set_defaults(fn=cmd_find)
    sub.add_parser("wake",   help="gera wake-up.md (L0+L1)").set_defaults(fn=cmd_wake)
    sp = sub.add_parser("save", help="salva bloco na sala certa")
    sp.add_argument("--room", required=True, help="sala, ex: 50-library")
    sp.add_argument("--title", help="título curto (vira id/slug)")
    sp.add_argument("--text", help="conteúdo (as linhas do bloco)")
    sp.add_argument("--tags", default="geral", help="tags csv: ui, inspiracao")
    sp.add_argument("--type", default="ideia", choices=list(TYPE_PREFIX), help="tipo do bloco")
    sp.add_argument("--source", help="URL de origem (refs)")
    sp.add_argument("--file", help="arquivo destino opcional (relativo)")
    sp.set_defaults(fn=cmd_save)
    sub.add_parser("stats", help="contagens").set_defaults(fn=cmd_stats)
    sub.add_parser("audit", help="saúde: inválidos, staleness, duplicatas").set_defaults(fn=cmd_audit)
    sub.add_parser("graph", help="grafo de links [[...]]").set_defaults(fn=cmd_graph)
    sub.add_parser("rooms", help="lista salas + contagem").set_defaults(fn=cmd_rooms)

    args = ap.parse_args()
    try:
        args.fn(args)
    except BrokenPipeError:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
