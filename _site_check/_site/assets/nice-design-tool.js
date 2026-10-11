(() => {
  const state = {
    nextId: 1
  };

  const $ = (selector) => document.querySelector(selector);
  const $$ = (selector) => Array.from(document.querySelectorAll(selector));

  const newId = (prefix) => `${prefix}-${state.nextId++}`;

  const escapeHtml = (value = "") => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const escapeMarkdownCell = (value = "") => String(value)
    .trim()
    .replaceAll("|", "\\|")
    .replace(/\r?\n/g, "<br>");

  const textOrEmpty = (value) => String(value || "").trim();

  function createRemoveButton() {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "nice-remove";
    button.setAttribute("aria-label", "Remove row");
    button.innerHTML = "&times;";
    button.addEventListener("click", () => {
      const row = button.closest("tr");
      row.remove();
      syncEvaluationTables();
      renderReport();
    });
    return button;
  }

  function createInput(placeholder, className, type = "text") {
    const input = document.createElement("input");
    input.type = type;
    input.placeholder = placeholder;
    input.className = className;
    input.addEventListener("input", handleInput);
    input.addEventListener("change", handleInput);
    return input;
  }

  function createTextarea(placeholder, className) {
    const textarea = document.createElement("textarea");
    textarea.placeholder = placeholder;
    textarea.className = className;
    textarea.addEventListener("input", handleInput);
    return textarea;
  }

  function addNeed() {
    const id = newId("need");
    const row = document.createElement("tr");
    row.dataset.rowId = id;

    const needCell = document.createElement("td");
    needCell.appendChild(createInput("Specific, testable requirement", "need-text"));

    const whyCell = document.createElement("td");
    whyCell.appendChild(createTextarea("Why is this required?", "need-why"));

    const testCell = document.createElement("td");
    testCell.appendChild(createTextarea("How will you prove pass or fail?", "need-test"));

    const removeCell = document.createElement("td");
    removeCell.className = "nice-remove-cell";
    removeCell.appendChild(createRemoveButton());

    row.append(needCell, whyCell, testCell, removeCell);
    $("#nice-needs-body").appendChild(row);
    syncEvaluationTables();
    renderReport();
  }

  function addNecessity() {
    const id = newId("necessity");
    const row = document.createElement("tr");
    row.dataset.rowId = id;

    const textCell = document.createElement("td");
    textCell.appendChild(createInput("Example: lighter is better", "necessity-text"));

    const whyCell = document.createElement("td");
    whyCell.appendChild(createTextarea("Why does this matter?", "necessity-why"));

    const importanceCell = document.createElement("td");
    const importance = createInput("1-10", "necessity-importance", "number");
    importance.min = "1";
    importance.max = "10";
    importance.step = "1";
    importanceCell.appendChild(importance);

    const removeCell = document.createElement("td");
    removeCell.className = "nice-remove-cell";
    removeCell.appendChild(createRemoveButton());

    row.append(textCell, whyCell, importanceCell, removeCell);
    $("#nice-necessities-body").appendChild(row);
    syncEvaluationTables();
    renderReport();
  }

  function addInquiry() {
    const row = document.createElement("tr");
    row.dataset.rowId = newId("inquiry");

    const investigateCell = document.createElement("td");
    investigateCell.appendChild(createTextarea("Product, user, material, process, technology...", "inquiry-topic"));

    const howCell = document.createElement("td");
    howCell.appendChild(createTextarea("Search, interview, observe, measure, test...", "inquiry-how"));

    const discoveryCell = document.createElement("td");
    discoveryCell.appendChild(createTextarea("What did you learn?", "inquiry-discovery"));

    const impactCell = document.createElement("td");
    impactCell.appendChild(createTextarea("How could this affect the design?", "inquiry-impact"));

    const removeCell = document.createElement("td");
    removeCell.className = "nice-remove-cell";
    removeCell.appendChild(createRemoveButton());

    row.append(investigateCell, howCell, discoveryCell, impactCell, removeCell);
    $("#nice-inquiry-body").appendChild(row);
    renderReport();
  }

  function handleInput() {
    syncEvaluationTables();
    renderReport();
  }

  function syncEvaluationTables() {
    const needEvalBody = $("#nice-needs-evaluation-body");
    const necessityEvalBody = $("#nice-necessities-evaluation-body");

    const currentNeedIds = new Set($$("#nice-needs-body tr").map((row) => row.dataset.rowId));
    const currentNecessityIds = new Set($$("#nice-necessities-body tr").map((row) => row.dataset.rowId));

    $$("#nice-needs-evaluation-body tr").forEach((row) => {
      if (!currentNeedIds.has(row.dataset.sourceId)) row.remove();
    });

    $$("#nice-necessities-evaluation-body tr").forEach((row) => {
      if (!currentNecessityIds.has(row.dataset.sourceId)) row.remove();
    });

    $$("#nice-needs-body tr").forEach((sourceRow) => {
      const id = sourceRow.dataset.rowId;
      const label = textOrEmpty(sourceRow.querySelector(".need-text")?.value) || "Untitled need";
      let evalRow = needEvalBody.querySelector(`tr[data-source-id="${id}"]`);

      if (!evalRow) {
        evalRow = document.createElement("tr");
        evalRow.dataset.sourceId = id;

        const labelCell = document.createElement("td");
        labelCell.className = "need-eval-label";

        const resultCell = document.createElement("td");
        const select = document.createElement("select");
        select.className = "need-eval-result";
        ["Not tested", "Pass", "Fail"].forEach((value) => {
          const option = document.createElement("option");
          option.value = value;
          option.textContent = value;
          select.appendChild(option);
        });
        select.addEventListener("change", renderReport);
        resultCell.appendChild(select);

        const evidenceCell = document.createElement("td");
        evidenceCell.appendChild(createTextarea("Measurement, observation, or test result", "need-eval-evidence"));

        evalRow.append(labelCell, resultCell, evidenceCell);
        needEvalBody.appendChild(evalRow);
      }

      evalRow.querySelector(".need-eval-label").textContent = label;
    });

    $$("#nice-necessities-body tr").forEach((sourceRow) => {
      const id = sourceRow.dataset.rowId;
      const label = textOrEmpty(sourceRow.querySelector(".necessity-text")?.value) || "Untitled necessity";
      const importance = textOrEmpty(sourceRow.querySelector(".necessity-importance")?.value);
      let evalRow = necessityEvalBody.querySelector(`tr[data-source-id="${id}"]`);

      if (!evalRow) {
        evalRow = document.createElement("tr");
        evalRow.dataset.sourceId = id;

        const labelCell = document.createElement("td");
        labelCell.className = "necessity-eval-label";

        const importanceCell = document.createElement("td");
        importanceCell.className = "necessity-eval-importance";

        const scoreCell = document.createElement("td");
        const score = createInput("1-10", "necessity-eval-score", "number");
        score.min = "1";
        score.max = "10";
        score.step = "1";
        scoreCell.appendChild(score);

        const weightedCell = document.createElement("td");
        weightedCell.className = "necessity-eval-weighted";
        weightedCell.textContent = "-";

        const evidenceCell = document.createElement("td");
        evidenceCell.appendChild(createTextarea("Why did you give it this score?", "necessity-eval-evidence"));

        evalRow.append(labelCell, importanceCell, scoreCell, weightedCell, evidenceCell);
        necessityEvalBody.appendChild(evalRow);
      }

      evalRow.querySelector(".necessity-eval-label").textContent = label;
      evalRow.querySelector(".necessity-eval-importance").textContent = importance || "-";

      const scoreValue = Number(evalRow.querySelector(".necessity-eval-score")?.value || 0);
      const importanceValue = Number(importance || 0);
      evalRow.querySelector(".necessity-eval-weighted").textContent = importanceValue && scoreValue
        ? `${importanceValue * scoreValue}/100`
        : "-";
    });
  }

  function getData() {
    const needs = $$("#nice-needs-body tr").map((row) => {
      const id = row.dataset.rowId;
      const evalRow = $(`#nice-needs-evaluation-body tr[data-source-id="${id}"]`);
      return {
        id,
        need: textOrEmpty(row.querySelector(".need-text")?.value),
        why: textOrEmpty(row.querySelector(".need-why")?.value),
        test: textOrEmpty(row.querySelector(".need-test")?.value),
        result: textOrEmpty(evalRow?.querySelector(".need-eval-result")?.value),
        evidence: textOrEmpty(evalRow?.querySelector(".need-eval-evidence")?.value)
      };
    }).filter((row) => row.need || row.why || row.test || row.evidence);

    const necessities = $$("#nice-necessities-body tr").map((row) => {
      const id = row.dataset.rowId;
      const evalRow = $(`#nice-necessities-evaluation-body tr[data-source-id="${id}"]`);
      const importance = textOrEmpty(row.querySelector(".necessity-importance")?.value);
      const score = textOrEmpty(evalRow?.querySelector(".necessity-eval-score")?.value);
      const weighted = Number(importance || 0) && Number(score || 0)
        ? Number(importance) * Number(score)
        : "";
      return {
        id,
        necessity: textOrEmpty(row.querySelector(".necessity-text")?.value),
        why: textOrEmpty(row.querySelector(".necessity-why")?.value),
        importance,
        score,
        weighted,
        evidence: textOrEmpty(evalRow?.querySelector(".necessity-eval-evidence")?.value)
      };
    }).filter((row) => row.necessity || row.why || row.importance || row.score || row.evidence);

    const inquiry = $$("#nice-inquiry-body tr").map((row) => ({
      topic: textOrEmpty(row.querySelector(".inquiry-topic")?.value),
      how: textOrEmpty(row.querySelector(".inquiry-how")?.value),
      discovery: textOrEmpty(row.querySelector(".inquiry-discovery")?.value),
      impact: textOrEmpty(row.querySelector(".inquiry-impact")?.value)
    })).filter((row) => row.topic || row.how || row.discovery || row.impact);

    return {
      title: textOrEmpty($("#nice-project-title").value) || "NICE Design Project",
      author: textOrEmpty($("#nice-author").value),
      situation: textOrEmpty($("#nice-situation").value),
      needs,
      necessities,
      inquiry,
      created: textOrEmpty($("#nice-created").value),
      communicated: textOrEmpty($("#nice-communicated").value),
      feedback: textOrEmpty($("#nice-feedback").value),
      createEvidence: textOrEmpty($("#nice-create-evidence").value),
      situationChanged: $("#nice-situation-changed").value,
      requirementsChanged: $("#nice-requirements-changed").value,
      learned: textOrEmpty($("#nice-learned").value),
      next: textOrEmpty($("#nice-next").value)
    };
  }

  function htmlParagraph(value) {
    if (!value) return '<p class="nice-empty">Not documented yet.</p>';
    return `<p>${escapeHtml(value).replace(/\r?\n/g, "<br>")}</p>`;
  }

  function renderReport() {
    const data = getData();
    const needRows = data.needs.length
      ? data.needs.map((row) => `<tr><td>${escapeHtml(row.need)}</td><td>${escapeHtml(row.why)}</td><td>${escapeHtml(row.test)}</td></tr>`).join("")
      : '<tr><td colspan="3" class="nice-empty">No needs documented yet.</td></tr>';

    const necessityRows = data.necessities.length
      ? data.necessities.map((row) => `<tr><td>${escapeHtml(row.necessity)}</td><td>${escapeHtml(row.why)}</td><td>${escapeHtml(row.importance || "-")}</td></tr>`).join("")
      : '<tr><td colspan="3" class="nice-empty">No necessities documented yet.</td></tr>';

    const inquiryRows = data.inquiry.length
      ? data.inquiry.map((row) => `<tr><td>${escapeHtml(row.topic)}</td><td>${escapeHtml(row.how)}</td><td>${escapeHtml(row.discovery)}</td><td>${escapeHtml(row.impact)}</td></tr>`).join("")
      : '<tr><td colspan="4" class="nice-empty">No inquiry documented yet.</td></tr>';

    const needEvalRows = data.needs.length
      ? data.needs.map((row) => `<tr><td>${escapeHtml(row.need || "Untitled need")}</td><td><strong>${escapeHtml(row.result || "Not tested")}</strong></td><td>${escapeHtml(row.evidence)}</td></tr>`).join("")
      : '<tr><td colspan="3" class="nice-empty">Add needs above to evaluate them here.</td></tr>';

    const necessityEvalRows = data.necessities.length
      ? data.necessities.map((row) => `<tr><td>${escapeHtml(row.necessity || "Untitled necessity")}</td><td>${escapeHtml(row.importance || "-")}</td><td>${escapeHtml(row.score || "-")}</td><td>${row.weighted !== "" ? `<span class="nice-score">${row.weighted}/100</span>` : "-"}</td><td>${escapeHtml(row.evidence)}</td></tr>`).join("")
      : '<tr><td colspan="5" class="nice-empty">Add necessities above to score them here.</td></tr>';

    $("#nice-report").innerHTML = `
      <h1>${escapeHtml(data.title)}</h1>
      ${data.author ? `<p><strong>Name or team:</strong> ${escapeHtml(data.author)}</p>` : ""}

      <h2>Situation</h2>
      ${htmlParagraph(data.situation)}

      <h2>N: Needs &amp; Necessities</h2>
      <h3>Needs</h3>
      <table><thead><tr><th>Need</th><th>Why</th><th>Test</th></tr></thead><tbody>${needRows}</tbody></table>
      <h3>Necessities</h3>
      <table><thead><tr><th>Necessity</th><th>Why it matters</th><th>Importance /10</th></tr></thead><tbody>${necessityRows}</tbody></table>

      <h2>I: Inquire &amp; Investigate</h2>
      <table><thead><tr><th>Investigated</th><th>How</th><th>Discovery</th><th>Design impact</th></tr></thead><tbody>${inquiryRows}</tbody></table>

      <h2>C: Create &amp; Communicate</h2>
      <h3>What was created?</h3>${htmlParagraph(data.created)}
      <h3>How was it communicated or tested?</h3>${htmlParagraph(data.communicated)}
      <h3>Feedback</h3>${htmlParagraph(data.feedback)}
      <h3>Evidence</h3>${htmlParagraph(data.createEvidence)}

      <h2>E: Evaluate</h2>
      <h3>Needs</h3>
      <table><thead><tr><th>Need</th><th>Result</th><th>Evidence or notes</th></tr></thead><tbody>${needEvalRows}</tbody></table>
      <h3>Necessities</h3>
      <table><thead><tr><th>Necessity</th><th>Importance /10</th><th>Result /10</th><th>Weighted result</th><th>Evidence or notes</th></tr></thead><tbody>${necessityEvalRows}</tbody></table>
      <p><strong>Did the situation change?</strong> ${escapeHtml(data.situationChanged)}</p>
      <p><strong>Do any needs or necessities need to change?</strong> ${escapeHtml(data.requirementsChanged)}</p>
      <h3>What did you learn?</h3>${htmlParagraph(data.learned)}
      <h3>What should happen next?</h3>${htmlParagraph(data.next)}
    `;
  }

  function markdownTable(headers, rows) {
    const header = `| ${headers.join(" | ")} |`;
    const divider = `| ${headers.map(() => "---").join(" | ")} |`;
    const body = rows.map((row) => `| ${row.map(escapeMarkdownCell).join(" | ")} |`).join("\n");
    return [header, divider, body].filter(Boolean).join("\n");
  }

  function buildMarkdown() {
    const data = getData();
    const lines = [`# ${data.title}`, ""];

    if (data.author) lines.push(`**Name or team:** ${data.author}`, "");

    lines.push("## Situation", "", data.situation || "_Not documented yet._", "");

    lines.push("## N: Needs & Necessities", "", "### Needs", "");
    lines.push(data.needs.length
      ? markdownTable(["Need", "Why", "Test"], data.needs.map((row) => [row.need, row.why, row.test]))
      : "_No needs documented yet._");
    lines.push("", "### Necessities", "");
    lines.push(data.necessities.length
      ? markdownTable(["Necessity", "Why it matters", "Importance /10"], data.necessities.map((row) => [row.necessity, row.why, row.importance]))
      : "_No necessities documented yet._");

    lines.push("", "## I: Inquire & Investigate", "");
    lines.push(data.inquiry.length
      ? markdownTable(["Investigated", "How", "Discovery", "Design impact"], data.inquiry.map((row) => [row.topic, row.how, row.discovery, row.impact]))
      : "_No inquiry documented yet._");

    lines.push("", "## C: Create & Communicate", "",
      "### What was created?", "", data.created || "_Not documented yet._", "",
      "### How was it communicated or tested?", "", data.communicated || "_Not documented yet._", "",
      "### Feedback", "", data.feedback || "_Not documented yet._", "",
      "### Evidence", "", data.createEvidence || "_Not documented yet._", "");

    lines.push("## E: Evaluate", "", "### Needs", "");
    lines.push(data.needs.length
      ? markdownTable(["Need", "Result", "Evidence or notes"], data.needs.map((row) => [row.need, row.result || "Not tested", row.evidence]))
      : "_No needs to evaluate yet._");

    lines.push("", "### Necessities", "");
    lines.push(data.necessities.length
      ? markdownTable(["Necessity", "Importance /10", "Result /10", "Weighted result", "Evidence or notes"], data.necessities.map((row) => [
          row.necessity,
          row.importance,
          row.score,
          row.weighted !== "" ? `${row.weighted}/100` : "",
          row.evidence
        ]))
      : "_No necessities to evaluate yet._");

    lines.push("",
      `**Did the situation change?** ${data.situationChanged}`,
      "",
      `**Do any needs or necessities need to change?** ${data.requirementsChanged}`,
      "",
      "### What did you learn?", "", data.learned || "_Not documented yet._", "",
      "### What should happen next?", "", data.next || "_Not documented yet._", "",
      "---", "",
      "NICE is iterative: Situation -> N -> I -> C -> E -> repeat.", "");

    return lines.join("\n");
  }

  function safeFileName() {
    const title = getData().title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 60);
    return title || "nice-design-project";
  }

  function downloadBlob(content, mimeType, extension) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `${safeFileName()}.${extension}`;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function downloadMarkdown() {
    downloadBlob(buildMarkdown(), "text/markdown;charset=utf-8", "md");
  }

  function downloadWord() {
    const title = escapeHtml(getData().title);
    const report = $("#nice-report").innerHTML;
    const html = `<!doctype html>
<html><head><meta charset="utf-8"><title>${title}</title>
<style>
body{font-family:Arial,sans-serif;line-height:1.45;color:#111;max-width:900px;margin:36px auto;padding:0 24px}
h1{font-size:26pt}h2{font-size:18pt;margin-top:24pt;border-bottom:1px solid #bbb;padding-bottom:4pt}h3{font-size:13pt;margin-top:16pt}
table{width:100%;border-collapse:collapse;margin:8pt 0 16pt}th,td{border:1px solid #aaa;padding:6pt;text-align:left;vertical-align:top}.nice-empty{color:#666;font-style:italic}
</style></head><body>${report}</body></html>`;
    downloadBlob("\ufeff" + html, "application/msword;charset=utf-8", "doc");
  }

  async function copyMarkdown() {
    const button = $("#nice-copy-md");
    const original = button.textContent;
    try {
      await navigator.clipboard.writeText(buildMarkdown());
      button.textContent = "Copied";
    } catch (error) {
      const textarea = document.createElement("textarea");
      textarea.value = buildMarkdown();
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      textarea.remove();
      button.textContent = "Copied";
    }
    setTimeout(() => { button.textContent = original; }, 1400);
  }

  $("#nice-add-need").addEventListener("click", addNeed);
  $("#nice-add-necessity").addEventListener("click", addNecessity);
  $("#nice-add-inquiry").addEventListener("click", addInquiry);
  $("#nice-download-md").addEventListener("click", downloadMarkdown);
  $("#nice-download-doc").addEventListener("click", downloadWord);
  $("#nice-save-pdf").addEventListener("click", () => window.print());
  $("#nice-copy-md").addEventListener("click", copyMarkdown);

  [
    "#nice-project-title",
    "#nice-author",
    "#nice-situation",
    "#nice-created",
    "#nice-communicated",
    "#nice-feedback",
    "#nice-create-evidence",
    "#nice-situation-changed",
    "#nice-requirements-changed",
    "#nice-learned",
    "#nice-next"
  ].forEach((selector) => {
    const element = $(selector);
    element.addEventListener("input", handleInput);
    element.addEventListener("change", handleInput);
  });

  addNeed();
  addNecessity();
  addInquiry();
  renderReport();
})();
