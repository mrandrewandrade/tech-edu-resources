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


COMMON_CLOSE = [
    md(
        "## Common errors\n\n"
        "- Check volts versus millivolts, amperes versus milliamperes, and ohms versus kilohms.\n"
        "- Run cells in order after restarting the kernel.\n"
        "- Read the last line of an error first and confirm every filename and variable name.\n"
        "- Keep full precision for intermediate values and round only the reported result.\n"
    ),
    md(
        "## Reflection\n\n"
        "What do you know, what do you need to find out, and how will you know when you are right? "
        "Explain what your check established and one limitation it could not remove.\n"
    ),
]


def notebooks() -> dict[str, dict[str, object]]:
    n1 = notebook(
        "Notebook 1: Python as an Engineering Calculator",
        "Use named variables, engineering units, Ohm's law, power, and assertions.",
        "Ohm's law, power, metric prefixes, and significant figures.",
        [
            md("## Working demonstration\n\nRun the cell unchanged first. Then explain each unit conversion.\n"),
            code(
                "voltage_V = 9.0\n"
                "resistance_ohm = 1000.0\n"
                "current_A = voltage_V / resistance_ohm\n"
                "power_W = voltage_V * current_A\n\n"
                "print(f'Current: {current_A * 1000:.2f} mA')\n"
                "print(f'Power: {power_W * 1000:.1f} mW')\n"
                "assert abs(current_A - 0.009) < 1e-12\n"
                "assert abs(power_W - 0.081) < 1e-12\n"
            ),
            md(
                "## Purposeful problem\n\nA 12.0 V supply drives a 2.2 kΩ resistor. Calculate current and power. "
                "Write values in base SI units in code, then report mA and mW with sensible significant figures.\n"
            ),
            code(
                "# Student code: replace None, then run the assertions.\n"
                "supply_V = 12.0\n"
                "load_ohm = 2200.0\n"
                "load_current_A = None\n"
                "load_power_W = None\n\n"
                "# assert abs(load_current_A - supply_V / load_ohm) < 1e-12\n"
                "# assert abs(load_power_W - supply_V * load_current_A) < 1e-12\n"
            ),
            md(
                "## Independent challenge\n\nChoose a standard resistor for a teacher-approved voltage and target current. "
                "Check the actual current and resistor power after choosing the available value.\n\n"
                "### Hints\n\n1. Start with $R=V/I$.\n"
                "2. Search the course reference for **standard 5% resistor values**.\n"
                "3. Compare calculated power with a rating that has a reasonable safety margin.\n"
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
                "**Monday:** follow the teacher demonstration and predict each result before the code runs.  \n"
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
                "5. **Repair:** change the smallest necessary part and explain why the documentation supports it.\n"
                "6. **Verify:** rerun from a clean kernel and use an independent equation, unit check, or residual.\n\n"
                "Your debugging record must include the exact error or wrong result, search terms, source consulted, the "
                "requirement you found, the repair, and the verification evidence.\n"
            ),
            md(
                "### Difficulty ladder\n\n"
                "1. **Working example:** run known-good code and explain its output.\n"
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
                "**Documentation evidence:** Copy the exact error, write the function signature you found, identify the "
                "incorrect keyword, and link [the official `numpy.round` page](https://numpy.org/doc/stable/reference/generated/numpy.round.html).\n"
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
                "**Documentation evidence:** What shape does `numpy.linalg.solve` require for $A$? Quote or paraphrase "
                "the requirement, link [the official `numpy.linalg.solve` page](https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html), "
                "repair the array, and show the verified solution below.\n"
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
                "## Parameter investigation: predict before running\n\n"
                "Predict what will happen to $I_1$ and $I_2$ as the left-loop source rises from "
                "$6\\,\\mathrm{V}$ to $14\\,\\mathrm{V}$.\n\n"
                "**Prediction:** ___\n"
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
                "## Reflection — complete in full sentences\n\n"
                "1. What two equations and variable order did you use?\n"
                "2. Did the handwritten, teacher, and Python answers agree?\n"
                "3. What does a near-zero residual establish?\n"
                "4. How could wrong circuit equations still produce near-zero residuals?\n"
                "5. Was your source-change prediction correct? Explain the trend.\n"
                "6. What does a negative current mean physically?\n"
            ),
            md(
                "## Progressive submission checkpoints\n\n"
                "### Checkpoint 1 — Tuesday\n\n"
                "- [ ] Original equations, variable order, and units are visible.\n"
                "- [ ] $A$, $\\mathbf{b}$, the solution, and residuals are complete.\n"
                "- [ ] Stage 1 records the exact keyword error, function signature, documentation source, and minimal repair.\n"
                "- [ ] The comparison table is complete.\n"
                "- [ ] A prediction appears before the parameter sweep.\n"
                "- [ ] The graph or complete numerical table is present.\n"
                "- [ ] The assigned reflections are answered and the `.ipynb` is saved and submitted.\n\n"
                "### Checkpoint 2 — later exception-driven debugging lesson\n\n"
                "- [ ] Stage 2 records the exact shape error, search terms, official source, requirement, repair, and verification.\n\n"
                "### Checkpoint 3 — later wrong-answer debugging lesson\n\n"
                "- [ ] Stage 3 repairs the wrong unit and protects the result with a unit-aware check.\n"
                "- [ ] All six reflections are complete by the final checkpoint.\n"
            ),
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
                "**The challenge:** explain every sign instead of copying the finished matrix.\n\n"
                "**The stumbling block:** the Loop 2 shared-resistor sign changes because the loop traversal is against $I_3$.\n\n"
                "**The investigation:** use the official NumPy or SymPy documentation when a solver object is unfamiliar.\n\n"
                "**The verification:** use residuals, substitution, and $I_3=I_1-I_2$.\n"
            ),
            md(
                "### Student explanation - replace every prompt\n\n"
                "**Current definitions:** Explain $I_1$, $I_2$, and $I_3$.\n\n"
                "**Loop 1 signs:** Explain why the terms are $+10$, $-3I_1$, and $-2I_3$.\n\n"
                "**Loop 1 algebra:** Show every line from KVL to $5I_1-2I_2=10$.\n\n"
                "**Loop 2 signs:** Explain why the shared-resistor term is $+2I_3$.\n\n"
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
                "| Quantity | Original work | Released answer | NumPy | SymPy exact | Agreement and explanation |\n"
                "|:--|--:|--:|--:|--:|:--|\n"
                "| $I_1$ | ___ | ___ | ___ | ___ | ___ |\n"
                "| $I_2$ | ___ | ___ | ___ | ___ | ___ |\n"
                "| $I_3$ | ___ | ___ | ___ | ___ | ___ |\n"
            ),
            md(
                "## Part B - transfer the method to Question 5\n\n"
                "Do not begin with the released Question 5 answer. Your job is to generate the matrix from the circuit and algebra. "
                "The symbols $a_{11}$ through $a_{22}$ and $b_1,b_2$ below are placeholders, not Question 5 values.\n\n"
                "### B1. Current definitions\n\n"
                "Replace each prompt with a complete answer:\n\n"
                "1. What directions did you choose for $I_1$, $I_2$, and $I_3$?\n"
                "2. Is $I_3=I_1-I_2$ or $I_3=I_2-I_1$ for your arrows? Why?\n"
                "3. Which terms are rises and which are drops in Loop 1?\n"
                "4. Which terms are rises and which are drops in Loop 2?\n\n"
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
                "**Challenge:** read both matrix rows back as equations, then explain why a solver can produce a clean result even when the copied coefficients represent the wrong circuit.\n\n"
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
                "## Reflection - complete in full sentences\n\n"
                "1. Which Loop 2 sign was easiest to miss, and why?\n"
                "2. How did standard form determine the matrix rows?\n"
                "3. Why did SymPy show fractions while NumPy showed decimals?\n"
                "4. What did the residual verify? What could it not verify?\n"
                "5. What step changed your understanding of the two-loop circuit?\n"
                "6. Which Question 5 helper question caught an error before the solver ran?\n"
            ),
            md(
                "## Save and submit\n\n"
                "- [ ] Current definitions and both complete derivations are visible.\n"
                "- [ ] The variable order, units, $A$, and $\\mathbf{b}$ are visible.\n"
                "- [ ] NumPy currents and residuals are visible.\n"
                "- [ ] SymPy exact fractions and $I_3$ are visible.\n"
                "- [ ] The comparison table and reflections are complete.\n"
                "- [ ] Question 5 includes both seven-line rearrangements and two boxed standard-form equations.\n"
                "- [ ] The Question 5 coefficient table, matrix, and two row read-backs are complete.\n"
                "- [ ] Question 5 was solved only after the matrix was derived and checked.\n"
                "- [ ] Restart the kernel and run all required cells from top to bottom.\n"
                "- [ ] Save and download `studentnumber-lastname-kirchhoff-jupyter.ipynb`.\n"
                "- [ ] Reopen the downloaded notebook before submitting it.\n"
            ),
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
                "## Purposeful problem\n\nAdd a 2.2 kΩ curve to the same voltage-current graph. Predict which line has the "
                "smaller slope before running the cell, then interpret the slope in mA/V.\n"
            ),
            code("# Student code: add the second curve, labels, legend, and a numerical slope check.\n"),
            md(
                "## Independent challenge\n\nHold voltage at 9.0 V, vary resistance from 100 Ω to 10 kΩ, and graph current. "
                "Choose a linear or logarithmic horizontal scale and justify it.\n\n"
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
                "CSV, document the instrument or simulator, and explain one model or measurement limitation.\n\n"
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
                "Write a measurable success criterion before coding.\n"
            ),
            md(
                "## Plan\n\n- **What I know:**\n- **What I need to find out:**\n- **How I will know when I am right:**\n- **Variables and units:**\n- **Safety and privacy boundary:**\n"
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
                "## Your investigation\n\nCreate the smallest working calculation first. Add one change at a time. Keep a brief "
                "troubleshooting record: observation, hypothesis, test, result, and next decision.\n"
            ),
            code("# Student investigation code. Add meaningful assertions or comparison checks.\n"),
            md(
                "## Challenge and hints\n\nMake one independent design decision and defend it with evidence.\n\n"
                "1. Choose a parameter that can change the decision, not only the appearance of a graph.\n"
                "2. Search official documentation using the function name and last line of any error.\n"
                "3. Compare the final result with a second equation, limiting case, simulation, or measurement.\n"
            ),
            md(
                "## Verification and conclusion\n\nState the result with units and significant figures. Explain whether it met the "
                "success criterion, what changed after troubleshooting, and what the evidence cannot establish.\n"
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
                "Predict the voltage at one time constant before running the cell.\n"
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
                "Choose new teacher-approved resistor and capacitor values. Predict the new time constant, verify the "
                "63.2% charging point, and determine how the initial slope changes. Add assertions before interpreting the graph.\n"
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
                "and optional XL741 measurement. Explain one difference caused by sampling and one difference a real op-amp "
                "could introduce.\n\n"
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
                "Choose one component section. Change one value, predict the direction of the result before running the "
                "cell, add a second independent check, and explain one real characteristic that the model omits.\n"
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

    return {
        "01-engineering-calculator.ipynb": n1,
        "02-series-parallel-calculations.ipynb": n2,
        "03a-two-loop-to-matrix-bridge.ipynb": n3a,
        "03-kirchhoff-systems.ipynb": n3,
        "04-graph-electrical-relationships.ipynb": n4,
        "05-experimental-data-analysis.ipynb": n5,
        "06-engineering-investigation.ipynb": n6,
        "07-rc-op-amp-calculus-bridge.ipynb": n7,
        "08-electronic-components-from-zero.ipynb": n8,
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
        "Open the nine notebooks in order or use the notebook matched to the current electronics lesson.\n"
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
