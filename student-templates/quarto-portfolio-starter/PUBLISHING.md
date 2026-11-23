# Optional publishing with GitHub Pages

Publishing is not required. Ask your teacher before making a repository or site
public. GitHub Pages sites are normally public even when some repository plans
allow a private repository, so never treat Pages as private classroom storage.

## Before publishing

1. Run `quarto render` and inspect `_site/index.html` in a browser.
2. Complete `privacy.qmd` as a checklist.
3. Search source files and images for student numbers, school email addresses,
   passwords, tokens, private URLs, network details, serial numbers, schedules,
   names, and faces.
4. Confirm that every image, quotation, and adaptation is yours, permitted, or
   properly licensed and attributed.
5. Have another person test navigation, keyboard focus, mobile layout, image alt
   text, and project links.

## Source files and `_site`

Your `.qmd`, YAML, CSS, images, scripts, and data are source files. Quarto creates
the `_site` folder from them. Fix source files and render again; do not fix the
generated HTML by hand. `_site` is ignored by Git in this starter.

## Optional GitHub Pages workflow

The repository contains an inactive example at
`.github/workflows/publish.yml.example`. After teacher approval:

1. make sure the default branch is named `main`, or update the workflow;
2. copy or rename it to `.github/workflows/publish.yml`;
3. commit and push the source repository;
4. on GitHub, open **Settings > Pages** and choose **GitHub Actions** as the
   publishing source;
5. open **Actions** and inspect the complete workflow log;
6. open the published URL and repeat the privacy and navigation check.

The workflow uses Quarto's documented `gh-pages` publishing approach and does
not execute notebooks. This starter contains no required notebook computation.

## Troubleshooting

### The local render fails

Read the first useful error, not only the final “render failed” line. Check YAML
indentation, profile spelling, quotation marks, filenames, and relative paths.
Run `quarto render --profile core` to determine whether an optional section is
involved.

### The workflow does not run

Check that the file ends in `.yml`, is inside `.github/workflows/`, and watches
the correct branch. Confirm GitHub Actions is enabled for the repository.

### The workflow runs but the site is missing

Inspect the publish step in the Actions log. Confirm Pages uses GitHub Actions,
the workflow has `contents: write`, and the repository permits the selected
actions. Confirm the URL shown in **Settings > Pages** rather than guessing it.

### A page or image works locally but not online

Filename capitalization matters online. Verify the exact relative path from the
source page and avoid spaces or special characters in filenames.

## Unpublish safely

In the repository's **Settings > Pages** area, use the menu beside the live-site
message and choose **Unpublish site**. This removes the deployment without
deleting source files. Disable or remove the publish workflow before the next
push, because another successful deployment can make the site live again.

Unpublishing is different from removing private information from Git history.
If a password, token, or private record was published, tell the teacher, revoke
the credential, and follow the approved incident-response process rather than
assuming unpublishing erased every copy.

## Official references

- <https://quarto.org/docs/publishing/github-pages.html>
- <https://docs.github.com/en/pages/getting-started-with-github-pages/unpublishing-a-github-pages-site>
