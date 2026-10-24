# Crystal Palace — architectural data sheet

Curated from the sources in `SOURCES.md`. Where sources disagree, both
figures are given — do not silently average them. Figures marked
**[Downes]** were read by Claude from Charles Downes's 1852 plates for
the model already in this folder (see `../BUILD_NOTES.md`); figures
marked **[Wiki]** are from the Wikipedia article text saved at
`sources/seed_article.txt`; **[Britannica]** is Encyclopædia Britannica.

## The building, Hyde Park (1851)

| Item | Figure | Source |
|---|---|---|
| Designer | Joseph Paxton (gardener/architect, Chatsworth) | [Wiki][Britannica] |
| Contractors / engineers | Fox, Henderson & Co.; Charles Fox; working drawings are the basis of Downes's plates | [Downes] |
| Decoration / colour scheme | Owen Jones | [Wiki] |
| Glass supplier | Chance Brothers (largest sheet-glass size then made set the module) | [Wiki] |
| Length | 1,851 ft (564 m) **[Wiki lead]** — but 1,848 ft (563 m) **[Britannica]** and 1,848 ft = 77 × 24 ft modules **[Wiki, structure section]** | see note 1 |
| Width (main body) | 408 ft (124 m) | [Britannica][Downes] |
| Width (plan, incl. side aisles as gridded) | 456 ft (139 m) = 19 × 24 ft modules | [Wiki] |
| Height, interior | 128 ft (39 m) | [Wiki lead] |
| Height, central transept (Hyde Park) | 108 ft (33 m) | [Britannica] |
| Floor / exhibition area | 990,000 sq ft (92,000 m²); ground footprint ~18–19 acres (7 ha) | [Wiki][Britannica] |
| Glass | 293,000 panes [Wiki lead]; pane size derived from Chance Brothers' 49 in (124 cm) sheet | [Wiki] |
| Display tables | more than 8 miles (13 km) on ground floor and galleries | [Britannica] |
| Cost (Hyde Park building) | Paxton's submission budgeted £85,800; building cost often quoted ~£150,000–£165,000 — sources differ, check before citing | [Wiki] |
| Construction time | ~39 weeks to complete [Wiki lead]; erection itself often quoted at ~22 weeks plus fitting-out | [Wiki] |

**Note 1 — the length discrepancy is real and worth keeping.** The
1,851 ft figure includes something the 77-bay grid does not (end walls /
measurement to extremes); the model's own bounding box in this folder
shows the same effect: 888 ft between column lines for 37 bays, but a
900.6 ft bounding box once flanges and the floor slab are counted
(`../BUILD_NOTES.md`). State which measure you mean.

## The module — the whole building is one repeated unit

- Basic structural module: a **24 ft × 24 ft (7.3 m) cube** — three
  8 ft × 24 ft roof units side by side on a cast-iron beam grid carried
  by slim cast-iron columns. [Wiki]
- Plan grid as built: **77 modules long × 19 modules wide**. Modules
  could be omitted to form larger courts, or stacked to add the gallery
  floor; every larger space is a multiple of 24 ft. [Wiki]
- Roof unit: a long triangular prism (ridge-and-furrow / ridge-and-
  valley). Paxton set its size from a single pane: the 49 in pane is the
  hypotenuse of a right triangle with base 4 ft (ratio 2.5:1); mirrored,
  it gives the 8 ft gable. The entire roof glazed with identical,
  untrimmed panes. [Wiki]
- Gutter pitch across the width: **8 ft**. **[Downes]**
- Tier widths (stepped cross-section): **408 ft / 264 ft / 120 ft**.
  **[Downes]**
- Girder tops above ground floor: **22′ 2″ / 42′ 2″ / 62′ 2″** for
  tiers 1–3. **[Downes]**
- Gallery floor surface: **22′ 11″** above ground floor. **[Downes]**
- Columns: cast iron, **8 in external diameter** sample shaft; top of
  column 18′ 11¾″; connecting pieces 3′ 4½″ (tier 1); cast-iron girders
  3 ft deep, 23′ 3¼″ face to face over a 24 ft bay. **[Downes]**
- Nave: **72 ft wide**, ~1,800 ft long, spanned with longer trellis
  girders. Avenues: **48 ft**. **[Downes][Wiki]**
- The transept's barrel vault was added to enclose Hyde Park's mature
  elm trees, which could not be felled. [Wiki]

## Materials and systems

- **Cast iron** frame: columns, girders, connecting pieces — prefabricated,
  interchangeable, bolted; the building was a kit of parts.
- **Wrought iron** for longer-span trellis girders (nave roof).
- **Plate glass** walls and roof — the greatest area of glass in any
  building to that date; no interior lighting needed by day.
- **Wood**: Paxton's patented gutter (hollow wooden gutters doubled as
  structural beams and carried rainwater to the columns, which acted
  as downpipes), flooring, sash bars.
- Ventilation / louvres and Owen Jones's colour scheme are part of the
  design but are **not** in the model in this folder yet (see
  `../DEPARTURES-LEDGER.md`).

## Two buildings, not one

1. **Hyde Park, 1851** — as above; opened 1 May 1851 for the Great
   Exhibition (1 May – 15 October 1851, 14,000+ exhibitors, ~6 million
   visitors).
2. **Sydenham (Penge), 1852–54 rebuild** — dismantled, transported and
   re-erected enlarged on Sydenham Hill: central transept raised and
   barrel-vaulted, additional transepts, water towers by Brunel for
   the fountains, gardens by Paxton with the Crystal Palace Dinosaurs
   (Waterhouse Hawkins, 1854). Destroyed by fire **30 November 1936**.

Images in this scrape are labelled by tier/folder, and the metadata
CSV records the source page for each file, so Hyde Park and Sydenham
photographs/engravings can be separated by their file descriptions.

## Primary drawing source

Charles Downes, *The Building Erected in Hyde Park for the Great
Exhibition of the Works of Industry of All Nations, 1851* (London:
John Weale, 1852) — 28 large plates (plans, elevations, sections,
details) drawn from Fox, Henderson & Co.'s working drawings.
McGill University Library scan, Internet Archive item
`McGillLibrary-rbsc_building-erected-hyde-park_folioNA6750L6D71852-21979`
— metadata and OCR text saved under `data/` and `sources/`; the 371 MB
PDF and 110 MB JP2 zip are linked in `SOURCES.md`, not committed.
Plates VI (transverse section) and XV (stair section) are the two
plates the model in this folder was checked against.

## What a modeller still needs (not settled by this scrape)

- Transept barrel-vault geometry (radius, rib spacing) — in Downes's
  plates, not yet extracted as figures.
- End elevations and entrances — Plate images, not yet measured.
- Owen Jones colour scheme specification.
- Sydenham version: dimensionally different building; do not model it
  from Hyde Park figures.
