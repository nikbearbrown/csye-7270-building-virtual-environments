#!/usr/bin/env python3
"""
scrape_crystal_palace.py — Crystal Palace (1851 / Sydenham) reference scraper

Written for Bear / CSYE 7270 Building Virtual Environments.
Target folder in the course repo:
    blender/crystal-palace-1851-claude/research-muse/

What it does
------------
1. SEED — en.wikipedia.org/wiki/The_Crystal_Palace
   * full article text (plain-text extract), outgoing article links,
     and every image used on the page, with MediaWiki imageinfo
     (direct URL, size, MIME, SHA-1, licence, artist, description).
2. DEPTH 1 — every article the seed page links to (396 at first run).
   * every image on each of those pages is *inventoried* (metadata only
     in data/images_depth1_all.csv/.json, with a direct URL, so any file
     can be fetched later with one click).
   * pages classified as architecturally / historically relevant
     (keyword + allow-list test in `is_relevant()`) have their images
     *downloaded* as well.
3. COMMONS — Wikimedia Commons category tree starting at
   Category:Crystal Palace (files + subcategories, recursive).
   * every file is inventoried; files whose titles mark them as
     plans / sections / elevations / diagrams / drawings / plates —
     and every file in a plans/drawings subcategory — are downloaded.
4. DOWNLOADS are de-duplicated by SHA-1, saved under images/<tier>/,
   at original resolution where the original is <= 10 MB, otherwise
   the largest Wikimedia thumbnail <= 2560 px wide. (GitHub-friendly:
   this is a reference set, not an archive of record — the CSVs carry
   the original URLs.)

Outputs (under --out, default ./research-muse)
----------------------------------------------
    data/architectural_data.json   curated headline facts + sources
    data/pages.json                  seed + depth-1 pages visited
    data/images_seed.json/.csv     every image on the seed page
    data/images_depth1_all.json/.csv   every image on every linked page
    data/images_commons_all.json/.csv  every file in the Commons tree
    data/downloads.json/.csv       what was actually downloaded, and where
    data/failures.json             anything that failed, with the error
    images/seed/  images/linked/  images/commons/
    sources/seed_article.txt       plain text of the seed article

Politeness: descriptive User-Agent, small delay between requests,
no login, public APIs only (MediaWiki Action API).

Usage
-----
    python3 scrape_crystal_palace.py --out ./research-muse
    python3 scrape_crystal_palace.py --out ./research-muse --no-download
    python3 scrape_crystal_palace.py --out ./research-muse --max-linked-pages 50

Licences: Wikimedia file licences are recorded per-file in the CSV/JSON
(extmetadata). Most Crystal Palace imagery is public domain (pre-1936
photographs, 1850s engravings and plates); check the licence column
before re-using any modern photograph.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

EN_API = "https://en.wikipedia.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "MuseCrystalPalaceScraper/1.0 (CSYE 7270 coursework; educational research)"}
SEED_TITLE = "The Crystal Palace"
DELAY = 0.12  # seconds between API calls
MAX_ORIGINAL_BYTES = 10 * 1024 * 1024
# Site furniture that turns up on relevant pages but is not content:
SKIP_DOWNLOAD_RE = re.compile(
    r"(oojs|commons-logo|wikimedia|wikipedia.*logo|question_book|"
    r"disambig|ambox|padlock|crystal_clear|edit-clear|symbol_support|"
    r"flag_of_|_icon_|icon_)", re.I)

# ---------------------------------------------------------------- relevant?
# A depth-1 page is "relevant" (its images get downloaded, not just
# inventoried) if its title hits one of these keywords, or is allow-listed.
RELEVANT_KEYWORDS = [
    "crystal palace", "great exhibition", "paxton", "sydenham", "hyde park",
    "chatsworth", "conservatory", "glasshouse", "greenhouse", "palm house",
    "kew", "cast iron", "plate glass", "curtain wall", "exhibition",
    "owen jones", "fox, henderson", "charles fox", "chance brothers",
    "penge", "dinosaurs", "waterhouse hawkins", "festival of empire",
    "imperial war museum", "national sports centre", "glaspalast",
    "garden palace", "alexandra palace", "new york crystal",
    "lily house", "great stove", "victoria amazonica", "prefabricat",
    "iron and glass", "transept", "nave",
]
RELEVANT_TITLES = {
    "Joseph Paxton", "Great Exhibition", "Crystal Palace Park",
    "Crystal Palace Dinosaurs", "Crystal Palace, London", "Owen Jones (architect)",
    "Charles Fox (engineer, born 1810)", "Fox, Henderson and Co.",
    "Chance Brothers", "Chatsworth House", "Benjamin Waterhouse Hawkins",
    "Festival of Empire", "Sydenham Hill", "Penge", "Upper Norwood",
    "Cast iron", "Curtain wall (architecture)", "Isambard Kingdom Brunel",
}

PLAN_KEYWORDS = [
    "plan", "section", "elevation", "diagram", "drawing", "plate",
    "blueprint", "floor plan", "layout", "map of", "sketch", "engraving",
    "lithograph", "transept", "nave", "girder", "column", "construction",
]

SKIP_TITLES = {"File:Commons-logo.svg"}  # site furniture, not content
DROPPED_BATCHES: list = []  # imageinfo batches lost to network drops


def is_relevant(title: str) -> bool:
    if title in RELEVANT_TITLES:
        return True
    t = title.lower()
    return any(k in t for k in RELEVANT_KEYWORDS)


def is_plan(title: str) -> bool:
    t = title.lower()
    return any(k in t for k in PLAN_KEYWORDS)


# ---------------------------------------------------------------- API helpers
def api(api_url: str, params: dict) -> dict:
    """One MediaWiki API call, with retries: the VM's egress proxy
    intermittently times out on the CONNECT tunnel (observed 2026-10-23:
    a run died on its first call and another stalled for minutes), so a
    bare urlopen is not reliable enough for a ~1,000-call scrape."""
    params = dict(params)
    params["format"] = "json"
    url = api_url + "?" + urllib.parse.urlencode(params)
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))
    raise last  # type: ignore[misc]


def paginate(api_url: str, params: dict, page_key: str) -> list:
    """Follow MediaWiki continuation for a per-page list property."""
    out, cont = [], {}
    while True:
        p = dict(params)
        p.update(cont)
        d = api(api_url, p)
        for pg in d.get("query", {}).get("pages", {}).values():
            if "missing" in pg:
                continue
            out.extend(pg.get(page_key, []))
        if "continue" in d:
            cont = d["continue"]
            time.sleep(DELAY)
        else:
            return out


def page_images(api_url: str, title: str) -> list:
    return paginate(api_url,
                    {"action": "query", "titles": title, "prop": "images",
                     "imlimit": "500"},
                    "images")


def page_links(title: str) -> list:
    return paginate(EN_API,
                    {"action": "query", "titles": title, "prop": "links",
                     "plnamespace": "0", "pllimit": "500"},
                    "links")


def image_info(api_url: str, file_titles: list, full: bool = True) -> dict:
    """Batch imageinfo lookup (50 titles per call). Returns title -> info.

    full=False fetches only url|size|mime|sha1 (no extmetadata): payloads
    are ~20x smaller, which matters when inventorying thousands of files.
    Licence/artist/description are then enriched only for files that are
    actually downloaded. (First version fetched extmetadata for all
    7,003 depth-1 files and stalled — measured, not guessed.)"""
    info = {}
    for i in range(0, len(file_titles), 50):
        batch = file_titles[i:i + 50]
        try:
            d = api(api_url,
                    {"action": "query", "titles": "|".join(batch),
                     "prop": "imageinfo",
                     "iiprop": "url|size|mime|sha1" + ("|extmetadata" if full else ""),
                     "iiurlwidth": "2560"})
        except Exception as e:  # noqa: BLE001
            # Batch-failure tolerant: the egress proxy drops out in
            # bursts (observed repeatedly 2026-10-23); losing one batch
            # of 50 must not lose the other ~7,000 files with it.
            print(f"    imageinfo batch at {i} failed ({e}); continuing",
                  flush=True)
            DROPPED_BATCHES.append({"at": i, "titles": batch, "error": str(e)})
            continue
        for pg in d.get("query", {}).get("pages", {}).values():
            ii = (pg.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata") or {}
            def v(k):
                return (em.get(k) or {}).get("value", "")
            info[pg["title"]] = {
                "file_title": pg["title"],
                "url": ii.get("url", ""),
                "thumb_url": ii.get("thumburl", ""),
                "description_url": ii.get("descriptionurl", ""),
                "width": ii.get("width", ""),
                "height": ii.get("height", ""),
                "size_bytes": ii.get("size", ""),
                "mime": ii.get("mime", ""),
                "sha1": ii.get("sha1", ""),
                "license": re.sub("<[^>]+>", "", v("LicenseShortName")),
                "artist": re.sub("<[^>]+>", "", v("Artist"))[:300],
                "credit": re.sub("<[^>]+>", "", v("Credit"))[:300],
                "description": re.sub("<[^>]+>", "", v("ImageDescription"))[:500],
            }
        if (i // 50) % 20 == 19:
            print(f"    imageinfo: {i + 50}/{len(file_titles)}", flush=True)
        time.sleep(DELAY)
    return info


def safe_name(file_title: str) -> str:
    name = file_title.replace("File:", "")
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    return name[:180] or "file"


# ---------------------------------------------------------------- download
def download(url: str, dest: str, failures: list, label: str) -> bool:
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return True
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
                while True:
                    chunk = r.read(1 << 16)
                    if not chunk:
                        break
                    f.write(chunk)
            return True
        except Exception as e:  # noqa: BLE001
            last = e
            if os.path.exists(dest):
                os.remove(dest)
            time.sleep(2 * (attempt + 1))
    failures.append({"item": label, "url": url, "error": str(last)})
    return False


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--out", default="./research-muse")
    ap.add_argument("--no-download", action="store_true",
                    help="inventory only, download nothing")
    ap.add_argument("--max-linked-pages", type=int, default=0,
                    help="0 = all depth-1 pages")
    args = ap.parse_args()

    out = args.out
    data_dir = os.path.join(out, "data")
    src_dir = os.path.join(out, "sources")
    for d in (data_dir, src_dir,
              os.path.join(out, "images", "seed"),
              os.path.join(out, "images", "linked"),
              os.path.join(out, "images", "commons")):
        os.makedirs(d, exist_ok=True)

    failures: list = []
    downloads: list = []
    seen_sha1: dict = {}

    def save_rows(name: str, rows: list):
        """Checkpoint writer: each phase saves its data as soon as it
        finishes (and Commons after every category), so a VM restart
        mid-scrape loses minutes, not the whole run."""
        with open(os.path.join(data_dir, name + ".json"), "w") as f:
            json.dump(rows, f, indent=1, ensure_ascii=False)
        # Always write the CSV, even for zero rows (a header-only file):
        # an interrupted phase must leave an honest empty file in the
        # repo, not a missing one the README then falsely points to.
        keys = sorted({k for r in rows for k in r}) or [
            "file_title", "source_page", "url", "thumb_url",
            "description_url", "width", "height", "size_bytes", "mime",
            "sha1", "license", "artist", "credit", "description"]
        with open(os.path.join(data_dir, name + ".csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, "") for k in keys})

    def record_download(rec: dict, tier: str):
        """Download one image record (deduped by sha1) and log it."""
        if args.no_download:
            return
        if tier != "seed" and SKIP_DOWNLOAD_RE.search(rec["file_title"]):
            return  # inventoried, but site furniture — not downloaded
        if tier != "seed" and (rec.get("mime") == "application/pdf"
                               or rec["file_title"].lower().endswith(".pdf")):
            return  # book PDFs: inventoried with URLs, not committed to git
            # (mime alone missed one: a Commons book PDF whose light
            # imageinfo came back without a usable mime — check both.)
        sha = rec.get("sha1") or rec["file_title"]
        if sha in seen_sha1:
            downloads.append({**rec, "tier": tier,
                              "local_path": seen_sha1[sha],
                              "note": "duplicate sha1, not re-downloaded"})
            return
        # pick source: original unless huge, else the <=2560px thumb
        url = rec["url"]
        if rec.get("size_bytes") and int(rec["size_bytes"]) > MAX_ORIGINAL_BYTES \
                and rec.get("thumb_url"):
            url = rec["thumb_url"]
        sub = {"seed": "images/seed", "linked": "images/linked",
               "commons": "images/commons"}[tier]
        dest = os.path.join(out, sub, safe_name(rec["file_title"]))
        if download(url, dest, failures, rec["file_title"]):
            rel = os.path.relpath(dest, out)
            seen_sha1[sha] = rel
            downloads.append({**rec, "tier": tier, "local_path": rel,
                              "downloaded_from": url, "note": ""})
            print(f"  got [{tier}] {rec['file_title']}", flush=True)
        time.sleep(DELAY)

    # ---------------------------------------------------------- 1. seed page
    print(f"[1/4] Seed page: {SEED_TITLE}", flush=True)
    d = api(EN_API, {"action": "query", "titles": SEED_TITLE,
                     "prop": "extracts|info", "explaintext": "1",
                     "inprop": "url"})
    page = next(iter(d["query"]["pages"].values()))
    extract = page.get("extract", "")
    with open(os.path.join(src_dir, "seed_article.txt"), "w") as f:
        f.write(extract)

    seed_imgs = [i for i in page_images(EN_API, SEED_TITLE)
                 if i["title"] not in SKIP_TITLES
                 and not i["title"].endswith("OOjs UI icon edit-ltr-progressive.svg")]
    seed_info = image_info(EN_API, [i["title"] for i in seed_imgs])
    seed_records = [seed_info[i["title"]] for i in seed_imgs if i["title"] in seed_info]
    for r in seed_records:
        r["source_page"] = SEED_TITLE
        record_download(r, "seed")
    save_rows("images_seed", seed_records)
    print(f"  seed images: {len(seed_records)}", flush=True)

    # ---------------------------------------------------------- 2. depth-1
    print("[2/4] Depth-1 linked pages", flush=True)
    links = page_links(SEED_TITLE)
    link_titles = [l["title"] for l in links]
    if args.max_linked_pages:
        link_titles = link_titles[:args.max_linked_pages]
    pages_index = [{"title": SEED_TITLE, "depth": 0, "relevant": True,
                    "url": page.get("fullurl", "")}]
    for title in link_titles:
        pages_index.append({
            "title": title, "depth": 1, "relevant": is_relevant(title),
            "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))})
    # Batch: prop=images accepts up to 50 titles per API call — collecting
    # page-by-page took ~50x as many calls. First pass collects the file
    # titles used on each page; imageinfo is then fetched once, globally,
    # de-duplicated by file title.
    page_files: dict = {}
    for i in range(0, len(link_titles), 50):
        batch = link_titles[i:i + 50]
        cont = {}
        while True:
            p = {"action": "query", "titles": "|".join(batch),
                 "prop": "images", "imlimit": "500"}
            p.update(cont)
            try:
                d = api(EN_API, p)
            except Exception as e:  # noqa: BLE001
                failures.append({"item": f"images-batch:{i}", "error": str(e)})
                d = {}
            for pg in d.get("query", {}).get("pages", {}).values():
                if "missing" in pg:
                    continue
                page_files.setdefault(pg["title"], []).extend(
                    im["title"] for im in pg.get("images", []))
            if "continue" in d:
                cont = d["continue"]
                time.sleep(DELAY)
            else:
                break
        print(f"  ... {min(i + 50, len(link_titles))}/{len(link_titles)} pages scanned",
              flush=True)
    all_files = sorted({t for ts in page_files.values() for t in ts})
    print(f"  unique depth-1 files: {len(all_files)} — fetching imageinfo (light)",
          flush=True)
    try:
        info_all = image_info(EN_API, all_files, full=False)
    except Exception as e:  # noqa: BLE001
        failures.append({"item": "imageinfo-depth1", "error": str(e)})
        info_all = {}
    # Enrich (licence/artist/description) only for files on relevant pages —
    # those are the ones downloaded, and the ones a reader will re-use.
    relevant_files = sorted({ft for t in link_titles if is_relevant(t)
                             for ft in page_files.get(t, [])})
    print(f"  enriching {len(relevant_files)} relevant files", flush=True)
    try:
        info_full = image_info(EN_API, relevant_files, full=True)
        for t, rec in info_full.items():
            if t in info_all:
                info_all[t].update(rec)
    except Exception as e:  # noqa: BLE001
        failures.append({"item": "imageinfo-depth1-enrich", "error": str(e)})
    depth1_records: list = []
    for title in link_titles:
        rel = is_relevant(title)
        for ft in page_files.get(title, []):
            if ft not in info_all:
                continue
            rec = dict(info_all[ft])
            rec["source_page"] = title
            rec["source_page_relevant"] = rel
            depth1_records.append(rec)
            if rel:
                record_download(rec, "linked")
    save_rows("images_depth1_all", depth1_records)
    save_rows("downloads", downloads)
    with open(os.path.join(data_dir, "pages.json"), "w") as f:
        json.dump(pages_index, f, indent=1, ensure_ascii=False)
    print(f"  depth-1: {len(link_titles)} pages, "
          f"{len(depth1_records)} image uses inventoried", flush=True)

    # ---------------------------------------------------------- 3. Commons tree
    # Category:Crystal Palace on Commons is the *neighbourhood* category
    # (streets, pubs, stations) — the building lives in its own subcats.
    # Roots are curated, and recursion only follows subcategories whose
    # titles still name the palace / the exhibition, pruning geography.
    print("[3/4] Wikimedia Commons category tree", flush=True)
    commons_records: list = []
    commons_roots = [
        "Category:Crystal Palace",
        "Category:Crystal Palace in Hyde Park",
        "Category:Crystal Palace in art",
        "Category:Crystal Palace in art (Hyde Park)",
        "Category:Crystal Palace in art (Sydenham)",
        "Category:Great Exhibition",
        "Category:Crystal Palace Park",
        "Category:Crystal Palace Dinosaurs",
        "Category:Exhibition of the works of industry of all nations 1851",
    ]
    prune_words = ["railway", "transmitter", "pubs", "football",
                   "road,", "street", " hill, london", "ward"]

    def followable(cat_title: str) -> bool:
        t = cat_title.lower()
        if any(w in t for w in prune_words):
            return False
        return ("crystal palace" in t or "great exhibition" in t
                or "works of industry" in t)
    cats_seen, cats_queue = set(), list(commons_roots)
    while cats_queue:
        cat = cats_queue.pop(0)
        if cat in cats_seen:
            continue
        cats_seen.add(cat)
        # categorymembers is a list= query, not a per-page prop: call directly
        cont = {}
        while True:
            p = {"action": "query", "list": "categorymembers",
                 "cmtitle": cat, "cmtype": "subcat", "cmlimit": "500"}
            p.update(cont)
            try:
                dd = api(COMMONS_API, p)
            except Exception as e:  # noqa: BLE001
                failures.append({"item": f"commons-subcats:{cat}", "error": str(e)})
                dd = {}
            for m in dd.get("query", {}).get("categorymembers", []):
                if m["title"] not in cats_seen and followable(m["title"]):
                    cats_queue.append(m["title"])
            if "continue" in dd:
                cont = dd["continue"]
            else:
                break
        cont = {}
        file_titles = []
        while True:
            p = {"action": "query", "list": "categorymembers",
                 "cmtitle": cat, "cmtype": "file", "cmlimit": "500"}
            p.update(cont)
            try:
                dd = api(COMMONS_API, p)
            except Exception as e:  # noqa: BLE001
                failures.append({"item": f"commons-files:{cat}", "error": str(e)})
                dd = {}
            file_titles += [m["title"] for m in
                            dd.get("query", {}).get("categorymembers", [])]
            if "continue" in dd:
                cont = dd["continue"]
            else:
                break
        if file_titles:
            try:
                info = image_info(COMMONS_API, file_titles, full=False)
            except Exception as e:  # noqa: BLE001
                failures.append({"item": f"commons-info:{cat}", "error": str(e)})
                info = {}
            plan_titles = [t for t in file_titles
                           if is_plan(t) or "plan" in cat.lower()
                           or "drawing" in cat.lower()]
            if plan_titles:
                try:
                    full = image_info(COMMONS_API, plan_titles, full=True)
                    for t, rec in full.items():
                        if t in info:
                            info[t].update(rec)
                except Exception as e:  # noqa: BLE001
                    failures.append({"item": f"commons-enrich:{cat}", "error": str(e)})
            for t in file_titles:
                if t not in info:
                    continue
                rec = dict(info[t])
                rec["source_page"] = cat
                rec["is_plan_or_drawing"] = t in plan_titles
                commons_records.append(rec)
                if rec["is_plan_or_drawing"]:
                    record_download(rec, "commons")
        save_rows("images_commons_all", commons_records)
        save_rows("downloads", downloads)
        print(f"  commons: {cat} (+{len(file_titles)} files, "
              f"queue {len(cats_queue)})", flush=True)
        time.sleep(DELAY)
    print(f"  commons total: {len(commons_records)} files in "
          f"{len(cats_seen)} categories", flush=True)

    # ------------------------------------------- 3b. Internet Archive (Downes)
    # Charles Downes (1852), *The Building Erected in Hyde Park...* —
    # 28 plates from Fox, Henderson & Co.'s working drawings: the primary
    # blueprint source for the 1851 building (McGill Library scan).
    # The PDF is 371 MB and the JP2 zip 110 MB, so we inventory the item,
    # save its full metadata + OCR text, and link the big files instead
    # of committing them to git.
    print("[3b] Internet Archive: Downes 1852 + item search", flush=True)
    ia_id = "McGillLibrary-rbsc_building-erected-hyde-park_folioNA6750L6D71852-21979"
    ia_items: list = []
    try:
        req = urllib.request.Request(
            f"https://archive.org/metadata/{ia_id}", headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            ia_meta = json.load(r)
        with open(os.path.join(data_dir, "internet_archive_downes1852_metadata.json"), "w") as f:
            json.dump(ia_meta, f, indent=1)
        ia_items.append({
            "identifier": ia_id,
            "title": (ia_meta.get("metadata") or {}).get("title", ""),
            "item_url": f"https://archive.org/details/{ia_id}",
            "pdf_url": f"https://archive.org/download/{ia_id}/rbsc_building-erected-hyde-park_folioNA6750L6D71852.pdf",
            "jp2_zip_url": f"https://archive.org/download/{ia_id}/rbsc_building-erected-hyde-park_folioNA6750L6D71852_jp2.zip",
            "note": "28 plates: plans, elevations, sections, details, from the contractors' working drawings. PDF 371 MB / JP2 zip 110 MB — linked, not committed.",
        })
        if not args.no_download:
            txt_url = f"https://archive.org/download/{ia_id}/rbsc_building-erected-hyde-park_folioNA6750L6D71852_djvu.txt"
            download(txt_url, os.path.join(src_dir, "downes_1852_ocr.txt"),
                     failures, "downes1852-djvu.txt")
    except Exception as e:  # noqa: BLE001
        failures.append({"item": "ia-downes1852", "error": str(e)})
    try:
        q = urllib.parse.urlencode({
            "q": '"crystal palace" AND mediatype:texts',
            "fl[]": "identifier", "rows": 50, "output": "json"})
        # urlencode collapses repeated fl[] keys; build manually instead
        q = ('q=%22crystal+palace%22+AND+mediatype%3Atexts'
             '&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=creator'
             '&fl%5B%5D=date&rows=50&output=json')
        req = urllib.request.Request(
            f"https://archive.org/advancedsearch.php?{q}", headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            ia_search = json.load(r)
        for doc in ia_search.get("response", {}).get("docs", []):
            ia_items.append({
                "identifier": doc.get("identifier", ""),
                "title": doc.get("title", ""),
                "creator": doc.get("creator", ""),
                "date": doc.get("date", ""),
                "item_url": "https://archive.org/details/" + doc.get("identifier", ""),
            })
    except Exception as e:  # noqa: BLE001
        failures.append({"item": "ia-search", "error": str(e)})
    with open(os.path.join(data_dir, "internet_archive_items.json"), "w") as f:
        json.dump(ia_items, f, indent=1, ensure_ascii=False)
    print(f"  IA items inventoried: {len(ia_items)}", flush=True)

    # ---------------------------------------------------------- 4. write data
    print("[4/4] Writing data files", flush=True)
    for db in DROPPED_BATCHES:
        failures.append({"item": "imageinfo-batch-dropped",
                         "at": db["at"], "n_titles": len(db["titles"]),
                         "error": db["error"]})

    def dump(name: str, rows: list):
        with open(os.path.join(data_dir, name + ".json"), "w") as f:
            json.dump(rows, f, indent=1, ensure_ascii=False)
        keys = sorted({k for r in rows for k in r}) or [
            "file_title", "source_page", "url", "thumb_url",
            "description_url", "width", "height", "size_bytes", "mime",
            "sha1", "license", "artist", "credit", "description"]
        with open(os.path.join(data_dir, name + ".csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, "") for k in keys})

    dump("images_seed", seed_records)
    dump("images_depth1_all", depth1_records)
    dump("images_commons_all", commons_records)
    dump("downloads", downloads)
    with open(os.path.join(data_dir, "pages.json"), "w") as f:
        json.dump(pages_index, f, indent=1, ensure_ascii=False)
    with open(os.path.join(data_dir, "failures.json"), "w") as f:
        json.dump(failures, f, indent=1, ensure_ascii=False)

    summary = {
        "seed_page": SEED_TITLE,
        "seed_images": len(seed_records),
        "depth1_pages": len(link_titles),
        "depth1_image_uses_inventoried": len(depth1_records),
        "commons_categories": len(cats_seen),
        "commons_files_inventoried": len(commons_records),
        "downloads": len([d for d in downloads if not d.get("note")]),
        "failures": len(failures),
    }
    with open(os.path.join(data_dir, "scrape_summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
