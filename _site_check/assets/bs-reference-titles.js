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

  function createReferencePanel() {
    const panel = document.createElement("aside");
    panel.className = "bs-reference-panel";
    panel.hidden = true;
    panel.setAttribute("aria-hidden", "true");
    panel.setAttribute("aria-labelledby", "bs-reference-panel-title");
    panel.innerHTML =
      '<div class="bs-reference-panel-heading">' +
      '<div><p class="bs-reference-panel-kicker">Reference</p>' +
      '<h2 id="bs-reference-panel-title" tabindex="-1">Source</h2></div>' +
      '<button type="button" class="bs-reference-panel-close" ' +
      'aria-label="Close reference">Close</button></div>' +
      '<p class="bs-reference-panel-locator" data-bs-reference-locator></p>' +
      '<div class="bs-reference-panel-content" data-bs-reference-content></div>' +
      '<p class="bs-reference-panel-actions">' +
      '<a data-bs-reference-page>View on references page</a></p>';
    document.body.appendChild(panel);
    return panel;
  }

  function referencePageUrl(link) {
    const url = new URL(link.getAttribute("href"), document.baseURI);
    url.pathname = url.pathname.replace(/\.qmd$/, ".html");
    return url;
  }

  function initializeReferencePanel() {
    const links = Array.from(document.querySelectorAll("a.bs-reference-link"));
    if (links.length === 0) return;

    const panel = createReferencePanel();
    const title = panel.querySelector("#bs-reference-panel-title");
    const locator = panel.querySelector("[data-bs-reference-locator]");
    const content = panel.querySelector("[data-bs-reference-content]");
    const pageLink = panel.querySelector("[data-bs-reference-page]");
    const close = panel.querySelector(".bs-reference-panel-close");
    const pagePromises = new Map();
    let returnFocus = null;

    function hidePanel() {
      panel.hidden = true;
      panel.setAttribute("aria-hidden", "true");
      document.body.classList.remove("bs-reference-panel-open");
      if (returnFocus && document.contains(returnFocus)) {
        returnFocus.focus({ preventScroll: true });
      }
      returnFocus = null;
    }

    function loadReferencePage(url) {
      const key = url.origin + url.pathname;
      if (!pagePromises.has(key)) {
        pagePromises.set(
          key,
          fetch(key, { credentials: "same-origin" })
            .then(function (response) {
              if (!response.ok) throw new Error("Reference page unavailable");
              return response.text();
            })
            .then(function (html) {
              return new DOMParser().parseFromString(html, "text/html");
            })
        );
      }
      return pagePromises.get(key);
    }

    function showReference(link) {
      const url = referencePageUrl(link);
      const id = referenceId(link);
      const sourceTitle = titles[id] || "Reference";
      const citationLabel = link.textContent.trim();

      returnFocus = link;
      title.textContent = sourceTitle;
      locator.textContent = citationLabel ? "Cited here as " + citationLabel : "";
      locator.hidden = !citationLabel;
      content.replaceChildren();
      const loading = document.createElement("p");
      loading.textContent = "Loading reference…";
      content.appendChild(loading);
      pageLink.href = url.href;
      panel.hidden = false;
      panel.setAttribute("aria-hidden", "false");
      document.body.classList.add("bs-reference-panel-open");
      title.focus({ preventScroll: true });

      loadReferencePage(url)
        .then(function (referenceDocument) {
          const entry = referenceDocument.getElementById(id);
          if (!entry) throw new Error("Reference entry unavailable");
          const clonedEntry = entry.cloneNode(true);
          clonedEntry.removeAttribute("id");
          clonedEntry.querySelectorAll("a[href]").forEach(function (sourceLink) {
            sourceLink.href = new URL(
              sourceLink.getAttribute("href"),
              url.href
            ).href;
          });
          content.replaceChildren(clonedEntry);
        })
        .catch(function () {
          const message = document.createElement("p");
          message.textContent =
            "The reference could not be loaded here. Open it on the references page instead.";
          content.replaceChildren(message);
        });
    }

    links.forEach(function (link) {
      link.addEventListener("click", function (event) {
        if (
          event.defaultPrevented ||
          event.button !== 0 ||
          event.metaKey ||
          event.ctrlKey ||
          event.shiftKey ||
          event.altKey
        ) {
          return;
        }
        event.preventDefault();
        showReference(link);
      });
    });

    close.addEventListener("click", hidePanel);
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !panel.hidden) hidePanel();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      addReferenceTitles(document);
      initializeReferencePanel();
    });
  } else {
    addReferenceTitles(document);
    initializeReferencePanel();
  }
})();
