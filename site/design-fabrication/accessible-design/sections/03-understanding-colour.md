## Why this is useful

Colour is easier to control when you separate what kind of colour it is from how intense and how light it is. The same model helps with screens, print, paint, and accessibility checks.

## How the eye receives colour information

::: {.ad-concept-figure}
![A simplified eye points to the retina and optic nerve, then labels long, medium, and short wavelength cones plus rods.](../../assets/accessible-design/source-guide/human-eye.png)

### Four receptor types

The guide simplifies the retina into three kinds of cone cells for colour and rod cells that are especially useful in low light.
:::

::: {.ad-concept-figure}
![A graph plots the overlapping response ranges of short, medium, and long wavelength cones and rods from 400 to 700 nanometres.](../../assets/accessible-design/source-guide/cone-response.jpg)

### Overlapping responses

The curves overlap. The brain interprets a pattern of signals rather than receiving a single red, green, or blue value. [Source noted in the guide](https://www.researchgate.net/publication/313657827_The_Information_Visualization_Thematic_Head_to_Head_with_Color_Blindness).
:::

## Separate hue, saturation, and value

::: {.ad-concept-figure}
![Three vertical scales show hue changing through the spectrum, red losing saturation toward grey, and value changing from white to black.](../../assets/accessible-design/source-guide/hue-saturation-value.png)

### Hue, saturation, value

**Hue** identifies the colour family. **Saturation** describes intensity or greyness. **Value** describes lightness or darkness. [Source](https://www.virtualartacademy.com/three-components-of-color/).
:::

::: {.ad-concept-figure}
![A colour wheel appears beside a greyscale copy. Yellow becomes very light while several blue, green, and purple hues become similar dark greys.](../../assets/accessible-design/source-guide/colour-value-wheel.png)

### Different hue, similar value

Strongly different colours can have nearly the same lightness. This is why a monochrome check can reveal weak contrast. [Source](https://www.virtualartacademy.com/value-in-art-for-beginners/).
:::

## Connect the model to design software

::: {.ad-two-up}
::: {.ad-figure-card}
![A rainbow comparison labelled RGB on the left and CMYK on the right. The CMYK side is duller in several regions.](../../assets/accessible-design/source-guide/rgb-cmyk.png)

### RGB screen, CMYK print

Screens mix emitted red, green, and blue light. Many printing systems use cyan, magenta, yellow, and black inks. A bright screen colour may reproduce with less intensity in print.
:::

::: {.ad-figure-card}
![Two white rectangles cover a pink flower photograph. The high-opacity rectangle hides the flower and the low-opacity rectangle allows it to show through.](../../assets/accessible-design/source-guide/opacity.jpg)

### Opacity controls what shows through

High opacity blocks more of the layer below. Low opacity allows more of it to affect the result. [Source noted in the guide](https://www.herronprinting.com/resources/the-ideas-collection/5-opacity-tips-you-should-know/).
:::
:::

<details>
<summary>Go deeper: the Munsell colour solid</summary>

::: {.ad-wide-figure}
![A three-dimensional Munsell colour solid places value on a vertical black-to-white axis, hue around the axis, and chroma moving outward.](../../assets/accessible-design/source-guide/munsell.png)
:::

<p class="ad-caption">The Munsell system organizes colour in three dimensions: value moves vertically, hue moves around the centre, and chroma moves outward. Source: <a href="https://www.britannica.com/science/Munsell-color-system">Encyclopaedia Britannica</a>.</p>

</details>

## Try it

Choose one hue in your design tool.

1. Make a vivid and a muted version by changing saturation.
2. Make a light and a dark version by changing value.
3. Convert the set to greyscale.
4. Record which differences remain visible without hue.

## Check your work

- You can name whether you changed hue, saturation, value, or opacity.
- Important colours still separate in greyscale.
- You previewed a screen design on the target screen or a print design in print.
- Opacity does not create an unpredictable background for text.

## Summary

Hue tells you the colour family, saturation tells you its intensity, and value tells you its lightness. Value is the most direct bridge to readable contrast. Continue to [Contrast, Emphasis & Output](contrast-and-output.qmd).
