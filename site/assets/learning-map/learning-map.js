(function () {
  "use strict";

  const root = document.querySelector("[data-learning-worlds]");
  if (!root) return;
  const $ = (selector) => root.querySelector(selector);
  const svg = $("[data-graph-svg]");
  const viewport = $("[data-graph-viewport]");
  const defs = $("[data-graph-defs]");
  const edgeLayer = $("[data-edge-layer]");
  const nodeLayer = $("[data-node-layer]");
  const detail = $("[data-node-detail]");
  const status = $("[data-map-status]");
  const list = $("[data-map-list]");
  const search = $("[data-map-search]");
  const searchResults = $("[data-search-results]");
  const courseFilter = $("[data-course-filter]");
  const strandFilter = $("[data-strand-filter]");
  const state = {
    data: null, nodes: new Map(), edges: [], adjacency: new Map(),
    children: new Map(), parent: new Map(), strands: new Map(),
    selectedId: "commons-hub", expanded: new Set(["commons-hub"]),
    revealed: new Set(), visited: new Set(["commons-hub"]),
    scope: "branch", layout: "web", positions: new Map(),
    transform: {x: 0, y: 0, scale: 1}, drag: null,
  };

  function announce(message) { status.textContent = message; }
  function escapeText(value) {
    const span = document.createElement("span");
    span.textContent = String(value ?? "");
    return span.innerHTML;
  }
  function hashNumber(value) {
    let hash = 2166136261;
    for (const char of String(value)) {
      hash ^= char.charCodeAt(0);
      hash = Math.imul(hash, 16777619);
    }
    return Math.abs(hash >>> 0);
  }
  function primaryStrand(node) { return node.strands?.[0] || null; }
  function strandColour(id, soft = false) {
    const strand = state.strands.get(id);
    return strand ? strand[soft ? "soft" : "colour"] : (soft ? "#eef2f5" : "#4c5b66");
  }
  function svgElement(name, attrs = {}) {
    const element = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attrs).forEach(([key, value]) => element.setAttribute(key, value));
    return element;
  }
  function loadProgress() {
    try {
      const saved = JSON.parse(localStorage.getItem(state.data.storage_key));
      if (saved?.selectedId && state.nodes.has(saved.selectedId)) state.selectedId = saved.selectedId;
      if (Array.isArray(saved?.visited)) {
        state.visited = new Set(saved.visited.filter((id) => state.nodes.has(id)));
        state.visited.add("commons-hub");
      }
    } catch (_) { /* Storage is optional. */ }
  }
  function saveProgress() {
    try {
      localStorage.setItem(state.data.storage_key, JSON.stringify({
        selectedId: state.selectedId, visited: [...state.visited],
      }));
    } catch (_) { /* The graph remains usable. */ }
  }
  function indexGraph() {
    state.nodes = new Map(state.data.nodes.map((node) => [node.id, node]));
    state.edges = state.data.edges;
    state.strands = new Map(state.data.strands.map((strand) => [strand.id, strand]));
    state.adjacency = new Map(state.data.nodes.map((node) => [node.id, new Set()]));
    state.children = new Map(state.data.nodes.map((node) => [node.id, []]));
    for (const edge of state.edges) {
      state.adjacency.get(edge.from).add(edge.to);
      state.adjacency.get(edge.to).add(edge.from);
      if (edge.type === "contains") {
        state.children.get(edge.from).push(edge.to);
        state.parent.set(edge.to, edge.from);
      }
    }
  }
  function ancestorIds(id) {
    const result = [];
    while (state.parent.has(id)) {
      id = state.parent.get(id);
      result.push(id);
    }
    return result;
  }
  function revealRoute(id) {
    state.revealed.add(id);
    for (const ancestor of ancestorIds(id)) {
      state.revealed.add(ancestor);
      state.expanded.add(ancestor);
    }
  }
  function matchesFilters(node) {
    if (node.kind === "hub" || node.kind === "course") return true;
    if (courseFilter.value && node.course !== courseFilter.value) return false;
    return !(strandFilter.value && !node.strands.includes(strandFilter.value));
  }
  function visibleIds() {
    let visible;
    if (state.scope === "all") {
      visible = new Set(state.nodes.keys());
    } else {
      visible = new Set(["commons-hub", ...state.revealed]);
      const queue = ["commons-hub"];
      const processed = new Set();
      while (queue.length) {
        const id = queue.shift();
        if (processed.has(id)) continue;
        processed.add(id);
        if (!state.expanded.has(id)) continue;
        for (const child of state.children.get(id) || []) {
          visible.add(child);
          queue.push(child);
        }
      }
    }
    visible = new Set([...visible].filter((id) => matchesFilters(state.nodes.get(id))));
    for (const id of [...visible]) ancestorIds(id).forEach((ancestor) => visible.add(ancestor));
    return visible;
  }
  function visibleEdges(ids) {
    return state.edges.filter((edge) => ids.has(edge.from) && ids.has(edge.to));
  }
  function clusterCentres(nodes) {
    const centres = new Map();
    const visibleStrands = new Set(nodes.map(primaryStrand).filter(Boolean));
    const ids = [...state.strands.keys()].filter((id) => visibleStrands.has(id));
    const radiusX = ids.length > 6 ? 760 : 500;
    const radiusY = ids.length > 6 ? 560 : 340;
    ids.forEach((id, index) => {
      const angle = -Math.PI / 2 + index / ids.length * Math.PI * 2;
      centres.set(id, {x: Math.cos(angle) * radiusX, y: Math.sin(angle) * radiusY});
    });
    return centres;
  }
  function webLayout(nodes, edges) {
    const centres = clusterCentres(nodes);
    const positions = new Map();
    for (const node of nodes) {
      if (node.id === "commons-hub") positions.set(node.id, {x: 0, y: 0});
      else if (node.kind === "course") positions.set(node.id, {x: node.course === "tej" ? -260 : 260, y: 0});
      else {
        const centre = centres.get(primaryStrand(node)) || {x: 0, y: 0};
        const seed = hashNumber(node.id);
        const angle = seed % 360 * Math.PI / 180;
        const radius = node.kind === "track" ? 30 : 80 + seed % 170;
        positions.set(node.id, {
          x: centre.x + Math.cos(angle) * radius,
          y: centre.y + Math.sin(angle) * radius,
        });
      }
    }
    for (let iteration = 0; iteration < 140; iteration += 1) {
      const cooling = 1 - iteration / 160;
      const forces = new Map(nodes.map((node) => [node.id, {x: 0, y: 0}]));
      for (let left = 0; left < nodes.length; left += 1) {
        for (let right = left + 1; right < nodes.length; right += 1) {
          const a = positions.get(nodes[left].id);
          const b = positions.get(nodes[right].id);
          let dx = a.x - b.x;
          let dy = a.y - b.y;
          const distanceSquared = Math.max(400, dx * dx + dy * dy);
          const distance = Math.sqrt(distanceSquared);
          const push = Math.min(10, 30000 / distanceSquared);
          dx /= distance;
          dy /= distance;
          forces.get(nodes[left].id).x += dx * push;
          forces.get(nodes[left].id).y += dy * push;
          forces.get(nodes[right].id).x -= dx * push;
          forces.get(nodes[right].id).y -= dy * push;
        }
      }
      for (const edge of edges) {
        const a = positions.get(edge.from);
        const b = positions.get(edge.to);
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const distance = Math.max(1, Math.hypot(dx, dy));
        const target = edge.type === "contains" ? 190 : 155;
        const strength = edge.type === "sequence" ? .036 : edge.type === "contains" ? .025 : .012;
        const pull = (distance - target) * strength;
        const fx = dx / distance * pull;
        const fy = dy / distance * pull;
        forces.get(edge.from).x += fx;
        forces.get(edge.from).y += fy;
        forces.get(edge.to).x -= fx;
        forces.get(edge.to).y -= fy;
      }
      for (const node of nodes) {
        if (node.id === "commons-hub") continue;
        const position = positions.get(node.id);
        const centre = node.kind === "course"
          ? {x: node.course === "tej" ? -260 : 260, y: 0}
          : (centres.get(primaryStrand(node)) || {x: 0, y: 0});
        const attraction = node.kind === "track" ? .055 : .018;
        forces.get(node.id).x += (centre.x - position.x) * attraction;
        forces.get(node.id).y += (centre.y - position.y) * attraction;
      }
      for (const node of nodes) {
        if (node.id === "commons-hub") continue;
        const position = positions.get(node.id);
        const force = forces.get(node.id);
        position.x += Math.max(-16, Math.min(16, force.x)) * cooling;
        position.y += Math.max(-16, Math.min(16, force.y)) * cooling;
      }
    }
    return positions;
  }

  function pathLayout(nodes) {
    const positions = new Map([["commons-hub", {x: -360, y: 820}]]);
    const offsets = {"design-fabrication": 0, tej: 1250};
    for (const course of nodes.filter((node) => node.kind === "course")) {
      positions.set(course.id, {x: -80, y: (offsets[course.course] || 0) + 470});
    }
    const tracks = nodes.filter((node) => node.kind === "track")
      .sort((a, b) => String(a.course).localeCompare(String(b.course)) || a.order - b.order);
    for (const track of tracks) {
      const y = (offsets[track.course] || 0) + track.order * 150;
      positions.set(track.id, {x: 240, y});
      const lessons = nodes.filter((node) =>
        node.kind === "lesson" && node.course === track.course && node.track === track.track);
      for (const lesson of lessons) positions.set(lesson.id, {x: 520 + (lesson.order - 1) * 185, y});
    }
    return positions;
  }
  function nodeRadius(node) {
    return {hub: 38, course: 32, track: 25, lesson: 17}[node.kind] || 17;
  }
  function titleLines(title, maximum = 24) {
    const lines = [];
    let line = "";
    for (const word of String(title).split(/\s+/)) {
      const candidate = line ? `${line} ${word}` : word;
      if (candidate.length <= maximum) line = candidate;
      else { if (line) lines.push(line); line = word; }
    }
    if (line) lines.push(line);
    return lines.slice(0, 3);
  }
  function nodeGradient(node, index) {
    const colours = (node.strands?.length ? node.strands : [null]).slice(0, 4)
      .map((id) => strandColour(id, true));
    if (colours.length === 1) return colours[0];
    const id = `node-gradient-${index}`;
    const gradient = svgElement("linearGradient", {id, x1: "0%", y1: "0%", x2: "100%", y2: "100%"});
    colours.forEach((colour, colourIndex) => gradient.append(svgElement("stop", {
      offset: `${colourIndex / (colours.length - 1) * 100}%`, "stop-color": colour,
    })));
    defs.append(gradient);
    return `url(#${id})`;
  }
  function edgePath(edge, index) {
    const start = state.positions.get(edge.from);
    const end = state.positions.get(edge.to);
    const dx = end.x - start.x;
    const dy = end.y - start.y;
    const length = Math.max(1, Math.hypot(dx, dy));
    const bend = edge.type === "related" ? (index % 2 ? 1 : -1) * Math.min(55, length * .12) : 0;
    const mx = (start.x + end.x) / 2 - dy / length * bend;
    const my = (start.y + end.y) / 2 + dx / length * bend;
    return `M ${start.x} ${start.y} Q ${mx} ${my} ${end.x} ${end.y}`;
  }

  function renderGraph({fit = false} = {}) {
    const ids = visibleIds();
    const nodes = [...ids].map((id) => state.nodes.get(id));
    const edges = visibleEdges(ids);
    state.positions = state.layout === "web" ? webLayout(nodes, edges) : pathLayout(nodes);
    defs.replaceChildren();
    const marker = svgElement("marker", {
      id: "sequence-arrow", markerWidth: "8", markerHeight: "8",
      refX: "7", refY: "4", orient: "auto", markerUnits: "strokeWidth",
    });
    marker.append(svgElement("path", {d: "M 0 0 L 8 4 L 0 8 z", fill: "#425466"}));
    defs.append(marker);
    edgeLayer.replaceChildren();
    nodeLayer.replaceChildren();

    edges.forEach((edge, index) => {
      const from = state.nodes.get(edge.from);
      const to = state.nodes.get(edge.to);
      const gradientId = `edge-gradient-${index}`;
      const gradient = svgElement("linearGradient", {
        id: gradientId, gradientUnits: "userSpaceOnUse",
        x1: state.positions.get(edge.from).x, y1: state.positions.get(edge.from).y,
        x2: state.positions.get(edge.to).x, y2: state.positions.get(edge.to).y,
      });
      gradient.append(svgElement("stop", {offset: "0%", "stop-color": strandColour(primaryStrand(from))}));
      gradient.append(svgElement("stop", {offset: "100%", "stop-color": strandColour(primaryStrand(to))}));
      defs.append(gradient);
      const path = svgElement("path", {
        d: edgePath(edge, index), class: `learning-edge learning-edge--${edge.type}`,
        stroke: `url(#${gradientId})`, "data-from": edge.from, "data-to": edge.to,
      });
      if (edge.type === "sequence") path.setAttribute("marker-end", "url(#sequence-arrow)");
      edgeLayer.append(path);
    });

    nodes.forEach((node, index) => {
      const position = state.positions.get(node.id);
      const group = svgElement("g", {
        class: `learning-node learning-node--${node.kind}${state.selectedId === node.id ? " is-selected" : ""}${state.visited.has(node.id) ? " is-visited" : ""}`,
        transform: `translate(${position.x} ${position.y})`, tabindex: "0", role: "button",
        "aria-label": `${node.title}. ${node.kind}. ${node.summary}`, "data-node-id": node.id,
      });
      const radius = nodeRadius(node);
      group.append(svgElement("circle", {
        class: "learning-node__halo", r: radius + 8, fill: strandColour(primaryStrand(node), true),
      }));
      group.append(svgElement("circle", {
        class: "learning-node__body", r: radius, fill: nodeGradient(node, index),
        stroke: strandColour(primaryStrand(node)),
      }));
      const hasChildren = (state.children.get(node.id) || []).length;
      if (hasChildren || state.visited.has(node.id)) {
        const mark = svgElement("text", {class: "learning-node__mark", x: "0", y: "6"});
        mark.textContent = hasChildren ? (state.expanded.has(node.id) || state.scope === "all" ? "−" : "+") : "✓";
        group.append(mark);
      }
      const lines = titleLines(node.title, node.kind === "lesson" ? 22 : 26);
      const label = svgElement("g", {
        class: "learning-node__label", transform: `translate(0 ${radius + 17})`,
      });
      const width = Math.max(98, Math.min(210, Math.max(...lines.map((line) => line.length), 8) * 8.4 + 20));
      label.append(svgElement("rect", {
        x: -width / 2, y: -13, width, height: lines.length * 17 + 10, rx: "7",
      }));
      lines.forEach((line, lineIndex) => {
        const text = svgElement("text", {x: "0", y: `${lineIndex * 17 + 1}`});
        text.textContent = line;
        label.append(text);
      });
      group.append(label);
      group.addEventListener("click", (event) => selectNode(node.id, event.detail > 1));
      group.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          selectNode(node.id, event.key === "Enter" && node.kind !== "lesson");
        }
      });
      nodeLayer.append(group);
    });
    updateConnectedState();
    announce(`${nodes.length} of ${state.data.nodes.length} nodes visible in ${state.layout === "web" ? "connected web" : "quest path"} layout.`);
    if (fit) requestAnimationFrame(fitGraph);
  }

  function updateConnectedState() {
    const connected = new Set([state.selectedId, ...(state.adjacency.get(state.selectedId) || [])]);
    nodeLayer.querySelectorAll("[data-node-id]").forEach((element) => {
      element.classList.toggle("is-nearby", connected.has(element.dataset.nodeId));
      element.classList.toggle("is-dimmed", !connected.has(element.dataset.nodeId) && state.selectedId !== "commons-hub");
    });
    edgeLayer.querySelectorAll("[data-from]").forEach((element) => {
      element.classList.toggle("is-nearby",
        element.dataset.from === state.selectedId || element.dataset.to === state.selectedId);
    });
  }
  function selectNode(id, toggle = false) {
    const node = state.nodes.get(id);
    if (!node) return;
    state.selectedId = id;
    state.visited.add(id);
    revealRoute(id);
    if (toggle && (state.children.get(id) || []).length) {
      if (state.expanded.has(id)) state.expanded.delete(id);
      else state.expanded.add(id);
    }
    saveProgress();
    showDetail(node);
    renderGraph();
  }
  function revealConnections(id) {
    revealRoute(id);
    for (const neighbour of state.adjacency.get(id) || []) revealRoute(neighbour);
    renderGraph({fit: true});
  }

  function showDetail(node) {
    const children = state.children.get(node.id) || [];
    const strands = node.strands.map((id) => state.strands.get(id)?.label).filter(Boolean);
    detail.innerHTML = `
      <p class="detail-kicker">${escapeText(node.kind)}${node.track ? ` · ${escapeText(node.track.replaceAll("-", " "))}` : ""}</p>
      <h2>${escapeText(node.title)}</h2>
      <p class="detail-summary">${escapeText(node.summary)}</p>
      <div class="detail-strands">${strands.map((label, index) => `<span style="--chip-colour:${strandColour(node.strands[index])};--chip-soft:${strandColour(node.strands[index], true)}">${escapeText(label)}</span>`).join("")}</div>
      <dl><div><dt>Connections</dt><dd>${state.adjacency.get(node.id)?.size || 0}</dd></div><div><dt>Map role</dt><dd>${escapeText(node.kind === "lesson" ? "Learning stop" : node.kind === "track" ? "Strand portal" : "World portal")}</dd></div></dl>
      <div class="detail-actions">
        <a class="map-action map-action--primary" href="${escapeText(node.href)}">Open page</a>
        <button class="map-action" type="button" data-detail-connections>Show connected ideas</button>
        ${children.length ? `<button class="map-action" type="button" data-detail-expand>${state.expanded.has(node.id) ? "Collapse this region" : `Expand ${children.length} next stops`}</button>` : ""}
      </div>
      <p class="detail-note">A checkmark records exploration on this browser. It is not a grade or a mastery claim.</p>`;
    detail.querySelector("[data-detail-connections]")?.addEventListener("click", () => revealConnections(node.id));
    detail.querySelector("[data-detail-expand]")?.addEventListener("click", () => {
      if (state.expanded.has(node.id)) state.expanded.delete(node.id);
      else state.expanded.add(node.id);
      renderGraph({fit: true});
      showDetail(node);
    });
  }

  function buildControls() {
    for (const course of state.data.nodes.filter((node) => node.kind === "course")) {
      const option = document.createElement("option");
      option.value = course.course;
      option.textContent = course.title;
      courseFilter.append(option);
    }
    for (const strand of state.data.strands) {
      const option = document.createElement("option");
      option.value = strand.id;
      option.textContent = strand.label;
      strandFilter.append(option);
    }
    [courseFilter, strandFilter].forEach((select) =>
      select.addEventListener("change", () => {
        renderGraph({fit: true});
        renderList();
      }));
    root.querySelectorAll("[data-layout]").forEach((button) => button.addEventListener("click", () => {
      state.layout = button.dataset.layout;
      root.querySelectorAll("[data-layout]").forEach((candidate) => {
        const active = candidate.dataset.layout === state.layout;
        candidate.classList.toggle("is-active", active);
        candidate.setAttribute("aria-pressed", String(active));
      });
      renderGraph({fit: true});
    }));
    $("[data-show-all]").addEventListener("click", () => {
      state.scope = "all";
      renderGraph({fit: true});
    });
    $("[data-focus-selected]").addEventListener("click", () => {
      state.scope = "branch";
      state.expanded = new Set(["commons-hub", ...ancestorIds(state.selectedId)]);
      state.revealed = new Set([state.selectedId, ...(state.adjacency.get(state.selectedId) || [])]);
      for (const id of [...state.revealed]) revealRoute(id);
      renderGraph({fit: true});
    });
    $("[data-reset-map]").addEventListener("click", () => {
      state.scope = "branch";
      state.selectedId = "commons-hub";
      state.expanded = new Set(["commons-hub"]);
      state.revealed.clear();
      courseFilter.value = "";
      strandFilter.value = "";
      showDetail(state.nodes.get("commons-hub"));
      renderList();
      renderGraph({fit: true});
    });
    $("[data-fit-map]").addEventListener("click", fitGraph);
    $("[data-reset-progress]").addEventListener("click", () => {
      state.visited = new Set(["commons-hub"]);
      saveProgress();
      renderGraph();
      announce("Exploration checkmarks reset.");
    });
    root.querySelectorAll("[data-view]").forEach((button) =>
      button.addEventListener("click", () => setView(button.dataset.view)));
  }

  function renderList() {
    list.replaceChildren();
    for (const track of state.data.nodes.filter((node) => node.kind === "track")) {
      if (courseFilter.value && track.course !== courseFilter.value) continue;
      if (strandFilter.value && !track.strands.includes(strandFilter.value)) continue;
      const section = document.createElement("section");
      section.className = "map-list-group";
      section.innerHTML = `<p class="map-list-kicker">${escapeText(state.nodes.get(state.parent.get(track.id))?.title || "")}</p><h2>${escapeText(track.title)}</h2><p>${escapeText(track.summary)}</p>`;
      const grid = document.createElement("div");
      grid.className = "map-list-grid";
      const lessons = state.data.nodes.filter((node) =>
        node.kind === "lesson" && node.track === track.track && node.course === track.course)
        .sort((a, b) => a.order - b.order);
      for (const lesson of lessons) {
        const card = document.createElement("article");
        card.className = "map-list-card";
        card.style.setProperty("--card-colour", strandColour(primaryStrand(lesson)));
        card.innerHTML = `<div class="map-list-card__meta">Stop ${lesson.order} · ${escapeText(state.strands.get(primaryStrand(lesson))?.label || "Lesson")}</div><h3>${escapeText(lesson.title)}</h3><p>${escapeText(lesson.summary)}</p><a href="${escapeText(lesson.href)}">Open page</a>`;
        grid.append(card);
      }
      section.append(grid);
      list.append(section);
    }
  }
  function setView(view) {
    root.dataset.view = view;
    root.querySelectorAll("[data-view]").forEach((button) => {
      const active = button.dataset.view === view;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    if (view === "map") requestAnimationFrame(fitGraph);
  }

  function renderSearchResults(query) {
    const value = query.trim().toLocaleLowerCase();
    searchResults.replaceChildren();
    if (value.length < 2) { searchResults.hidden = true; return; }
    const matches = state.data.nodes.filter((node) =>
      node.kind !== "hub" &&
      [node.title, node.summary, node.track, ...node.strands].join(" ").toLocaleLowerCase().includes(value)
    ).slice(0, 8);
    if (!matches.length) {
      searchResults.innerHTML = "<p>No matching learning stops.</p>";
      searchResults.hidden = false;
      return;
    }
    for (const node of matches) {
      const button = document.createElement("button");
      button.type = "button";
      button.innerHTML = `<strong>${escapeText(node.title)}</strong><span>${escapeText(node.kind)} · ${escapeText(node.track || node.course || "commons")}</span>`;
      button.addEventListener("click", () => {
        state.scope = "branch";
        revealRoute(node.id);
        for (const neighbour of state.adjacency.get(node.id) || []) revealRoute(neighbour);
        state.selectedId = node.id;
        state.visited.add(node.id);
        search.value = "";
        searchResults.hidden = true;
        setView("map");
        showDetail(node);
        renderGraph({fit: true});
      });
      searchResults.append(button);
    }
    searchResults.hidden = false;
  }

  function graphBounds() {
    const values = [...state.positions.values()];
    if (!values.length) return {minX: -100, minY: -100, maxX: 100, maxY: 100};
    return {
      minX: Math.min(...values.map((value) => value.x)) - 130,
      minY: Math.min(...values.map((value) => value.y)) - 100,
      maxX: Math.max(...values.map((value) => value.x)) + 130,
      maxY: Math.max(...values.map((value) => value.y)) + 120,
    };
  }
  function applyTransform() {
    viewport.setAttribute("transform",
      `translate(${state.transform.x} ${state.transform.y}) scale(${state.transform.scale})`);
  }
  function fitGraph() {
    const rect = svg.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    const bounds = graphBounds();
    const width = bounds.maxX - bounds.minX;
    const height = bounds.maxY - bounds.minY;
    const scale = Math.max(.16, Math.min(1.25,
      Math.min((rect.width - 36) / width, (rect.height - 36) / height)));
    state.transform = {
      scale,
      x: rect.width / 2 - (bounds.minX + width / 2) * scale,
      y: rect.height / 2 - (bounds.minY + height / 2) * scale,
    };
    applyTransform();
  }
  function installPanZoom() {
    svg.addEventListener("wheel", (event) => {
      event.preventDefault();
      const rect = svg.getBoundingClientRect();
      const pointerX = event.clientX - rect.left;
      const pointerY = event.clientY - rect.top;
      const graphX = (pointerX - state.transform.x) / state.transform.scale;
      const graphY = (pointerY - state.transform.y) / state.transform.scale;
      const scale = Math.max(.14, Math.min(2.4,
        state.transform.scale * (event.deltaY < 0 ? 1.12 : .89)));
      state.transform.x = pointerX - graphX * scale;
      state.transform.y = pointerY - graphY * scale;
      state.transform.scale = scale;
      applyTransform();
    }, {passive: false});
    svg.addEventListener("pointerdown", (event) => {
      if (event.target.closest?.("[data-node-id]")) return;
      state.drag = {
        x: event.clientX, y: event.clientY,
        originX: state.transform.x, originY: state.transform.y,
      };
      svg.setPointerCapture(event.pointerId);
    });
    svg.addEventListener("pointermove", (event) => {
      if (!state.drag) return;
      state.transform.x = state.drag.originX + event.clientX - state.drag.x;
      state.transform.y = state.drag.originY + event.clientY - state.drag.y;
      applyTransform();
    });
    svg.addEventListener("pointerup", () => { state.drag = null; });
    svg.addEventListener("pointercancel", () => { state.drag = null; });
  }

  async function init() {
    try {
      const response = await fetch(root.dataset.manifest);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      state.data = await response.json();
      indexGraph();
      loadProgress();
      revealRoute(state.selectedId);
      buildControls();
      renderList();
      showDetail(state.nodes.get(state.selectedId));
      renderGraph({fit: true});
      installPanZoom();
      search.addEventListener("input", () => renderSearchResults(search.value));
      document.addEventListener("click", (event) => {
        if (!event.target.closest(".map-search-wrap")) searchResults.hidden = true;
      });
      setView(window.matchMedia("(max-width: 760px)").matches ? "list" : "map");
      root.classList.add("is-ready");
      announce(`Learning web ready with ${state.data.nodes.length} nodes and ${state.data.edges.length} connections.`);
    } catch (error) {
      root.classList.add("has-error");
      announce("The learning web could not load. Use the normal course navigation or printable map.");
      console.error("Learning web failed to load", error);
    }
  }

  init();
})();
