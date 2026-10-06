# Commons authoring guide

Edit `.qmd` source under `site/`. Run `quarto render site` from the repository
root and inspect `site/_site`; never edit that output. `quarto preview site`
watches the project. `bash scripts/serve-built.sh` serves the existing build.

All navbar and course sidebar entries live in `site/_quarto.yml`. Course folders
select their sidebar in `_metadata.yml`. Link to source `.qmd` files; Quarto
resolves the output routes. The inherited `bs-` CSS classes remain the shared
presentation system; Commons styling lives in `commons-overrides.css`.

## Daily slide decks

Follow the canonical [Technology Commons Daily Slide Deck SOP](https://docs.google.com/document/d/1WNEgA-xn0oCiB0sp5rv67_SmsFuHpgxotrgjdXWIwB8/edit)
when creating decks or publishing their links. A Fun Day closes the current
instructional week. The first daily deck after a Fun Day starts a new week, so
use or create the next `Week N` folder and list that day under a new `Week N`
heading on the course slides page.

Lore lists `site/lore/*.qmd`. Give stories a title, description, actual date,
categories, and tags. Follow existing article metadata. Store images under
`site/assets/lore` and preserve source attribution.

NICE's guide and slides live in `site/resources`. Its builder uses a raw HTML
block and separate CSS/JS. The Word export is Word-compatible HTML (`.doc`);
PDF uses browser printing. Entries exist in the page only: export before leaving.

## Glossary

Edit `glossary/glossary.json`, then run `python scripts/commons_glossary.py generate`.
This updates public JSON, `_entries.html`, and lookup JSON. Validation compares
full generated contents. Current Backgammon terms are preserved without links
to the retired lesson corpus. Do not use `learn_glossary.py generate`: Commons
uses its shared parsing/rendering functions through `commons_glossary.py`.

## Verification

After rendering, run `python scripts/check_commons.py --rendered`. It runs all
retained Python and JavaScript tests plus local HTML/CSS link and asset checks.
CI renders and checks the site on pushes to master and pull requests.
For browser checks, install Playwright and Chromium and run
`python scripts/check_commons_browser.py`. Screenshots go to `.tools/review`.

The next phase adds course vocabulary and first-week content. This consolidation
does not add curriculum or build the classroom-openings system.
