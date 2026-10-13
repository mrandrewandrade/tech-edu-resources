(function () {
  "use strict";

  const sourceByKey = new Map(
    (window.terEquationSources || []).map(function (entry) {
      return [entry.key, entry.source];
    })
  );
  let nextEquationKey = sourceByKey.size + 1;

  function equationSource(equation) {
    return equation.textContent
      .trim()
      .replace(/^\\\[\s*/, "")
      .replace(/\s*\\\]$/, "")
      .replace(/\s*\\tag\{[^}]+\}\s*$/, "")
      .trim();
  }

  function equationsIn(root) {
    const equations = [];
    if (root && root.matches && root.matches("span.math.display")) {
      equations.push(root);
    }
    if (root && root.querySelectorAll) {
      root.querySelectorAll("span.math.display").forEach(function (equation) {
        equations.push(equation);
      });
    }
    return equations;
  }

  function registerEquationSources(root) {
    const equations = equationsIn(root);
    window.terEquationSources = window.terEquationSources || [];

    equations.forEach(function (equation) {
      let key = equation.dataset.terEquationKey;
      if (!key) {
        do {
          key = "ter-equation-" + nextEquationKey;
          nextEquationKey += 1;
        } while (sourceByKey.has(key));
        equation.dataset.terEquationKey = key;
      }

      if (!sourceByKey.has(key)) {
        const source = equationSource(equation);
        sourceByKey.set(key, source);
        window.terEquationSources.push({ key: key, source: source });
      }
    });

    return equations;
  }

  function announce(button, message) {
    const original = button.dataset.originalLabel || button.textContent;
    button.dataset.originalLabel = original;
    button.textContent = message;
    window.setTimeout(function () {
      button.textContent = original;
    }, 1300);
  }

  function legacyCopy(text) {
    const field = document.createElement("textarea");
    field.value = text;
    field.setAttribute("readonly", "");
    field.style.position = "fixed";
    field.style.left = "-9999px";
    document.body.appendChild(field);
    field.select();
    const copied = document.execCommand("copy");
    field.remove();
    if (!copied) throw new Error("The browser did not allow copying.");
  }

  async function writeText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      try {
        await navigator.clipboard.writeText(text);
        return;
      } catch (_error) {
        // Managed browsers may deny the modern API while allowing execCommand.
      }
    }
    legacyCopy(text);
  }

  async function copyLatex(button, source) {
    await writeText(source);
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

    if (navigator.clipboard && navigator.clipboard.write && window.ClipboardItem) {
      try {
        await navigator.clipboard.write([
          new ClipboardItem({
            "text/plain": new Blob([plainText], { type: "text/plain" }),
            "text/html": new Blob([html], { type: "text/html" })
          })
        ]);
        announce(button, "Copied");
        return;
      } catch (_error) {
        // Fall through to the plain-text copy path.
      }
    }
    await writeText(plainText);
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

  function enhanceEquations(root) {
    equationsIn(root || document).forEach(function (equation) {
      if (!equation.dataset.terEquationKey) return;
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

  function mountEquations(root) {
    const mountRoot = root || document;
    const equations = registerEquationSources(mountRoot);
    const pending = equations.filter(function (equation) {
      return !equation.querySelector("mjx-container");
    });

    function finish() {
      enhanceEquations(mountRoot);
    }

    if (!pending.length) {
      finish();
      return Promise.resolve();
    }

    if (window.MathJax && typeof window.MathJax.typesetPromise === "function") {
      return window.MathJax.typesetPromise(pending).then(finish, function (error) {
        finish();
        throw error;
      });
    }

    if (window.MathJax && typeof window.MathJax.typeset === "function") {
      window.MathJax.typeset(pending);
    }
    finish();
    return Promise.resolve();
  }

  window.TEREquations = window.TEREquations || {};
  window.TEREquations.mount = mountEquations;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      mountEquations(document).catch(function (error) {
        window.console.warn("Equation rendering failed", error);
      });
    }, { once: true });
  } else {
    mountEquations(document).catch(function (error) {
      window.console.warn("Equation rendering failed", error);
    });
  }
})();
