# Student tutorial style guide

Use this guide for student tutorials on the Technology Commons site.

## Write for a beginner

Assume the student has never used the tool.

- Use short sentences.
- Use common words.
- Give one action at a time.
- Start steps with a clear verb: **Open**, **Click**, **Choose**, **Type**, **Drag**, or **Save**.
- Explain a new word the first time you use it.
- Tell students what they should see after an action.
- Avoid long background sections before the first useful step.
- Do not use a harder word when a simple word works.

Use **line thickness**, not *visual weight*, unless you explain the term. Use **make both sides even**, not *correct the proportions*, when that is what the student must do.

## Put sections in this order

1. **Learning goals** — two to four short “I can” statements.
2. **Why this is useful** — explain the real reason for learning the skill.
3. **What you will make** — show the finished goal in plain language.
4. **Before you start** — list files, tools, and settings.
5. **Numbered steps** — one small task in each section.
6. **Check your work** — show what success looks like.
7. **Save, export, or submit** — name the files students need.
8. **Common issues** — describe the problem first, then the fix.
9. **Summary** — repeat the main skill and link to the next lesson.

Keep **Learning goals** near the top. Keep **Summary** at the end.

## Use screenshots well

- Use one screenshot for one important stage.
- Crop out the taskbar, other tabs, bookmarks, downloads, and recording controls.
- Keep the tool, canvas, and layer panel visible when they help explain the step.
- Put the screenshot after the action that creates that result.
- Write alt text that says what the student needs to notice.
- Do not use a screenshot when one short sentence is clearer.

## Use visuals before adding more text

When a picture, diagram, map, or example can teach the idea faster, use it and
shorten the surrounding explanation.

- Look for an accurate source visual before writing another paragraph.
- Prefer visuals published by the people, community, artist, or institution
  whose knowledge or work is being discussed.
- Reuse a visual only when its licence or permission allows it. If reuse rights
  are unclear, link to the creator's official page instead of copying the image.
- Credit the creator, community or Nation when known, source, licence, and any
  changes directly beside the visual.
- Do not trace, imitate, or generate work in a living Indigenous artist's style.
  Use a neutral instructional diagram for explanation and direct students to
  the artist's own presentation of the work.
- Give each visual useful alt text. Describe what the learner should notice,
  not every decorative detail.
- Use a short pattern: one-sentence introduction, visual, short caption, then
  only the explanation the visual cannot carry.
- Label reconstructions, interpretations, and classroom-use diagrams clearly.
  Do not present an inferred process as a community's traditional procedure.

## Explain menu steps the same way

Use this form:

> Choose **File > Export as > SVG**.

Use the exact words shown in the program. Put button names, menu names, filenames, and values in bold or code formatting.

## Teach file naming and renaming

When students download or submit files:

- Put the exact required filename beside the save or export step.
- Make every submitted filename begin with the student's number, followed by the student's last name.
- Use the pattern `studentnumber-lastname-project.filetype`.
- Give one fake example, such as `123456789-Smith-logo.svg`.
- Remind students to keep the file ending, such as `.psd`, `.png`, or `.svg`.
- Include the shared Chromebook, Windows, and Linux renaming help from `site/design-fabrication/logo-design/_rename-downloaded-file.qmd`.

## Show the course path

The main beginner path is:

1. **N.I.C.E. Design Process** — find a need, make an idea, test it, and improve it.
2. **Photopea Lesson 1** — build the 11 × 4 inch nameplate text and leave a 4 × 4 inch logo space.
3. **Photopea Lesson 2** — turn a rough sketch into clean editable vector lines.
4. **Photopea Lesson 3** — combine the logo and nameplate, then export PSD, PNG, and SVG files.
5. **Raster, Vector, and SVG** — learn how image files work and choose the right type.
6. **Animation** — use the same design idea across frames and time.
7. **Name Tag Laser Cutting** — use the finished digital files to make a real object.

The name tag begins the fabrication section. It is not another graphics lesson. It uses the digital-design skills students already learned.

## Put a new tutorial in the right place

- Design-process lessons go in `site/design-fabrication/design-process/`.
- Photopea and logo lessons go in `site/design-fabrication/logo-design/`.
- Raster, vector, SVG, and animation lessons go in `site/design-fabrication/02-digital-design/`.
- Laser-cutting projects go in `site/design-fabrication/03-laser-cutting/`.

When you add a tutorial:

1. Add it to the `render` list in `site/_quarto.yml`.
2. Add it to the correct sidebar section.
3. Link to it from the Design & Fabrication home page.
4. Add a link from the lesson before it.
5. Add a link to the lesson after it.
6. Add known glossary slugs in `terms` when the page uses those terms.
7. Add a short curriculum note using the `ter-curriculum-relevance` callout.

Do not put a tutorial in a convenient folder and leave it unlinked. Its place in the learning sequence must be clear.

## Basic page setup

```yaml
---
title: "Clear lesson title"
description: "One short sentence that says what the student will do."
sidebar: design-fabrication
body-classes: "ter-design-fabrication bs-learn-article ter-notes-lesson"
toc: true
execute:
  enabled: false
---
```

Only add `terms` that already exist in the site glossary.

## Before publishing

- Read every sentence aloud. Shorten anything that feels hard to say.
- Check that a beginner can find the first step quickly.
- Check every screenshot and link.
- Make sure the page has a clear previous and next lesson.
- Render the page.
- Run the site link checker.
- Check the live page after deployment.
