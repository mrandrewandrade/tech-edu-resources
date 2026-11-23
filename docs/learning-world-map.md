# Technology Commons Learning Worlds

The Learning Worlds map is an optional visual front door for TEJ and TAS. It does not replace Quarto navigation, direct lesson URLs, or site search.

## Teacher editing

Edit `site/assets/learning-map/learning-map.yml`. Each node has:

- a unique `id`, student-facing `title`, `world`, and `region`;
- a `type` (`hub`, `portal`, `lesson`, `project`, `safety`, `portfolio`, or `help`);
- a `status` (`required` or `optional`);
- `x` and `y` coordinates from 0 to 100;
- a site-relative `href` to a real lesson;
- concise `summary`, `do`, and `look_for` text;
- reciprocal `neighbours`, which are the only routes the marker can travel;
- an optional `reference` with a title and HTTPS URL;
- an optional `video` URL. Omit it when no mission video exists. Videos never autoplay.

After editing, run:

```powershell
python scripts/build_learning_map.py
python -m unittest tests.test_learning_map -v
quarto render site/learning-worlds
```

The builder validates the graph, then generates the browser JSON, no-JavaScript lesson list, and printable SVG. Commit the YAML source and all generated files together.

## Student behaviour

- The marker starts at `commons-hub` on a new browser.
- A click, tap, arrow key, or W/A/S/D key moves only to a connected neighbour.
- Space shows details; Enter opens the focused lesson.
- Visited stops are saved only in that browser's `localStorage`.
- Reset clears the visited route. A visit is not mastery, assessment, or a prerequisite.
- On small screens the lesson list opens first. The map remains available as an option.
- With JavaScript unavailable, the generated lesson list provides every destination.

## Visuals and sources

The map and field-guide diagrams are original SVG/CSS drawings. They use standard conventions and cite the authoritative tutorial or open textbook that informed the redraw. Do not paste figures from commercial textbooks such as *Grob's Basic Electronics* unless the school has explicit reuse permission. Use the textbook as a technical cross-check, then create a new classroom diagram and cite it as a reference.

The relay/horn drawing is deliberately conceptual. The capacitor is in a low-current timing stage, while a separate fused 12 V load circuit supplies the horn through correctly rated relay contacts. The actual relay datasheet, horn current, wire size, fuse, terminals, and enclosure control the build.
