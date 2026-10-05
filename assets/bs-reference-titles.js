(function () {
  "use strict";

  const titles = {
    "ref-grob2016": "Grob's Basic Electronics",
    "ref-opencircuits2023": "Open Circuits: The Inner Beauty of Electronic Components",
    "ref-ngss2013": "Appendix I: Engineering Design in the NGSS",
    "ref-nistairmf2023": "Artificial Intelligence Risk Management Framework (AI RMF 1.0)",
    "ref-nistgenai2024": "Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile",
    "ref-unescoai2023": "Guidance for Generative AI in Education and Research",
    "ref-privacyai2023": "Principles for Responsible, Trustworthy and Privacy-Protective Generative AI Technologies",
    "ref-w3csvg2023": "Scalable Vector Graphics (SVG) 2",
    "ref-mdnimages2025": "Image File Type and Format Guide",
    "ref-pencil2dmanual": "Pencil2D User Manual",
    "ref-htmlstandard": "HTML Living Standard",
    "ref-mdnurl2025": "What Is a URL?",
    "ref-onshapesketch": "Sketch Basics",
    "ref-onshapefeatures": "Feature Basics",
    "ref-onshapeassembly": "Assembly Basics",
    "ref-blendermesh": "Introduction to Meshes",
    "ref-blenderanimation": "Introduction to Keyframes",
    "ref-nistadditive": "Additive Manufacturing",
    "ref-threemfcore": "3MF Core Specification, Version 1.3.0",
    "ref-prusaslicer": "PrusaSlicer Knowledge Base",
    "ref-glowforgealignment": "Alignment",
    "ref-glowforgeautofocus": "About Autofocus",
    "ref-nasafasteners1990": "Fastener Design Manual",
    "ref-cipocopyright": "A Guide to Copyright",
    "ref-wcag22": "Web Content Accessibility Guidelines (WCAG) 2.2",
    "ref-troteclaserparameters": "Laser Parameters",
    "ref-cengel2008": "Introduction to Thermodynamics and Heat Transfer",
    "ref-chapra2010": "Numerical Methods for Engineers"
  };

  function referenceId(link) {
    try {
      const url = new URL(link.getAttribute("href"), document.baseURI);
      return url.hash.slice(1);
    } catch (_error) {
      return "";
    }
  }

  function addReferenceTitles(root) {
    (root || document).querySelectorAll(
      'a[href*="references.html#ref-"], a[href*="references.qmd#ref-"]'
    ).forEach(function (link) {
      const title = titles[referenceId(link)];
      if (!title) return;

      link.classList.add("bs-reference-link");
      link.title = title;

      const label = link.getAttribute("aria-label") || link.textContent.trim();
      if (label && !label.includes(title)) {
        link.setAttribute("aria-label", label + ": " + title);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      addReferenceTitles(document);
    });
  } else {
    addReferenceTitles(document);
  }
})();
