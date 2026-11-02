# TEJ Quarto portfolio starter

This small, offline-capable Quarto website contains a home page, about page,
searchable and sortable project grid, four engineering examples, and an optional
blog. It uses Quarto's native website, search, category, and listing features;
it does not require custom JavaScript or an external data service.

## Requirements

Install the current Quarto CLI from <https://quarto.org/docs/get-started/>. Git is
recommended. JupyterLite cannot render this website.

## Preview and render

Open a terminal in this folder:

```sh
quarto check
quarto preview
quarto render
```

The rendered site is in `_site`. Edit the `.qmd`, YAML, CSS, and asset sources,
not files inside `_site`.

## Add a project

1. Copy a file in `projects/` and give it a short lowercase filename.
2. Replace its title, description, date, categories, image, and image alt text.
3. Use the required engineering-story headings from the course portfolio lesson.
4. Preview and test the project listing, category filter, sort control, search,
   images, and relative links.
5. Run `quarto render` before committing or sharing.

The project listing is configured in `projects/index.qmd`. Use the official
Quarto listing documentation to change `sort`, `sort-ui`, `filter-ui`, fields,
or categories.

## Use or remove the optional blog

To use it, copy a file in `blog/posts/`, update its metadata, and write the post.

To remove it:

1. remove the Blog entry from `_quarto.yml`;
2. delete the `blog/` folder;
3. render again and test the navbar and search.

## Publish safely

Publishing is optional. A local render or private classroom submission can show
the same learning. Before any public publish, remove student numbers, faces,
private contact details, classroom codes, network details, serial numbers,
passwords, tokens, and identifiable information about other students.

Follow the official Quarto GitHub Pages guide:
<https://quarto.org/docs/publishing/github-pages.html>.

## Licence and attribution

This educational starter is provided with the Technology Education Resources
project under CC BY-SA 4.0 for educational content and AGPL-3.0-only for project
code. Preserve attribution to Andrew Andrade, <https://andrewandrade.ca/>, and
<https://github.com/mrandrewandrade>. Add your own attribution for adaptations.
