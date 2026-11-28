# TEJ Quarto portfolio starter

This offline-capable Quarto website is a starting point, not a finished student
portfolio. It includes a responsive home page, searchable project collection,
four clearly labelled examples, optional Learning Log and Skills sections,
privacy guidance, and templates for new work.

The design borrows three useful portfolio ideas:

1. lead with a small number of strong projects instead of treating every file as
   equally important;
2. let a visitor scan the role, problem, evidence, revision, and outcome before
   choosing to read the full case study;
3. make claims inspectable through calculations, code, tests, measurements, and
   honest limitations.

## Requirements

Install the current Quarto CLI from <https://quarto.org/docs/get-started/>. Git is
recommended. JupyterLite can edit notebooks but cannot render this website.

## Start with the smallest successful site

Open `START-HERE.md` and use the `core` profile first. Do not begin with every optional page. Render the small site, make one Git commit, and add sections only after that works.

## Ten-minute setup

1. Open `_quarto.yml`.
2. In the clearly marked **Student setup** section, replace
   `Student Name or Initials`, `My Technology Portfolio`, the description, and
   footer attribution with teacher-approved wording. This is the one place for
   site identity and title.
3. Keep `core` for the first successful render. Later, choose one profile after `default:`:
   - `core` — Home, Projects, About, Privacy;
   - `blog` — core plus Learning Log;
   - `skills` — core plus Skills and Tools;
   - `full` — every section.
4. Open `_brand.yml` and keep the Harbour colours or copy one of the palettes
   from `docs/colour-palettes.md`.
5. Replace the project-specific introduction in `index.qmd` and the process
   prompts in `about.qmd`.
6. Open a terminal in this folder and run:

```sh
quarto preview
```

Changing the profile changes rendering, navigation, and search. A disabled
section is not placed in `_site`.

## Render and inspect

```sh
quarto check
quarto render
python scripts/validate_portfolio.py
```

The rendered site is in `_site`. Edit `.qmd`, YAML, CSS, and asset source files;
do not edit generated files inside `_site`.

To test a profile without changing the default:

```sh
quarto render --profile core
quarto render --profile full
```

## Add a project

1. Copy the closest file from `templates/` into `projects/`.
2. Rename it with a short lowercase filename such as
   `automatic-night-light.qmd`.
3. Replace title, description, date, categories, image, and image alt text.
4. Replace every prompt and synthetic sample value with approved evidence.
5. Preview the site and test project search, filters, images, links, tables, and
   code blocks.
6. Run a complete render before committing or submitting.

The project page should answer:

- What problem did you solve and what was your role?
- What constraints and risks mattered?
- What did you predict before testing?
- What evidence did you collect?
- What problem did the evidence expose?
- What did you revise?
- What can you conclude, and what remains uncertain?

## Add a Learning Log post

Use the `blog` or `full` profile. Copy `templates/blog-post.qmd` into
`blog/posts/`, give it a lowercase filename, and replace all prompts. A post
captures one useful test, discovery, source, or revision; complete project
reports belong in `projects/`.

## Change the look without breaking it

- Change colours and typography in `_brand.yml`.
- Use `docs/colour-palettes.md` for accessible starting points.
- Keep system fonts so the site works offline.
- Do not use colour alone for status, polarity, or warnings.
- Check keyboard focus, mobile layout, grayscale printing, and reduced motion.

## Publish only when approved

Public publishing is optional. A local render or private classroom submission
can demonstrate the same learning. Read `PUBLISHING.md` before placing anything
on GitHub Pages. The included workflow is an inactive example until it is copied
or renamed to `.github/workflows/publish.yml`.

Before sharing, remove student numbers, faces, private contact details,
classroom codes, network details, serial numbers, passwords, tokens, private
URLs, and identifying information about other students.

## Official references

- Quarto websites: <https://quarto.org/docs/websites/>
- Quarto listings: <https://quarto.org/docs/websites/website-listings.html>
- Quarto project profiles: <https://quarto.org/docs/projects/profiles.html>
- Quarto branding: <https://quarto.org/docs/authoring/brand.html>
- Quarto GitHub Pages: <https://quarto.org/docs/publishing/github-pages.html>

## Licence and attribution

This educational starter is provided with the Technology Education Resources
project under CC BY-SA 4.0 for educational content and AGPL-3.0-only for project
code. Preserve attribution to Andrew Andrade,
<https://andrewandrade.ca/>, and
<https://github.com/mrandrewandrade>. Add your own attribution for adaptations.
