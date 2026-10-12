"""Offline documentation integrity checks; does not run MASS experiments.

SPDX-License-Identifier: CC-BY-4.0
"""

from pathlib import Path
import json
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


def heading_ids(text):
    """GitHub-style identifiers for this repository's simple headings."""
    result, counts = set(), {}
    for match in re.finditer(r"^#{1,6}\s+(.+)$", text, re.M):
        title = re.sub(r"[`*_]", "", match.group(1)).strip().lower()
        slug = "".join(c for c in title if c in " -_" or
                       unicodedata.category(c)[0] in "LN").replace(" ", "-")
        index = counts.get(slug, 0)
        counts[slug] = index + 1
        result.add(slug + (f"-{index}" if index else ""))
    result.update(re.findall(r'<a\s+(?:id|name)="([^"]+)"', text))
    return result


required = [
    "README.md", "AGENTS.md", "ATTRIBUTION.md", "LICENSE.md", "CONTRIBUTING.md",
    "CITATION.cff", "references/paper.bib", "metadata/paper.json",
    "metadata/claims.json", "metadata/results.json",
    "notes/01-paper-map.md", "notes/02-method-and-notation.md", "notes/03-results.md",
    "notes/04-limitations.md", "notes/05-workflow-examples.md",
    "notes/06-figures-and-tables.md",
]
for name in required:
    require((ROOT / name).is_file(), f"Missing file: {name}")
if errors:
    print("\n".join(errors))
    sys.exit(1)

texts = {}
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
        continue
    if path.suffix.lower() in {".pdf", ".png", ".jpg", ".jpeg", ".zip"}:
        errors.append(f"Unexpected source/binary asset: {path.relative_to(ROOT)}")
        continue
    if path.suffix in {".md", ".json", ".cff", ".bib", ".py"}:
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeError:
            errors.append(f"Invalid UTF-8: {path.relative_to(ROOT)}")
            continue
        require(bool(content.strip()), f"Empty content: {path.relative_to(ROOT)}")
        require(not any(ord(c) < 32 and c not in "\n\r\t" for c in content),
                f"Control character: {path.relative_to(ROOT)}")
        require("\ufffd" not in content, f"Replacement character: {path.relative_to(ROOT)}")
        if path.suffix == ".md":
            texts[path.resolve()] = content
            require("Private integration note" not in content,
                    f"Private draft marker: {path.relative_to(ROOT)}")
            require("oaiusercontent" not in content and "libfile_" not in content,
                    f"Private transfer identifier: {path.relative_to(ROOT)}")
            require(content.count("```") % 2 == 0,
                    f"Unbalanced code fences: {path.relative_to(ROOT)}")

links_checked = 0
for path, content in texts.items():
    for match in re.finditer(r"!?\[[^\]\n]+\]\(([^\s)]+)\)", content):
        target = match.group(1).strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme in {"https", "http", "mailto"}:
            if parsed.netloc == "arxiv.org" and parsed.path.startswith("/pdf/"):
                require(parsed.path == "/pdf/2610.12176v1", f"Unpinned PDF: {target}")
                if parsed.fragment:
                    require(bool(re.fullmatch(r"page=([1-9]|[12][0-9]|3[0-9])", parsed.fragment)),
                            f"Invalid source page: {target}")
            continue
        require(not parsed.scheme, f"Unsupported link: {target}")
        linked_path = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        require(linked_path.is_relative_to(ROOT), f"Link leaves repository: {target}")
        require(linked_path.is_file(), f"Broken link in {path.name}: {target}")
        if parsed.fragment and linked_path in texts:
            require(unquote(parsed.fragment) in heading_ids(texts[linked_path]),
                    f"Broken anchor in {path.name}: {target}")
        links_checked += 1

paper = json.loads((ROOT / "metadata/paper.json").read_text(encoding="utf-8"))
results = json.loads((ROOT / "metadata/results.json").read_text(encoding="utf-8"))
claims = json.loads((ROOT / "metadata/claims.json").read_text(encoding="utf-8"))
require(paper["arxiv"]["versioned_id"] == "2610.12176v1", "Wrong paper version")
require(paper["pages"] == 39, "Wrong page count")
require(len(paper["authors"]) == 7, "Wrong author count")
require(paper["license"]["spdx"] == "CC-BY-4.0", "Wrong source licence")
require(not paper["companion"]["experiments_reproduced"], "Unsupported reproduction flag")
require(not paper["companion"]["source_assets_redistributed"], "Wrong redistribution flag")
require(not paper["verification"]["attachment_comparison"]["byte_equality_verified"],
        "Unsupported attachment byte-equality claim")
require(bool(re.fullmatch(r"[0-9a-f]{64}", paper["verification"]["public_pdf"]["sha256"])),
        "Invalid source SHA-256")

bib = (ROOT / "references/paper.bib").read_text(encoding="utf-8")
cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
preferred = cff.split("preferred-citation:", 1)[1]
for author in paper["authors"]:
    require(f'{author["family"]}, {author["given"]}' in bib,
            f"BibTeX missing author: {author['name']}")
    require(f'given-names: "{author["given"]}"' in preferred and
            f'family-names: "{author["family"]}"' in preferred,
            f"CFF missing author: {author['name']}")
    require(author["name"] in texts[ROOT / "README.md"],
            f"README missing author: {author['name']}")
require("0xHayd3n" not in preferred and "Hayden" not in preferred,
        "Companion maintainer incorrectly in paper citation")
require("2610.12176v1" in bib and "2610.12176v1" in preferred, "Citation version missing")

for item in (results, claims):
    require(item["paper_version"] == paper["arxiv"]["versioned_id"], "Metadata version mismatch")
require(len(results["public_benchmarks"]) == 6, "Wrong public benchmark count")
mlr = next(b for b in results["public_benchmarks"] if b["name"] == "MLR-Bench")
require(mlr["tasks_per_trial"] == 12 and mlr["trials"] == 5, "MLR v1 appendix scope mismatch")
require(mlr["scores"]["L2"]["mean"] == 2.40, "MLR v1 result mismatch")
for scope in results["private_first_cycle"].values():
    if isinstance(scope, dict) and "wins" in scope:
        require(round(100 * scope["wins"] / (scope["wins"] + scope["losses"]), 1)
                == scope["win_share_percent"], "Private win-share arithmetic mismatch")
ids = [claim["id"] for claim in claims["claims"]]
require(len(ids) == len(set(ids)), "Duplicate claim ID")
for claim in claims["claims"]:
    require(bool(claim["qualifications"]), f"Missing qualifications: {claim['id']}")
    require((ROOT / claim["note"]).is_file(), f"Broken claim note: {claim['id']}")
    source = claim["source"]
    pages = source.get("pdf_pages", [source.get("pdf_page")])
    require(all(isinstance(page, int) and 1 <= page <= 39 for page in pages),
            f"Invalid claim source pages: {claim['id']}")

if errors:
    print("Documentation checks FAILED:")
    print("\n".join(f"- {message}" for message in errors))
    sys.exit(1)
print(f"PASS: {len(texts)} Markdown files, {links_checked} local links/anchors, "
      f"3 JSON records, citation authors/version, 6 benchmarks, and {len(ids)} qualified claims.")
print("These checks validate documentation integrity, not research reproduction.")
