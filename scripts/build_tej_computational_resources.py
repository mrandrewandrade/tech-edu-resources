#!/usr/bin/env python3
"""Build the versioned TEJ notebook collection and student-template download."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import zipfile


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "site" / "assets" / "tej-computational"
NOTEBOOK_ROOT = ASSET_ROOT / "notebooks"
DATA_ROOT = ASSET_ROOT / "data"
TEMPLATE_ROOT = ROOT / "student-templates" / "quarto-portfolio-starter"
TEMPLATE_ZIP = ROOT / "site" / "assets" / "tej-portfolio" / "quarto-portfolio-starter.zip"
COLLECTION_ZIP = ASSET_ROOT / "tej-computational-engineering-notebooks.zip"


def md(source: str) -> dict[str, object]:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str) -> dict[str, object]:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def notebook(title: str, goal: str, prior: str, cells: list[dict[str, object]]) -> dict[str, object]:
    opening = md(
        f"# {title}\n\n"
        f"**Learning goal:** {goal}\n\n"
        "**Why it matters:** A reproducible calculation keeps the engineering assumptions, "
        "evidence, and explanation together.\n\n"
        f"**Prior knowledge:** {prior}\n\n"
        "> A computed answer does not prove that the original circuit model, units, wiring, "
        "or measurements were correct. Use the checks and compare with physical evidence.\n"
    )
    notebook_cells = copy.deepcopy([opening, *cells])
    for index, cell in enumerate(notebook_cells, start=1):
        cell["id"] = f"cell-{index:02d}"
    return {
        "cells": notebook_cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def beginner_notebook(title: str, cells: list[dict[str, object]]) -> dict[str, object]:
    opening = md(
        f"# {title}\n\n"
        "**Learning goal:** Run simple Python, edit the syntax, and make the code work.\n\n"
        "**Why it matters:** Python follows instructions exactly. Quotation marks, brackets, commas, names, and spelling matter.\n\n"
        "**Prior knowledge:** No previous Python, Jupyter, or NumPy experience is needed.\n\n"
        "> A notebook is a page made of boxes called cells. Run one cell at a time with **Shift+Enter**.\n"
    )
    notebook_cells = copy.deepcopy([opening, *cells])
    for index, cell in enumerate(notebook_cells, start=1):
        cell["id"] = f"cell-{index:02d}"
    return {
        "cells": notebook_cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


IMPROVEMENT_FEEDBACK = [
    md(
        "## Help improve this lesson (optional)\n\n"
        "If something got in the way, leave a short note for the teacher:\n\n"
        "1. Which step or word was unclear?\n"
        "2. What do you still not know how to do?\n"
        "3. What one change would make this easier for the next student?\n\n"
        "If you can fix the wording, example, diagram, screenshot, or starter code, show the teacher. "
        "Useful fixes may be added to the course materials and credited. This feedback is optional.\n"
    ),
]


COMMON_CLOSE = [
    md(
        "## Common errors\n\n"
        "- Check volts versus millivolts, amperes versus milliamperes, and ohms versus kilohms.\n"
        "- Run cells in order after restarting the kernel.\n"
        "- Read the last line of an error first, then read the code line above it.\n"
        "- Use `np.allclose` instead of exact `==` when checking decimal arrays.\n"
        "- Keep full precision for intermediate values and round only the reported result.\n"
    ),
    *IMPROVEMENT_FEEDBACK,
]


def life_checkpoint_upgrade_notebook() -> dict[str, object]:
    return notebook(
        "Life Checkpoint Upgrade: Make It, Solve It, Check It",
        "Use a fun Python warm-up, LaTeX, NumPy, and Tinkercad to correct and verify the Life Checkpoint.",
        "The original Life Checkpoint, basic Jupyter cells, Ohm's law, power, schematic symbols, KCL, and KVL.",
        [
            md(
                "## One assignment for Monday and Tuesday\n\n"
                "Use this **same notebook for both days**. Download a backup before leaving each day. Rename the file "
                "`studentnumber-lastname-life-checkpoint-upgrade.ipynb`.\n\n"
                "**This is your opportunity to improve your Life Checkpoint mark to 100%. Correct every section, "
                "show your calculations, and use Tinkercad and Python to verify your work.**\n\n"
                "Submit this notebook, the direct Tinkercad URL, and one screenshot with the simulation running and "
                "a meter reading visible.\n"
            ),
            md(
                "## Two-day plan\n\n"
                "**Monday:** complete the Jupyter warm-up, Ohm's law and power, schematic evidence, loop diagrams, and KCL.\n\n"
                "**Tuesday:** complete both KVL derivations, the matrix, NumPy check, current dashboard, and Tinkercad verification.\n\n"
                "If one part stops you, continue to the next part and return later.\n"
            ),
            md(
                "## 1. Run the setup cell\n\n"
                "Click the code cell and press **Shift+Enter**. Run cells from top to bottom. No Linux command is "
                "required in JupyterLite.\n"
            ),
            code(
                "import numpy as np\n"
                "import matplotlib.pyplot as plt\n\n"
                "from matplotlib.colors import BoundaryNorm, ListedColormap\n\n"
                "print('NumPy is ready:', np.__version__)\n"
                "print('Matplotlib is ready.')\n"
            ),
            md(
                "## 2. Working demonstration: Circuit Grid\n\n"
                "The grid is a tiny circuit board. `0` means a missing piece and `1` means wire. Change only "
                "`repair_piece` from `0` to `1`, then run the cell again. The picture and message will tell you "
                "whether the lamp has power.\n"
            ),
            code(
                "def show_circuit_grid(repair_piece):\n"
                "    board = np.zeros((8, 12), dtype=int)\n"
                "    board[2, 1:11] = 1\n"
                "    board[5, 1:11] = 1\n"
                "    board[2:6, 1] = 1\n"
                "    board[2:6, 10] = 1\n"
                "    board[3:5, 1] = 2       # battery\n"
                "    board[2, 5] = 3         # resistor\n"
                "    powered = repair_piece == 1\n"
                "    board[5, 7] = 1 if powered else 6\n"
                "    board[3:5, 10] = 5 if powered else 4\n\n"
                "    colours = ['#10131a', '#36c5f0', '#ffd23f', '#ff8c42',\n"
                "               '#59636f', '#b8ff5a', '#ef476f']\n"
                "    colour_map = ListedColormap(colours)\n"
                "    colour_norm = BoundaryNorm(np.arange(-0.5, 7.5, 1), colour_map.N)\n\n"
                "    fig, ax = plt.subplots(figsize=(9, 5))\n"
                "    fig.patch.set_facecolor('#10131a')\n"
                "    ax.set_facecolor('#10131a')\n"
                "    ax.imshow(board, cmap=colour_map, norm=colour_norm, interpolation='nearest')\n"
                "    ax.set_xticks(np.arange(-0.5, 12, 1), minor=True)\n"
                "    ax.set_yticks(np.arange(-0.5, 8, 1), minor=True)\n"
                "    ax.grid(which='minor', color='#39424e', linewidth=1.3)\n"
                "    ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)\n"
                "    ax.text(1, 3.5, '+\\n−', ha='center', va='center', fontsize=16, weight='bold', color='#10131a')\n"
                "    ax.text(5, 2, 'R', ha='center', va='center', fontsize=14, weight='bold', color='#10131a')\n"
                "    ax.text(10, 3.5, 'ON' if powered else 'OFF', ha='center', va='center',\n"
                "            fontsize=11, weight='bold', color='#10131a')\n"
                "    ax.text(7, 5, '✓' if powered else '?', ha='center', va='center',\n"
                "            fontsize=16, weight='bold', color='white')\n"
                "    status = 'CIRCUIT COMPLETE — LAMP ON' if powered else 'OPEN CIRCUIT — FIND THE MISSING WIRE'\n"
                "    status_colour = '#b8ff5a' if powered else '#ef476f'\n"
                "    ax.set_title(status, color=status_colour, fontsize=17, weight='bold', pad=14)\n"
                "    plt.show()\n"
                "    return powered\n\n"
                "# CHANGE ONLY THIS NUMBER from 0 to 1, then run the cell again.\n"
                "repair_piece = 0\n"
                "grid_complete = show_circuit_grid(repair_piece)\n\n"
                "if grid_complete:\n"
                "    print('LEVEL COMPLETE: current has a closed path around the loop.')\n"
                "else:\n"
                "    print('TRY AGAIN: change repair_piece to 1 and rerun this cell.')\n"
            ),
            md(
                "### Circuit Grid Level 2: Tune the current\n\n"
                "The lamp needs between **5 mA and 7 mA**. Try one resistor at a time: `1000`, `1500`, `2000`, "
                "or `3000` ohms. Change only `resistor_choice_ohm`, run the cell, and use the meter feedback to "
                "bring the current into the green zone.\n"
            ),
            code(
                "# CHANGE ONLY THIS NUMBER, then run the cell again.\n"
                "resistor_choice_ohm = 1000\n\n"
                "level_voltage_V = 12.0\n"
                "level_current_mA = level_voltage_V / resistor_choice_ohm * 1000\n"
                "safe_current = 5.0 <= level_current_mA <= 7.0\n"
                "too_high = level_current_mA > 7.0\n"
                "bar_colour = '#b8ff5a' if safe_current else ('#ef476f' if too_high else '#ffd23f')\n"
                "status = 'SAFE RANGE - LAMP ON' if safe_current else (\n"
                "    'TOO MUCH CURRENT' if too_high else 'NOT ENOUGH CURRENT'\n"
                ")\n\n"
                "fig, ax = plt.subplots(figsize=(9, 2.8))\n"
                "fig.patch.set_facecolor('#10131a')\n"
                "ax.set_facecolor('#10131a')\n"
                "ax.axvspan(5.0, 7.0, color='#285c35', alpha=0.75, label='safe zone')\n"
                "bar_length = min(12.0, level_current_mA)\n"
                "ax.barh(['current'], [bar_length], color=bar_colour, edgecolor='white', height=0.48)\n"
                "ax.set_xlim(0, 12)\n"
                "ax.set_xticks(range(13))\n"
                "ax.tick_params(colors='white')\n"
                "ax.set_xlabel('current (mA)', color='white')\n"
                "ax.set_title(f'{status}: {level_current_mA:.1f} mA', color=bar_colour,\n"
                "             fontsize=17, weight='bold', pad=12)\n"
                "for spine in ax.spines.values():\n"
                "    spine.set_color('#59636f')\n"
                "plt.show()\n\n"
                "if safe_current:\n"
                "    print('LEVEL COMPLETE: the resistor keeps the lamp current safe.')\n"
                "else:\n"
                "    print('TRY AGAIN: choose another resistor and rerun this cell.')\n"
            ),
            md(
                "## 3. Bug Hunt: Repair the current checker\n\n"
                "The program below stores the resistance as text, so Python cannot divide by it. Run the cell once, "
                "read the message, then remove only the quotation marks around `2000` and run it again.\n"
            ),
            code(
                "bug_voltage_V = 12.0\n"
                "bug_resistance_ohm = '2000'  # Remove the quotation marks to repair the program.\n\n"
                "if isinstance(bug_resistance_ohm, str):\n"
                "    print('BUG FOUND: resistance is text because it has quotation marks.')\n"
                "    print('Repair: change the text to a number, then run this cell again.')\n"
                "else:\n"
                "    repaired_current_mA = bug_voltage_V / bug_resistance_ohm * 1000\n"
                "    print(f'REPAIRED: current = {repaired_current_mA:.1f} mA')\n"
                "    assert np.isclose(repaired_current_mA, 6.0)\n"
                "    print('BUG HUNT COMPLETE.')\n"
            ),
            md(
                "## 4. Customize your circuit-lab title card\n\n"
                "Change only the three values under **EDIT THESE**. Run the cell again. The words are strings stored "
                "in variables. The colours are stored in a list.\n"
            ),
            code(
                "# EDIT THESE three values. Keep the quotation marks and brackets.\n"
                "display_name = 'Circuit Detective'\n"
                "lab_message = 'Make it. Solve it. Check it.'\n"
                "card_colours = ['#6a00ff', '#00b7ff', '#ffcc00']\n\n"
                "assert len(display_name.strip()) > 0\n"
                "assert len(lab_message.strip()) > 0\n"
                "assert len(card_colours) == 3\n\n"
                "fig, ax = plt.subplots(figsize=(8, 2.5))\n"
                "ax.set_facecolor(card_colours[0])\n"
                "ax.text(0.5, 0.64, f\"{display_name}'s Circuit Lab\", ha='center', va='center',\n"
                "        fontsize=24, weight='bold', color='white')\n"
                "ax.text(0.5, 0.30, lab_message, ha='center', va='center',\n"
                "        fontsize=15, color=card_colours[2])\n"
                "ax.plot([0.12, 0.88], [0.10, 0.10], linewidth=8, color=card_colours[1])\n"
                "ax.set_xlim(0, 1)\nax.set_ylim(0, 1)\nax.axis('off')\nplt.show()\n"
                "print('Title card complete.')\n"
            ),
            md(
                "### Tiny challenge\n\n"
                "Change the displayed name, message, and three colours. Run the cell until you like the card.\n\n"
                "**Hint:** colour names such as `'purple'`, `'deepskyblue'`, and `'gold'` work. If a colour causes "
                "an error, read the final line and replace only that colour.\n"
            ),
            md(
                "## 5. Ohm's law and power\n\n"
                "A $12\\,\\mathrm{V}$ supply is connected across a $2.0\\,\\mathrm{k\\Omega}$ resistor. Insert a "
                "Markdown cell below. Show the formula, substitution, answer, and unit for current and power. Use one "
                "displayed equation for each move.\n\n"
                "```text\n"
                "$$I=\\frac{V}{R}$$\n"
                "$$I=\\frac{12\\,\\mathrm{V}}{2000\\,\\mathrm{\\Omega}}$$\n"
                "$$I=\\ldots\\,\\mathrm{A}=\\ldots\\,\\mathrm{mA}$$\n"
                "```\n"
            ),
            code(
                "# Replace the two None values with expressions using the variable names.\n"
                "voltage_V = 12.0\n"
                "resistance_ohm = 2000.0\n"
                "current_A = None       # voltage_V / resistance_ohm\n"
                "power_W = None         # voltage_V * current_A\n\n"
                "if current_A is None or power_W is None:\n"
                "    print('Complete current_A and power_W, then run this cell again.')\n"
                "else:\n"
                "    print(f'Current = {current_A:.6f} A = {current_A * 1000:.1f} mA')\n"
                "    print(f'Power = {power_W:.3f} W = {power_W * 1000:.1f} mW')\n"
                "    assert np.isclose(current_A, 0.006)\n"
                "    assert np.isclose(power_W, 0.072)\n"
                "    print(\"CHECKED: Ohm's law and power are correct.\")\n"
            ),
            md(
                "## 6. Digitize the schematic evidence\n\n"
                "The original checkpoint asked for a series loop containing a $9\\,\\mathrm{V}$ source, closed switch "
                "$S1$, resistor $R1=1\\,\\mathrm{k\\Omega}$, source polarity, and a conventional-current arrow.\n\n"
                "![Corrected series-loop schematic with a 9 volt source, closed switch, 1 kilohm resistor, and current "
                "arrow.](https://andrewandrade.ca/tech-edu-resources/assets/electronics/schematics/life-checkpoint-series.svg)\n\n"
                "Compare this with your original drawing. In a new Markdown cell, list what you corrected. If the "
                "original was already complete, write `No correction needed`.\n"
            ),
            md(
                "## 7. Read the two-loop circuit\n\n"
                "![Life Checkpoint circuit with two sources, three resistors, and currents I1, I2, and I3.]"
                "(https://andrewandrade.ca/tech-edu-resources/assets/electronics/schematics/life-checkpoint-two-loop-clean.png)\n\n"
                "Use the isolated-loop diagrams to check which components belong in each loop.\n\n"
                "| Loop | Correct components | Your original drawing corrected? |\n"
                "|:--|:--|:--|\n"
                "| Loop 1 | $V_{S1}$, $R_1$, $R_3$ | type here |\n"
                "| Loop 2 | $V_{S2}$, $R_2$, $R_3$ | type here |\n\n"
                "![Loop 1 only.](https://andrewandrade.ca/tech-edu-resources/assets/electronics/schematics/life-checkpoint-loop-1.svg)\n\n"
                "![Loop 2 only.](https://andrewandrade.ca/tech-edu-resources/assets/electronics/schematics/life-checkpoint-loop-2.svg)\n"
            ),
            md(
                "## 8. KCL and KVL in LaTeX\n\n"
                "Read the arrows. $I_1$ enters the centre node. $I_2$ and $I_3$ leave. Type the KCL equation and the "
                "rearranged equation for $I_3$ in a Markdown cell.\n\n"
                "Then show each KVL algebra move. Do not jump directly to standard form.\n\n"
                "### Loop 1 scaffold\n\n"
                "$$+12-5I_1-2I_3=0$$\n\n"
                "Substitute your KCL expression for $I_3$, expand the brackets, and rearrange.\n\n"
                "### Loop 2 scaffold\n\n"
                "$$+5-7I_2+2I_3=0$$\n\n"
                "Substitute the same expression for $I_3$, expand the brackets, and rearrange.\n\n"
                "**Insert a Markdown cell below. Show KCL and every algebra line for both loops.**\n"
            ),
            md(
                "### Restart point\n\n"
                "If an earlier algebra line stopped you, use these standard-form equations for the remaining work. "
                "Return and repair the derivation afterward.\n\n"
                "$$7I_1-2I_2=12$$\n\n"
                "$$-2I_1+9I_2=5$$\n\n"
                "Write the matching matrix equation in a Markdown cell before entering it in Python.\n"
            ),
            md(
                "## 9. Enter and solve the matrix\n\n"
                "Replace both `None` values. Keep row order Loop 1, Loop 2 and variable order $[I_1,I_2]$.\n\n"
                "Example syntax: `np.array([[1.0, 2.0], [3.0, 4.0]])`\n"
            ),
            code(
                "A = None  # Replace with the 2 by 2 coefficient array.\n"
                "b = None  # Replace with the two right-side values.\n\n"
                "if A is None or b is None:\n"
                "    currents_mA = None\n"
                "    print('Complete A and b, then run this cell again.')\n"
                "else:\n"
                "    assert A.shape == (2, 2), 'A must have 2 rows and 2 columns.'\n"
                "    assert b.shape == (2,), 'b must contain 2 values.'\n"
                "    currents_mA = np.linalg.solve(A, b)\n"
                "    I1_mA, I2_mA = currents_mA\n"
                "    I3_mA = I1_mA - I2_mA\n"
                "    residual_V = A @ currents_mA - b\n"
                "    print(f'I1 = {I1_mA:.3f} mA')\n"
                "    print(f'I2 = {I2_mA:.3f} mA')\n"
                "    print(f'I3 = {I3_mA:.3f} mA')\n"
                "    print('Residuals:', residual_V)\n"
                "    assert np.allclose(residual_V, 0.0, atol=1e-10)\n"
                "    assert np.allclose([I1_mA, I2_mA, I3_mA], [2.0, 1.0, 1.0])\n"
                "    print('CHECKED: the matrix produces the Life Checkpoint currents.')\n"
            ),
            md(
                "## 10. Make the current dashboard\n\n"
                "The solved currents become a graph. Change the graph title and colours if you want. Do not change "
                "the current values.\n"
            ),
            code(
                "dashboard_title = f\"{display_name}'s Life Checkpoint\"\n"
                "bar_colours = ['#6a00ff', '#00b7ff', '#ffcc00']\n\n"
                "if currents_mA is None:\n"
                "    print('Solve the matrix first.')\n"
                "else:\n"
                "    dashboard_currents = np.array([I1_mA, I2_mA, I3_mA])\n"
                "    fig, ax = plt.subplots(figsize=(7, 4))\n"
                "    bars = ax.bar(['I1', 'I2', 'I3'], dashboard_currents, color=bar_colours, edgecolor='black')\n"
                "    ax.bar_label(bars, fmt='%.1f mA', padding=4, fontsize=12)\n"
                "    ax.set_ylim(0, max(dashboard_currents) + 1.0)\n"
                "    ax.set_ylabel('Current (mA)')\n"
                "    ax.set_title(dashboard_title, weight='bold')\n"
                "    ax.grid(axis='y', alpha=0.25)\n"
                "    plt.show()\n"
            ),
            md(
                "## 11. Independent checks\n\n"
                "In a Markdown cell, substitute the solved currents into KCL and both standard-form KVL equations. "
                "Show the left side and right side with units. Then run the code check below.\n"
            ),
            code(
                "if currents_mA is None:\n"
                "    print('Solve the matrix first.')\n"
                "else:\n"
                "    print('KCL difference:', I1_mA - I2_mA - I3_mA, 'mA')\n"
                "    print('Loop 1 difference:', 7 * I1_mA - 2 * I2_mA - 12, 'V')\n"
                "    print('Loop 2 difference:', -2 * I1_mA + 9 * I2_mA - 5, 'V')\n"
                "    assert np.isclose(I1_mA, I2_mA + I3_mA)\n"
                "    assert np.isclose(7 * I1_mA - 2 * I2_mA, 12)\n"
                "    assert np.isclose(-2 * I1_mA + 9 * I2_mA, 5)\n"
                "    print('CHECKED: KCL and both KVL equations agree.')\n"
            ),
            md(
                "## 12. Unlock the Python Check\n\n"
                "Run this after the matrix and independent checks pass. It uses the verified values to unlock the "
                "checkpoint screen.\n"
            ),
            code(
                "if currents_mA is None:\n"
                "    print('Solve and check the circuit first.')\n"
                "else:\n"
                "    python_verified = (\n"
                "        np.allclose([I1_mA, I2_mA, I3_mA], [2.0, 1.0, 1.0])\n"
                "        and np.isclose(I1_mA, I2_mA + I3_mA)\n"
                "    )\n"
                "    if python_verified:\n"
                "        rng = np.random.default_rng(741)\n"
                "        fig, ax = plt.subplots(figsize=(8, 4))\n"
                "        ax.set_facecolor('#10131a')\n"
                "        ax.scatter(rng.random(120), rng.random(120), s=rng.integers(20, 120, 120),\n"
                "                   c=rng.random(120), cmap='hsv', alpha=0.85)\n"
                "        ax.text(0.5, 0.58, 'CIRCUIT VERIFIED', ha='center', va='center',\n"
                "                fontsize=28, weight='bold', color='white',\n"
                "                bbox=dict(facecolor='#173f2a', edgecolor='lime', boxstyle='round,pad=0.5'))\n"
                "        ax.text(0.5, 0.35, 'PYTHON CHECK PASSED', ha='center', va='center',\n"
                "                fontsize=16, color='lime')\n"
                "        ax.set_xlim(0, 1)\n"
                "        ax.set_ylim(0, 1)\n"
                "        ax.axis('off')\n"
                "        plt.show()\n"
                "    else:\n"
                "        print('LOCKED: return to the matrix and check the three currents.')\n"
            ),
            md(
                "## 13. Tinkercad Boss Level\n\n"
                "Build the Life Checkpoint circuit using $12\\,\\mathrm{V}$, $5\\,\\mathrm{V}$, "
                "$5\\,\\mathrm{k\\Omega}$, $7\\,\\mathrm{k\\Omega}$, and $2\\,\\mathrm{k\\Omega}$. Save it as "
                "`studentnumber-lastname-life-checkpoint`.\n\n"
                "Measure the voltage across all three resistors. Use $I=V/R$ to calculate each current. Directly "
                "measure at least one current with the meter in series.\n\n"
                "| Quantity | Python prediction | Tinkercad result | absolute difference |\n"
                "|:--|--:|--:|--:|\n"
                "| $I_1$ (mA) | 2.0 | ___ | ___ |\n"
                "| $I_2$ (mA) | 1.0 | ___ | ___ |\n"
                "| $I_3$ (mA) | 1.0 | ___ | ___ |\n\n"
                "**Tinkercad circuit URL:** paste it here  \n"
                "**Screenshot filename:** `studentnumber-lastname-life-checkpoint.png`\n"
            ),
            md(
                "### Final match\n\n"
                "After measuring the three currents, enter them in the code cell below. Use this format: "
                "`np.array([2.00, 1.00, 1.00])`. Values within $0.10\\,\\mathrm{mA}$ of Python unlock the final screen.\n"
            ),
            code(
                "tinkercad_currents_mA = None  # Replace with np.array([I1, I2, I3]) from Tinkercad.\n\n"
                "if tinkercad_currents_mA is None:\n"
                "    print('Enter the three Tinkercad currents, then run this cell again.')\n"
                "else:\n"
                "    python_currents_mA = np.array([I1_mA, I2_mA, I3_mA])\n"
                "    differences_mA = np.abs(tinkercad_currents_mA - python_currents_mA)\n"
                "    print('Absolute differences (mA):', differences_mA)\n"
                "    if np.all(differences_mA <= 0.10):\n"
                "        fig, ax = plt.subplots(figsize=(8, 3))\n"
                "        ax.set_facecolor('#10131a')\n"
                "        ax.text(0.5, 0.63, 'SIMULATION MATCH', ha='center', va='center',\n"
                "                fontsize=28, weight='bold', color='lime')\n"
                "        ax.text(0.5, 0.34, 'LIFE CHECKPOINT: 100% AVAILABLE', ha='center', va='center',\n"
                "                fontsize=16, color='white')\n"
                "        ax.plot([0.16, 0.84], [0.15, 0.15], color='deepskyblue', linewidth=10)\n"
                "        ax.set_xlim(0, 1)\n"
                "        ax.set_ylim(0, 1)\n"
                "        ax.axis('off')\n"
                "        plt.show()\n"
                "    else:\n"
                "        print('NOT YET: compare component values, nodes, polarity, and meter placement.')\n"
            ),
            md(
                "## Marks: opportunity to earn 100%\n\n"
                "| Evidence | Marks |\n"
                "|:--|--:|\n"
                "| Circuit Grid, Bug Hunt, and title card are complete | 10 |\n"
                "| Ohm's law, power, units, and simple schematic | 15 |\n"
                "| Complete circuit, isolated loops, and KCL | 15 |\n"
                "| KVL algebra and LaTeX shown one move at a time | 20 |\n"
                "| Matrix, NumPy solution, dashboard, and independent checks | 20 |\n"
                "| Tinkercad topology, measurements, URL, screenshot, and comparison | 20 |\n"
                "| **Total** | **100** |\n\n"
                "Correct work earns marks at every stage. An error in one section does not erase correct work later.\n"
            ),
            md(
                "## Common errors and final check\n\n"
                "- LaTeX is visible as raw text: change the cell to Markdown and press **Shift+Enter**.\n"
                "- The graph does not appear: run the setup cell and matrix cell first.\n"
                "- The answer is off by 1000: keep $\\mathrm{k\\Omega}$ with $\\mathrm{mA}$, or "
                "$\\mathrm{\\Omega}$ with $\\mathrm{A}$.\n"
                "- The matrix has the wrong shape: `A` needs two rows and two columns; `b` needs two values.\n"
                "- Tinkercad current is zero: trace the branch and put the current meter in series.\n\n"
                "### Final check\n\n"
                "- [ ] I completed the Circuit Grid and Bug Hunt.\n"
                "- [ ] My title card is customized.\n"
                "- [ ] My Ohm's law and power work is rendered in LaTeX.\n"
                "- [ ] My schematic corrections, loop evidence, KCL, and KVL work are complete.\n"
                "- [ ] NumPy prints $I_1=2.0\\,\\mathrm{mA}$, $I_2=1.0\\,\\mathrm{mA}$, and "
                "$I_3=1.0\\,\\mathrm{mA}$.\n"
                "- [ ] My dashboard graph appears.\n"
                "- [ ] The Python verified screen and Tinkercad simulation match screen appear.\n"
                "- [ ] My Tinkercad table, direct URL, and screenshot filename are present.\n"
                "- [ ] **Kernel > Restart Kernel and Run All Cells** finishes without an unexpected error.\n"
                "- [ ] The downloaded notebook reopens with my work and output present.\n"
            ),
            *IMPROVEMENT_FEEDBACK,
        ],
    )


def notebooks() -> dict[str, dict[str, object]]:
    n0 = beginner_notebook(
        "Notebook 0: Python First Steps",
        [
            md(
                "## Before you type anything\n\n"
                "A **Markdown cell** contains directions. A **code cell** contains Python. "
                "Click a cell once and press **Shift+Enter**. Work from top to bottom. If a cell shows a red message, "
                "stop and read the last line before changing anything.\n"
            ),
            md(
                "## Videos\n\n"
                "1. Watch [Khan Academy: Print statements and expressions]"
                "(https://www.khanacademy.org/computing/intro-to-python-fundamentals/"
                "x5279a44ae0ab15d6%3Acomputational-thinking-with-variables/"
                "x5279a44ae0ab15d6%3Aprogram-execution/v/plus-operator-and-the-print-function). Do TASK 1 and TASK 2.\n"
                "2. Watch [Khan Academy: Variables and assignment]"
                "(https://www.khanacademy.org/computing/intro-to-python-fundamentals/"
                "x5279a44ae0ab15d6%3Acomputational-thinking-with-variables/"
                "x5279a44ae0ab15d6%3Avariables/v/what-is-a-variable-python). Do TASK 3 and TASK 4.\n"
                "3. Watch [Khan Academy: Lists]"
                "(https://www.khanacademy.org/computing/intro-to-python-fundamentals/"
                "x5279a44ae0ab15d6%3Aautomating-tasks-with-lists/"
                "x5279a44ae0ab15d6%3Alist-indices/v/lists). Do TASK 5 and TASK 6.\n\n"
                "Need more help? Open [Python for Beginners: Learn Python in 1 Hour]"
                "(https://www.youtube.com/watch?v=kqtD5dpn9C8). Watch only the part you need: first program and "
                "variables from **1:15 to 9:08**, strings and arithmetic from **18:49 to 25:59**, or lists from "
                "**45:11 to 48:47**.\n"
            ),
            md("## Example 1: run one line\n\nClick the code cell below. Press **Shift+Enter**.\n"),
            code("print('Hello, TEJ!')\n"),
            md(
                "You should see `Hello, TEJ!` under the cell. `print()` tells Python to display something. Text goes "
                "inside quotation marks.\n\n"
                "### Your turn\n\nChange only the words inside the quotation marks. Run the cell again.\n"
            ),
            code("# TASK 1: replace the words, but keep the quotation marks.\nprint('Type your message here')\n"),
            md("## Example 2: use Python as a calculator\n\nRun this cell. Read each printed answer.\n"),
            code(
                "print('2 + 3 =', 2 + 3)\n"
                "print('10 - 4 =', 10 - 4)\n"
                "print('3 × 5 =', 3 * 5)\n"
                "print('12 ÷ 4 =', 12 / 4)\n"
            ),
            md(
                "### Tiny challenge\n\n"
                "Change the numbers so the answer is `10`.\n\n"
                "**Hint:** keep the `+` sign and change only the two numbers.\n"
            ),
            code(
                "# TASK 2: change the two numbers.\n"
                "answer = 2 + 3\n"
                "print(answer)\n"
                "assert answer == 10\n"
                "print('TASK 2 passed.')\n"
            ),
            md(
                "## Example 3: give values names\n\n"
                "A **variable** is a name that stores a value. The `=` sign stores the value on the right in the name "
                "on the left. Read `voltage_V = 9.0` as “store 9.0 in voltage_V.”\n"
            ),
            code(
                "voltage_V = 9.0\n"
                "resistance_ohm = 1000\n"
                "component_name = 'resistor'\n"
                "circuit_ready = False\n\n"
                "print(voltage_V)\n"
                "print(resistance_ohm)\n"
                "print(component_name)\n"
                "print(circuit_ready)\n"
            ),
            md(
                "## Four basic types\n\n"
                "A **type** tells Python what kind of value it has.\n\n"
                "| Type | Meaning | Example |\n"
                "|---|---|---|\n"
                "| `int` | whole number | `1000` |\n"
                "| `float` | number with a decimal point | `9.0` |\n"
                "| `str` | text inside quotation marks | `'resistor'` |\n"
                "| `bool` | `True` or `False` | `False` |\n\n"
                "Run the next cell to ask Python for each type.\n"
            ),
            code(
                "print(type(resistance_ohm))\n"
                "print(type(voltage_V))\n"
                "print(type(component_name))\n"
                "print(type(circuit_ready))\n"
            ),
            md("### Your turn\n\nComplete the four values. Run the cell and check the four types.\n"),
            code(
                "# TASK 3: replace each starter value with the requested type.\n"
                "my_whole_number = 0\n"
                "my_decimal_number = 0.0\n"
                "my_text = 'replace this text'\n"
                "my_true_or_false = False\n\n"
                "print(type(my_whole_number))\n"
                "print(type(my_decimal_number))\n"
                "print(type(my_text))\n"
                "print(type(my_true_or_false))\n"
            ),
            md(
                "## Example 4: calculate with variables\n\n"
                "Ohm's law is $I=V/R$. Python uses `/` for division. The first answer is in amperes. Multiplying by "
                "1000 converts amperes to milliamperes.\n"
            ),
            code(
                "voltage_V = 9.0\n"
                "resistance_ohm = 1000.0\n"
                "current_A = voltage_V / resistance_ohm\n"
                "current_mA = current_A * 1000\n\n"
                "print('Current in amperes:', current_A)\n"
                "print('Current in milliamperes:', current_mA)\n"
            ),
            md(
                "### Your turn\n\n"
                "Change the resistance to `2000.0`. Then run the cell and check the new current.\n"
            ),
            code(
                "# TASK 4: change the resistance to 2000.0.\n"
                "test_voltage_V = 9.0\n"
                "test_resistance_ohm = 1000.0\n"
                "test_current_mA = test_voltage_V / test_resistance_ohm * 1000\n\n"
                "print('Current:', test_current_mA, 'mA')\n"
                "assert test_resistance_ohm == 2000.0\n"
                "print('TASK 4 passed.')\n"
            ),
            md(
                "## Keep several values together\n\n"
                "Suppose we test a circuit at three voltages. We could make three separate variables:\n\n"
                "```python\n"
                "voltage_1_V = 1.5\n"
                "voltage_2_V = 3.0\n"
                "voltage_3_V = 4.5\n"
                "```\n\n"
                "That works, but the values are harder to keep together. A **list** puts the values together under "
                "one name.\n"
            ),
            md(
                "## Example 5: store several values in a list\n\n"
                "Square brackets make a list: `[1.5, 3.0, 4.5]`. Each stored value has a numbered position called an "
                "**index**. Python begins at index `0`.\n\n"
                "| index | 0 | 1 | 2 |\n"
                "|---|---:|---:|---:|\n"
                "| voltage (V) | 1.5 | 3.0 | 4.5 |\n\n"
                "Think of the index as the label on a small parts drawer. Index `0` labels the first drawer.\n"
            ),
            code(
                "voltage_list_V = [1.5, 3.0, 4.5]\n"
                "print('Complete list:', voltage_list_V)\n"
                "print('First value:', voltage_list_V[0])\n"
                "print('Second value:', voltage_list_V[1])\n"
                "print('Number of values:', len(voltage_list_V))\n"
            ),
            md(
                "### Your turn\n\n"
                "Replace the three starter values with `2.0`, `4.0`, and `6.0`. Then print the third value by changing "
                "the index.\n"
            ),
            code(
                "# TASK 5: replace the values and change the index.\n"
                "my_voltage_list_V = [0.0, 0.0, 0.0]\n"
                "third_value = my_voltage_list_V[0]\n"
                "print('Third value:', third_value)\n"
                "assert my_voltage_list_V == [2.0, 4.0, 6.0]\n"
                "assert third_value == 6.0\n"
                "print('TASK 5 passed.')\n"
            ),
            md(
                "## Make a NumPy array\n\n"
                "A **NumPy array stores numbers in order**. Square brackets hold the numbers, and commas separate them.\n\n"
                "| place | first | middle | last |\n"
                "|---|---:|---:|---:|\n"
                "| number | 1.0 | 2.0 | 3.0 |\n"
            ),
            md(
                "## Example 6: make one array\n\n"
                "NumPy is the tool that makes the array. Run the code. Do not change it yet.\n"
            ),
            code(
                "import numpy as np\n\n"
                "numbers = np.array([1.0, 2.0, 3.0])\n"
                "print(numbers)\n"
            ),
            md(
                "## Small task\n\n"
                "1. Find the middle number: `2.0`.\n"
                "2. Change only `2.0` to `4.0`.\n"
                "3. Press **Shift+Enter**.\n"
                "4. Keep fixing the code until it prints `Checks passed.`\n"
            ),
            code(
                "# TASK 6: change only the middle number.\n"
                "my_numbers = np.array([1.0, 2.0, 3.0])\n"
                "print(my_numbers)\n\n"
                "# These checks confirm the change.\n"
                "assert len(my_numbers) == 3\n"
                "assert my_numbers[1] == 4.0\n"
                "print('Checks passed.')\n"
            ),
            md(
                "## Check your work\n\n"
                "- Every code cell has been run from top to bottom.\n"
                "- TASK 1 through TASK 6 are complete.\n"
                "- The final cell prints three numbers and `Checks passed.`\n"
            ),
            md(
                "## Save and submit\n\n"
                "Download the notebook as `studentnumber-lastname-python-first-steps.ipynb`. Example: "
                "`123456789-Smith-python-first-steps.ipynb`. Keep the `.ipynb` ending.\n"
            ),
            md(
                "## Common errors\n\n"
                "- `NameError`: check the spelling of the variable and run the cell that creates it.\n"
                "- `SyntaxError`: check quotation marks, brackets, and punctuation.\n"
                "- Wrong or old answer: choose **Kernel > Restart Kernel and Run All Cells**.\n"
            ),
            *IMPROVEMENT_FEEDBACK,
        ],
    )

    n1 = notebook(
        "Notebook 1: Python and NumPy Foundations",
        "Use Jupyter cells, Python variables and functions, NumPy arrays, plots, documentation, and verification checks.",
        "Ohm's law, metric prefixes, and basic circuit quantities. No previous Python experience is required.",
        [
            md(
                "## How to work through this notebook\n\n"
                "Run each working demonstration unchanged before editing anything. Make one change, rerun the cell, and "
                "read the output. Use **Shift+Enter** to run a cell. Markdown cells give directions; code cells calculate. "
                "Complete every numbered `TODO` before submitting.\n"
            ),
            md(
                "## Command detective routine\n\n"
                "You are not expected to recognize every command immediately. When you meet an unfamiliar command:\n\n"
                "1. **Run** the small working example.\n"
                "2. **Read** the output or the last line of the error.\n"
                "3. **Open help** with `help(command)`, `command?`, or the official documentation.\n"
                "4. **Change one input** and run the small example again.\n"
                "5. **Use the command** in the task and keep fixing it until the check passes.\n"
            ),
            md("## Working demonstration 1: variables, arithmetic, and output\n\nRun this cell unchanged first.\n"),
            code(
                "voltage_V = 9.0\n"
                "resistance_ohm = 1000.0\n"
                "current_A = voltage_V / resistance_ohm\n"
                "power_W = voltage_V * current_A\n\n"
                "current_mA = current_A * 1000\n"
                "power_mW = power_W * 1000\n\n"
                "print(f'Current: {current_mA:.2f} mA')\n"
                "print(f'Power: {power_mW:.1f} mW')\n"
                "assert abs(current_A - 0.009) < 1e-12\n"
                "assert abs(power_W - 0.081) < 1e-12\n"
            ),
            md(
                "### Checkpoint 1\n\n"
                "1. Change the resistance to $2.2\\,\\mathrm{k\\Omega}$.\n"
                "2. Run the cell.\n"
                "3. Add an assertion that checks the current is positive.\n"
            ),
            code(
                "# TODO 1: complete the checkpoint without changing the variable names.\n"
                "checkpoint1_voltage_V = 9.0\n"
                "checkpoint1_resistance_ohm = 2200.0\n"
                "checkpoint1_current_mA = checkpoint1_voltage_V / checkpoint1_resistance_ohm * 1000\n"
                "checkpoint1_power_mW = checkpoint1_voltage_V * checkpoint1_current_mA\n\n"
                "print(f'Current: {checkpoint1_current_mA:.2f} mA')\n"
                "print(f'Power: {checkpoint1_power_mW:.1f} mW')\n"
                "# TODO: add one assertion that checks a result is positive.\n"
            ),
            md(
                "## Working demonstration 2: lists, indexing, and a loop\n\n"
                "A list stores several related values. Python starts counting positions at zero.\n"
            ),
            code(
                "resistor_values_ohm = [1000.0, 2200.0, 3300.0, 4700.0]\n"
                "print('First value:', resistor_values_ohm[0])\n"
                "print('Number of values:', len(resistor_values_ohm))\n\n"
                "for value_ohm in resistor_values_ohm:\n"
                "    current_mA = 9.0 / value_ohm * 1000\n"
                "    print(f'{value_ohm:6.0f} ohm -> {current_mA:5.2f} mA')\n"
            ),
            md(
                "### Checkpoint 2\n\nPrint the last resistance using a negative index. Then add $6800\\,\\Omega$ to "
                "the list and rerun the loop.\n"
            ),
            code(
                "# TODO 2: change the two starter values.\n"
                "checkpoint2_values_ohm = [1000.0, 2200.0, 3300.0, 4700.0]\n"
                "last_index = 0  # Replace 0 with the negative index for the final item.\n"
                "value_to_add_ohm = 0.0  # Replace 0.0 with the required resistance.\n\n"
                "print('Selected value:', checkpoint2_values_ohm[last_index])\n"
                "if value_to_add_ohm > 0:\n"
                "    checkpoint2_values_ohm.append(value_to_add_ohm)\n"
                "print('Updated list:', checkpoint2_values_ohm)\n"
            ),
            md(
                "## Working demonstration 3: NumPy arrays\n\n"
                "NumPy performs the same operation on a complete array without writing a separate calculation for every "
                "value. Inspect `shape`, `dtype`, and the first and last results before trusting the output.\n"
            ),
            code(
                "import numpy as np\n\n"
                "voltage_V = np.array([1.5, 3.0, 4.5, 6.0, 7.5, 9.0])\n"
                "resistance_ohm = 2200.0\n"
                "current_mA = voltage_V / resistance_ohm * 1000\n"
                "power_mW = voltage_V * current_mA\n\n"
                "print('shape:', voltage_V.shape)\n"
                "print('dtype:', voltage_V.dtype)\n"
                "print('current (mA):', current_mA)\n"
                "print('minimum and maximum:', current_mA.min(), current_mA.max())\n"
                "print('mean:', current_mA.mean())\n\n"
                "assert voltage_V.shape == current_mA.shape\n"
                "assert np.all(current_mA > 0)\n"
                "assert np.all(np.diff(current_mA) > 0)\n"
            ),
            md(
                "### Checkpoint 3\n\n"
                "Use indexing to print the result for $6.0\\,\\mathrm{V}$. Then use a **Boolean filter** to display only "
                "currents below $3\\,\\mathrm{mA}$.\n"
            ),
            code(
                "# TODO 3: run the scaffold and make both checks pass.\n"
                "selected_index = 3\n"
                "current_limit_mA = 3.0\n"
                "below_limit = current_mA < current_limit_mA\n\n"
                "print('Current at 6.0 V:', current_mA[selected_index])\n"
                "print('Mask:', below_limit)\n"
                "print('Currents below the limit:', current_mA[below_limit])\n"
                "assert voltage_V[selected_index] == 6.0\n"
                "assert np.all(current_mA[below_limit] < current_limit_mA)\n"
            ),
            md(
                "### Try NumPy help\n\n"
                "Run the sandbox. Uncomment one `help(...)` line. Change one number in `command_sample`, run the cell "
                "again, and find the changed output.\n"
            ),
            code(
                "# Command sandbox: uncomment one help line, then change the sample values.\n"
                "command_sample = np.array([2.0, 4.0, 6.0])\n"
                "print('type:', type(command_sample))\n"
                "print('shape:', command_sample.shape)\n"
                "print('mean:', command_sample.mean())\n"
                "# help(np.array)\n"
                "# help(np.mean)\n"
                "# TODO: change one value above and run the cell again.\n"
            ),
            md("## Working demonstration 4: write and test a function\n"),
            code(
                "def calculate_current_mA(voltage_V, resistance_ohm):\n"
                "    \"\"\"Return resistor current in milliamperes.\"\"\"\n"
                "    return np.asarray(voltage_V) / resistance_ohm * 1000\n\n"
                "test_current_mA = calculate_current_mA([3.0, 6.0, 9.0], 3000.0)\n"
                "print(test_current_mA)\n"
                "assert np.allclose(test_current_mA, [1.0, 2.0, 3.0])\n"
            ),
            code(
                "# TODO 4: call the function with a new voltage list and resistance.\n"
                "your_voltage_V = [2.0, 4.0, 6.0]\n"
                "your_resistance_ohm = 2000.0\n"
                "your_current_mA = calculate_current_mA(your_voltage_V, your_resistance_ohm)\n"
                "print(your_current_mA)\n"
                "# TODO: add an assertion for one current you can calculate by hand.\n"
                "# TODO: use help(np.asarray) or help(np.allclose), then rerun this cell.\n"
            ),
            md(
                "## Before the error challenge\n\n"
                "Read a traceback from the bottom. Read the **final line** first; it names the error. Then read the code "
                "line above it.\n\n"
                "| Last line says | Meaning | Check |\n"
                "|---|---|---|\n"
                "| `missing required positional argument` | The function needs another value | Compare your call with the function signature |\n"
                "| `unexpected keyword argument` | The keyword name is not accepted | Copy the exact name from the documentation |\n"
                "| `AssertionError` | A check was false | Print both values; use `np.allclose` for decimals |\n\n"
                "## Error challenge: repair one keyword\n\n"
                "1. Change `trigger_documentation_error` to `True` and run the cell.\n"
                "2. Read the final line, then the code line above it.\n"
                "3. Open `help(np.round)` or the official NumPy documentation.\n"
                "4. Compare the function signature with the broken line from left to right.\n"
                "5. Repair only the incorrect keyword and run the cell again.\n"
            ),
            code(
                "trigger_documentation_error = False\n\n"
                "if trigger_documentation_error:\n"
                "    rounded_current_mA = np.round(current_mA, digits=2)\n"
                "    print(rounded_current_mA)\n"
                "else:\n"
                "    print('Set the flag to True when you are ready to practise reading documentation.')\n"
            ),
            md("## Working demonstration 5: graph an array\n"),
            code(
                "import matplotlib.pyplot as plt\n\n"
                "plt.plot(voltage_V, current_mA, marker='o')\n"
                "plt.xlabel('Voltage (V)')\n"
                "plt.ylabel('Current (mA)')\n"
                "plt.title('Current through a 2.2 kOhm resistor')\n"
                "plt.grid(True)\n"
                "plt.show()\n"
            ),
            md(
                "## Purposeful problem: coding assignment\n\n"
                "Create a new section titled **My resistor investigation**. Use the supplied "
                "$2.0\\,\\mathrm{k\\Omega}$ resistor and voltage values. The numbers give clean whole-number currents. "
                "Your work must include:\n\n"
                "1. named variables with units;\n"
                "2. the supplied NumPy voltage array;\n"
                "3. one current calculation using the supplied function;\n"
                "4. one printed current selected by its position;\n"
                "5. one `np.allclose` check; and\n"
                "6. a graph with title, axis labels, units, markers, and grid.\n"
            ),
            code(
                "# STEP 1 — use the supplied inputs.\n"
                "student_resistance_ohm = 2000.0\n"
                "student_voltage_V = np.array([2, 4, 6, 8, 10, 12])\n"
                "print('Voltage values:', student_voltage_V)\n"
                "# TODO 5: change the final voltage from 12 to 14, run the cell, then change it back.\n"
            ),
            code(
                "# STEP 2 — calculate the current array.\n"
                "student_current_mA = calculate_current_mA(student_voltage_V, student_resistance_ohm)\n"
                "\n"
                "print('Current (mA):', student_current_mA)\n"
                "assert np.allclose(student_current_mA, [1, 2, 3, 4, 5, 6])\n"
            ),
            code(
                "# STEP 3 — print one value by its position.\n"
                "student_index = 2  # Position 2 is the third item.\n"
                "print('Selected voltage:', student_voltage_V[student_index])\n"
                "print('Selected current:', student_current_mA[student_index])\n"
                "# TODO 6: change the position to print the fifth item.\n"
            ),
            code(
                "# STEP 4 — verify and graph the investigation.\n"
                "# np.allclose is safer than == for decimal calculations.\n"
                "# TODO 7: complete the expected current values.\n"
                "assert np.allclose(student_current_mA, [1, 2, 3, __, __, __])\n\n"
                "plt.plot(student_voltage_V, student_current_mA, marker='o')\n"
                "plt.xlabel('Voltage (V)')\n"
                "plt.ylabel('Current (mA)')\n"
                "plt.title('TODO 8: write a specific graph title')\n"
                "plt.grid(True)\n"
                "plt.show()\n"
            ),
            md(
                "## Independent challenge\n\n"
                "Compare two resistor values on the same graph. Label both lines and add an assertion that checks which "
                "current array is larger at the same voltage.\n\n"
                "### Hints\n\n"
                "1. Reuse the same voltage array for a fair comparison.\n"
                "2. Call `calculate_current_mA` once for each resistor.\n"
                "3. Add a label to each `plt.plot` call and finish with `plt.legend()`.\n"
                "4. If a function is unfamiliar, inspect its signature and examples before guessing.\n"
            ),
            md(
                "## Submission checklist\n\n"
                "- [ ] Restarting the kernel and running all cells completes after the intentional error is repaired.\n"
                "- [ ] The assignment contains the supplied array, current calculation, one selected value, one check, and a graph.\n"
                "- [ ] Every numbered `TODO` has been completed.\n"
                "- [ ] The help sandbox was run with one changed input.\n"
                "- [ ] The error challenge runs after the keyword is repaired.\n"
                "- [ ] The downloaded filename follows `studentnumber-lastname-jupyter-foundations.ipynb`.\n"
                "- [ ] The downloaded notebook reopens with code and output present.\n"
            ),
            *COMMON_CLOSE,
        ],
    )

    n2 = notebook(
        "Notebook 2: Series and Parallel Circuit Calculations",
        "Calculate equivalent resistance, currents, voltage drops, power, and conservation checks.",
        "Series rules, parallel rules, Ohm's law, and Python lists.",
        [
            md("## Working demonstration: series circuit\n"),
            code(
                "source_V = 15.0\n"
                "series_ohm = [1000.0, 2200.0, 3300.0]\n"
                "total_ohm = sum(series_ohm)\n"
                "total_A = source_V / total_ohm\n"
                "drops_V = [total_A * value for value in series_ohm]\n"
                "print(total_ohm, total_A * 1000, drops_V)\n"
                "assert abs(sum(drops_V) - source_V) < 1e-12\n"
            ),
            md("## Working demonstration: parallel circuit\n"),
            code(
                "parallel_ohm = [1000.0, 2200.0, 3300.0]\n"
                "equivalent_ohm = 1 / sum(1 / value for value in parallel_ohm)\n"
                "branch_A = [source_V / value for value in parallel_ohm]\n"
                "total_parallel_A = source_V / equivalent_ohm\n"
                "assert abs(sum(branch_A) - total_parallel_A) < 1e-12\n"
                "assert equivalent_ohm < min(parallel_ohm)\n"
                "print(f'Equivalent resistance: {equivalent_ohm:.2f} ohm')\n"
            ),
            md(
                "## Purposeful problem\n\nFor a 12.0 V source, place 1.0 kΩ in series with a parallel pair of "
                "2.2 kΩ and 3.3 kΩ. Calculate total current, each branch current, every voltage, and total power.\n"
            ),
            code(
                "# Student code. Preserve values in ohms, volts, amperes, and watts.\n"
                "source_V = 12.0\nR1_ohm, R2_ohm, R3_ohm = 1000.0, 2200.0, 3300.0\n"
                "# Add calculations and assertions for KCL, KVL, and power.\n"
            ),
            md(
                "## Independent challenge\n\nChange one resistor to an available 5% value so total current is below a "
                "teacher-set limit while branch current remains above a target. Justify the choice.\n\n"
                "### Hints\n\n1. Reduce the parallel group before adding the series resistance.\n"
                "2. Search the course notes for **series-parallel reduce solve expand check**.\n"
                "3. Verify both $I_2+I_3=I_T$ and $V_1+V_{23}=V_T$.\n"
            ),
            *COMMON_CLOSE,
        ],
    )

    n3 = notebook(
        "Notebook 3: Kirchhoff Systems — Solve, Verify, and Investigate",
        "Convert two KVL equations to matrix form, solve them with NumPy, read documentation to repair code, verify residuals, and investigate a changed source.",
        "KCL, KVL, simultaneous equations, metric prefixes, and the completed five-question assignment.",
        [
            md(
                "**Monday:** follow the teacher demonstration and run each check.  \n"
                "**Tuesday:** complete the independent verification lab using one two-loop question you already solved and corrected.\n\n"
                "## Workflow\n\n"
                "**Write Equations → Standard Form → $A\\mathbf{x}=\\mathbf{b}$ → Solve → Verify → Investigate**\n\n"
                "> A near-zero residual proves that the computed currents satisfy the entered equations. It does not prove "
                "that those equations correctly represent the circuit.\n"
            ),
            md(
                "## Working demonstration: from KVL to a matrix\n\n"
                "Use the completed Question 4 equations:\n\n"
                "$$5I_1-2I_2=10$$\n\n"
                "$$-2I_1+7I_2=6.$$\n\n"
                "Keep the variable order $[I_1,I_2]$ in every row. Then\n\n"
                "$$\n"
                "\\underbrace{\\begin{bmatrix}5&-2\\\\-2&7\\end{bmatrix}}_{A}"
                "\\underbrace{\\begin{bmatrix}I_1\\\\I_2\\end{bmatrix}}_{\\mathbf{x}}"
                "=\\underbrace{\\begin{bmatrix}10\\\\6\\end{bmatrix}}_{\\mathbf{b}}.\n"
                "$$\n\n"
                "With resistance in $\\mathrm{k\\Omega}$ and voltage in $\\mathrm{V}$, the currents are in $\\mathrm{mA}$.\n"
            ),
            code(
                "import numpy as np\n"
                "try:\n"
                "    import matplotlib.pyplot as plt\n"
                "except ImportError:\n"
                "    plt = None\n"
                "    print('Matplotlib is unavailable; use the numerical table for the investigation.')\n\n"
                "variable_names = np.array(['I1', 'I2'])\n"
                "A_demo = np.array([[5.0, -2.0], [-2.0, 7.0]])  # kOhm\n"
                "b_demo = np.array([10.0, 6.0])                  # V\n"
            ),
            code(
                "currents_demo_mA = np.linalg.solve(A_demo, b_demo)\n"
                "residual_demo_V = A_demo @ currents_demo_mA - b_demo\n"
                "for name, value in zip(variable_names, currents_demo_mA):\n"
                "    print(f'{name} = {value:.6f} mA')\n"
                "print('Residuals (V):', residual_demo_V)\n"
                "print('Maximum absolute residual (V):', np.max(np.abs(residual_demo_V)))\n"
                "assert np.allclose(residual_demo_V, 0.0, atol=1e-10)\n"
            ),
            md(
                "### Read the output\n\n"
                "- A positive current agrees with the chosen arrow.\n"
                "- A negative current means the real current is opposite the chosen arrow.\n"
                "- Each residual is the left side minus the right side of one entered equation.\n"
            ),
            md(
                "## Documentation-driven debugging\n\n"
                "Engineers are not expected to memorize every function. They are expected to reproduce a problem, read "
                "the exact message, inspect the inputs, find the relevant documentation, and verify the repair.\n\n"
                "Use this protocol before asking for the corrected line of code:\n\n"
                "1. **Reproduce:** run the smallest cell that still shows the problem.\n"
                "2. **Read:** copy the final exception line or describe the suspicious output precisely.\n"
                "3. **Inspect:** print `type(...)`, `.shape`, units, and the values entering the function.\n"
                "4. **Research:** try `help(function)`, `function?`, or search the exact error with the library and function name. "
                "Prefer the official NumPy or Jupyter documentation.\n"
                "5. **Repair:** change the smallest necessary part shown by the documentation.\n"
                "6. **Verify:** rerun from a clean kernel and use an independent equation, unit check, or residual.\n\n"
                "Your debugging record must include the exact error or wrong result, search terms, source consulted, the "
                "requirement you found, the repair, and the verification evidence.\n"
            ),
            md(
                "### Difficulty ladder\n\n"
                "1. **Working example:** run known-good code and match its output to the shown result.\n"
                "2. **Easy:** fix one incorrect function keyword using `help()` or the function signature.\n"
                "3. **Medium:** diagnose incompatible array shapes using an exception and the official documentation.\n"
                "4. **Harder:** catch a believable unit error even though the program runs and its residual is near zero.\n"
            ),
            md(
                "### Stage 1 — easy: one incorrect keyword\n\n"
                "Change `trigger_easy_error` to `True`. Read the final exception line, then use `help(np.round)`, "
                "`np.round?`, or the official NumPy documentation to find the keyword used for decimal places.\n"
            ),
            code(
                "trigger_easy_error = False  # Change to True to begin Stage 1.\n\n"
                "if trigger_easy_error:\n"
                "    rounded_currents_mA = np.round(currents_demo_mA, decimal=3)\n"
                "    print(rounded_currents_mA)\n"
                "else:\n"
                "    print('Set the flag to True when you are ready for the easy documentation task.')\n"
            ),
            md(
                "Open [the official `numpy.round` page](https://numpy.org/doc/stable/reference/generated/numpy.round.html), "
                "find the keyword for decimal places, and repair the code below.\n"
            ),
            code(
                "# Student repair for Stage 1. Change only the incorrect keyword.\n"
                "# rounded_currents_mA = np.round(currents_demo_mA, ...=3)\n"
                "# print(rounded_currents_mA)\n"
            ),
            md(
                "### Stage 2 — medium: make NumPy complain about shape\n\n"
                "Change `trigger_documentation_error` to `True` and run the cell. Do not ask for the repaired line yet. "
                "Use the exception, the array shapes, and the `numpy.linalg.solve` documentation to determine what is wrong.\n"
            ),
            code(
                "trigger_documentation_error = False  # Change to True to begin the debugging task.\n\n"
                "A_broken = np.array([[5.0, -2.0, 0.0], [-2.0, 7.0, 0.0]])\n"
                "b_broken = np.array([10.0, 6.0])\n"
                "print('A_broken shape:', A_broken.shape)\n"
                "print('b_broken shape:', b_broken.shape)\n\n"
                "if trigger_documentation_error:\n"
                "    broken_solution = np.linalg.solve(A_broken, b_broken)\n"
                "else:\n"
                "    print('Set the flag to True when you are ready to trigger the intentional error.')\n"
            ),
            md(
                "Open [the official `numpy.linalg.solve` page](https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html). "
                "Use the required shape for $A$, repair the array, and make the residual check pass.\n"
            ),
            code(
                "# Student repair for the seeded error. Do not paste a complete solution from a search result.\n"
                "A_repaired = None\n"
                "# repaired_solution_mA = np.linalg.solve(A_repaired, b_broken)\n"
                "# repaired_residual_V = A_repaired @ repaired_solution_mA - b_broken\n"
                "# print(repaired_solution_mA, repaired_residual_V)\n"
                "# assert np.allclose(repaired_residual_V, 0.0, atol=1e-10)\n"
            ),
            md(
                "### Stage 3 — harder: no exception is raised\n\n"
                "The next cell runs, but the printed unit is wrong. A near-zero residual will not expose that mistake. "
                "Use dimensional analysis and the variable names to repair the report, then add a check that would catch "
                "the original factor-of-1000 error.\n"
            ),
            code(
                "A_demo_ohm = A_demo * 1000.0\n"
                "currents_from_ohm_A = np.linalg.solve(A_demo_ohm, b_demo)\n"
                "print('INTENTIONALLY WRONG REPORT')\n"
                "for name, value in zip(variable_names, currents_from_ohm_A):\n"
                "    print(f'{name} = {value:.6f} mA')  # Wrong: value is still in amperes.\n"
                "print('Residuals (V):', A_demo_ohm @ currents_from_ohm_A - b_demo)\n"
            ),
            code(
                "# Student repair for the seeded wrong answer.\n"
                "# Convert amperes to milliamperes, print the corrected values, and add an assertion.\n"
            ),
            md(
                "## Tuesday independent lab\n\n"
                "Use one completed two-loop question. Question 4 is entered below; replace the values if you choose Question 5.\n\n"
                "1. Copy both original equations.\n"
                "2. Rewrite them in standard form.\n"
                "3. State the variable order and units.\n"
                "4. Identify which coefficient belongs in each row and column.\n"
            ),
            code(
                "# STEP 1 — Replace these values only if you selected another completed question.\n"
                "student_variable_names = np.array(['I1', 'I2'])\n"
                "student_A = np.array([[5.0, -2.0], [-2.0, 7.0]])  # kOhm\n"
                "student_b = np.array([10.0, 6.0])                  # V\n"
                "print('Variable order:', student_variable_names)\n"
                "print('A =\\n', student_A)\n"
                "print('b =', student_b)\n"
            ),
            code(
                "# STEP 2 — Solve and verify.\n"
                "student_currents_mA = np.linalg.solve(student_A, student_b)\n"
                "student_residual_V = student_A @ student_currents_mA - student_b\n"
                "for name, value in zip(student_variable_names, student_currents_mA):\n"
                "    print(f'{name} = {value:.6f} mA')\n"
                "for row_number, residual in enumerate(student_residual_V, start=1):\n"
                "    print(f'Equation {row_number} residual = {residual:.3e} V')\n"
                "assert np.allclose(student_residual_V, 0.0, atol=1e-10)\n"
            ),
            md(
                "## Comparison table\n\n"
                "Edit this Markdown cell and replace every blank.\n\n"
                "| Method | $I_1$ | $I_2$ | Shared current, if required |\n"
                "|:--|--:|--:|--:|\n"
                "| Your original handwritten work | ___ | ___ | ___ |\n"
                "| Teacher answer | ___ | ___ | ___ |\n"
                "| Python result | ___ | ___ | ___ |\n"
            ),
            md(
                "## Parameter investigation\n\n"
                "Run the sweep from $6\\,\\mathrm{V}$ to $14\\,\\mathrm{V}$. Read the printed current table and graph.\n"
            ),
            code(
                "# STEP 3 — Change one source systematically and graph the response.\n"
                "source_row = 0\n"
                "source_values_V = np.linspace(6.0, 14.0, 9)\n"
                "sweep_currents_mA = []\n"
                "for source_V in source_values_V:\n"
                "    b_changed = student_b.copy()\n"
                "    b_changed[source_row] = source_V\n"
                "    sweep_currents_mA.append(np.linalg.solve(student_A, b_changed))\n"
                "sweep_currents_mA = np.array(sweep_currents_mA)\n\n"
                "print('Source (V)    I1 (mA)    I2 (mA)')\n"
                "for source_V, row in zip(source_values_V, sweep_currents_mA):\n"
                "    print(f'{source_V:8.2f} {row[0]:10.4f} {row[1]:10.4f}')\n\n"
                "if plt is not None:\n"
                "    plt.figure(figsize=(8, 5))\n"
                "    for column, name in enumerate(student_variable_names):\n"
                "        plt.plot(source_values_V, sweep_currents_mA[:, column], marker='o', label=name)\n"
                "    plt.axhline(0.0, color='black', linewidth=0.8)\n"
                "    plt.xlabel('Changed source voltage (V)')\n"
                "    plt.ylabel('Solved current (mA)')\n"
                "    plt.title('How the circuit solution changes with the source')\n"
                "    plt.grid(True, alpha=0.3)\n"
                "    plt.legend()\n"
                "    plt.show()\n"
            ),
            md(
                "## Independent challenge and hints\n\n"
                "**Challenge:** change one resistor instead of a source. Determine every affected coefficient before editing $A$.\n\n"
                "### Hints\n\n"
                "1. Keep the variable order identical in every row.\n"
                "2. Use $\\mathrm{k\\Omega}$ with $\\mathrm{mA}$.\n"
                "3. Print each matrix row beside its original KVL equation.\n"
            ),
            md(
                "## Common errors\n\n"
                "- Copying a coefficient into the wrong column.\n"
                "- Changing the variable order between rows.\n"
                "- Mixing ohms with milliamperes or kilohms with amperes.\n"
                "- Treating a negative current as an automatic error.\n"
                "- Assuming a near-zero residual proves the circuit model itself is correct.\n"
            ),
            md(
                "## Progressive submission checkpoints\n\n"
                "### Checkpoint 1 — Tuesday\n\n"
                "- [ ] Original equations, variable order, and units are visible.\n"
                "- [ ] $A$, $\\mathbf{b}$, the solution, and residuals are complete.\n"
                "- [ ] Stage 1 runs after the keyword is repaired.\n"
                "- [ ] The comparison table is complete.\n"
                "- [ ] The graph or complete numerical table is present.\n"
                "- [ ] The `.ipynb` is saved and submitted.\n\n"
                "### Checkpoint 2 — later exception-driven debugging lesson\n\n"
                "- [ ] Stage 2 uses the documented shape and the residual check passes.\n\n"
                "### Checkpoint 3 — later wrong-answer debugging lesson\n\n"
                "- [ ] Stage 3 repairs the wrong unit and protects the result with a unit-aware check.\n"
            ),
            *IMPROVEMENT_FEEDBACK,
        ],
    )

    n3a = notebook(
        "Notebook 3A: From Two Loops to a Matrix",
        "Derive two KVL equations, arrange them as a matrix, and solve the same system numerically and symbolically.",
        "KCL, KVL, resistor voltage drops, signed loop traversal, and the completed Question 4 and Question 5 circuits.",
        [
            md(
                "## Before you start\n\n"
                "Use the [printable two-loop-to-matrix guide](https://andrewandrade.ca/tech-edu-resources/assets/electronics/handouts/two-loop-to-matrix-bridge.pdf) "
                "beside this notebook. Keep your returned Question 4 and Question 5 work available. Use Question 4 as the worked model, "
                "then derive Question 5 without copying its released answer.\n\n"
                "**Workflow:** arrows $\\rightarrow$ two KVL equations $\\rightarrow$ standard form "
                "$\\rightarrow A\\mathbf{x}=\\mathbf{b}$ $\\rightarrow$ NumPy $\\rightarrow$ SymPy $\\rightarrow$ checks.\n\n"
                "> This is a guided computational bridge. The intentional debugging stages and parameter sweep in Notebook 3 are later lessons.\n"
            ),
            md(
                "## Working demonstration: define the currents\n\n"
                "Use clockwise mesh currents $I_1$ and $I_2$. Define $I_3$ downward through the shared resistor. "
                "The mesh currents oppose each other there. Write KCL first:\n\n"
                "$$I_1-I_2-I_3=0.$$\n\n"
                "Now isolate the shared-branch current:\n\n"
                "$$I_3=I_1-I_2.$$\n\n"
                "A negative value of $I_3$ would mean that the real shared-branch current is upward, opposite the chosen arrow.\n"
            ),
            md(
                "## Working demonstration: derive Loop 1\n\n"
                "Walking clockwise gives a $+10\\,\\mathrm{V}$ source rise, a $-3I_1$ drop, and a $-2I_3$ drop.\n\n"
                "Write the voltage changes before substituting Ohm's law:\n\n"
                "$$+10-V_{R1}-V_{R3}=0$$\n\n"
                "Replace the resistor voltages with $IR$:\n\n"
                "$$V_{R1}=I_1R_1=3I_1,\\qquad V_{R3}=I_3R_3=2I_3$$\n\n"
                "$$+10-3I_1-2I_3=0$$\n\n"
                "Substitute $I_3=I_1-I_2$:\n\n"
                "$$+10-3I_1-2(I_1-I_2)=0$$\n\n"
                "Distribute $-2$ to both terms:\n\n"
                "$$+10-3I_1-2I_1+2I_2=0$$\n\n"
                "Combine the $I_1$ terms:\n\n"
                "$$+10-5I_1+2I_2=0$$\n\n"
                "Subtract $10$ from both sides:\n\n"
                "$$-5I_1+2I_2=-10$$\n\n"
                "Multiply the complete equation by $-1$:\n\n"
                "$$\\boxed{5I_1-2I_2=10}.$$\n"
            ),
            md(
                "## Working demonstration: derive Loop 2\n\n"
                "Walking clockwise gives a $+6\\,\\mathrm{V}$ source rise and a $-5I_2$ drop. "
                "The walk crosses the shared resistor against the defined $I_3$ direction, so that term is $+2I_3$.\n\n"
                "Write the voltage changes before substituting Ohm's law:\n\n"
                "$$+6-V_{R2}+V_{R3}=0$$\n\n"
                "Replace the resistor voltages with $IR$:\n\n"
                "$$V_{R2}=I_2R_2=5I_2,\\qquad V_{R3}=I_3R_3=2I_3$$\n\n"
                "$$+6-5I_2+2I_3=0$$\n\n"
                "Substitute $I_3=I_1-I_2$:\n\n"
                "$$+6-5I_2+2(I_1-I_2)=0$$\n\n"
                "Distribute $+2$ to both terms:\n\n"
                "$$+6-5I_2+2I_1-2I_2=0$$\n\n"
                "Reorder the current terms:\n\n"
                "$$+6+2I_1-5I_2-2I_2=0$$\n\n"
                "Combine the $I_2$ terms:\n\n"
                "$$+6+2I_1-7I_2=0$$\n\n"
                "Subtract $6$ from both sides:\n\n"
                "$$2I_1-7I_2=-6$$\n\n"
                "Multiply the complete equation by $-1$:\n\n"
                "$$\\boxed{-2I_1+7I_2=6}.$$\n"
            ),
            md(
                "## Working demonstration: read equations into a matrix\n\n"
                "Keep the variable order $[I_1,I_2]$ in both rows.\n\n"
                "| Equation | coefficient of $I_1$ | coefficient of $I_2$ | right side |\n"
                "|:--|--:|--:|--:|\n"
                "| $5I_1-2I_2=10$ | $5$ | $-2$ | $10$ |\n"
                "| $-2I_1+7I_2=6$ | $-2$ | $7$ | $6$ |\n\n"
                "$$"
                "\\underbrace{\\begin{bmatrix}5&-2\\\\-2&7\\end{bmatrix}}_{A\\,[\\mathrm{k\\Omega}]}"
                "\\underbrace{\\begin{bmatrix}I_1\\\\I_2\\end{bmatrix}}_{\\mathbf{x}\\,[\\mathrm{mA}]}"
                "=\\underbrace{\\begin{bmatrix}10\\\\6\\end{bmatrix}}_{\\mathbf{b}\\,[\\mathrm{V}]}."
                "$$\n\n"
                "The units work because $[\\mathrm{k\\Omega}][\\mathrm{mA}]=[\\mathrm{V}]$.\n"
                "\nExpand the matrix product one row at a time:\n\n"
                "$$\\begin{bmatrix}5I_1+(-2)I_2\\\\(-2)I_1+7I_2\\end{bmatrix}"
                "=\\begin{bmatrix}10\\\\6\\end{bmatrix}.$$\n\n"
                "The top row must read back as Equation 1 and the bottom row as Equation 2 before you use a solver.\n"
            ),
            code(
                "import numpy as np\n"
                "import sympy as sp\n\n"
                "variable_order = ['I1', 'I2']\n"
                "A_demo = np.array([[5.0, -2.0],\n"
                "                   [-2.0, 7.0]])  # kOhm\n"
                "b_demo = np.array([10.0, 6.0])     # V\n\n"
                "print('Variable order:', variable_order)\n"
                "print('Row 1 ->', A_demo[0, 0], 'I1 +', A_demo[0, 1], 'I2 =', b_demo[0])\n"
                "print('Row 2 ->', A_demo[1, 0], 'I1 +', A_demo[1, 1], 'I2 =', b_demo[1])\n"
                "assert A_demo.shape == (2, 2)\n"
                "assert b_demo.shape == (2,)\n"
            ),
            md(
                "## Numerical linear algebra with NumPy\n\n"
                "`numpy.linalg.solve(A, b)` solves $A\\mathbf{x}=\\mathbf{b}$ without asking you to calculate the inverse. "
                "The residual $A\\mathbf{x}-\\mathbf{b}$ checks the two equations entered.\n"
            ),
            code(
                "currents_demo_mA = np.linalg.solve(A_demo, b_demo)\n"
                "I1_numeric_mA, I2_numeric_mA = currents_demo_mA\n"
                "I3_numeric_mA = I1_numeric_mA - I2_numeric_mA\n"
                "residual_demo_V = A_demo @ currents_demo_mA - b_demo\n\n"
                "print(f'I1 = {I1_numeric_mA:.6f} mA')\n"
                "print(f'I2 = {I2_numeric_mA:.6f} mA')\n"
                "print(f'I3 = {I3_numeric_mA:.6f} mA')\n"
                "print('Residuals (V):', residual_demo_V)\n"
                "assert np.allclose(residual_demo_V, 0.0, atol=1e-10)\n"
            ),
            md(
                "## Symbolic solution with SymPy\n\n"
                "A symbolic solver preserves exact fractions. This makes the algebra visible before decimal rounding.\n"
            ),
            code(
                "I1, I2 = sp.symbols('I1 I2')\n"
                "equations_demo = [\n"
                "    sp.Eq(5*I1 - 2*I2, 10),\n"
                "    sp.Eq(-2*I1 + 7*I2, 6),\n"
                "]\n"
                "exact_demo = sp.solve(equations_demo, (I1, I2), dict=True)[0]\n"
                "I1_exact = exact_demo[I1]\n"
                "I2_exact = exact_demo[I2]\n"
                "I3_exact = sp.simplify(I1_exact - I2_exact)\n\n"
                "print('Exact solution:', exact_demo)\n"
                "print('I3 exact:', I3_exact)\n"
                "print('Decimal check:', [sp.N(I1_exact, 8), sp.N(I2_exact, 8), sp.N(I3_exact, 8)])\n"
                "assert sp.simplify(5*I1_exact - 2*I2_exact - 10) == 0\n"
                "assert sp.simplify(-2*I1_exact + 7*I2_exact - 6) == 0\n"
                "assert np.allclose([float(I1_exact), float(I2_exact)], currents_demo_mA)\n"
            ),
            md(
                "## Assignment overview\n\n"
                "**Part A:** show how the completed Question 4 circuit becomes two equations, one matrix, and two matching solver results.\n\n"
                "**Part B:** transfer the same process to Question 5 using helper questions that do not reveal its matrix or currents.\n\n"
                "**The essential skill:** keep the shared-current definition and variable order consistent.\n\n"
                "**The challenge:** show every signed term instead of copying the finished matrix.\n\n"
                "**The stumbling block:** the Loop 2 shared-resistor sign changes because the loop traversal is against $I_3$.\n\n"
                "**The investigation:** use the official NumPy or SymPy documentation when a solver object is unfamiliar.\n\n"
                "**The verification:** use residuals, substitution, and $I_3=I_1-I_2$.\n"
            ),
            md(
                "### Student derivation\n\n"
                "**Current definitions:** Draw and label $I_1$, $I_2$, and $I_3$.\n\n"
                "**Loop 1 signs:** Write the signed terms $+10$, $-3I_1$, and $-2I_3$.\n\n"
                "**Loop 1 algebra:** Show every line from KVL to $5I_1-2I_2=10$.\n\n"
                "**Loop 2 signs:** Write the shared-resistor term as $+2I_3$.\n\n"
                "**Loop 2 algebra:** Show every line from KVL to $-2I_1+7I_2=6$.\n\n"
                "**Variable order and units:** State them before entering the matrix.\n"
            ),
            code(
                "# Keep False for a clean first run. Change to True after replacing every None.\n"
                "begin_student_work = False\n\n"
                "if begin_student_work:\n"
                "    student_A = np.array([[None, None],\n"
                "                          [None, None]], dtype=float)  # kOhm\n"
                "    student_b = np.array([None, None], dtype=float)    # V\n"
                "else:\n"
                "    student_A = A_demo.copy()\n"
                "    student_b = b_demo.copy()\n"
                "    print('Working values loaded. Replace the None values before setting the flag to True.')\n\n"
                "print('Row 1:', student_A[0], '=', student_b[0])\n"
                "print('Row 2:', student_A[1], '=', student_b[1])\n"
            ),
            code(
                "# Numerical solution and residual. Run after replacing every None.\n"
                "student_currents_mA = np.linalg.solve(student_A, student_b)\n"
                "student_residual_V = student_A @ student_currents_mA - student_b\n"
                "student_I3_mA = student_currents_mA[0] - student_currents_mA[1]\n\n"
                "print('I1, I2 (mA):', student_currents_mA)\n"
                "print('I3 (mA):', student_I3_mA)\n"
                "print('Residuals (V):', student_residual_V)\n"
                "assert np.allclose(student_residual_V, 0.0, atol=1e-10)\n"
            ),
            code(
                "# Symbolic solution: replace the coefficient and right-side blanks.\n"
                "student_I1, student_I2 = sp.symbols('student_I1 student_I2')\n"
                "if begin_student_work:\n"
                "    student_equations = [\n"
                "        sp.Eq(None*student_I1 + None*student_I2, None),\n"
                "        sp.Eq(None*student_I1 + None*student_I2, None),\n"
                "    ]\n"
                "    # student_exact = sp.solve(student_equations, (student_I1, student_I2), dict=True)[0]\n"
                "    # student_I3_exact = sp.simplify(student_exact[student_I1] - student_exact[student_I2])\n"
                "    # print(student_exact, 'I3 =', student_I3_exact)\n"
                "else:\n"
                "    print('Symbolic student scaffold is ready. Replace the None values before setting the flag to True.')\n"
            ),
            md(
                "## Comparison table - replace every blank\n\n"
                "| Quantity | Original work | Released answer | NumPy | SymPy exact |\n"
                "|:--|--:|--:|--:|--:|\n"
                "| $I_1$ | ___ | ___ | ___ | ___ |\n"
                "| $I_2$ | ___ | ___ | ___ | ___ |\n"
                "| $I_3$ | ___ | ___ | ___ | ___ |\n"
            ),
            md(
                "## Part B - transfer the method to Question 5\n\n"
                "Do not begin with the released Question 5 answer. Your job is to generate the matrix from the circuit and algebra. "
                "The symbols $a_{11}$ through $a_{22}$ and $b_1,b_2$ below are placeholders, not Question 5 values.\n\n"
                "### B1. Current definitions\n\n"
                "Add arrows for $I_1$, $I_2$, and $I_3$. Write the matching $I_3$ equation. Then write the signed rise "
                "and drop terms for Loop 1 and Loop 2.\n\n"
                "### B2. Seven algebra lines for each loop\n\n"
                "For **each** loop, show: (1) signed KVL with resistor-voltage symbols, (2) every $V_R=IR$ substitution, "
                "(3) the shared-current substitution, (4) distribution, (5) reordering into $[I_1,I_2]$, "
                "(6) collection of like terms, and (7) moving the constant to the right.\n\n"
                "Finish with two boxed equations in this structure:\n\n"
                "$$\\boxed{a_{11}I_1+a_{12}I_2=b_1}$$\n\n"
                "$$\\boxed{a_{21}I_1+a_{22}I_2=b_2}.$$\n"
            ),
            md(
                "### B3. Question 5 coefficient table and matrix\n\n"
                "Replace every blank from your two boxed equations.\n\n"
                "| Equation | coefficient of $I_1$ | coefficient of $I_2$ | right side |\n"
                "|:--|--:|--:|--:|\n"
                "| Equation 1 | ___ | ___ | ___ |\n"
                "| Equation 2 | ___ | ___ | ___ |\n\n"
                "Use the same variable order in both rows:\n\n"
                "$$\\underbrace{\\begin{bmatrix}a_{11}&a_{12}\\\\a_{21}&a_{22}\\end{bmatrix}}_{A}"
                "\\underbrace{\\begin{bmatrix}I_1\\\\I_2\\end{bmatrix}}_{\\mathbf{x}}"
                "=\\underbrace{\\begin{bmatrix}b_1\\\\b_2\\end{bmatrix}}_{\\mathbf{b}}.$$\n\n"
                "Replace the six placeholders with your Question 5 values. Expand the top row back into Equation 1 and the bottom row "
                "back into Equation 2. Do not run a solver until both read-back equations match your boxed equations.\n"
            ),
            code(
                "# Question 5: enter coefficients only after completing the algebra and row read-back.\n"
                "q5_ready = False\n\n"
                "q5_A = np.array([[None, None],\n"
                "                 [None, None]], dtype=object)  # kOhm\n"
                "q5_b = np.array([None, None], dtype=object)    # V\n\n"
                "# Use +1.0 when I3 = I1 - I2; use -1.0 when I3 = I2 - I1.\n"
                "q5_shared_sign = None\n\n"
                "if q5_ready:\n"
                "    q5_A = q5_A.astype(float)\n"
                "    q5_b = q5_b.astype(float)\n"
                "    assert q5_shared_sign in (-1.0, 1.0)\n"
                "    print('Variable order: [I1, I2]')\n"
                "    print('Row 1 ->', q5_A[0, 0], 'I1 +', q5_A[0, 1], 'I2 =', q5_b[0])\n"
                "    print('Row 2 ->', q5_A[1, 0], 'I1 +', q5_A[1, 1], 'I2 =', q5_b[1])\n"
                "else:\n"
                "    print('Complete B1-B3, replace every None, then set q5_ready = True.')\n"
            ),
            code(
                "# Question 5: solve only after the two printed rows match the boxed equations.\n"
                "if q5_ready:\n"
                "    q5_currents_mA = np.linalg.solve(q5_A, q5_b)\n"
                "    q5_I3_mA = q5_shared_sign * (q5_currents_mA[0] - q5_currents_mA[1])\n"
                "    q5_residual_V = q5_A @ q5_currents_mA - q5_b\n"
                "    print('Question 5 I1, I2 (mA):', q5_currents_mA)\n"
                "    print('Question 5 I3 (mA):', q5_I3_mA)\n"
                "    print('Question 5 residuals (V):', q5_residual_V)\n"
                "    assert np.allclose(q5_residual_V, 0.0, atol=1e-10)\n"
                "else:\n"
                "    print('Solver skipped: Question 5 matrix is not ready yet.')\n"
            ),
            md(
                "## Independent challenge and progressive hints\n\n"
                "**Challenge:** read both matrix rows back as equations. Change one coefficient deliberately, rerun the "
                "solver, and observe that a near-zero residual can still occur for the wrong entered equations.\n\n"
                "### Hint 1 - concept clue\n\nThe shared resistor carries $I_1-I_2$ because the mesh currents oppose each other there.\n\n"
                "### Hint 2 - documentation clue\n\nSearch `numpy.linalg.solve A shape` or `SymPy solve simultaneous equations`.\n\n"
                "### Hint 3 - technical clue\n\nWith order $[I_1,I_2]$, the two rows are $[5,-2]$ and $[-2,7]$, with right side $[10,6]$.\n"
            ),
            md(
                "## Common errors\n\n"
                "- Jumping to a matrix before defining $I_3$.\n"
                "- Using $-2I_3$ in both loops even though Loop 2 travels against $I_3$.\n"
                "- Expanding $-2(I_1-I_2)$ as $-2I_1-2I_2$ instead of $-2I_1+2I_2$.\n"
                "- Changing the variable order between rows.\n"
                "- Mixing ohms with milliamperes or kilohms with amperes.\n"
                "- Assuming a near-zero residual proves that the circuit model is correct.\n"
            ),
            md(
                "## Save and submit\n\n"
                "- [ ] Current definitions and both complete derivations are visible.\n"
                "- [ ] The variable order, units, $A$, and $\\mathbf{b}$ are visible.\n"
                "- [ ] NumPy currents and residuals are visible.\n"
                "- [ ] SymPy exact fractions and $I_3$ are visible.\n"
                "- [ ] The comparison table is complete.\n"
                "- [ ] Question 5 includes both seven-line rearrangements and two boxed standard-form equations.\n"
                "- [ ] The Question 5 coefficient table, matrix, and two row read-backs are complete.\n"
                "- [ ] Question 5 was solved only after the matrix was derived and checked.\n"
                "- [ ] Restart the kernel and run all required cells from top to bottom.\n"
                "- [ ] Save and download `studentnumber-lastname-kirchhoff-jupyter.ipynb`.\n"
                "- [ ] Reopen the downloaded notebook before submitting it.\n"
            ),
            *IMPROVEMENT_FEEDBACK,
        ],
    )

    n4 = notebook(
        "Notebook 4: Graphing Electrical Relationships",
        "Create labelled voltage-current and resistance-current graphs, then interpret a changed parameter.",
        "Ohm's law, arrays, independent and dependent variables, and graph labels.",
        [
            md("## Working demonstration\n"),
            code(
                "import numpy as np\nimport matplotlib.pyplot as plt\n\n"
                "resistance_ohm = 1000.0\n"
                "voltage_V = np.linspace(0.0, 12.0, 13)\n"
                "current_mA = voltage_V / resistance_ohm * 1000.0\n"
                "assert np.allclose(current_mA, voltage_V)\n\n"
                "plt.plot(voltage_V, current_mA, marker='o', label='1.0 kOhm model')\n"
                "plt.xlabel('Voltage (V)')\nplt.ylabel('Current (mA)')\n"
                "plt.title('Ohmic resistor model')\nplt.grid(True)\nplt.legend()\nplt.show()\n"
            ),
            md(
                "## Purposeful problem\n\nAdd a 2.2 kΩ curve to the same voltage-current graph. Calculate both slopes in "
                "mA/V and add an assertion that checks which slope is smaller.\n"
            ),
            code("# Student code: add the second curve, labels, legend, and a numerical slope check.\n"),
            md(
                "## Independent challenge\n\nHold voltage at 9.0 V, vary resistance from 100 Ω to 10 kΩ, and graph current. "
                "Use a logarithmic horizontal scale so the full range is readable.\n\n"
                "### Hints\n\n1. Current is inversely proportional to resistance at fixed voltage.\n"
                "2. Search the Matplotlib quick start for **axis scale** and **legend**.\n"
                "3. `plt.xscale('log')` can make a wide resistance range easier to inspect.\n"
            ),
            *COMMON_CLOSE,
        ],
    )

    n5 = notebook(
        "Notebook 5: Experimental Data Analysis",
        "Import CSV evidence, compare it with an Ohm's-law prediction, calculate differences, and interpret limitations.",
        "CSV tables, Ohm's law, absolute and percentage differences, and graph labels.",
        [
            md(
                "## Working demonstration\n\nUpload `circuit-measurements.csv` beside this notebook. Preserve the raw file unchanged.\n"
            ),
            code(
                "from pathlib import Path\nimport numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n"
                "csv_path = Path('circuit-measurements.csv')\n"
                "if not csv_path.exists():\n    csv_path = Path('../data/circuit-measurements.csv')\n"
                "data = pd.read_csv(csv_path)\n"
                "required = {'voltage_V', 'resistance_ohm', 'measured_current_mA'}\n"
                "assert required.issubset(data.columns)\nassert not data[list(required)].isna().any().any()\n"
                "data['predicted_current_mA'] = data['voltage_V'] / data['resistance_ohm'] * 1000.0\n"
                "data['absolute_difference_mA'] = (data['measured_current_mA'] - data['predicted_current_mA']).abs()\n"
                "reference = data['predicted_current_mA'].abs()\n"
                "data['percentage_difference'] = np.where(reference > 0, data['absolute_difference_mA'] / reference * 100.0, np.nan)\n"
                "display(data)\n"
            ),
            code(
                "plt.scatter(data['voltage_V'], data['measured_current_mA'], label='Measured')\n"
                "plt.plot(data['voltage_V'], data['predicted_current_mA'], label='Predicted')\n"
                "plt.xlabel('Voltage (V)')\nplt.ylabel('Current (mA)')\n"
                "plt.title('Measured and predicted current')\nplt.grid(True)\nplt.legend()\nplt.show()\n"
                "assert data['absolute_difference_mA'].max() < 0.2\n"
            ),
            md(
                "## Purposeful problem\n\nIdentify the largest absolute difference. Decide whether absolute difference, "
                "percentage difference, or both best describe it. A zero predicted reference has no defined percentage difference.\n"
            ),
            code("# Student code: locate the row, report it with units, and add a justified tolerance check.\n"),
            md(
                "## Independent challenge\n\nAdd or replace measurements from a teacher-approved circuit. Preserve the original "
                "CSV, put the instrument or simulator name in the `source` column, and add checks for missing or impossible values.\n\n"
                "### Hints\n\n1. Inspect row count, headers, units, missing values, and impossible values first.\n"
                "2. Read the pandas `read_csv` documentation and Matplotlib quick start.\n"
                "3. Plot raw points before calculating a fit or removing a suspicious value.\n"
            ),
            *COMMON_CLOSE,
        ],
    )

    n6 = notebook(
        "Notebook 6: Engineering Investigation",
        "Define a small engineering question, test a model, troubleshoot evidence, and communicate a supported conclusion.",
        "At least one earlier circuit notebook and the matching electronics lesson.",
        [
            md(
                "## The problem\n\nChoose or receive one focused question. Examples: Which available resistor best meets "
                "a current target? How sensitive is branch current to a resistor tolerance? Where does a simulated result diverge from a simple model?\n\n"
                "Write the success limit as a variable before coding.\n"
            ),
            code(
                "# Set the values and the pass/fail limit for your investigation.\n"
                "# Keep units in every variable name.\n"
                "success_limit = None\n"
            ),
            md("## Working demonstration\n\nInspect how a 5% resistor tolerance changes the possible current range.\n"),
            code(
                "# Working demonstration: tolerance range for a nominal resistor.\n"
                "import numpy as np\nimport matplotlib.pyplot as plt\n\n"
                "source_V = 5.0\nnominal_ohm = 1000.0\ntolerance = 0.05\n"
                "resistance_ohm = np.linspace(nominal_ohm * (1-tolerance), nominal_ohm * (1+tolerance), 101)\n"
                "current_mA = source_V / resistance_ohm * 1000.0\n"
                "assert current_mA.min() > 0\n"
                "print(f'Current range: {current_mA.min():.3f} to {current_mA.max():.3f} mA')\n"
                "plt.plot(resistance_ohm, current_mA)\nplt.xlabel('Resistance (ohm)')\n"
                "plt.ylabel('Current (mA)')\nplt.title('Effect of 5% resistor tolerance')\nplt.grid(True)\nplt.show()\n"
            ),
            md(
                "## Your investigation\n\nCreate the smallest working calculation first. Add one change at a time. Print the "
                "input values and add an assertion or comparison check after each change.\n"
            ),
            code("# Student investigation code. Add meaningful assertions or comparison checks.\n"),
            md(
                "## Challenge and hints\n\nMake one independent design decision and show the evidence in a graph, table, or check.\n\n"
                "1. Choose a parameter that can change the decision, not only the appearance of a graph.\n"
                "2. Search official documentation using the function name and last line of any error.\n"
                "3. Compare the final result with a second equation, limiting case, simulation, or measurement.\n"
            ),
            md(
                "## Verification\n\nPrint the final result with units and significant figures. Add a Boolean pass/fail check "
                "against `success_limit`, then show the final graph or table.\n"
            ),
            *COMMON_CLOSE,
        ],
    )

    n7 = notebook(
        "Notebook 7: RC Circuits, Op-Amps, and a Bridge to Calculus",
        "Model an RC transient, estimate slope and accumulated area numerically, and compare ideal integrator and differentiator behaviour without requiring physical hardware.",
        "Capacitors, RC time constants, voltage-time graphs, basic op-amp feedback, and NumPy arrays.",
        [
            md(
                "## Core and optional evidence\n\n"
                "Every student can complete the model, numerical checks, graphs, and simulation comparison. "
                "A physical XL741 build or teacher demonstration is optional. If hardware is unavailable, label the result "
                "**modelled** or **simulated**, not measured.\n"
            ),
            md(
                "## Working demonstration: RC charging\n\n"
                "For a charging capacitor, $V_C(t)=V_S(1-e^{-t/RC})$. The time constant is $\\tau=RC$. "
                "Run the cell and check the voltage at one time constant.\n"
            ),
            code(
                "import numpy as np\nimport matplotlib.pyplot as plt\n\n"
                "source_V = 5.0\nresistance_ohm = 10_000.0\ncapacitance_F = 100e-6\n"
                "tau_s = resistance_ohm * capacitance_F\n"
                "time_s = np.linspace(0.0, 5.0 * tau_s, 501)\n"
                "capacitor_V = source_V * (1.0 - np.exp(-time_s / tau_s))\n"
                "index_tau = np.argmin(np.abs(time_s - tau_s))\n"
                "print(f'Time constant: {tau_s:.3f} s')\n"
                "print(f'Voltage at one time constant: {capacitor_V[index_tau]:.3f} V')\n"
                "assert abs(capacitor_V[index_tau] / source_V - (1 - np.exp(-1))) < 1e-12\n\n"
                "plt.plot(time_s, capacitor_V, label='Capacitor voltage')\n"
                "plt.axvline(tau_s, color='tab:orange', linestyle='--', label='one time constant')\n"
                "plt.xlabel('Time (s)')\nplt.ylabel('Voltage (V)')\n"
                "plt.title('RC charging model')\nplt.grid(True)\nplt.legend()\nplt.show()\n"
            ),
            md(
                "## From average slope to a derivative\n\n"
                "A finite difference estimates $\\Delta V/\\Delta t$ between samples. `numpy.gradient` combines nearby "
                "differences to estimate the instantaneous slope. Compare it with the known derivative of the RC model.\n"
            ),
            code(
                "numerical_slope_V_per_s = np.gradient(capacitor_V, time_s)\n"
                "model_slope_V_per_s = source_V / tau_s * np.exp(-time_s / tau_s)\n"
                "largest_interior_error = np.max(np.abs(numerical_slope_V_per_s[1:-1] - model_slope_V_per_s[1:-1]))\n"
                "print(f'Largest interior slope difference: {largest_interior_error:.5f} V/s')\n"
                "assert largest_interior_error < 0.001\n\n"
                "plt.plot(time_s, numerical_slope_V_per_s, label='Numerical slope')\n"
                "plt.plot(time_s, model_slope_V_per_s, '--', label='Model derivative')\n"
                "plt.xlabel('Time (s)')\nplt.ylabel('Rate of voltage change (V/s)')\n"
                "plt.title('Finite difference and derivative model')\nplt.grid(True)\nplt.legend()\nplt.show()\n"
            ),
            md(
                "## From accumulated rectangles to an integral\n\n"
                "A running sum of $V\\,\\Delta t$ estimates area under a voltage-time graph. An ideal inverting op-amp "
                "integrator scales that accumulated area by $-1/(RC)$.\n"
            ),
            code(
                "sample_time_s = np.linspace(0.0, 4.0, 801)\n"
                "dt_s = sample_time_s[1] - sample_time_s[0]\n"
                "input_V = np.where((sample_time_s % 2.0) < 1.0, 1.0, -1.0)\n"
                "accumulated_Vs = np.cumsum(input_V) * dt_s\n"
                "integrator_R_ohm = 100_000.0\nintegrator_C_F = 10e-6\n"
                "ideal_integrator_output_V = -accumulated_Vs / (integrator_R_ohm * integrator_C_F)\n"
                "assert np.isfinite(ideal_integrator_output_V).all()\n\n"
                "fig, axes = plt.subplots(2, 1, sharex=True)\n"
                "axes[0].plot(sample_time_s, input_V)\naxes[0].set_ylabel('Input (V)')\naxes[0].grid(True)\n"
                "axes[1].plot(sample_time_s, ideal_integrator_output_V)\n"
                "axes[1].set_xlabel('Time (s)')\naxes[1].set_ylabel('Ideal output (V)')\naxes[1].grid(True)\n"
                "fig.suptitle('Square-wave input and ideal numerical integrator')\nplt.show()\n"
            ),
            md(
                "## Ideal differentiator and real limits\n\n"
                "An ideal differentiator responds strongly at a sudden edge because the slope is very large. Real op-amps "
                "have finite bandwidth, slew rate, output range, noise, component tolerances, and supply limits. A numerical "
                "or ideal simulation is therefore a model to test, not proof of physical performance.\n"
            ),
            code(
                "input_slope_V_per_s = np.gradient(input_V, sample_time_s)\n"
                "differentiator_R_ohm = 10_000.0\ndifferentiator_C_F = 1e-6\n"
                "ideal_differentiator_output_V = -(differentiator_R_ohm * differentiator_C_F) * input_slope_V_per_s\n"
                "assert np.max(np.abs(ideal_differentiator_output_V)) > 0\n"
                "plt.plot(sample_time_s, ideal_differentiator_output_V)\n"
                "plt.xlabel('Time (s)')\nplt.ylabel('Ideal output (V)')\n"
                "plt.title('Numerical ideal differentiator response')\nplt.grid(True)\nplt.show()\n"
            ),
            md(
                "## Optional XL741 voltage-follower pre-lab\n\n"
                "The XL741 v2.0 assembly sheet suggests a simple unity-gain voltage-follower test with $+15$ V and "
                "$-15$ V supply rails and an input kept within $\\pm13$ V. The model below is only an ideal system-level "
                "prediction. It does not simulate the kit's individual transistors, protection diodes, compensation "
                "capacitor, output limits, offset, bandwidth, or assembly faults. Verify the current manufacturer "
                "documentation and teacher-approved supply setup before any physical test.\n"
            ),
            code(
                "positive_supply_V = 15.0\nnegative_supply_V = -15.0\n"
                "documented_test_input_limit_V = 13.0\n"
                "follower_input_V = np.linspace(-documented_test_input_limit_V, documented_test_input_limit_V, 261)\n"
                "ideal_follower_output_V = follower_input_V.copy()\n"
                "assert ideal_follower_output_V.max() < positive_supply_V\n"
                "assert ideal_follower_output_V.min() > negative_supply_V\n"
                "assert np.allclose(ideal_follower_output_V, follower_input_V)\n\n"
                "plt.plot(follower_input_V, ideal_follower_output_V, label='Ideal follower')\n"
                "plt.plot(follower_input_V, follower_input_V, '--', label='Vout = Vin reference')\n"
                "plt.xlabel('Input voltage (V)')\nplt.ylabel('Output voltage (V)')\n"
                "plt.title('XL741 follower pre-lab: ideal prediction only')\n"
                "plt.grid(True)\nplt.legend()\nplt.show()\n"
            ),
            md(
                "## Purposeful problem\n\n"
                "Choose new teacher-approved resistor and capacitor values. Calculate the new time constant, verify the "
                "63.2% charging point, and calculate the initial slope. Add assertions before graphing.\n"
            ),
            code(
                "# Student code: change R and C, calculate tau, generate the model, and check V(tau).\n"
                "student_R_ohm = 22_000.0\nstudent_C_F = 47e-6\n"
                "# Add calculations, labelled graphs, and at least two independent checks.\n"
            ),
            md(
                "## Evidence table\n\n"
                "Complete every available column. Leave **Measured** marked *not available* when no physical kit or "
                "instrument is used; do not copy simulated values into that column.\n\n"
                "| Quantity | Hand estimate | Python model | Circuit simulation | Measured, optional |\n"
                "|---|---:|---:|---:|---:|\n"
                "| RC time constant (s) |  |  |  |  |\n"
                "| Voltage at one time constant (V) |  |  |  |  |\n"
                "| Initial slope (V/s) |  |  |  |  |\n"
                "| Integrator output change (V) |  |  |  |  |\n"
            ),
            md(
                "## Independent challenge\n\n"
                "Compare the same input four ways when possible: hand estimate, Python numerical model, circuit simulation, "
                "and optional XL741 measurement. Put the numerical differences in the evidence table.\n\n"
                "### Hints\n\n"
                "1. Find slope with two nearby points before using derivative notation.\n"
                "2. Find accumulated area with rectangles before using integral notation.\n"
                "3. Reduce the time step and see whether the numerical result converges.\n"
                "4. Never claim the model validates soldering, wiring, ratings, or hardware safety.\n"
            ),
            *COMMON_CLOSE,
        ],
    )

    n8 = notebook(
        "Notebook 8: Electronic Components from Zero",
        "Connect resistor, capacitor, diode, transistor, and op-amp symbols to small numerical models and clearly state what each model leaves out.",
        "No programming experience beyond running Notebook 1; read the matching Component Foundations pages as each section begins.",
        [
            md(
                "## Model boundary\n\n"
                "This notebook is a start-now laboratory when physical parts are unavailable. A model can support a "
                "prediction, comparison, or design choice. It cannot identify a real pinout, inspect soldering, verify a "
                "rating, or prove that a physical circuit is safe.\n"
            ),
            md("## Working demonstration 1: resistor current and power\n"),
            code(
                "import numpy as np\nimport matplotlib.pyplot as plt\n\n"
                "source_V = 5.0\n"
                "resistance_ohm = np.array([220.0, 330.0, 470.0, 680.0, 1000.0])\n"
                "current_mA = source_V / resistance_ohm * 1000.0\n"
                "power_mW = source_V**2 / resistance_ohm * 1000.0\n"
                "assert np.all(np.diff(current_mA) < 0)\n"
                "for R, I, P in zip(resistance_ohm, current_mA, power_mW):\n"
                "    print(f'{R:5.0f} ohm: {I:6.2f} mA, {P:6.2f} mW')\n"
            ),
            md(
                "A larger resistance produces less current at the same voltage. This calculation does not automatically "
                "approve a resistor's tolerance, power rating, temperature, or package.\n"
            ),
            md("## Working demonstration 2: capacitor charge and energy\n"),
            code(
                "capacitance_F = np.array([33e-12, 100e-9, 10e-6, 100e-6])\n"
                "capacitor_voltage_V = 5.0\n"
                "charge_C = capacitance_F * capacitor_voltage_V\n"
                "energy_J = 0.5 * capacitance_F * capacitor_voltage_V**2\n"
                "assert np.all(charge_C > 0) and np.all(energy_J > 0)\n"
                "for C, Q, E in zip(capacitance_F, charge_C, energy_J):\n"
                "    print(f'{C:.3e} F: Q={Q:.3e} C, E={E:.3e} J')\n"
            ),
            md(
                "The 33 pF value matches the scale of the XL741 compensation capacitor. It stores much less energy than "
                "a 100 µF capacitor at the same voltage, but it can still have an important signal-stability role.\n"
            ),
            md("## Working demonstration 3: LED resistor choices\n"),
            code(
                "led_source_V = 5.0\nled_forward_V_model = 2.0\n"
                "candidate_ohm = np.array([220.0, 330.0, 470.0, 680.0, 1000.0])\n"
                "led_current_mA = (led_source_V - led_forward_V_model) / candidate_ohm * 1000.0\n"
                "target_mA = 10.0\n"
                "best_index = np.argmin(np.abs(led_current_mA - target_mA))\n"
                "print(f'Modelled closest choice: {candidate_ohm[best_index]:.0f} ohm at {led_current_mA[best_index]:.2f} mA')\n"
                "assert np.all(led_current_mA > 0)\n\n"
                "plt.plot(candidate_ohm, led_current_mA, marker='o')\n"
                "plt.axhline(target_mA, color='tab:orange', linestyle='--', label='target')\n"
                "plt.xlabel('Series resistance (ohm)')\nplt.ylabel('Modelled LED current (mA)')\n"
                "plt.title('LED current using a fixed forward-voltage model')\nplt.grid(True)\nplt.legend()\nplt.show()\n"
            ),
            md(
                "The fixed forward-voltage model is only a first estimate. A real LED's forward voltage depends on device, "
                "current, temperature, and manufacturing variation.\n"
            ),
            md("## Working demonstration 4: ideal transistor switch\n"),
            code(
                "input_state = np.array([0, 1])  # 0=off, 1=on in this deliberately simple model\n"
                "load_resistance_ohm = 470.0\nload_supply_V = 5.0\n"
                "ideal_load_current_mA = input_state * load_supply_V / load_resistance_ohm * 1000.0\n"
                "assert ideal_load_current_mA[0] == 0\nassert ideal_load_current_mA[1] > 0\n"
                "print('Ideal switch load currents (mA):', ideal_load_current_mA)\n"
            ),
            md(
                "This two-state model omits base or gate drive, saturation voltage, leakage, gain variation, switching time, "
                "thermal limits, and pinout. Use it to understand the control idea, not to approve hardware.\n"
            ),
            md("## Working demonstration 5: op-amp follower and modelled saturation\n"),
            code(
                "follower_input_V = np.linspace(-15.0, 15.0, 301)\n"
                "assumed_output_limit_V = 12.0  # explicit model assumption, not an XL741 specification\n"
                "ideal_follower_V = follower_input_V.copy()\n"
                "limited_follower_V = np.clip(follower_input_V, -assumed_output_limit_V, assumed_output_limit_V)\n"
                "assert np.all(np.abs(limited_follower_V) <= assumed_output_limit_V)\n\n"
                "plt.plot(follower_input_V, ideal_follower_V, '--', label='ideal Vout = Vin')\n"
                "plt.plot(follower_input_V, limited_follower_V, label='example limited-output model')\n"
                "plt.xlabel('Input voltage (V)')\nplt.ylabel('Output voltage (V)')\n"
                "plt.title('Ideal follower and an explicit saturation assumption')\nplt.grid(True)\nplt.legend()\nplt.show()\n"
            ),
            md(
                "The limit above is chosen only to show saturation. Replace it with verified datasheet or measured values "
                "for a specific device and operating condition.\n"
            ),
            md(
                "## Purposeful problem\n\n"
                "Choose one component section. Change one value, rerun the cell, and add a second independent check. Keep "
                "the model boundary shown above.\n"
            ),
            code(
                "# Student work: copy only the smallest relevant model, change one justified input, and add assertions.\n"
            ),
            md(
                "## Independent challenge\n\n"
                "Design a simulation-first test plan for one circuit that uses at least three component types. Include a "
                "schematic, model assumptions, expected graph or table, safe physical measurement to add later, and a rule "
                "for deciding whether the model and evidence agree closely enough.\n\n"
                "### Hints\n\n"
                "1. Begin with the source, control, protection, and load roles.\n"
                "2. Use a resistor-limited LED switched by a transistor, or an RC signal observed by an op-amp follower.\n"
                "3. Keep calculated, modelled, simulated, and measured columns separate.\n"
                "4. A correct Python result can still represent the wrong circuit or an unsafe part choice.\n"
            ),
            *COMMON_CLOSE,
        ],
    )

    n9_three_current_extension = notebook(
        "Midterm: Three-Current Circuit Investigation",
        "Show a three-equation circuit calculation in LaTeX, solve it with NumPy, and verify the same circuit in Tinkercad.",
        "Ohm's law, power, schematic reading, KCL, KVL, Python variables and arrays, and the two-loop matrix lesson.",
        [
            md(
                "## Due and submission\n\n"
                "**Due Thursday, November 12, 2026 at 7:00 p.m.**\n\n"
                "Submit this completed notebook, the direct URL for the saved Tinkercad circuit, and one screenshot with "
                "the simulation running and a meter reading visible. Rename this file "
                "`studentnumber-lastname-midterm-circuit.ipynb`.\n"
            ),
            md(
                "## Week plan: begin with the Life Checkpoint bridge\n\n"
                "**Monday and Tuesday:** complete the bridge work below. Do not begin the new three-current challenge "
                "until the teacher launches it on Wednesday.\n\n"
                "The checkpoint and midterm use the same KCL/KVL workflow, but the current arrows are not identical. "
                "Read the arrows instead of reusing a memorized equation.\n"
            ),
            md(
                "## 1. Run the setup cell\n\n"
                "This browser-safe cell records the Python environment and current notebook folder. No Linux shell command "
                "is required in JupyterLite.\n"
            ),
            code(
                "import sys\n"
                "import platform\n"
                "from pathlib import Path\n"
                "import numpy as np\n\n"
                "print('Python:', sys.version.split()[0])\n"
                "print('Platform:', platform.platform())\n"
                "print('Notebook folder:', Path.cwd())\n"
                "print('NumPy:', np.__version__)\n"
            ),
            md(
                "## 2. Working demonstration: basic LaTeX in a Markdown cell\n\n"
                "Double-click this cell to see the syntax. Press **Shift+Enter** to render it.\n\n"
                "- Inline: `$V=IR$` becomes $V=IR$.\n"
                "- Subscript: `$I_1$` becomes $I_1$.\n"
                "- Fraction: `$I=\\frac{V}{R}$` becomes $I=\\frac{V}{R}$.\n"
                "- Units: `$12\\,\\mathrm{V}$` becomes $12\\,\\mathrm{V}$.\n"
                "- A display equation starts and ends with `$$`.\n\n"
                "Working example:\n\n"
                "$$\n"
                "I=\\frac{V}{R}\n"
                "$$\n\n"
                "$$\n"
                "I=\\frac{5.00\\,\\mathrm{V}}{1.00\\,\\mathrm{k\\Omega}}\n"
                "$$\n\n"
                "$$\n"
                "I=5.00\\,\\mathrm{mA}\n"
                "$$\n"
            ),
            md(
                "### TASK A — type one complete LaTeX calculation\n\n"
                "Replace the three lines below with a calculation for a $6.00\\,\\mathrm{V}$ source and a "
                "$2.00\\,\\mathrm{k\\Omega}$ resistor. Show the formula, substitution, and answer on separate displayed "
                "lines. Include units.\n\n"
                "**Replace this sentence with your three rendered equations.**\n"
            ),
            md(
                "## Monday bridge — checkpoint equations in LaTeX\n\n"
                "![Life Checkpoint circuit with 12 V and 5 V sources, 5 kilohm and 7 kilohm upper resistors, a "
                "2 kilohm shared resistor, and currents I1, I2, and I3.]"
                "(https://andrewandrade.ca/tech-edu-resources/assets/electronics/schematics/life-checkpoint-two-loop-clean.png)\n\n"
                "In this checkpoint diagram, $I_1$ enters the centre node while $I_2$ and $I_3$ leave. Type each "
                "supplied line in a Markdown cell and press **Shift+Enter**:\n\n"
                "1. $I_1=I_2+I_3$\n"
                "2. $7I_1-2I_2=12$\n"
                "3. $-2I_1+9I_2=5$\n\n"
                "Then type the matrix equation:\n\n"
                "$$\n"
                "\\begin{bmatrix}7&-2\\\\-2&9\\end{bmatrix}"
                "\\begin{bmatrix}I_1\\\\I_2\\end{bmatrix}"
                "=\\begin{bmatrix}12\\\\5\\end{bmatrix}.\n"
                "$$\n"
            ),
            code(
                "# Working bridge: run this cell unchanged and read each printed line.\n"
                "checkpoint_A = np.array([[7.0, -2.0], [-2.0, 9.0]])\n"
                "checkpoint_b = np.array([12.0, 5.0])\n"
                "checkpoint_I1_mA, checkpoint_I2_mA = np.linalg.solve(checkpoint_A, checkpoint_b)\n"
                "checkpoint_I3_mA = checkpoint_I1_mA - checkpoint_I2_mA\n\n"
                "print('I1 =', checkpoint_I1_mA, 'mA')\n"
                "print('I2 =', checkpoint_I2_mA, 'mA')\n"
                "print('I3 =', checkpoint_I3_mA, 'mA')\n"
                "assert np.allclose([checkpoint_I1_mA, checkpoint_I2_mA, checkpoint_I3_mA], [2.0, 1.0, 1.0])\n"
            ),
            md(
                "## Tuesday bridge — checkpoint circuit in Tinkercad\n\n"
                "1. Open the assigned starter with two supplies, three resistors, and a multimeter.\n"
                "2. Build the checkpoint circuit using $12\\,\\mathrm{V}$, $5\\,\\mathrm{V}$, "
                "$5\\,\\mathrm{k\\Omega}$, $7\\,\\mathrm{k\\Omega}$, and $2\\,\\mathrm{k\\Omega}$.\n"
                "3. Start the simulation and measure the voltage across one resistor.\n"
                "4. Calculate that current using $I=V/R$.\n"
                "5. Save the design as `studentnumber-lastname-checkpoint-bridge`.\n"
                "6. Record the URL and screenshot below. Keep the design so it can be duplicated on Wednesday.\n\n"
                "| Quantity | NumPy prediction | Tinkercad result |\n"
                "|:--|--:|--:|\n"
                "| $I_1$ (mA) | 2.0 | ___ |\n"
                "| $I_2$ (mA) | 1.0 | ___ |\n"
                "| $I_3$ (mA) | 1.0 | ___ |\n\n"
                "**Checkpoint circuit URL:** paste it here  \n"
                "**Checkpoint screenshot filename:** `studentnumber-lastname-checkpoint-bridge.png`\n\n"
                "**STOP HERE UNTIL THE WEDNESDAY TEACHER LAUNCH.**\n"
            ),
            md(
                "## 3. Three-current challenge\n\n"
                "![Two sources feed a top node through R1 and R2. I1 and I2 enter the node, and I3 leaves downward through R3.]"
                "(https://andrewandrade.ca/tech-edu-resources/assets/electronics/schematics/midterm-three-current-network.svg)\n\n"
                "This is the Wednesday extension. Duplicate the working checkpoint circuit before changing its values. "
                "Use $I_1$, $I_2$, and $I_3$ in that order throughout the notebook.\n\n"
                "- $V_{S1}=12\\,\\mathrm{V}$ and $R_1=2.2\\,\\mathrm{k\\Omega}$\n"
                "- $V_{S2}=9\\,\\mathrm{V}$ and $R_2=3.3\\,\\mathrm{k\\Omega}$\n"
                "- $R_3=1.0\\,\\mathrm{k\\Omega}$\n"
            ),
            md(
                "### TASK B — Equation 1: KCL\n\n"
                "Write current entering = current leaving. Then move every current term to the left so the right side is zero. "
                "Show both lines in LaTeX.\n\n"
                "**Replace this sentence with your KCL work.**\n"
            ),
            md(
                "### TASK C — Equation 2: left-loop KVL\n\n"
                "![The isolated left loop contains the 12 volt source, R1 carrying I1, and R3 carrying I3.]"
                "(https://andrewandrade.ca/tech-edu-resources/assets/electronics/schematics/midterm-three-current-loop1.svg)\n\n"
                "Show one algebra move per displayed line:\n\n"
                "1. source rise and resistor-voltage drops;\n"
                "2. replace each resistor voltage with $IR$;\n"
                "3. substitute the values;\n"
                "4. use variable order $[I_1,I_2,I_3]$;\n"
                "5. box the standard-form equation.\n\n"
                "**Replace this sentence with your left-loop work.**\n"
            ),
            md(
                "### TASK D — Equation 3: right-loop KVL\n\n"
                "![The isolated right loop contains the 9 volt source, R2 carrying I2, and R3 carrying I3.]"
                "(https://andrewandrade.ca/tech-edu-resources/assets/electronics/schematics/midterm-three-current-loop2.svg)\n\n"
                "Repeat the five steps from TASK C. A missing current has coefficient zero.\n\n"
                "**Replace this sentence with your right-loop work.**\n"
            ),
            md(
                "## 4. Coefficient table and matrix\n\n"
                "Replace every blank using your three standard-form equations.\n\n"
                "| Equation | $I_1$ coefficient | $I_2$ coefficient | $I_3$ coefficient | right side |\n"
                "|:--|--:|--:|--:|--:|\n"
                "| KCL | ___ | ___ | ___ | ___ |\n"
                "| left-loop KVL | ___ | ___ | ___ | ___ |\n"
                "| right-loop KVL | ___ | ___ | ___ | ___ |\n\n"
                "State the units, then replace the placeholders in this display:\n\n"
                "$$\n"
                "\\begin{bmatrix}a_{11}&a_{12}&a_{13}\\\\a_{21}&a_{22}&a_{23}\\\\a_{31}&a_{32}&a_{33}\\end{bmatrix}"
                "\\begin{bmatrix}I_1\\\\I_2\\\\I_3\\end{bmatrix}"
                "=\\begin{bmatrix}b_1\\\\b_2\\\\b_3\\end{bmatrix}.\n"
                "$$\n\n"
                "Read every row back as an equation before entering the numbers in Python.\n\n"
                "### Hints\n\n"
                "- A current missing from an equation has coefficient zero.\n"
                "- The KCL row has no voltage source, so its right side is zero.\n"
                "- Keep the order $[I_1,I_2,I_3]$ in all three rows.\n"
            ),
            md(
                "## 5. Enter the matrix\n\n"
                "Replace `None` with `np.array(...)` objects built from your coefficient table. Keep the row order "
                "KCL, left-loop KVL, right-loop KVL.\n"
            ),
            code(
                "# Example shape only: np.array([[1.0, 2.0], [3.0, 4.0]])\n"
                "A = None  # Replace with a 3 by 3 NumPy array.\n"
                "b = None  # Replace with a one-dimensional NumPy array containing 3 values.\n\n"
                "if A is None or b is None:\n"
                "    print('STOP: complete A and b from your coefficient table.')\n"
                "else:\n"
                "    print('A =\\n', A)\n"
                "    print('b =', b)\n"
                "    print('A shape:', A.shape, 'b shape:', b.shape)\n"
                "    assert A.shape == (3, 3), 'A must have 3 rows and 3 columns.'\n"
                "    assert b.shape == (3,), 'b must contain 3 values.'\n"
                "    assert np.linalg.matrix_rank(A) == 3, 'The three rows must be independent. Read them back as equations.'\n"
            ),
            md(
                "## 6. Solve and calculate residuals\n\n"
                "[`numpy.linalg.solve`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html) solves "
                "$A\\mathbf{x}=\\mathbf{b}$. The residual vector is $A\\mathbf{x}-\\mathbf{b}$.\n"
            ),
            code(
                "currents_mA = None\n"
                "residual = None\n\n"
                "if A is None or b is None:\n"
                "    print('Complete A and b first.')\n"
                "else:\n"
                "    currents_mA = np.linalg.solve(A, b)\n"
                "    residual = A @ currents_mA - b\n"
                "    for name, value in zip(['I1', 'I2', 'I3'], currents_mA):\n"
                "        print(f'{name} = {value:.6f} mA')\n"
                "    print('Residuals:', residual)\n"
                "    assert np.allclose(residual, 0.0, atol=1e-10)\n"
            ),
            md(
                "## 7. Independent checks\n\n"
                "In a Markdown cell below this one, use LaTeX to substitute the solved currents into:\n\n"
                "1. KCL at the top node;\n"
                "2. left-loop KVL;\n"
                "3. right-loop KVL.\n\n"
                "Then use $P=I^2R$ for each resistor. Use the current through that resistor, not automatically the total current.\n\n"
                "**Insert a new Markdown cell below and show the checks.**\n"
            ),
            code(
                "# Complete the three resistor-power calculations. Convert mA to A and kOhm to ohm.\n"
                "if currents_mA is None:\n"
                "    print('Solve the currents first.')\n"
                "else:\n"
                "    I1_A, I2_A, I3_A = currents_mA / 1000.0\n"
                "    R1_ohm, R2_ohm, R3_ohm = 2200.0, 3300.0, 1000.0\n"
                "    P_R1_W = None  # Replace None with I1_A**2 * R1_ohm\n"
                "    P_R2_W = None  # Replace None with the correct expression.\n"
                "    P_R3_W = None  # Replace None with the correct expression.\n"
                "    print('Replace all three None values, then print power in mW.')\n"
            ),
            md(
                "## 8. Tinkercad evidence\n\n"
                "Build the exact circuit in the teacher's Tinkercad Classroom. Save it as "
                "`studentnumber-lastname-midterm-circuit`. Measure the voltage across each resistor and use $I=V/R$. "
                "Directly measure at least one current with the meter in series.\n\n"
                "Replace every blank.\n\n"
                "| Quantity | NumPy prediction | Tinkercad result | absolute difference |\n"
                "|:--|--:|--:|--:|\n"
                "| $I_1$ (mA) | ___ | ___ | ___ |\n"
                "| $I_2$ (mA) | ___ | ___ | ___ |\n"
                "| $I_3$ (mA) | ___ | ___ | ___ |\n"
                "| top-node voltage (V) | ___ | ___ | ___ |\n"
                "| $P_{R3}$ (mW) | ___ | ___ | ___ |\n\n"
                "**Tinkercad circuit URL:** paste it here  \n"
                "**Screenshot filename:** `studentnumber-lastname-midterm-circuit.png`\n"
            ),
            md(
                "## Common errors\n\n"
                "- Raw LaTeX is still visible: change the cell to Markdown and press **Shift+Enter**.\n"
                "- The matrix is singular: read every row back as an equation and check for an unfinished zero row.\n"
                "- The answer is off by 1000: keep $\\mathrm{k\\Omega}$ with $\\mathrm{mA}$, or $\\Omega$ with $\\mathrm{A}$.\n"
                "- Tinkercad current is zero: trace the complete branch and place the meter in series.\n\n"
                "## 9. Final check\n\n"
                "- [ ] TASK A contains three rendered LaTeX lines with units.\n"
                "- [ ] The Monday bridge contains the checkpoint equations, $2\\times2$ matrix, and clean current values.\n"
                "- [ ] The Tuesday bridge contains the checkpoint Tinkercad URL and screenshot filename.\n"
                "- [ ] KCL and both KVL derivations show one move per line.\n"
                "- [ ] The coefficient table and $3\\times3$ matrix are complete.\n"
                "- [ ] NumPy prints three currents and near-zero residuals.\n"
                "- [ ] KCL, both KVL equations, and three resistor powers are checked.\n"
                "- [ ] The Tinkercad table, direct URL, and screenshot filename are present.\n"
                "- [ ] **Kernel > Restart Kernel and Run All Cells** finishes without an unexpected error.\n"
                "- [ ] The downloaded notebook reopens with all work and output present.\n"
            ),
            *IMPROVEMENT_FEEDBACK,
        ],
    )

    # Keep the three-current extension above for the later teacher-led lesson.
    # This week's distributed notebook is the two-day Life Checkpoint upgrade.
    n9 = life_checkpoint_upgrade_notebook()

    return {
        "00-python-first-steps.ipynb": n0,
        "01-engineering-calculator.ipynb": n1,
        "02-series-parallel-calculations.ipynb": n2,
        "03a-two-loop-to-matrix-bridge.ipynb": n3a,
        "03-kirchhoff-systems.ipynb": n3,
        "04-graph-electrical-relationships.ipynb": n4,
        "05-experimental-data-analysis.ipynb": n5,
        "06-engineering-investigation.ipynb": n6,
        "07-rc-op-amp-calculus-bridge.ipynb": n7,
        "08-electronic-components-from-zero.ipynb": n8,
        "09-midterm-three-current-circuit.ipynb": n9,
    }


CSV_TEXT = """trial,voltage_V,resistance_ohm,measured_current_mA,source
1,1.0,1000.0,1.01,simulated
2,2.0,1000.0,1.98,simulated
3,3.0,1000.0,3.02,simulated
4,4.0,1000.0,4.01,simulated
5,5.0,1000.0,4.97,simulated
6,6.0,1000.0,6.04,simulated
"""


REQUIREMENTS_TEXT = """jupyterlab>=4.2,<5
numpy>=2.0,<3
pandas>=2.2,<3
matplotlib>=3.9,<4
sympy>=1.13,<2
nbclient>=0.10,<1
nbformat>=5.10,<6
"""


def write_resources() -> None:
    NOTEBOOK_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    for name, content in notebooks().items():
        (NOTEBOOK_ROOT / name).write_text(
            json.dumps(content, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
        )
    (DATA_ROOT / "circuit-measurements.csv").write_text(CSV_TEXT, encoding="utf-8", newline="\n")
    (ASSET_ROOT / "requirements-jupyter.txt").write_text(
        REQUIREMENTS_TEXT, encoding="utf-8", newline="\n"
    )


def zip_tree(source: Path, destination: Path, prefix: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            relative = path.relative_to(source)
            if not path.is_file() or "_site" in relative.parts or ".quarto" in relative.parts:
                continue
            archive.write(path, Path(prefix) / relative)


def build_collection_zip() -> None:
    stage = ROOT / ".quarto" / "tej-computational-engineering"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    shutil.copytree(NOTEBOOK_ROOT, stage / "notebooks")
    shutil.copytree(DATA_ROOT, stage / "data")
    shutil.copy2(ASSET_ROOT / "requirements-jupyter.txt", stage / "requirements-jupyter.txt")
    (stage / "README.txt").write_text(
        "Open the eleven notebooks in order or use the notebook matched to the current electronics lesson.\n"
        "Upload data/circuit-measurements.csv beside Notebook 5. Notebook 7 works without physical hardware.\n"
        "For local JupyterLab, create a virtual environment and install requirements-jupyter.txt.\n"
        "Browser storage is not a backup: download work after every JupyterLite session.\n",
        encoding="utf-8",
        newline="\n",
    )
    zip_tree(stage, COLLECTION_ZIP, "tej-computational-engineering")


def main() -> int:
    if not TEMPLATE_ROOT.is_dir():
        raise SystemExit(f"Missing template source: {TEMPLATE_ROOT}")
    write_resources()
    build_collection_zip()
    zip_tree(TEMPLATE_ROOT, TEMPLATE_ZIP, "quarto-portfolio-starter")
    print(f"Built {len(notebooks())} notebooks, {COLLECTION_ZIP}, and {TEMPLATE_ZIP}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
