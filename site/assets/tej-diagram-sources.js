(function () {
  "use strict";

  function fallbackCopy(text) {
    const area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    const copied = document.execCommand("copy");
    area.remove();
    return copied;
  }

  async function copySource(button, source) {
    const response = await fetch(source, { credentials: "same-origin" });
    if (!response.ok) throw new Error("Unable to load diagram source.");
    const text = await response.text();
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
    } else if (!fallbackCopy(text)) {
      throw new Error("Clipboard access is unavailable.");
    }
    const original = button.textContent;
    button.textContent = "Copied LaTeX";
    window.setTimeout(function () { button.textContent = original; }, 1800);
  }

  function enhanceDiagramSources() {
    document.querySelectorAll(".ter-circuit-figure[data-diagram-source]").forEach(function (figure) {
      if (figure.querySelector(".ter-diagram-source-tools")) return;
      const source = figure.dataset.diagramSource;
      const tools = document.createElement("div");
      tools.className = "ter-diagram-source-tools";

      const copy = document.createElement("button");
      copy.type = "button";
      copy.className = "ter-diagram-source-copy";
      copy.textContent = "Copy LaTeX";
      copy.addEventListener("click", async function () {
        copy.disabled = true;
        try {
          await copySource(copy, source);
        } catch (error) {
          copy.textContent = "Copy failed";
          window.setTimeout(function () { copy.textContent = "Copy LaTeX"; }, 2200);
        } finally {
          copy.disabled = false;
        }
      });

      const view = document.createElement("a");
      view.className = "ter-diagram-source-link";
      view.href = source;
      view.textContent = "View LaTeX source";
      view.setAttribute("target", "_blank");
      view.setAttribute("rel", "noopener");

      tools.append(copy, view);
      figure.appendChild(tools);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enhanceDiagramSources);
  } else {
    enhanceDiagramSources();
  }
})();
