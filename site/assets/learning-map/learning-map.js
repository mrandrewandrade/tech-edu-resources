(function () {
  "use strict";

  const root = document.querySelector("[data-learning-worlds]");
  if (!root) return;

  const dataUrl = root.dataset.manifest;
  const typeMarks = { hub: "●", portal: "↗", lesson: "•", project: "◆", safety: "!", portfolio: "★", help: "?" };
  const state = { data: null, byId: new Map(), current: "commons-hub", visited: new Set(["commons-hub"]), view: "map" };

  const $ = (selector) => root.querySelector(selector);
  const status = $("[data-map-status]");
  const map = $("[data-map-canvas]");
  const pathLayer = $("[data-path-layer]");
  const nodeLayer = $("[data-node-layer]");
  const detail = $("[data-node-detail]");
  const list = $("[data-map-list]");
  const search = $("[data-map-search]");

  function announce(message) { status.textContent = message; }

  function loadProgress() {
    try {
      const saved = JSON.parse(localStorage.getItem(state.data.storage_key));
      if (saved && state.byId.has(saved.current)) state.current = saved.current;
      if (saved && Array.isArray(saved.visited)) {
        state.visited = new Set(saved.visited.filter((id) => state.byId.has(id)));
        state.visited.add("commons-hub");
      }
    } catch (_) { /* A disabled or malformed local store should never block lessons. */ }
  }

  function saveProgress() {
    try {
      localStorage.setItem(state.data.storage_key, JSON.stringify({ current: state.current, visited: [...state.visited] }));
    } catch (_) { /* The map remains fully usable without storage. */ }
  }

  function edgeKey(a, b) { return [a, b].sort().join("--"); }

  function renderPaths() {
    const seen = new Set();
    pathLayer.replaceChildren();
    state.data.nodes.forEach((node) => {
      node.neighbours.forEach((id) => {
        const key = edgeKey(node.id, id);
        if (seen.has(key)) return;
        seen.add(key);
        const other = state.byId.get(id);
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", node.x);
        line.setAttribute("y1", node.y);
        line.setAttribute("x2", other.x);
        line.setAttribute("y2", other.y);
        line.dataset.edge = key;
        pathLayer.append(line);
      });
    });
  }

  function renderNodes() {
    nodeLayer.replaceChildren();
    state.data.nodes.forEach((node) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `world-node world-node--${node.world} world-node--${node.type}`;
      button.style.left = `${node.x}%`;
      button.style.top = `${node.y}%`;
      button.dataset.nodeId = node.id;
      button.setAttribute("aria-label", `${node.title}. ${node.status}. ${node.summary}`);
      button.innerHTML = `<span class="world-node__mark" aria-hidden="true">${typeMarks[node.type]}</span><span class="world-node__label">${node.title}</span>`;
      button.addEventListener("click", () => moveTo(node.id));
      button.addEventListener("keydown", (event) => handleNodeKey(event, node));
      nodeLayer.append(button);
    });
    updateNodeState();
  }

  function updateNodeState() {
    root.querySelectorAll("[data-node-id]").forEach((element) => {
      const id = element.dataset.nodeId;
      const isCurrent = id === state.current;
      element.classList.toggle("is-current", isCurrent);
      element.classList.toggle("is-visited", state.visited.has(id));
      if (element.matches("button")) element.setAttribute("aria-current", isCurrent ? "location" : "false");
    });
    pathLayer.querySelectorAll("line").forEach((line) => {
      const [a, b] = line.dataset.edge.split("--");
      line.classList.toggle("is-travelled", state.visited.has(a) && state.visited.has(b));
      line.classList.toggle("is-nearby", a === state.current || b === state.current);
    });
  }

  function moveTo(id, options = {}) {
    const node = state.byId.get(id);
    if (!node) return;
    const currentNode = state.byId.get(state.current);
    const connected = id === state.current || currentNode.neighbours.includes(id);
    if (!connected) {
      showDetail(node);
      announce(`${node.title} is not connected to your current stop. Open its lesson directly, or follow the map paths from ${currentNode.title}.`);
      if (options.focus) nodeLayer.querySelector(`[data-node-id="${CSS.escape(id)}"]`)?.focus();
      return;
    }
    state.current = id;
    state.visited.add(id);
    saveProgress();
    updateNodeState();
    showDetail(node);
    announce(`Moved to ${node.title}. Visited means explored, not mastered.`);
    if (options.focus) nodeLayer.querySelector(`[data-node-id="${CSS.escape(id)}"]`)?.focus();
  }

  function escapeText(value) {
    const span = document.createElement("span");
    span.textContent = value;
    return span.innerHTML;
  }

  function showDetail(node) {
    const source = node.reference
      ? `<a class="map-action map-action--reference" href="${escapeText(node.reference.url)}" target="_blank" rel="noopener">${escapeText(node.reference.title)} ↗</a>`
      : "";
    const video = node.video
      ? `<a class="map-action map-action--video" href="${escapeText(node.video)}">Watch mission video</a>`
      : "";
    detail.innerHTML = `
      <div class="detail-kicker">${escapeText(node.region)} · ${escapeText(node.status)}</div>
      <h2>${escapeText(node.title)}</h2>
      <p class="detail-summary">${escapeText(node.summary)}</p>
      <dl><div><dt>Do</dt><dd>${escapeText(node.do)}</dd></div><div><dt>Look for</dt><dd>${escapeText(node.look_for)}</dd></div></dl>
      <div class="detail-actions"><a class="map-action map-action--primary" href="${escapeText(node.href)}">Open lesson</a>${source}${video}</div>
      <p class="detail-note">A visited stop records exploration, not mastery or a grade.</p>`;
  }

  function directionalNeighbour(node, key) {
    const desired = {
      ArrowLeft: [-1, 0], a: [-1, 0], A: [-1, 0],
      ArrowRight: [1, 0], d: [1, 0], D: [1, 0],
      ArrowUp: [0, -1], w: [0, -1], W: [0, -1],
      ArrowDown: [0, 1], s: [0, 1], S: [0, 1],
    }[key];
    if (!desired) return null;
    const candidates = node.neighbours.map((id) => state.byId.get(id)).map((other) => {
      const dx = other.x - node.x;
      const dy = other.y - node.y;
      const length = Math.hypot(dx, dy) || 1;
      return { other, alignment: (dx / length) * desired[0] + (dy / length) * desired[1], distance: length };
    }).filter((item) => item.alignment > 0.15);
    candidates.sort((a, b) => b.alignment - a.alignment || a.distance - b.distance);
    return candidates[0]?.other || null;
  }

  function handleNodeKey(event, node) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      moveTo(node.id);
      if (event.key === "Enter") window.location.href = node.href;
      return;
    }
    const target = directionalNeighbour(node, event.key);
    if (target) {
      event.preventDefault();
      moveTo(target.id, { focus: true });
    }
  }

  function renderList(filter = "") {
    const query = filter.trim().toLocaleLowerCase();
    const worlds = [["hub", "Central Hub"], ["tej", "Circuit and Computing Realms"], ["tas", "Fabrication Frontier"]];
    list.replaceChildren();
    let matches = 0;
    worlds.forEach(([world, heading]) => {
      const nodes = state.data.nodes.filter((node) => node.world === world && [node.title, node.region, node.summary, node.do, node.look_for].join(" ").toLocaleLowerCase().includes(query));
      if (!nodes.length) return;
      const section = document.createElement("section");
      section.className = "map-list-group";
      section.innerHTML = `<h2>${heading}</h2>`;
      const grid = document.createElement("div");
      grid.className = "map-list-grid";
      nodes.forEach((node) => {
        matches += 1;
        const card = document.createElement("article");
        card.className = `map-list-card map-list-card--${world}`;
        card.dataset.nodeId = node.id;
        card.innerHTML = `<div class="map-list-card__meta">${typeMarks[node.type]} ${escapeText(node.region)} · ${escapeText(node.status)}</div><h3>${escapeText(node.title)}</h3><p>${escapeText(node.summary)}</p><div><button type="button" data-select-node="${node.id}">Show details</button> <a href="${escapeText(node.href)}">Open lesson</a></div>`;
        card.querySelector("button").addEventListener("click", () => { showDetail(node); setView("map"); announce(`Showing ${node.title}. Follow connected paths to move the marker, or open the lesson directly.`); });
        grid.append(card);
      });
      section.append(grid);
      list.append(section);
    });
    if (!matches) list.innerHTML = '<p class="map-empty">No map stops match that search. Try a component, tool, process, or course name.</p>';
    updateNodeState();
  }

  function setView(view) {
    state.view = view;
    root.dataset.view = view;
    root.querySelectorAll("[data-view]").forEach((button) => {
      const active = button.dataset.view === view;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    if (view === "map") map.focus({ preventScroll: true });
  }

  function resetProgress() {
    state.current = "commons-hub";
    state.visited = new Set(["commons-hub"]);
    saveProgress();
    updateNodeState();
    showDetail(state.byId.get(state.current));
    announce("Map progress reset. You are back at Technology Commons Hub.");
  }

  async function init() {
    try {
      const response = await fetch(dataUrl);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      state.data = await response.json();
      state.data.nodes.forEach((node) => state.byId.set(node.id, node));
      loadProgress();
      renderPaths();
      renderNodes();
      renderList();
      showDetail(state.byId.get(state.current));
      root.querySelectorAll("[data-view]").forEach((button) => button.addEventListener("click", () => setView(button.dataset.view)));
      search.addEventListener("input", () => renderList(search.value));
      $("[data-reset-progress]").addEventListener("click", resetProgress);
      const mobile = window.matchMedia("(max-width: 760px)").matches;
      setView(mobile ? "list" : "map");
      root.classList.add("is-ready");
      announce(`Map ready with ${state.data.nodes.length} stops. Start at ${state.byId.get(state.current).title}.`);
    } catch (error) {
      root.classList.add("has-error");
      announce("The interactive map could not load. Use the lesson links below or the normal course navigation.");
      console.error("Learning map failed to load", error);
    }
  }

  init();
})();
