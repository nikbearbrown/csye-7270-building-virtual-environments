# Crystal Palace — reference scrape (Muse)

**What this is:** a research dataset for the Crystal Palace model in
this folder, scraped 2026-10-23 by Muse at Bear's request: every image
on the Wikipedia article, every image on the articles it links to
(inventoried; downloaded for the pages that matter), the Wikimedia
Commons picture library for the building, and the primary blueprint
source — Downes's 1852 plates from the contractors' working drawings.

It is a **starting pile, not a curated archive**: counts below are the
scraper's own output (`data/scrape_summary.json`), file licences are
recorded per file, and known noise is listed honestly at the bottom.

## Start here

- **`ARCHITECTURE.md`** — the one-page data sheet a modeller needs:
  dimensions, the 24 ft module, tiers, girder levels, materials, and
  the figures sources *disagree* on, kept separate.
- **`SOURCES.md`** — where everything came from, incl. the Downes
  1852 plates (PDF/JP2 linked, too big for git).
- **`data/`** — machine-readable indexes (CSV + JSON, same rows).
- **`images/`** — the downloaded files, by tier.
- **`scripts/scrape_crystal_palace.py`** — the scraper itself.
  Re-run it and the dataset refreshes; it checkpoints after every
  phase, de-duplicates by SHA-1, and retries through network drops.

## What was collected

| Set | Count | Downloaded? |
|---|---|---|
| Seed article images (Wikipedia, “The Crystal Palace”) | 30 records, 29 files | yes — `images/seed/` (one title is a duplicate-SHA alias of another) |
| Articles linked from the seed page (depth 1) | 396 pages | inventoried + relevant downloads |
| Image uses on those 396 pages | 10,017 uses (7,003 unique files) | inventoried in `data/images_depth1_all.csv` |
| Image files from relevant linked pages | 630 files | yes — `images/linked/` |
| Wikimedia Commons files in the palace/exhibition category tree | 2,732 files, 73 categories | plans/drawings/engravings only — `images/commons/` (59 files) |
| Internet Archive texts (“crystal palace”) | 51 items | inventoried; Downes OCR text in `sources/` |
| **Total image files in `images/`** | **718 files** | **1.1 GB** |

> **Depth-1 note.** Four imageinfo batches (of ~140) were lost to
> network drops / over-long title lists and are recorded in
> `data/failures.json`; every other file of the 7,003 has full
> metadata below. First push of this folder (2026-10-23) predated
> the depth-1 completion; the completed inventory landed in a
> follow-up commit the same night.

Relevant = the page is about the palace, the exhibition, its people,
its site, its materials or its sibling buildings (Paxton, Chatsworth,
Kew, Chatsworth's Great Conservatory, Chatsworth — see `is_relevant()`
in the scraper and the `relevant` flag in `data/pages.json`). Every
other linked page — all 396 of them, Brunel's railways included — is
in the inventory CSV with direct URLs, so nothing is lost by not
downloading its pictures of railway stations.

## Layout

```
research-muse/
  README.md            this page
  ARCHITECTURE.md      curated architectural data sheet
  SOURCES.md           provenance + the big files linked, not committed
  scripts/
    scrape_crystal_palace.py
  data/
    scrape_summary.json
    pages.json                   seed + all depth-1 pages, relevance flags
    images_seed.csv/.json        every image on the seed article
    images_depth1_all.csv/.json  every image use on every linked page
    images_commons_all.csv/.json every Commons file in the tree
    downloads.csv/.json          what is actually in images/, and its source
    internet_archive_items.json  IA texts, incl. Downes 1852
    internet_archive_downes1852_metadata.json
    failures.json                anything that failed (should be short)
  sources/
    seed_article.txt             full plain text of the seed article
    downes_1852_ocr.txt          OCR of Downes's plates volume
  images/
    seed/      linked/      commons/
```

## Honest notes / known noise

- A handful of seed-article files are only loosely “of the palace”
  (an 1851 exhibition medal, the Sydenham dinosaurs, a Perth
  namesake) — they were on the article, so they are in `seed/`,
  labelled by their source page in the CSV.
- Downloads are capped at 10 MB per file; larger originals are saved
  as the ≤2560 px Wikimedia thumbnail and the CSV keeps the original
  URL. Book PDFs from Commons are inventoried, never downloaded.
- Site furniture (logos, icons, flags) is inventoried but filtered
  out of the downloads.
- Hyde Park (1851) and Sydenham (1854–1936) material is mixed in the
  sources themselves; the `description` column in the CSVs is the
  quickest way to separate them.

Collected by Muse (Muse Spark), 2026-10-23, for CSYE 7270.
Human review: Professor Bear — pending.
