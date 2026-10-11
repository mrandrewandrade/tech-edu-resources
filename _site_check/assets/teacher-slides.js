(function () {
  "use strict";

  function normalise(value) {
    return String(value || "").trim().toLowerCase();
  }

  function normaliseCollection(value) {
    const collection = normalise(value);
    if (collection === "human well-being" || collection === "wellbeing") {
      return "well-being";
    }
    if (collection === "number-systems") {
      return "number systems";
    }
    return collection;
  }

  function parseList(value) {
    return String(value || "")
      .split("|")
      .map(normalise)
      .filter(Boolean);
  }

  function buildFilterButtons(container, values, dataName) {
    if (!container) return;

    Array.from(values.entries())
      .sort(function (a, b) {
        return a[0].localeCompare(b[0]);
      })
      .forEach(function (entry) {
        const button = document.createElement("button");
        button.type = "button";
        button.dataset[dataName] = entry[0];
        button.setAttribute("aria-pressed", "false");
        const label = dataName === "slideCourse"
          ? entry[0].toUpperCase()
          : entry[0].replace(/\b\w/g, function (char) {
              return char.toUpperCase();
            });
        button.textContent = label + " ×" + entry[1];
        container.appendChild(button);
      });
  }

  function readUrlState() {
    const params = new URLSearchParams(window.location.search);
    return {
      query: params.get("q") || "",
      collection: params.get("collection") || "",
      course: params.get("course") || "",
      topic: params.get("topic") || ""
    };
  }

  function writeUrlState(query, collection, course, topic) {
    const url = new URL(window.location.href);

    [
      ["q", query],
      ["collection", collection],
      ["course", course],
      ["topic", topic]
    ].forEach(function (entry) {
      if (entry[1]) {
        url.searchParams.set(entry[0], entry[1]);
      } else {
        url.searchParams.delete(entry[0]);
      }
    });

    window.history.replaceState({}, "", url.pathname + url.search + url.hash);
  }

  function initPanel(controls) {
    const cards = Array.from(document.querySelectorAll("[data-slide-card]"));
    const search = controls.querySelector("[data-slide-search]");
    const collectionFilters = controls.querySelector("[data-slide-collection-filters]");
    const courseFilters = controls.querySelector("[data-slide-course-filters]");
    const topicFilters = controls.querySelector("[data-slide-topic-filters]");
    const resultCount = controls.querySelector("[data-slide-result-count]");
    const clear = controls.querySelector("[data-slide-clear]");
    const empty = document.querySelector("[data-slide-empty]");

    if (!cards.length || !search || !collectionFilters) return;

    let activeCollection = "";
    let activeCourse = "";
    let activeTopic = "";

    const courseCounts = new Map();
    const topicCounts = new Map();

    cards.forEach(function (card) {
      parseList(card.dataset.courses).forEach(function (course) {
        courseCounts.set(course, (courseCounts.get(course) || 0) + 1);
      });
      parseList(card.dataset.tags).forEach(function (topic) {
        topicCounts.set(topic, (topicCounts.get(topic) || 0) + 1);
      });
    });

    buildFilterButtons(courseFilters, courseCounts, "slideCourse");
    buildFilterButtons(topicFilters, topicCounts, "slideTopic");

    function updatePressed(container, dataKey, activeValue) {
      if (!container) return;
      container.querySelectorAll("button").forEach(function (button) {
        const active = normalise(button.dataset[dataKey]) === activeValue;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-pressed", active ? "true" : "false");
      });
    }

    function update(syncUrl) {
      const query = normalise(search.value);
      let visible = 0;

      cards.forEach(function (card) {
        const cardCollection = normaliseCollection(card.dataset.collection);
        const courses = parseList(card.dataset.courses);
        const topics = parseList(card.dataset.tags);
        const haystack = normalise(
          [
            card.dataset.search,
            card.dataset.collection,
            card.dataset.courses,
            card.dataset.tags,
            card.textContent
          ].join(" ")
        );

        const matchesQuery = !query || haystack.includes(query);
        const matchesCollection =
          !activeCollection || cardCollection === activeCollection;
        const matchesCourse =
          !activeCourse || courses.includes(activeCourse);
        const matchesTopic =
          !activeTopic || topics.includes(activeTopic);
        const show =
          matchesQuery && matchesCollection && matchesCourse && matchesTopic;

        card.hidden = !show;
        if (show) visible += 1;
      });

      const singular = controls.dataset.itemSingular || "item";
      const plural = controls.dataset.itemPlural || singular + "s";
      if (resultCount) {
        resultCount.textContent =
          visible + " " + (visible === 1 ? singular : plural) + " shown";
      }

      if (empty) empty.hidden = visible !== 0;
      if (clear) {
        clear.hidden =
          !query && !activeCollection && !activeCourse && !activeTopic;
      }

      if (syncUrl !== false) {
        writeUrlState(query, activeCollection, activeCourse, activeTopic);
      }
    }

    function setCollection(value, syncUrl) {
      activeCollection = normaliseCollection(value);
      updatePressed(collectionFilters, "slideCollectionFilter", activeCollection);
      update(syncUrl);
    }

    function setCourse(value, syncUrl) {
      activeCourse = normalise(value);
      updatePressed(courseFilters, "slideCourse", activeCourse);
      update(syncUrl);
    }

    function setTopic(value, syncUrl) {
      activeTopic = normalise(value);
      updatePressed(topicFilters, "slideTopic", activeTopic);
      update(syncUrl);
    }

    function applyUrlState() {
      const state = readUrlState();
      search.value = state.query;
      activeCollection = normaliseCollection(state.collection);
      activeCourse = normalise(state.course);
      activeTopic = normalise(state.topic);
      updatePressed(collectionFilters, "slideCollectionFilter", activeCollection);
      updatePressed(courseFilters, "slideCourse", activeCourse);
      updatePressed(topicFilters, "slideTopic", activeTopic);
      update(false);
    }

    search.addEventListener("input", function () {
      update(true);
    });

    collectionFilters.addEventListener("click", function (event) {
      const button = event.target.closest("[data-slide-collection-filter]");
      if (!button) return;
      const next = normaliseCollection(button.dataset.slideCollectionFilter);
      setCollection(next === activeCollection ? "" : next, true);
    });

    if (courseFilters) {
      courseFilters.addEventListener("click", function (event) {
        const button = event.target.closest("[data-slide-course]");
        if (!button) return;
        const next = normalise(button.dataset.slideCourse);
        setCourse(next === activeCourse ? "" : next, true);
      });
    }

    if (topicFilters) {
      topicFilters.addEventListener("click", function (event) {
        const button = event.target.closest("[data-slide-topic]");
        if (!button) return;
        const next = normalise(button.dataset.slideTopic);
        setTopic(next === activeTopic ? "" : next, true);
      });
    }

    document.addEventListener("click", function (event) {
      const topicButton = event.target.closest("[data-slide-card-tag]");
      if (topicButton) {
        setTopic(topicButton.dataset.slideCardTag, true);
      }

      const courseButton = event.target.closest("[data-slide-card-course]");
      if (courseButton) {
        setCourse(courseButton.dataset.slideCardCourse, true);
      }

      if (topicButton || courseButton) {
        window.scrollTo({
          top: Math.max(
            0,
            search.getBoundingClientRect().top + window.scrollY - 110
          ),
          behavior: "smooth"
        });
      }
    });

    if (clear) {
      clear.addEventListener("click", function () {
        search.value = "";
        activeCollection = "";
        activeCourse = "";
        activeTopic = "";
        updatePressed(collectionFilters, "slideCollectionFilter", "");
        updatePressed(courseFilters, "slideCourse", "");
        updatePressed(topicFilters, "slideTopic", "");
        update(true);
        search.focus();
      });
    }

    window.addEventListener("popstate", applyUrlState);
    applyUrlState();
  }

  function init() {
    document.querySelectorAll("[data-slide-controls]").forEach(initPanel);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
