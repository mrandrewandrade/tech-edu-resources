# Series-parallel circuit slide assets

This folder contains the editable LaTeX and TikZ source for seven equation panels used in the TEJ series-parallel circuit deck.

- `series-parallel-assets.tex` contains every general equation, circuit-specific equation, substitution, solution, and check.
- `series-parallel-circuits.tex` contains the reusable TikZ circuit-diagram generator.
- `render-assets.ps1` compiles the source and creates the slide images.

The source produces:

1. guided-example schematic with general and circuit-specific equations
2. guided-example substitutions, solutions, and checks
3. Question 2 schematic with general and circuit-specific equations
4. Question 2 substitutions, solutions, and checks
5. Question 2 final answers and checks table
6. Question 4 schematic with general and circuit-specific equations
7. Question 4 substitutions, solutions, and checks
8. series and parallel rule overview

Run `render-assets.ps1` from PowerShell to compile the PDF and create the six PNG files. The schematic and equation source are kept together so a future editor can update component values, equations, and slide images from one file.

Generated slide assets:

- `guided-equations.png`
- `guided-solve-check.png`
- `question-2-equations.png`
- `question-2-solve-check.png`
- `question-2-final-answers.png`
- `question-4-equations.png`
- `question-4-solve-check.png`
- `series-parallel-rules.png`

