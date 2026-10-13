## Why this is useful

“Looks different” is not a reliable contrast test. Two colours can have different hues and still be almost the same lightness. Measure the pair, then test the real output.

## Use a measurable minimum

::: {.ad-contrast-demo aria-label="Visual comparison of passing and failing contrast"}
::: {.ad-contrast-sample .is-strong}
<span>Clear contrast</span>

**12.6:1** · comfortably above the minimum
:::
::: {.ad-contrast-sample .is-minimum}
<span>Minimum contrast</span>

**4.5:1** · passes for normal-size text
:::
::: {.ad-contrast-sample .is-failing}
<span>Weak contrast</span>

**2.0:1** · fails for text and essential graphics
:::
:::

Large text, at least 24 px regular or about 18.5 px bold, can use **3:1**. Essential icons, controls, and graphic boundaries also need **3:1**. Do not round: 4.49:1 does not meet 4.5:1.

These are WCAG 2.2 Level AA thresholds for digital content. They are a starting point, not a promise that every person or output device will find the result easy to use. Aim higher when you can.

## Compare the guide's examples

::: {.ad-large-example}
![Black text on white and white text on black are labelled good contrast. Pale green on yellow and pale grey on light grey are labelled bad contrast.](../../assets/accessible-design/source-guide/good-bad-contrast.png)

### Light-dark difference matters

The top two pairs have a large value difference. The bottom pairs do not. [Source noted in the guide](https://aatt.d.umn.edu/february-color-and-contrast).
:::

::: {.ad-large-example}
![Six colour pairs place bad contrast examples in a left column and better contrast versions in a right column.](../../assets/accessible-design/source-guide/contrast-grid.png)

### Hue is not enough

Changing the background value makes each word easier to separate, even when the hue remains similar. [Source noted in the guide](https://www.localguidesconnect.com/t5/General-Discussion/Web-Accessibility-Good-Contrast/td-p/3115065).
:::

::: {.ad-large-example}
![Green text on red and pale blue text on blue are labelled bad choices. Pale yellow text on dark green is labelled a good choice.](../../assets/accessible-design/source-guide/colour-choices.png)

### Some pairs interfere

Red-green and similar-blue pairs can fail for different reasons. The final pair adds a clear light-dark difference. [Source noted in the guide](https://www.sitepoint.com/typography-cheat-sheet/).
:::

## Do not use colour alone

If colour communicates a status, category, warning, or selected state, add another cue.

::: {.ad-rule-grid}
::: {.ad-rule-card}
### Add a label

Write **Pass** and **Revise**, not just green and red dots.
:::

::: {.ad-rule-card}
### Add a shape or pattern

Use different marker shapes, line styles, or fill patterns in a chart.
:::

::: {.ad-rule-card}
### Add position

Keep categories in a stable order and label them directly.
:::

::: {.ad-rule-card}
### Add emphasis

Use weight, size, an icon, or a border together with colour.
:::
:::

## Test the real result

1. Check the design at its final size, not only while zoomed in.
2. Use a contrast checker for digital text and essential graphics.
3. View a greyscale copy.
4. Test on the target projector, printer, material, cutter, or engraver.
5. Show it without explaining it. Ask what the person noticed first and what was difficult to understand.
6. Revise and test again.

For fabrication, make a small sample before the final piece. Check thin lines, small gaps, inside spaces, surface finish, and lighting.

## Check your work

- Normal-size text meets at least 4.5:1.
- Large text and essential non-text graphics meet at least 3:1.
- Colour is never the only signal.
- Text over a photograph has a dependable background or a tested halo.
- The real output has been checked from the expected viewing distance.

## Summary

Measure contrast, add a second cue, and test the actual output. Return to the [Accessible Design guide](index.qmd) and use the four checks before publishing.

Sources: [W3C Understanding Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [W3C Understanding Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), and [W3C Understanding Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html).
