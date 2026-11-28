# Start here

Your first goal is a small website that works. Do not redesign everything.

## 1. Open `_quarto.yml`

Replace only:

- `Student Name or Initials`
- `My Technology Portfolio`
- the one-sentence description

Keep this setting:

```yaml
profile:
  default: core
```

## 2. Edit `index.qmd`

Replace the sample introduction with two or three sentences about what you are learning or building.

## 3. Preview

Open a terminal in this folder:

```bash
quarto check
quarto preview
```

Open the local address printed in the terminal. Stop the preview using `Ctrl+C`.

## 4. Make one mission page

Copy `templates/general-project.qmd` into `projects/`. Give it a short lowercase filename such as `reaction-timer.qmd`. Replace the title and the minimum-result prompts.

## 5. Render

```bash
quarto render
```

The generated website is in `_site`. Do not edit files inside `_site`.

## 6. Save a Git checkpoint

```bash
git status
git add _quarto.yml index.qmd projects
git diff --staged
git commit -m "Build my course website"
git log --oneline
```

You are successful when the home page and project page open and `git log --oneline` shows your commit.

After the `core` version works, read `README.md` to add Skills, a Learning Log, new colours, or optional publishing.
