(function () {
  "use strict";

  const sourceByKey = new Map(
    (window.terEquationSources || []).map(function (entry) {
      return [entry.key, entry.source];
    })
  );

  function announce(button, message) {
    const original = button.dataset.originalLabel || button.textContent;
    button.dataset.originalLabel = original;
    button.textContent = message;
    window.setTimeout(function () {
      button.textContent = original;
    }, 1300);
  }

  async function copyLatex(button, source) {
    await navigator.clipboard.writeText(source);
    announce(button, "Copied");
  }

  async function copyEquation(button, equation, source) {
    const math = equation.querySelector("mjx-assistive-mml math");
    const plainText = math
      ? math.textContent.replace(/\s+/g, " ").trim()
      : source;
    const html = math
      ? math.outerHTML
      : '<span role="math">' + plainText.replace(/[&<>"]/g, function (character) {
          return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[character];
        }) + "</span>";

    if (navigator.clipboard.write && window.ClipboardItem) {
      await navigator.clipboard.write([
        new ClipboardItem({
          "text/plain": new Blob([plainText], { type: "text/plain" }),
          "text/html": new Blob([html], { type: "text/html" })
        })
      ]);
    } else {
      await navigator.clipboard.writeText(plainText);
    }
    announce(button, "Copied");
  }

  function createButton(label, handler) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "ter-equation-copy";
    button.textContent = label;
    button.setAttribute("aria-label", label);
    button.addEventListener("click", function () {
      Promise.resolve(handler(button)).catch(function () {
        announce(button, "Copy failed");
      });
    });
    return button;
  }

  function enhanceEquations() {
    document.querySelectorAll("span.math.display[data-ter-equation-key]").forEach(function (equation) {
      if (equation.closest(".ter-equation-shell")) return;

      const source = sourceByKey.get(equation.dataset.terEquationKey) || "";
      const paragraph = equation.closest("p");
      if (!paragraph || !paragraph.parentNode) return;

      const shell = document.createElement("div");
      shell.className = "ter-equation-shell";
      paragraph.parentNode.insertBefore(shell, paragraph);
      shell.appendChild(paragraph);

      const toolbar = document.createElement("div");
      toolbar.className = "ter-equation-toolbar";
      toolbar.setAttribute("aria-label", "Equation copy tools");
      toolbar.appendChild(createButton("Copy equation", function (button) {
        return copyEquation(button, equation, source);
      }));
      toolbar.appendChild(createButton("Copy LaTeX", function (button) {
        return copyLatex(button, source);
      }));
      shell.appendChild(toolbar);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enhanceEquations, { once: true });
  } else {
    enhanceEquations();
  }
})();
