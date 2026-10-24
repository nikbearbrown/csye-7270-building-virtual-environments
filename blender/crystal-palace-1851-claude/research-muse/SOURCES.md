# Sources

Everything in this folder traces to one of the sources below. The
scraper (`scripts/scrape_crystal_palace.py`) records, for every image,
its source page, file page, direct URL, licence and artist in
`data/*.csv` — check there before re-using any file.

## Primary seed

- **Wikipedia — “The Crystal Palace”**
  https://en.wikipedia.org/wiki/The_Crystal_Palace
  Seed for the whole scrape: its images were all downloaded
  (`images/seed/`), its outgoing article links define the depth-1 set
  (`data/pages.json`), and its plain text is saved at
  `sources/seed_article.txt` (CC BY-SA, Wikipedia contributors).

## Depth-1 Wikipedia pages

- All 396 articles linked from the seed page were visited and the
  images on them counted (7,003 unique files). The per-file metadata
  inventory (`data/images_depth1_all.csv`) is **empty in this commit**:
  en.wikipedia.org became unreachable mid-fetch — see the ⚠ note in
  `README.md`; re-running the scraper completes it. Images were
  downloaded (`images/linked/`) only from pages classified as
  architecturally/historically relevant to the palace (see
  `is_relevant()` in the scraper and the `relevant` flag in
  `data/pages.json`).

## Wikimedia Commons

- Category tree rooted at Category:Crystal Palace and the building /
  exhibition subcategories (Crystal Palace in Hyde Park; Crystal
  Palace in art; Great Exhibition; Crystal Palace Park; Crystal
  Palace Dinosaurs; …), pruned of neighbourhood geography
  (streets, pubs, stations). Every file inventoried in
  `data/images_commons_all.csv`; plans, sections, elevations,
  diagrams, drawings, plates and engravings downloaded to
  `images/commons/`.
- Start browsing: https://commons.wikimedia.org/wiki/Category:Crystal_Palace

## The working drawings (primary blueprint source)

- Charles Downes, *The Building Erected in Hyde Park for the Great
  Exhibition of the Works of Industry of All Nations, 1851*
  (London: John Weale, 1852). 28 large plates — plans, elevations,
  sections and details — “laid down to a large scale from the working
  drawings of the contractors, Messrs. Fox, Henderson, and Co.”
- McGill University Library scan, Internet Archive:
  https://archive.org/details/McGillLibrary-rbsc_building-erected-hyde-park_folioNA6750L6D71852-21979
  - Full metadata saved: `data/internet_archive_downes1852_metadata.json`
  - OCR text saved: `sources/downes_1852_ocr.txt`
  - PDF (371 MB): https://archive.org/download/McGillLibrary-rbsc_building-erected-hyde-park_folioNA6750L6D71852-21979/rbsc_building-erected-hyde-park_folioNA6750L6D71852.pdf
  - Per-page JP2 zip (110 MB): https://archive.org/download/McGillLibrary-rbsc_building-erected-hyde-park_folioNA6750L6D71852-21979/rbsc_building-erected-hyde-park_folioNA6750L6D71852_jp2.zip
  - Linked, not committed to git (file-size). Plates VI and XV are the
    two plates the model in this folder was dimension-checked against.

## Further primary / institutional sources (indexed, not scraped)

Inventoried in `data/internet_archive_items.json` (≈50 Internet
Archive texts matching “crystal palace”), plus:

- **V&A Museum** — Paxton's original blotting-paper sketch and the
  submitted perspective drawing (object D.29-1905):
  https://collections.vam.ac.uk/item/O18166/original-sketch-of-the-great-exhibition-building-architectural-rendering-paxton-joseph-sir/
- **Encyclopædia Britannica** — “Crystal Palace” entry (headline
  dimensions cross-checked against Wikipedia in `ARCHITECTURE.md`):
  https://www.britannica.com/topic/Crystal-Palace-building-London
- **Historic England / RIBA / London Metropolitan Archives** hold
  further photographs and drawings; their catalogues are the next
  places to look for Sydenham-era material. Not scraped here
  (catalogue images are not openly licensed for redistribution).

## Licence note

Most 1851–1936 imagery here is public domain. Modern photographs
(Sydenham site today, the dinosaurs, the park) carry individual
Creative Commons licences — the per-file licence, artist and credit
are in the CSVs. The scrape itself (code) was written by Muse for
this course repo; the data files are indexes of the sources above.
