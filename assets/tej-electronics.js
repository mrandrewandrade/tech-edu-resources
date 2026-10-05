document.addEventListener("DOMContentLoaded", () => {
  const catalogue = document.querySelector("[data-tej-catalogue]");
  if (!catalogue) return;

  const search = document.querySelector("[data-tej-search]");
  const status = document.querySelector("[data-tej-status]");
  const access = document.querySelector("[data-tej-access]");
  const count = document.querySelector("[data-tej-count]");
  const cards = [...catalogue.querySelectorAll("[data-tej-module]")];

  function applyFilters() {
    const query = (search?.value || "").trim().toLowerCase();
    const statusValue = status?.value || "all";
    const accessValue = access?.value || "all";
    let shown = 0;

    cards.forEach((card) => {
      const text = `${card.dataset.search || ""} ${card.textContent}`.toLowerCase();
      const matches = (!query || text.includes(query)) &&
        (statusValue === "all" || card.dataset.status === statusValue) &&
        (accessValue === "all" || card.dataset.access === accessValue);
      card.hidden = !matches;
      if (matches) shown += 1;
    });

    if (count) count.textContent = `${shown} module${shown === 1 ? "" : "s"} shown`;
  }

  [search, status, access].forEach((control) => control?.addEventListener("input", applyFilters));
  applyFilters();
});
