(function () {
  "use strict";

  function moveLoreTaxonomyToMargin() {
    if (!document.body.classList.contains("bs-research-article")) {
      return;
    }

    const categories = document.querySelector(".quarto-categories");
    const margin = document.querySelector("#quarto-margin-sidebar");
    if (!categories || !margin || margin.querySelector(".commons-lore-taxonomy")) {
      return;
    }

    const links = Array.from(categories.querySelectorAll("a, .quarto-category"));
    if (!links.length) {
      categories.remove();
      return;
    }

    const panel = document.createElement("section");
    panel.className = "commons-lore-taxonomy";
    panel.setAttribute("aria-label", "Article themes");

    const heading = document.createElement("div");
    heading.className = "commons-lore-taxonomy-heading";
    heading.textContent = "Themes";
    panel.appendChild(heading);

    const list = document.createElement("div");
    list.className = "commons-lore-taxonomy-list";

    links.forEach(function (source) {
      const item = document.createElement("span");
      item.className = "commons-lore-taxonomy-item";
      item.textContent = source.textContent.trim();
      list.appendChild(item);
    });

    panel.appendChild(list);
    categories.remove();

    const toc = margin.querySelector("#TOC");
    if (toc) {
      toc.insertAdjacentElement("afterend", panel);
    } else {
      margin.prepend(panel);
    }
  }

  function compactLoreMetadataLabels() {
    if (!document.body.classList.contains("bs-research-article")) {
      return;
    }
    document.querySelectorAll(".quarto-title-meta-heading").forEach(function (heading) {
      const text = heading.textContent.trim().toLowerCase();
      if (text === "author" || text === "published" || text === "date") {
        heading.classList.add("commons-lore-meta-label");
      }
    });
  }

  function init() {
    moveLoreTaxonomyToMargin();
    compactLoreMetadataLabels();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
