### What is Colour? (A Brief Primer for Nerds)

#### How Colours Are Perceived (Understood) by Humans

Light is an electromagnetic wave of photon particles, and when its frequency falls in the range of the visible spectrum (400–700 nanometers (nm) or 400 Terahertz THz to 800 THz), the human eye can detect, and the brain can then understand colour in the form of a saturated hue.

Graphic Caption: Visual description of the relationship between Frequency (Hz) and Wavelength (meters) for different types of light including visible (for human sight).

Source: https://physics.stackexchange.com/questions/334734/how-is-hue-saturation-and-brightness-of-colours-explained-via-em-and-qed

We will learn about different colour representation models soon, first let’s understand how the human mind perceives or understands colour.  A simplification of the eye is shown on the next page, but at the back of our eye (the retina), we have colour sensors (a layer of photoreceptor cells) that captures incoming light (photons) and transmits the information using electrical and chemical signals through neural pathways (optical nerve) to the brain.  A chart also on the next page shows the wavelength sensitivity ranges for each of these cones.

Graphic Caption: Simplified version of the human eye where the 4 types of photoreceptors in the Retina of the eye are shown.  L cones for large wavelength (red light), M cones for medium wavelength (green light), S Cones for small wavelength (blue light) and Rods for sensing low light.

Source (modified): https://www.researchgate.net/publication/313657827_The_Information_Visualization_Thematic_Head_to_Head_with_Color_Blindness

Graphic Caption: This chart shows how sensitive the eye's four types of receptors are to different light when it enters the eye.   When various ligh t enters your eye, the photoreceptors react based on the number of photons at different wavelengths and their sensitivity to those wavelengths to give you colour.

The 4 types of photoreceptors create a data signal (rather than a stream of photons) that is sent to the brain through the optical nerve and the body’s nervous system.  The brain uses this data signal to create 3 components or parts: Hue, Saturation and Brightness Value to understand colour.  These 3 signal components are not just red, green and blue values, because remember, there are rod cells which also give a different (non hue) signal than the cone cells do.  Confused?  Read on!

#### 3 Component Colour Representation

Colour can be broken into three parts or components: Hue, Saturation and Value as shown below.

Graphic Caption: Hue (left) is what most people think of when using the term colour, it corresponds to its position in the spectrum (known as spectral wavelength).  The saturation (middle) of a colour is its degree of richness, intensity, purity, or greyness.  Brightness Value (right) is the relative lightness or darkness of a colour in greyscale.

Source: https://www.virtualartacademy.com/three-components-of-color/

Examples of different hues are: red, orange, yellow, green, blue, violet.  In scientific (nerd) terms, hue is the combination of different spectral wavelengths of a colour that produces the perception of being red, yellow, blue, and so on.

Other commonly used terms for saturation are intensity or chroma, which is technically a different attribute, but to simplify things most people treat it the same.  For example, cadmium orange is a high saturation colour, and burnt sienna is a low saturation colour. Both colours are the same hue (orange).  Similarly, yellow ochre is less saturated than cadmium yellow, though both are considered yellow.

Brightness Value is the relative lightness or darkness of a colour. This is what you see when you take a black and white photograph.When you convert a full color wheel image to monochrome (black and white) which removes the hue, you can clearly see each one has a different “value” in Art, Science and Engineering)

Graphic Caption: Graphic in full colour (left) and black and white (right) shows how many colours in the colour wheel have similar values, despite having very different hues.

If you want to understand this better, please read this article, which is the source for the image: https://www.virtualartacademy.com/value-in-art-for-beginners/

When placed next to each other, some colours (e.g. RG or YRGY or RPBG or PB) would have very little contrast in value and your viewer’s eye/brain may find it difficult to identify which colour has more importance in your product.

Now that you understand how the brain understands colour (Hue, Saturation and Value), let’s understand how humans represent colours in software and hardware.

#### How Colours Are Represented in Software and Hardware

This video (made by the author) explains this concept:

There are so many different ways to represent colours that there are multiple textbooks on the subject (called Colour Spaces,  Colour Profiles, or Colour Models).  This guide goes over the basics to help you with creating high quality graphics with accessibility in mind.  But first, let's learn how most graphic softwares represent colours in many different ways.  You may notice different ways to select colour, with the simplest being RGB values or  Hex code (#) which Google Docs uses (show below):

Graphics Caption: Google Docs has a Hex code (#) and R. G. B. number input.

Other more sophisticated systems use many different ways to represent colour, so let’s learn the acronyms used in common systems so you can recognize how colour is represented as you use these tools.

#### Colour Selection in Raster Image Editors with Examples

Raster graphics editors such as GNU Image Manipulation Program, PhotoPea.com or Adobe Photoshop may use many different colour selection systems (e.g. RGB, LCh, HSV, Hex HTML #, CMYk, HSB/HSB, and Lab) as shown in the graphics below. What do all those letters and numbers represent?  Read on!

Graphics Caption: Colour picker tool from GNU Image Manipulation Program has many ways to select colour such as RGB, LCh, HSV, HTML Notation, CMYk, Hue selector and a Colour Triangle Wheel.  Adobe Photoshop is similar.

Graphics Caption: PhotoPea.com Colour picker tool which uses HSB, RGB, Lab system numbers and percentages to represent colours.

#### Colour Selection in Vector Image Editors with Examples

Vector graphics editors such as Inkscape, vecteezy.com and Adobe Illustrator also have similar types of colour input.  In Inkscape, you will find 5 different colour selection modes: RGB, CMYk, HSL, HSV, and a Color Wheel.  Let’s see each one briefly (selecting sky blue colour) , then dive into how each one works in the next section.

Graphics Caption: In the RBG model (left) we can see the Red, Green and Blue values.  In the CMYK model (right), we can see values on how printers print colours (Cyan, Magenta, Yellow and Blank ink).  The numbers represent the values of each.

Graphics Caption: HSL (left) and HSV (right) breaks the colour down into how humans perceive colours (Hue, Saturation, Lightness/Value).Graphics Caption: HSL (left)

Graphics Caption: The color wheel offers an alternative way to select Hue, Saturation Brightness Values.

Observant readers may notice a little field labelled RGBA in the bottom right corner of the dialog: it is the name of the colour in hexadecimal (hex) code, as it is used in a web page’s style sheet (CSS).  The Hex code for the sky blue colour selected was 729fcfff.  If you try and use that use that code to highlight the text, (e.g. like this), you can only enter 729fcf (6 digits total), because the the last two digits (e.g. ff) appended to the code determine the opacity or ‘alpha value’ (shown in the slider labelled A in each graphic above).  Google Docs does not allow opacity for text, so the Hex code is shorter. Why not?  Wait…what the heck is Opacity or alpha value in graphics?

##### What is opacity and alpha channel?

RGBa colour value model are an extension of RGB model with an alpha channel - which specifies the opacity for a colour.  Opacity correlates to transparency or the amount of light that passes through an object. An object with high opacity has low transparency, meaning little or no light can pass through.

Graphic Caption:  High Opacity (right) does not let light (and colours) through, while low opacity does.  For paper printing the thickness and material of paper should be considered.

Source: https://www.herronprinting.com/resources/the-ideas-collection/5-opacity-tips-you-should-know/

If an object is completely opaque like a solid wood or metal door, no light can pass through, and anything behind the door will not be visible. In contrast, a partially opaque object, like a window covered by a thin curtain, allows light to pass through and objects behind the window will be somewhat visible.

In design software, the fill typically defaults to 100% opacity. As the opacity is lowered, the layer will become more transparent and any colours or shapes behind the layer will become visible, as shown in the graphic below.

Graphic Caption:   Different percentages of opacity show that it is opposite of transparency & represents the degree to which the content will be hidden behind an element.

Source: https://www.codecademy.com/resources/docs/uiux/opacity

The opacity property is used in the image to describe the transparency of the image. The value of opacity lies between 0.0 to 1.0 where a low value represents high transparency and a high value represents low transparency. The percentage of opacity is calculated as Opacity % = Opacity x 100.

Graphic Caption: 100% Opacity (0% Transparency) is shown at the top, and 50% opacity shown at the bottom.

Source: https://www.geeksforgeeks.org/css-opacity-transparency/

Different software have different ways of representing opacity/transparency/fill, and you can change the opacity value with code in the source above (click the link above and go try it out for yourself, I will wait for you back here).  Now you are back, let’s dive into each of the colour models in detail, now that we know where we can use them.

##### Screens vs Print Representation of Colours

Screens such as computer monitors and modern televisions (TVs)  use a 3 channel model with lights: RGB (Red, Green, Blue), while printing uses a CMYK (Cyan, Magenta, Yellow and Black) model (due to common ink colours).

Graphic Caption:  A comparison of RGB and CMYK colour models.  This image demonstrates the difference between how colours will look on a computer monitor (RGB) compared to how they might reproduce in a particular CMYK print process.

Graphic caption: RGB is additive colour mixing: Three overlapping light bulbs in a vacuum, adding together to create white.  CMYk is subtractive colour mixing: Three splotches of ink or paint on white paper, subtracting together to turn the paper black.

Let’s dig into the more complex systems, closer to how our brain interprets colour.

#### Munsell Colour System

Using Munsell colour notation, each colour has a logical and visual relationship to all other colours, so it makes it easier to select colours for our graphic.  This is particularly important when selecting colours for an audience with different needs.

The Munsell Color Theory is like a 3D model where each color has three parts: hue (where on the colour wheel), saturation (how intense it is), and brightness (how light or dark it is). See the diagrams below for some visualisations of this system which measures:

(Brightness) value is measured vertically from 0 (black) to 10 (white)

Hue is measured by angles (degrees) around the color wheel (from 0 to 360 degrees) 0 (or 360) is red, 120 is green, 240 is blue. It is formally defined as “the degree to which a stimulus can be described as red, green, blue, and yellow” (source).

Saturation (chroma or intensity) measured radially outward from the neutral (gray) vertical axis

Graphics Caption: Value (vertical), Chroma (horizontal) and Hue (circular)

Source: https://www.britannica.com/science/Munsell-color-system

Graphic caption: value, measured vertically (up and down) on the core cylinder from 0 (black) to 10 (white). hue, measured by angles (degrees) around horizontal circles and saturation measured radially outward (left and right) from the neutral (gray) vertical axis

Source: https://en.wikipedia.org/wiki/Munsell_color_system

Graphic caption: Munsell colour system broken into three parts: Hue which distinguishes one colour from another on a wheel, Value which indicates the lightness or darkness of the colour and chroma which indicates the intensity (strength or weakness) of a colour.

Source: https://www.britannica.com/science/Munsell-color-system

#### Graphic caption: Three dimensional view of the Munsell colour system

Source: https://www.britannica.com/science/Munsell-color-system

Now if we go back to the colour wheel selector, each of the three dimensions make sense:

Angles around the colour wheel give us the hue value .  A hue is set on a selected vertex of a triangle.

Moving across the right (clockwise) side of the triangle gives us the saturation value.

Moving across the opposite side of the triangle gives the brightness value.

This video explains it:

Exactly 260 seconds in the colour wheel triangle is explained in detail with examples:

https://youtu.be/KgUu_6HQJYg?t=260
