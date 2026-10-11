document.addEventListener("DOMContentLoaded", () => {
  const roadmap = document.querySelector("[data-tej-roadmap]");
  const panel = document.querySelector("[data-tej-roadmap-filters]");
  if (!roadmap || !panel) return;

  const search = panel.querySelector("[data-tej-roadmap-search]");
  const status = panel.querySelector("[data-tej-roadmap-status]");
  const pathway = panel.querySelector("[data-tej-roadmap-pathway]");
  const access = panel.querySelector("[data-tej-roadmap-access]");
  const count = document.querySelector("[data-tej-roadmap-count]");
  const empty = document.querySelector("[data-tej-roadmap-empty]");
  const cards = [...roadmap.querySelectorAll("[data-tej-roadmap-module]")];

  function applyFilters() {
    const query = (search?.value || "").trim().toLowerCase();
    const statusValue = status?.value || "all";
    const pathwayValue = pathway?.value || "all";
    const accessValue = access?.value || "all";
    let shown = 0;

    cards.forEach((card) => {
      const haystack = `${card.dataset.search || ""} ${card.textContent}`.toLowerCase();
      const matches = (!query || haystack.includes(query)) &&
        (statusValue === "all" || card.dataset.status === statusValue) &&
        (pathwayValue === "all" || card.dataset.pathway === pathwayValue) &&
        (accessValue === "all" || card.dataset.access === accessValue);
      card.hidden = !matches;
      if (matches) shown += 1;
    });

    roadmap.querySelectorAll(".tej-roadmap-module-grid").forEach((grid) => {
      const unitSection = grid.closest("section");
      if (unitSection) unitSection.hidden = !grid.querySelector("[data-tej-roadmap-module]:not([hidden])");
    });

    if (count) count.textContent = `${shown} module${shown === 1 ? "" : "s"} shown`;
    if (empty) empty.hidden = shown !== 0;
  }

  [search, status, pathway, access].forEach((control) => control?.addEventListener("input", applyFilters));
  applyFilters();
});
