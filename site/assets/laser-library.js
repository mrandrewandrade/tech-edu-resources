(function () {
  "use strict";

  const PAGE_SIZE = 48;
  const FILTERS = ["type", "shop", "function", "geometry", "material", "operation", "editor", "level", "theme"];

  function normalise(value) {
    return String(value || "")
      .normalize("NFKD")
      .replace(/[\u0300-\u036f]/g, "")
      .trim()
      .toLowerCase();
  }

  function titleCase(value) {
    return String(value || "")
      .replace(/[-_]+/g, " ")
      .replace(/\b\w/g, function (letter) { return letter.toUpperCase(); });
  }

  function uniqueSorted(values) {
    return Array.from(new Set(values.filter(Boolean))).sort(function (a, b) {
      return a.localeCompare(b);
    });
  }

  function valueFor(asset, key) {
    if (key === "type") return asset.category;
    if (key === "shop") return asset.shop;
    if (key === "function") return asset.tool_family === "none" ? "" : asset.tool_family;
    if (key === "geometry") return asset.subcategory;
    if (key === "material") return asset.material && asset.material.name;
    if (key === "operation") return asset.operations || [];
    if (key === "editor") return asset.editors || [];
    if (key === "level") return asset.skill_level;
    if (key === "theme") return asset.category === "themed-starters" ? asset.subcategory : "";
    return "";
  }

  function matchesValue(asset, key, expected) {
    if (!expected) return true;
    const actual = valueFor(asset, key);
    if (Array.isArray(actual)) return actual.some(function (value) { return normalise(value) === expected; });
    return normalise(actual) === expected;
  }

  function appendText(parent, tag, text, className) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    element.textContent = text;
    parent.appendChild(element);
    return element;
  }

  function actionLink(parent, text, href, primary, download) {
    const link = document.createElement("a");
    link.className = "bs-laser-button" + (primary ? " bs-laser-button-primary" : "");
    link.textContent = text;
    link.href = href;
    if (download) link.setAttribute("download", "");
    parent.appendChild(link);
  }

  function makeCard(asset) {
    const card = document.createElement("article");
    card.className = "bs-laser-card";
    card.dataset.assetId = asset.id;

    const previewLink = document.createElement("a");
    previewLink.className = "bs-laser-card-preview";
    const svgUrl = "https://raw.githubusercontent.com/mrandrewandrade/assets/master/laser/" + asset.files.svg;
    previewLink.href = svgUrl;
    previewLink.setAttribute("aria-label", "Open canonical SVG for " + asset.title);
    const image = document.createElement("img");
    image.src = "../../assets/laser-library/" + asset.files.preview.replace(/^generated\//, "");
    image.alt = "Preview of " + asset.title;
    image.loading = "lazy";
    previewLink.appendChild(image);
    card.appendChild(previewLink);

    const body = document.createElement("div");
    body.className = "bs-laser-card-body";
    appendText(body, "p", titleCase(asset.category) + " · " + titleCase(asset.subcategory), "bs-laser-kicker");
    appendText(body, "h3", asset.title, "bs-laser-card-title");
    appendText(body, "p", asset.description, "bs-laser-card-description");

    const facts = document.createElement("dl");
    facts.className = "bs-laser-card-facts";
    const factValues = [
      ["Size", asset.dimensions.width + " × " + asset.dimensions.height + " " + asset.units],
      ["Operations", asset.operations.join(" + ")],
      ["Material", (asset.material && asset.material.name ? asset.material.name : "Measure selected stock") + " · measure sheet"],
      ["Shop", titleCase(asset.shop)],
      ["Level", titleCase(asset.skill_level)]
    ];
    factValues.forEach(function (fact) {
      const wrapper = document.createElement("div");
      appendText(wrapper, "dt", fact[0]);
      appendText(wrapper, "dd", fact[1]);
      facts.appendChild(wrapper);
    });
    body.appendChild(facts);

    if (asset.fit_type !== "none") {
      appendText(body, "p", "Fit warning: " + titleCase(asset.fit_type) + ". Measure stock and cut a calibration sample first.", "bs-laser-fit-warning");
    }

    const actions = document.createElement("div");
    actions.className = "bs-laser-actions";
    actionLink(actions, "Open SVG", svgUrl, true, false);
    actionLink(actions, "Download", svgUrl, false, true);
    if ((asset.editors || []).includes("Veccy")) {
      actionLink(actions, "Veccy recipe", "#veccy-guidance", false, false);
    }
    body.appendChild(actions);
    appendText(body, "p", asset.license + " · " + asset.review_status + " · " + asset.source_reference, "bs-laser-license-note");
    card.appendChild(body);
    return card;
  }

  function init(root) {
    const catalogUrl = root.dataset.catalog;
    const grid = root.querySelector("[data-laser-grid]");
    const search = root.querySelector("[data-laser-search]");
    const count = root.querySelector("[data-laser-count]");
    const empty = root.querySelector("[data-laser-empty]");
    const clear = root.querySelector("[data-laser-clear]");
    const more = root.querySelector("[data-laser-more]");
    const filterDetails = root.querySelector("[data-laser-filter-details]");
    const filterCount = root.querySelector("[data-laser-filter-count]");
    const selects = Array.from(root.querySelectorAll("[data-laser-filter]"));
    let assets = [];
    let shown = PAGE_SIZE;

    function readState() {
      const params = new URLSearchParams(window.location.search);
      search.value = params.get("q") || "";
      selects.forEach(function (select) { select.value = params.get(select.dataset.laserFilter) || ""; });
    }

    function writeState() {
      const url = new URL(window.location.href);
      const values = { q: normalise(search.value) };
      selects.forEach(function (select) { values[select.dataset.laserFilter] = select.value; });
      Object.keys(values).forEach(function (key) {
        if (values[key]) url.searchParams.set(key, values[key]);
        else url.searchParams.delete(key);
      });
      window.history.replaceState({}, "", url.pathname + url.search + url.hash);
    }

    function filteredAssets() {
      const query = normalise(search.value);
      const queryTokens = query.split(/\s+/).filter(Boolean);
      const active = {};
      selects.forEach(function (select) { active[select.dataset.laserFilter] = normalise(select.value); });
      return assets.filter(function (asset) {
        const haystack = normalise([
          asset.id, asset.title, asset.description, asset.category, asset.subcategory,
          asset.shop, asset.tool_family, (asset.tags || []).join(" "),
          (asset.operations || []).join(" "), (asset.editors || []).join(" ")
        ].join(" "));
        const matchesQuery = !query || haystack.includes(query) || queryTokens.every(function (token) {
          return haystack.includes(token) || (token.endsWith("s") && haystack.includes(token.slice(0, -1)));
        });
        return matchesQuery && FILTERS.every(function (key) {
          return matchesValue(asset, key, active[key]);
        });
      });
    }

    function render(syncUrl) {
      if (syncUrl !== false) writeState();
      const matches = filteredAssets();
      const visible = matches.slice(0, shown);
      grid.replaceChildren();
      const fragment = document.createDocumentFragment();
      visible.forEach(function (asset) { fragment.appendChild(makeCard(asset)); });
      grid.appendChild(fragment);
      count.textContent = matches.length + (matches.length === 1 ? " asset matches" : " assets match") +
        (matches.length > visible.length ? " · showing " + visible.length : "");
      empty.hidden = matches.length !== 0;
      more.hidden = matches.length <= visible.length;
      const activeFilterCount = selects.filter(function (select) { return Boolean(select.value); }).length;
      filterCount.textContent = String(activeFilterCount);
      filterCount.parentElement.setAttribute("aria-label", "Filters, " + activeFilterCount + " active");
      clear.hidden = !normalise(search.value) && activeFilterCount === 0;
    }

    function populateFilters() {
      selects.forEach(function (select) {
        const key = select.dataset.laserFilter;
        const values = uniqueSorted(assets.flatMap(function (asset) {
          const value = valueFor(asset, key);
          return Array.isArray(value) ? value : [value];
        }));
        values.forEach(function (value) {
          const option = document.createElement("option");
          option.value = normalise(value);
          option.textContent = titleCase(value);
          select.appendChild(option);
        });
      });
    }

    function resetPageAndRender() {
      shown = PAGE_SIZE;
      render(true);
    }

    fetch(catalogUrl)
      .then(function (response) {
        if (!response.ok) throw new Error("Catalogue request failed: " + response.status);
        return response.json();
      })
      .then(function (document) {
        assets = document.assets || [];
        root.querySelectorAll("[data-laser-total]").forEach(function (element) {
          element.textContent = assets.length + " purpose-built generated assets";
        });
        populateFilters();
        readState();
        render(false);
      })
      .catch(function (error) {
        count.textContent = "The catalogue could not be loaded.";
        empty.hidden = false;
        empty.textContent = error.message;
      });

    search.addEventListener("input", resetPageAndRender);
    selects.forEach(function (select) { select.addEventListener("change", resetPageAndRender); });
    clear.addEventListener("click", function () {
      search.value = "";
      selects.forEach(function (select) { select.value = ""; });
      filterDetails.open = false;
      resetPageAndRender();
      search.focus();
    });
    more.addEventListener("click", function () { shown += PAGE_SIZE; render(false); });
    root.addEventListener("click", function (event) {
      const preset = event.target.closest("[data-laser-preset]");
      if (!preset) return;
      search.value = "";
      selects.forEach(function (select) { select.value = ""; });
      const target = root.querySelector('[data-laser-filter="' + preset.dataset.laserPreset + '"]');
      if (!target) return;
      target.value = normalise(preset.dataset.laserValue);
      filterDetails.open = false;
      resetPageAndRender();
      root.querySelector("[data-laser-controls]").scrollIntoView({ behavior: "smooth", block: "start" });
    });
    window.addEventListener("popstate", function () { readState(); shown = PAGE_SIZE; render(false); });
  }

  function start() {
    document.querySelectorAll("[data-laser-library]").forEach(init);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, { once: true });
  else start();
})();
