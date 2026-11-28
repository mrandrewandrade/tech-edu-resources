window.TECHNOLOGY_COMMONS_LEARNING_GRAPH = {
  "version": 1,
  "title": "Technology Commons Learning Web",
  "subtitle": "Expand a route, follow a quest path, or discover where ideas connect.",
  "storage_key": "technology-commons-learning-web-v1",
  "strands": [
    {
      "id": "circuits",
      "label": "Circuits & Electronics",
      "colour": "#1677a6",
      "soft": "#d9f2ff"
    },
    {
      "id": "programming",
      "label": "Programming & Data",
      "colour": "#6f42c1",
      "soft": "#eee5ff"
    },
    {
      "id": "linux",
      "label": "Linux & Tools",
      "colour": "#4557b8",
      "soft": "#e4e8ff"
    },
    {
      "id": "systems",
      "label": "Computer Systems & Networks",
      "colour": "#087f8c",
      "soft": "#d9f5f2"
    },
    {
      "id": "portfolio",
      "label": "Portfolio & Evidence",
      "colour": "#2d7d52",
      "soft": "#ddf4e6"
    },
    {
      "id": "design-process",
      "label": "Design Process",
      "colour": "#a86700",
      "soft": "#fff0c7"
    },
    {
      "id": "visual-design",
      "label": "Visual Communication",
      "colour": "#b2387a",
      "soft": "#f9e1ee"
    },
    {
      "id": "fabrication",
      "label": "Fabrication",
      "colour": "#b84c22",
      "soft": "#ffe5d8"
    },
    {
      "id": "culture",
      "label": "Culture & Place",
      "colour": "#62751f",
      "soft": "#edf4d2"
    }
  ],
  "nodes": [
    {
      "id": "commons-hub",
      "kind": "hub",
      "title": "Technology Commons",
      "summary": "Begin here, choose a world, and expand only the routes you want to explore.",
      "href": "../index.html",
      "course": null,
      "track": null,
      "strands": [],
      "order": 0
    },
    {
      "id": "course-design-fabrication",
      "kind": "course",
      "title": "General Design & Fabrication",
      "summary": "Choose a strand to see its lessons and connected ideas.",
      "href": "../design-fabrication/index.html",
      "course": "design-fabrication",
      "track": null,
      "strands": [
        "culture",
        "design-process",
        "fabrication",
        "visual-design"
      ],
      "order": 1
    },
    {
      "id": "course-tej",
      "kind": "course",
      "title": "TEJ3/4 Computer Engineering",
      "summary": "Choose a strand to see its lessons and connected ideas.",
      "href": "../tej3-4/index.html",
      "course": "tej",
      "track": null,
      "strands": [
        "circuits",
        "linux",
        "portfolio",
        "programming",
        "systems"
      ],
      "order": 2
    },
    {
      "id": "track-design-fabrication-culture-land",
      "kind": "track",
      "title": "Culture and Land-Based Learning",
      "summary": "Connect design decisions to place, story, seasons, and respectful observation.",
      "href": "../design-fabrication/culture-land-based-learning/index.html",
      "course": "design-fabrication",
      "track": "culture-land",
      "strands": [
        "culture"
      ],
      "order": 1
    },
    {
      "id": "track-design-fabrication-design-process",
      "kind": "track",
      "title": "S.O. N.I.C.E. Design Process",
      "summary": "Understand the situation, spot an opportunity to improve it, then move through needs, ideas, feedback, and revision.",
      "href": "../design-fabrication/design-process/index.html",
      "course": "design-fabrication",
      "track": "design-process",
      "strands": [
        "design-process"
      ],
      "order": 2
    },
    {
      "id": "track-design-fabrication-emotions-visual-communication",
      "kind": "track",
      "title": "Emotions and Visual Communication",
      "summary": "Understand what emotions do and use emotional signals deliberately in visual communication.",
      "href": "../design-fabrication/emotions/index.html",
      "course": "design-fabrication",
      "track": "emotions-visual-communication",
      "strands": [
        "visual-design"
      ],
      "order": 3
    },
    {
      "id": "track-design-fabrication-logo-design",
      "kind": "track",
      "title": "Logo Design in Photopea",
      "summary": "Learn browser-based graphic design by building a nameplate and logo in five short projects.",
      "href": "../design-fabrication/logo-design/index.html",
      "course": "design-fabrication",
      "track": "logo-design",
      "strands": [
        "visual-design"
      ],
      "order": 4
    },
    {
      "id": "track-design-fabrication-logo-animation",
      "kind": "track",
      "title": "Logo Animation",
      "summary": "Apply animation foundations in a four-day browser project using the logo students already designed.",
      "href": "../design-fabrication/02-digital-design/05-animation-ui-ux.html",
      "course": "design-fabrication",
      "track": "logo-animation",
      "strands": [
        "visual-design"
      ],
      "order": 5
    },
    {
      "id": "track-design-fabrication-accessible-design",
      "kind": "track",
      "title": "Accessible Design",
      "summary": "Build accessibility checks into graphic design instead of adding them at the end.",
      "href": "../design-fabrication/accessible-design/index.html",
      "course": "design-fabrication",
      "track": "accessible-design",
      "strands": [
        "visual-design"
      ],
      "order": 6
    },
    {
      "id": "track-design-fabrication-fabrication-tools",
      "kind": "track",
      "title": "Laser Cutting and Fabrication Tools",
      "summary": "Use measured drawings, joint design, adhesives, finishing choices, builders, and reusable files to make laser-cut projects.",
      "href": "../design-fabrication/laser-cutting/index.html",
      "course": "design-fabrication",
      "track": "fabrication-tools",
      "strands": [
        "fabrication"
      ],
      "order": 7
    },
    {
      "id": "track-design-fabrication-phone-holder-project",
      "kind": "track",
      "title": "Making the Phone Holder",
      "summary": "Choose a phone holder, make the CAD, learn the tools, and build it.",
      "href": "../design-fabrication/cad-parametric-modeling/index.html",
      "course": "design-fabrication",
      "track": "phone-holder-project",
      "strands": [
        "fabrication"
      ],
      "order": 8
    },
    {
      "id": "track-design-fabrication-advanced-making",
      "kind": "track",
      "title": "Keychain, Stamps, Then Optional Extensions",
      "summary": "Begin with the basic keychain, build the AA and original stamps, then choose optional Blender, PCSS or faux-enamel extensions.",
      "href": "../design-fabrication/04-3d-printing/index.html",
      "course": "design-fabrication",
      "track": "advanced-making",
      "strands": [
        "fabrication"
      ],
      "order": 9
    },
    {
      "id": "track-tej-portfolio",
      "kind": "track",
      "title": "Project Portfolio",
      "summary": "Collect plans, tests, code, measurements, photographs, and reflections.",
      "href": "../tej3-4/portfolio/index.html",
      "course": "tej",
      "track": "portfolio",
      "strands": [
        "portfolio"
      ],
      "order": 4
    },
    {
      "id": "track-tej-circuits-electronics",
      "kind": "track",
      "title": "Circuits and Electronics",
      "summary": "Move from measurement and notation to progressively harder circuit analysis packages.",
      "href": "../tej3-4/electronics-library/index.html",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 5
    },
    {
      "id": "track-tej-computer-systems",
      "kind": "track",
      "title": "Computer Systems",
      "summary": "Connect physical computer parts, storage, displays, USB, peripherals, and safe workstation setup.",
      "href": "../tej3-4/computer-systems/index.html",
      "course": "tej",
      "track": "computer-systems",
      "strands": [
        "systems"
      ],
      "order": 6
    },
    {
      "id": "track-tej-linux-operating-systems",
      "kind": "track",
      "title": "Linux and Operating Systems",
      "summary": "Choose, install, explore, administer, program, and measure a Linux computer in a linear sequence.",
      "href": "../tej3-4/linux-operating-systems/index.html",
      "course": "tej",
      "track": "linux-operating-systems",
      "strands": [
        "linux"
      ],
      "order": 7
    },
    {
      "id": "track-tej-networking",
      "kind": "track",
      "title": "Networking",
      "summary": "Follow data through Wi-Fi, Ethernet, switches, routers, and the Internet, then build and test a patch cable.",
      "href": "../tej3-4/networking/index.html",
      "course": "tej",
      "track": "networking",
      "strands": [
        "systems"
      ],
      "order": 8
    },
    {
      "id": "track-tej-programming-interfacing",
      "kind": "track",
      "title": "Computational Engineering",
      "summary": "Use browser-based or locally installed Python notebooks to calculate, graph, test, debug, and explain engineering evidence.",
      "href": "../tej3-4/computational-engineering/index.html",
      "course": "tej",
      "track": "programming-interfacing",
      "strands": [
        "programming"
      ],
      "order": 9
    },
    {
      "id": "track-tej-missions-physical-computing",
      "kind": "track",
      "title": "Missions and Physical Computing",
      "summary": "Choose a mission, sign out a complete equipment bin, simulate or verify each stage, then build and document a safe working system.",
      "href": "../tej3-4/capstone/index.html",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 10
    },
    {
      "id": "lesson-design-fabrication-culture-land-based-learning-grandmother-moon-seasons-qmd",
      "kind": "lesson",
      "title": "Grandmother Moon, Seasons, and Turtle's Back",
      "summary": "Read seasonal patterns and use a turtle-shell model to organize observations.",
      "href": "../design-fabrication/culture-land-based-learning/grandmother-moon-seasons.html",
      "source": "design-fabrication/culture-land-based-learning/grandmother-moon-seasons.qmd",
      "course": "design-fabrication",
      "track": "culture-land",
      "strands": [
        "culture"
      ],
      "order": 1,
      "sequence_index": 0
    },
    {
      "id": "lesson-design-fabrication-culture-land-based-learning-land-lettermark-qmd",
      "kind": "lesson",
      "title": "Land Lettermark",
      "summary": "Build a lettermark from a place-based observation and document the design choice.",
      "href": "../design-fabrication/culture-land-based-learning/land-lettermark.html",
      "source": "design-fabrication/culture-land-based-learning/land-lettermark.qmd",
      "course": "design-fabrication",
      "track": "culture-land",
      "strands": [
        "culture"
      ],
      "order": 2,
      "sequence_index": 1
    },
    {
      "id": "lesson-design-fabrication-design-process-situation-qmd",
      "kind": "lesson",
      "title": "Understand the Situation & Opportunity",
      "summary": "Separate facts, assumptions, and interpretations, then identify an opportunity to improve the situation.",
      "href": "../design-fabrication/design-process/situation.html",
      "source": "design-fabrication/design-process/situation.qmd",
      "course": "design-fabrication",
      "track": "design-process",
      "strands": [
        "design-process",
        "portfolio"
      ],
      "order": 1,
      "sequence_index": 2
    },
    {
      "id": "lesson-design-fabrication-design-process-user-needs-qmd",
      "kind": "lesson",
      "title": "Record User Needs",
      "summary": "Observe and record what people actually need in the setting.",
      "href": "../design-fabrication/design-process/user-needs.html",
      "source": "design-fabrication/design-process/user-needs.qmd",
      "course": "design-fabrication",
      "track": "design-process",
      "strands": [
        "design-process"
      ],
      "order": 2,
      "sequence_index": 3
    },
    {
      "id": "lesson-design-fabrication-design-process-necessities-nice-to-haves-qmd",
      "kind": "lesson",
      "title": "Necessities and Nice-to-Haves",
      "summary": "Separate non-negotiable constraints from preferences.",
      "href": "../design-fabrication/design-process/necessities-nice-to-haves.html",
      "source": "design-fabrication/design-process/necessities-nice-to-haves.qmd",
      "course": "design-fabrication",
      "track": "design-process",
      "strands": [
        "design-process"
      ],
      "order": 3,
      "sequence_index": 4
    },
    {
      "id": "lesson-design-fabrication-design-process-rank-priorities-qmd",
      "kind": "lesson",
      "title": "Rank Priorities",
      "summary": "Rank preferences so the most valuable improvements stay visible.",
      "href": "../design-fabrication/design-process/rank-priorities.html",
      "source": "design-fabrication/design-process/rank-priorities.qmd",
      "course": "design-fabrication",
      "track": "design-process",
      "strands": [
        "design-process"
      ],
      "order": 4,
      "sequence_index": 5
    },
    {
      "id": "lesson-design-fabrication-design-process-investigate-inquire-qmd",
      "kind": "lesson",
      "title": "Investigate and Inquire",
      "summary": "Research, observe, measure, collect precedents, and generate several ideas.",
      "href": "../design-fabrication/design-process/investigate-inquire.html",
      "source": "design-fabrication/design-process/investigate-inquire.qmd",
      "course": "design-fabrication",
      "track": "design-process",
      "strands": [
        "design-process",
        "portfolio"
      ],
      "order": 5,
      "sequence_index": 6
    },
    {
      "id": "lesson-design-fabrication-design-process-create-communicate-qmd",
      "kind": "lesson",
      "title": "Create and Communicate",
      "summary": "Develop an idea, make the proposal understandable, pitch it, and collect feedback.",
      "href": "../design-fabrication/design-process/create-communicate.html",
      "source": "design-fabrication/design-process/create-communicate.qmd",
      "course": "design-fabrication",
      "track": "design-process",
      "strands": [
        "design-process"
      ],
      "order": 6,
      "sequence_index": 7
    },
    {
      "id": "lesson-design-fabrication-design-process-evaluate-repeat-qmd",
      "kind": "lesson",
      "title": "Evaluate and Repeat",
      "summary": "Score ideas against necessities and priorities, then revise the strongest option.",
      "href": "../design-fabrication/design-process/evaluate-repeat.html",
      "source": "design-fabrication/design-process/evaluate-repeat.qmd",
      "course": "design-fabrication",
      "track": "design-process",
      "strands": [
        "design-process",
        "portfolio"
      ],
      "order": 7,
      "sequence_index": 8
    },
    {
      "id": "lesson-design-fabrication-emotions-fear-anxiety-qmd",
      "kind": "lesson",
      "title": "Fear and Anxiety",
      "summary": "Notice danger, uncertainty, preparation, and the urge to escape, avoid, or freeze.",
      "href": "../design-fabrication/emotions/fear-anxiety.html",
      "source": "design-fabrication/emotions/fear-anxiety.qmd",
      "course": "design-fabrication",
      "track": "emotions-visual-communication",
      "strands": [
        "visual-design"
      ],
      "order": 1,
      "sequence_index": 9
    },
    {
      "id": "lesson-design-fabrication-emotions-anger-qmd",
      "kind": "lesson",
      "title": "Anger",
      "summary": "Connect anger with blocked goals, unfairness, boundaries, and action.",
      "href": "../design-fabrication/emotions/anger.html",
      "source": "design-fabrication/emotions/anger.qmd",
      "course": "design-fabrication",
      "track": "emotions-visual-communication",
      "strands": [
        "visual-design"
      ],
      "order": 2,
      "sequence_index": 10
    },
    {
      "id": "lesson-design-fabrication-emotions-disgust-qmd",
      "kind": "lesson",
      "title": "Disgust",
      "summary": "Notice signals of danger, harm, or a conflict with values.",
      "href": "../design-fabrication/emotions/disgust.html",
      "source": "design-fabrication/emotions/disgust.qmd",
      "course": "design-fabrication",
      "track": "emotions-visual-communication",
      "strands": [
        "visual-design"
      ],
      "order": 3,
      "sequence_index": 11
    },
    {
      "id": "lesson-design-fabrication-emotions-envy-qmd",
      "kind": "lesson",
      "title": "Envy",
      "summary": "Turn comparison and desire into a specific healthy goal.",
      "href": "../design-fabrication/emotions/envy.html",
      "source": "design-fabrication/emotions/envy.qmd",
      "course": "design-fabrication",
      "track": "emotions-visual-communication",
      "strands": [
        "visual-design"
      ],
      "order": 4,
      "sequence_index": 12
    },
    {
      "id": "lesson-design-fabrication-emotions-jealousy-qmd",
      "kind": "lesson",
      "title": "Jealousy",
      "summary": "Distinguish fear of losing a relationship, role, place, or attention from envy.",
      "href": "../design-fabrication/emotions/jealousy.html",
      "source": "design-fabrication/emotions/jealousy.qmd",
      "course": "design-fabrication",
      "track": "emotions-visual-communication",
      "strands": [
        "visual-design"
      ],
      "order": 5,
      "sequence_index": 13
    },
    {
      "id": "lesson-design-fabrication-emotions-guilt-qmd",
      "kind": "lesson",
      "title": "Guilt",
      "summary": "Use guilt to notice when behaviour may not match values.",
      "href": "../design-fabrication/emotions/guilt.html",
      "source": "design-fabrication/emotions/guilt.qmd",
      "course": "design-fabrication",
      "track": "emotions-visual-communication",
      "strands": [
        "visual-design"
      ],
      "order": 6,
      "sequence_index": 14
    },
    {
      "id": "lesson-design-fabrication-emotions-shame-qmd",
      "kind": "lesson",
      "title": "Shame",
      "summary": "Separate a mistaken action from a belief that something is wrong with the whole person.",
      "href": "../design-fabrication/emotions/shame.html",
      "source": "design-fabrication/emotions/shame.qmd",
      "course": "design-fabrication",
      "track": "emotions-visual-communication",
      "strands": [
        "visual-design"
      ],
      "order": 7,
      "sequence_index": 15
    },
    {
      "id": "lesson-design-fabrication-emotions-happiness-qmd",
      "kind": "lesson",
      "title": "Happiness",
      "summary": "Notice reward, connection, celebration, and momentum.",
      "href": "../design-fabrication/emotions/happiness.html",
      "source": "design-fabrication/emotions/happiness.qmd",
      "course": "design-fabrication",
      "track": "emotions-visual-communication",
      "strands": [
        "visual-design"
      ],
      "order": 8,
      "sequence_index": 16
    },
    {
      "id": "lesson-design-fabrication-emotions-love-qmd",
      "kind": "lesson",
      "title": "Love",
      "summary": "Connect love with care, belonging, values, boundaries, and support.",
      "href": "../design-fabrication/emotions/love.html",
      "source": "design-fabrication/emotions/love.qmd",
      "course": "design-fabrication",
      "track": "emotions-visual-communication",
      "strands": [
        "visual-design"
      ],
      "order": 9,
      "sequence_index": 17
    },
    {
      "id": "lesson-design-fabrication-emotions-sadness-qmd",
      "kind": "lesson",
      "title": "Sadness",
      "summary": "Notice loss, meaning, support, and the need to slow down.",
      "href": "../design-fabrication/emotions/sadness.html",
      "source": "design-fabrication/emotions/sadness.qmd",
      "course": "design-fabrication",
      "track": "emotions-visual-communication",
      "strands": [
        "visual-design"
      ],
      "order": 10,
      "sequence_index": 18
    },
    {
      "id": "lesson-design-fabrication-logo-design-nameplate-text-photopea-qmd",
      "kind": "lesson",
      "title": "Build the Nameplate Text",
      "summary": "Make an 11 by 4 inch file, leave room for a logo, and choose readable type.",
      "href": "../design-fabrication/logo-design/nameplate-text-photopea.html",
      "source": "design-fabrication/logo-design/nameplate-text-photopea.qmd",
      "course": "design-fabrication",
      "track": "logo-design",
      "strands": [
        "visual-design"
      ],
      "order": 1,
      "sequence_index": 19
    },
    {
      "id": "lesson-design-fabrication-logo-design-rough-sketch-to-svg-photopea-qmd",
      "kind": "lesson",
      "title": "Warm-Up: Trace the AA Logo",
      "summary": "Rebuild a simple hand-drawn mark with four clean vector lines.",
      "href": "../design-fabrication/logo-design/rough-sketch-to-svg-photopea.html",
      "source": "design-fabrication/logo-design/rough-sketch-to-svg-photopea.qmd",
      "course": "design-fabrication",
      "track": "logo-design",
      "strands": [
        "visual-design"
      ],
      "order": 2,
      "sequence_index": 20
    },
    {
      "id": "lesson-design-fabrication-logo-design-02b-advanced-multilayer-tracing-photopea-qmd",
      "kind": "lesson",
      "title": "Trace a Multi-Layer Logo",
      "summary": "Trace a landscape sketch as four named vector shapes and export an animation-ready SVG.",
      "href": "../design-fabrication/logo-design/02b-advanced-multilayer-tracing-photopea.html",
      "source": "design-fabrication/logo-design/02b-advanced-multilayer-tracing-photopea.qmd",
      "course": "design-fabrication",
      "track": "logo-design",
      "strands": [
        "visual-design"
      ],
      "order": 3,
      "sequence_index": 21
    },
    {
      "id": "lesson-design-fabrication-logo-design-03-combine-logo-nameplate-qmd",
      "kind": "lesson",
      "title": "Combine Logo and Nameplate",
      "summary": "Combine the ANDRADE logo and nameplate, then export the complete design.",
      "href": "../design-fabrication/logo-design/03-combine-logo-nameplate.html",
      "source": "design-fabrication/logo-design/03-combine-logo-nameplate.qmd",
      "course": "design-fabrication",
      "track": "logo-design",
      "strands": [
        "visual-design"
      ],
      "order": 4,
      "sequence_index": 22
    },
    {
      "id": "lesson-design-fabrication-03-laser-cutting-01-name-logo-qmd",
      "kind": "lesson",
      "title": "Design Your Own Name Tag",
      "summary": "Apply the tutorial skills to an original name-and-logo design and defend the choices.",
      "href": "../design-fabrication/03-laser-cutting/01-name-logo.html",
      "source": "design-fabrication/03-laser-cutting/01-name-logo.qmd",
      "course": "design-fabrication",
      "track": "logo-design",
      "strands": [
        "visual-design"
      ],
      "order": 5,
      "sequence_index": 23
    },
    {
      "id": "lesson-design-fabrication-02-digital-design-animate-your-logo-qmd",
      "kind": "lesson",
      "title": "Bring Your Brand to Life: Animate Your Logo",
      "summary": "Create a 5–8 second animated logo intro with intentional changes, a complete sequence, feedback, and improvement.",
      "href": "../design-fabrication/02-digital-design/animate-your-logo.html",
      "source": "design-fabrication/02-digital-design/animate-your-logo.qmd",
      "course": "design-fabrication",
      "track": "logo-animation",
      "strands": [
        "visual-design"
      ],
      "order": 1,
      "sequence_index": 24
    },
    {
      "id": "lesson-design-fabrication-accessible-design-access-and-alt-text-qmd",
      "kind": "lesson",
      "title": "Access and Alt Text",
      "summary": "Describe the instructional purpose of an image and identify barriers to access.",
      "href": "../design-fabrication/accessible-design/access-and-alt-text.html",
      "source": "design-fabrication/accessible-design/access-and-alt-text.qmd",
      "course": "design-fabrication",
      "track": "accessible-design",
      "strands": [
        "visual-design"
      ],
      "order": 1,
      "sequence_index": 25
    },
    {
      "id": "lesson-design-fabrication-accessible-design-fonts-and-text-effects-qmd",
      "kind": "lesson",
      "title": "Fonts and Text Effects",
      "summary": "Compare typefaces and test backgrounds, outlines, shadows, and decorative effects.",
      "href": "../design-fabrication/accessible-design/fonts-and-text-effects.html",
      "source": "design-fabrication/accessible-design/fonts-and-text-effects.qmd",
      "course": "design-fabrication",
      "track": "accessible-design",
      "strands": [
        "visual-design"
      ],
      "order": 2,
      "sequence_index": 26
    },
    {
      "id": "lesson-design-fabrication-accessible-design-understanding-colour-qmd",
      "kind": "lesson",
      "title": "Understanding Colour",
      "summary": "Use hue, saturation, value, opacity, and colour models deliberately.",
      "href": "../design-fabrication/accessible-design/understanding-colour.html",
      "source": "design-fabrication/accessible-design/understanding-colour.qmd",
      "course": "design-fabrication",
      "track": "accessible-design",
      "strands": [
        "visual-design"
      ],
      "order": 3,
      "sequence_index": 27
    },
    {
      "id": "lesson-design-fabrication-accessible-design-contrast-and-output-qmd",
      "kind": "lesson",
      "title": "Contrast and Output",
      "summary": "Check contrast, real size, file type, and final screen, print, or fabrication output.",
      "href": "../design-fabrication/accessible-design/contrast-and-output.html",
      "source": "design-fabrication/accessible-design/contrast-and-output.qmd",
      "course": "design-fabrication",
      "track": "accessible-design",
      "strands": [
        "visual-design",
        "design-process"
      ],
      "order": 4,
      "sequence_index": 28
    },
    {
      "id": "lesson-design-fabrication-03-laser-cutting-02-make-it-stand-qmd",
      "kind": "lesson",
      "title": "Make It Stand",
      "summary": "Compare ways to support a flat design as a stable object.",
      "href": "../design-fabrication/03-laser-cutting/02-make-it-stand.html",
      "source": "design-fabrication/03-laser-cutting/02-make-it-stand.qmd",
      "course": "design-fabrication",
      "track": "fabrication-tools",
      "strands": [
        "fabrication",
        "design-process"
      ],
      "order": 1,
      "sequence_index": 29
    },
    {
      "id": "lesson-design-fabrication-03-laser-cutting-03-measure-place-qmd",
      "kind": "lesson",
      "title": "Measure and Place",
      "summary": "Measure a real object and place openings and supports from evidence.",
      "href": "../design-fabrication/03-laser-cutting/03-measure-place.html",
      "source": "design-fabrication/03-laser-cutting/03-measure-place.qmd",
      "course": "design-fabrication",
      "track": "fabrication-tools",
      "strands": [
        "fabrication"
      ],
      "order": 2,
      "sequence_index": 30
    },
    {
      "id": "lesson-design-fabrication-03-laser-cutting-04-material-fit-calibration-qmd",
      "kind": "lesson",
      "title": "Material Fit and Calibration",
      "summary": "Test material thickness, kerf, and fit before cutting a full project.",
      "href": "../design-fabrication/03-laser-cutting/04-material-fit-calibration.html",
      "source": "design-fabrication/03-laser-cutting/04-material-fit-calibration.qmd",
      "course": "design-fabrication",
      "track": "fabrication-tools",
      "strands": [
        "fabrication"
      ],
      "order": 3,
      "sequence_index": 31
    },
    {
      "id": "lesson-design-fabrication-03-laser-cutting-05-assemblies-hybrid-fabrication-qmd",
      "kind": "lesson",
      "title": "Assemblies and Hybrid Fabrication",
      "summary": "Combine cut parts, fasteners, and other processes into an assembly.",
      "href": "../design-fabrication/03-laser-cutting/05-assemblies-hybrid-fabrication.html",
      "source": "design-fabrication/03-laser-cutting/05-assemblies-hybrid-fabrication.qmd",
      "course": "design-fabrication",
      "track": "fabrication-tools",
      "strands": [
        "fabrication"
      ],
      "order": 4,
      "sequence_index": 32
    },
    {
      "id": "lesson-design-fabrication-03-laser-cutting-assembly-adhesives-finishing-qmd",
      "kind": "lesson",
      "title": "Laser-Cut Assembly, Adhesives & Finishing",
      "summary": "Select joints, adhesives, cleanup tools, sanding, stain, and surface details as connected design decisions.",
      "href": "../design-fabrication/03-laser-cutting/assembly-adhesives-finishing.html",
      "source": "design-fabrication/03-laser-cutting/assembly-adhesives-finishing.qmd",
      "course": "design-fabrication",
      "track": "fabrication-tools",
      "strands": [
        "fabrication"
      ],
      "order": 5,
      "sequence_index": 33
    },
    {
      "id": "lesson-design-fabrication-03-laser-cutting-07-wall-bench-module-qmd",
      "kind": "lesson",
      "title": "Wall and Bench Tool Module",
      "summary": "Design a visible, labelled, stable holder for a wall or workbench.",
      "href": "../design-fabrication/03-laser-cutting/07-wall-bench-module.html",
      "source": "design-fabrication/03-laser-cutting/07-wall-bench-module.qmd",
      "course": "design-fabrication",
      "track": "fabrication-tools",
      "strands": [
        "fabrication",
        "design-process"
      ],
      "order": 6,
      "sequence_index": 34
    },
    {
      "id": "lesson-design-fabrication-03-laser-cutting-08-capstone-qmd",
      "kind": "lesson",
      "title": "Design and Fabrication Capstone",
      "summary": "Plan, prototype, test, and document an original fabricated solution.",
      "href": "../design-fabrication/03-laser-cutting/08-capstone.html",
      "source": "design-fabrication/03-laser-cutting/08-capstone.qmd",
      "course": "design-fabrication",
      "track": "fabrication-tools",
      "strands": [
        "fabrication",
        "portfolio",
        "design-process"
      ],
      "order": 7,
      "sequence_index": 35
    },
    {
      "id": "lesson-design-fabrication-cad-parametric-modeling-phone-holder-design-qmd",
      "kind": "lesson",
      "title": "Choose Your Phone Holder",
      "summary": "Choose the simple Level 3 holder or create a Level 4 design.",
      "href": "../design-fabrication/cad-parametric-modeling/phone-holder-design.html",
      "source": "design-fabrication/cad-parametric-modeling/phone-holder-design.qmd",
      "course": "design-fabrication",
      "track": "phone-holder-project",
      "strands": [
        "fabrication"
      ],
      "order": 1,
      "sequence_index": 36
    },
    {
      "id": "lesson-design-fabrication-cad-parametric-modeling-introduction-to-cad-qmd",
      "kind": "lesson",
      "title": "CAD You Need",
      "summary": "Sketch, size, extrude, assemble, and draw the parts.",
      "href": "../design-fabrication/cad-parametric-modeling/introduction-to-cad.html",
      "source": "design-fabrication/cad-parametric-modeling/introduction-to-cad.qmd",
      "course": "design-fabrication",
      "track": "phone-holder-project",
      "strands": [
        "fabrication"
      ],
      "order": 2,
      "sequence_index": 37
    },
    {
      "id": "lesson-design-fabrication-hand-tools-tools-machines-qmd",
      "kind": "lesson",
      "title": "Tools and Machines",
      "summary": "See what each possible tool does in this project.",
      "href": "../design-fabrication/hand-tools/tools-machines.html",
      "source": "design-fabrication/hand-tools/tools-machines.qmd",
      "course": "design-fabrication",
      "track": "phone-holder-project",
      "strands": [
        "fabrication"
      ],
      "order": 3,
      "sequence_index": 38
    },
    {
      "id": "lesson-design-fabrication-hand-tools-phone-holder-qmd",
      "kind": "lesson",
      "title": "Build Steps",
      "summary": "Lay out, cut, drill, notch, sand, fit, and finish the holder.",
      "href": "../design-fabrication/hand-tools/phone-holder.html",
      "source": "design-fabrication/hand-tools/phone-holder.qmd",
      "course": "design-fabrication",
      "track": "phone-holder-project",
      "strands": [
        "fabrication"
      ],
      "order": 4,
      "sequence_index": 39
    },
    {
      "id": "lesson-design-fabrication-04-3d-printing-01-additive-cad-qmd",
      "kind": "lesson",
      "title": "Mission 1: Basic Keychain + CAD Foundations",
      "summary": "Learn the workplane, primitives, alignment, grouping, a through-hole and export before beginning the stamp project.",
      "href": "../design-fabrication/04-3d-printing/01-additive-cad.html",
      "source": "design-fabrication/04-3d-printing/01-additive-cad.qmd",
      "course": "design-fabrication",
      "track": "advanced-making",
      "strands": [
        "fabrication"
      ],
      "order": 1,
      "sequence_index": 40
    },
    {
      "id": "lesson-design-fabrication-04-3d-printing-logo-stamp-mission-qmd",
      "kind": "lesson",
      "title": "Mission 2: AA Stamp → Your Stamp",
      "summary": "Build and test the supplied AA arrow stamp, then repeat the workflow with an original logo.",
      "href": "../design-fabrication/04-3d-printing/logo-stamp-mission.html",
      "source": "design-fabrication/04-3d-printing/logo-stamp-mission.qmd",
      "course": "design-fabrication",
      "track": "advanced-making",
      "strands": [
        "fabrication",
        "design-process",
        "visual-design"
      ],
      "order": 2,
      "sequence_index": 41
    },
    {
      "id": "lesson-design-fabrication-04-3d-printing-tinkercad-logo-stamp-qmd",
      "kind": "lesson",
      "title": "Tinkercad Stamp Pathway",
      "summary": "Build the AA arrow first, then import, mirror, align, group, export, and test an original stamp.",
      "href": "../design-fabrication/04-3d-printing/tinkercad-logo-stamp.html",
      "source": "design-fabrication/04-3d-printing/tinkercad-logo-stamp.qmd",
      "course": "design-fabrication",
      "track": "advanced-making",
      "strands": [
        "fabrication",
        "visual-design"
      ],
      "order": 3,
      "sequence_index": 42
    },
    {
      "id": "lesson-design-fabrication-04-3d-printing-onshape-logo-stamp-qmd",
      "kind": "lesson",
      "title": "Onshape Stamp Pathway",
      "summary": "Build the same required AA-to-original sequence with variables, constrained sketches, and named features.",
      "href": "../design-fabrication/04-3d-printing/onshape-logo-stamp.html",
      "source": "design-fabrication/04-3d-printing/onshape-logo-stamp.qmd",
      "course": "design-fabrication",
      "track": "advanced-making",
      "strands": [
        "fabrication",
        "design-process",
        "visual-design"
      ],
      "order": 4,
      "sequence_index": 43
    },
    {
      "id": "lesson-design-fabrication-04-3d-printing-blender-stamp-handle-qmd",
      "kind": "lesson",
      "title": "Bonus: Blender Custom Stamp Handle",
      "summary": "After both required stamps pass, preserve the tested stamp face and add an ergonomic or sculptural mesh handle.",
      "href": "../design-fabrication/04-3d-printing/blender-stamp-handle.html",
      "source": "design-fabrication/04-3d-printing/blender-stamp-handle.qmd",
      "course": "design-fabrication",
      "track": "advanced-making",
      "strands": [
        "fabrication",
        "design-process"
      ],
      "order": 5,
      "sequence_index": 44
    },
    {
      "id": "lesson-design-fabrication-04-3d-printing-tinkercad-faux-enamel-logo-qmd",
      "kind": "lesson",
      "title": "Bonus: Tinkercad Faux-Enamel Badge",
      "summary": "Optionally reuse the successful original stamp logo as enclosed colour cavities.",
      "href": "../design-fabrication/04-3d-printing/tinkercad-faux-enamel-logo.html",
      "source": "design-fabrication/04-3d-printing/tinkercad-faux-enamel-logo.qmd",
      "course": "design-fabrication",
      "track": "advanced-making",
      "strands": [
        "fabrication",
        "visual-design"
      ],
      "order": 6,
      "sequence_index": 45
    },
    {
      "id": "lesson-design-fabrication-04-3d-printing-faux-enamel-pin-jewellery-qmd",
      "kind": "lesson",
      "title": "Bonus: Onshape Faux-Enamel Jewellery",
      "summary": "Optionally develop the fillable jewellery design as an editable parametric Onshape model.",
      "href": "../design-fabrication/04-3d-printing/faux-enamel-pin-jewellery.html",
      "source": "design-fabrication/04-3d-printing/faux-enamel-pin-jewellery.qmd",
      "course": "design-fabrication",
      "track": "advanced-making",
      "strands": [
        "fabrication",
        "portfolio",
        "design-process"
      ],
      "order": 7,
      "sequence_index": 46
    },
    {
      "id": "lesson-tej3-4-portfolio-index-qmd",
      "kind": "lesson",
      "title": "Build a Technical Portfolio",
      "summary": "Document an engineering problem, evidence, revisions, and conclusions in a private or teacher-approved format.",
      "href": "../tej3-4/portfolio/index.html",
      "source": "tej3-4/portfolio/index.qmd",
      "course": "tej",
      "track": "portfolio",
      "strands": [
        "portfolio"
      ],
      "order": 1,
      "sequence_index": 47
    },
    {
      "id": "lesson-tej3-4-electronics-library-components-schematic-basics-qmd",
      "kind": "lesson",
      "title": "Component Foundations: Circuits and Schematics",
      "summary": "Start from zero with circuit roles, schematic symbols, wires, nodes, junctions, ground, and one complete current path.",
      "href": "../tej3-4/electronics-library/components/schematic-basics.html",
      "source": "tej3-4/electronics-library/components/schematic-basics.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 1,
      "sequence_index": 48
    },
    {
      "id": "lesson-tej3-4-electronics-library-components-resistors-qmd",
      "kind": "lesson",
      "title": "Component Foundations: Resistors",
      "summary": "Distinguish resistance from a resistor and use value, tolerance, power, Ohm's law, and current limiting.",
      "href": "../tej3-4/electronics-library/components/resistors.html",
      "source": "tej3-4/electronics-library/components/resistors.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 2,
      "sequence_index": 49
    },
    {
      "id": "lesson-tej3-4-electronics-library-components-capacitors-qmd",
      "kind": "lesson",
      "title": "Capacitors 1: Capacitors from Zero",
      "summary": "Learn capacitor structure, symbols, units, polarity, voltage rating, stored charge, and energy.",
      "href": "../tej3-4/electronics-library/components/capacitors.html",
      "source": "tej3-4/electronics-library/components/capacitors.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 3,
      "sequence_index": 50
    },
    {
      "id": "lesson-tej3-4-electronics-library-components-rc-charge-discharge-qmd",
      "kind": "lesson",
      "title": "Capacitors 2: RC Charging and Discharging",
      "summary": "Predict starting conditions, steady state, charging curves, and discharging curves.",
      "href": "../tej3-4/electronics-library/components/rc-charge-discharge.html",
      "source": "tej3-4/electronics-library/components/rc-charge-discharge.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 4,
      "sequence_index": 51
    },
    {
      "id": "lesson-tej3-4-electronics-library-components-rc-time-constant-design-qmd",
      "kind": "lesson",
      "title": "Capacitors 3: RC Time Constants and Design",
      "summary": "Calculate a time constant, solve for a part value, select a standard part, and verify the actual result.",
      "href": "../tej3-4/electronics-library/components/rc-time-constant-design.html",
      "source": "tej3-4/electronics-library/components/rc-time-constant-design.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 5,
      "sequence_index": 52
    },
    {
      "id": "lesson-tej3-4-electronics-library-components-diodes-leds-qmd",
      "kind": "lesson",
      "title": "Component Foundations: Diodes and LEDs",
      "summary": "Learn diode direction, polarity, forward voltage, reverse blocking, LED current limiting, and diode-mode testing.",
      "href": "../tej3-4/electronics-library/components/diodes-leds.html",
      "source": "tej3-4/electronics-library/components/diodes-leds.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 6,
      "sequence_index": 53
    },
    {
      "id": "lesson-tej3-4-electronics-library-components-transistors-qmd",
      "kind": "lesson",
      "title": "Component Foundations: Transistors",
      "summary": "Introduce NPN and PNP transistor terminals, switching, ratings, pinout verification, and controlled load current.",
      "href": "../tej3-4/electronics-library/components/transistors.html",
      "source": "tej3-4/electronics-library/components/transistors.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 7,
      "sequence_index": 54
    },
    {
      "id": "lesson-tej3-4-electronics-library-components-op-amps-qmd",
      "kind": "lesson",
      "title": "Component Foundations: Operational Amplifiers",
      "summary": "Explain differential inputs, supply rails, negative feedback, voltage followers, real limits, and the optional XL741.",
      "href": "../tej3-4/electronics-library/components/op-amps.html",
      "source": "tej3-4/electronics-library/components/op-amps.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 8,
      "sequence_index": 55
    },
    {
      "id": "lesson-tej3-4-circuits-parallel-circuits-qmd",
      "kind": "lesson",
      "title": "Package 1: Basic Electricity and Parallel Circuits",
      "summary": "Connect basic electrical quantities, components, measurement, computer loads, and parallel-circuit calculations.",
      "href": "../tej3-4/circuits/parallel-circuits.html",
      "source": "tej3-4/circuits/parallel-circuits.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 9,
      "sequence_index": 56
    },
    {
      "id": "lesson-tej3-4-circuits-series-circuits-qmd",
      "kind": "lesson",
      "title": "Package 2: Parallel Review and Series Circuits",
      "summary": "Review one parallel calculation, then calculate current, voltage drops, resistance, and power in one-path circuits.",
      "href": "../tej3-4/circuits/series-circuits.html",
      "source": "tej3-4/circuits/series-circuits.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 10,
      "sequence_index": 57
    },
    {
      "id": "lesson-tej3-4-circuits-series-parallel-circuits-qmd",
      "kind": "lesson",
      "title": "Series-Parallel Combination Circuits, Part A",
      "summary": "Assignment 1.4: reduce mixed networks in stages and verify currents and voltages.",
      "href": "../tej3-4/circuits/series-parallel-circuits.html",
      "source": "tej3-4/circuits/series-parallel-circuits.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 11,
      "sequence_index": 58
    },
    {
      "id": "lesson-tej3-4-circuits-kirchhoffs-laws-qmd",
      "kind": "lesson",
      "title": "Kirchhoff's Laws",
      "summary": "Write current and voltage equations for circuits that cannot be reduced directly.",
      "href": "../tej3-4/circuits/kirchhoffs-laws.html",
      "source": "tej3-4/circuits/kirchhoffs-laws.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 12,
      "sequence_index": 59
    },
    {
      "id": "lesson-tej3-4-circuits-linear-algebra-circuits-qmd",
      "kind": "lesson",
      "title": "Linear Algebra for Circuits",
      "summary": "Solve simultaneous circuit equations by substitution, elimination, and matrices.",
      "href": "../tej3-4/circuits/linear-algebra-circuits.html",
      "source": "tej3-4/circuits/linear-algebra-circuits.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 13,
      "sequence_index": 60
    },
    {
      "id": "lesson-tej3-4-circuits-tinkercad-circuits-qmd",
      "kind": "lesson",
      "title": "Build and Measure Circuits in Tinkercad",
      "summary": "Build a low-voltage circuit, run the simulation, measure it, and compare the evidence with a calculation.",
      "href": "../tej3-4/circuits/tinkercad-circuits.html",
      "source": "tej3-4/circuits/tinkercad-circuits.qmd",
      "course": "tej",
      "track": "circuits-electronics",
      "strands": [
        "circuits"
      ],
      "order": 14,
      "sequence_index": 61
    },
    {
      "id": "lesson-tej3-4-computer-systems-safe-opening-and-parts-index-qmd",
      "kind": "lesson",
      "title": "Open a Computer Safely and Identify the Parts",
      "summary": "Use power and static precautions, identify the main internal parts, and compare HDD, SATA SSD, and M.2 storage.",
      "href": "../tej3-4/computer-systems/safe-opening-and-parts/index.html",
      "source": "tej3-4/computer-systems/safe-opening-and-parts/index.qmd",
      "course": "tej",
      "track": "computer-systems",
      "strands": [
        "systems"
      ],
      "order": 1,
      "sequence_index": 62
    },
    {
      "id": "lesson-tej3-4-computer-systems-usb-and-cable-management-index-qmd",
      "kind": "lesson",
      "title": "USB, Peripherals, and Cable Management",
      "summary": "Recognize USB connector shapes, check USB-C capabilities, connect common peripherals, and route cables cleanly.",
      "href": "../tej3-4/computer-systems/usb-and-cable-management/index.html",
      "source": "tej3-4/computer-systems/usb-and-cable-management/index.qmd",
      "course": "tej",
      "track": "computer-systems",
      "strands": [
        "systems"
      ],
      "order": 2,
      "sequence_index": 63
    },
    {
      "id": "lesson-tej3-4-linux-operating-systems-choosing-a-distribution-qmd",
      "kind": "lesson",
      "title": "Choosing a Linux Distribution",
      "summary": "Compare distribution families, desktop environments, hardware needs, software, and support.",
      "href": "../tej3-4/linux-operating-systems/choosing-a-distribution.html",
      "source": "tej3-4/linux-operating-systems/choosing-a-distribution.qmd",
      "course": "tej",
      "track": "linux-operating-systems",
      "strands": [
        "linux"
      ],
      "order": 1,
      "sequence_index": 64
    },
    {
      "id": "lesson-tej3-4-linux-operating-systems-install-linux-mint-qmd",
      "kind": "lesson",
      "title": "Install Linux Mint",
      "summary": "Prepare installation media, protect data, install Mint, and verify the result.",
      "href": "../tej3-4/linux-operating-systems/install-linux-mint.html",
      "source": "tej3-4/linux-operating-systems/install-linux-mint.qmd",
      "course": "tej",
      "track": "linux-operating-systems",
      "strands": [
        "linux"
      ],
      "order": 2,
      "sequence_index": 65
    },
    {
      "id": "lesson-tej3-4-linux-operating-systems-explore-linux-qmd",
      "kind": "lesson",
      "title": "Explore Linux",
      "summary": "Complete Computer Detective, explore Bashcrawl, and customize the Linux Mint desktop using separate submission contracts.",
      "href": "../tej3-4/linux-operating-systems/explore-linux.html",
      "source": "tej3-4/linux-operating-systems/explore-linux.qmd",
      "course": "tej",
      "track": "linux-operating-systems",
      "strands": [
        "linux"
      ],
      "order": 3,
      "sequence_index": 66
    },
    {
      "id": "lesson-tej3-4-linux-operating-systems-know-your-computer-qmd",
      "kind": "lesson",
      "title": "Know Your Linux Computer",
      "summary": "Record hardware, operating-system, storage, and device information.",
      "href": "../tej3-4/linux-operating-systems/know-your-computer.html",
      "source": "tej3-4/linux-operating-systems/know-your-computer.qmd",
      "course": "tej",
      "track": "linux-operating-systems",
      "strands": [
        "linux"
      ],
      "order": 4,
      "sequence_index": 67
    },
    {
      "id": "lesson-tej3-4-linux-operating-systems-files-terminal-permissions-qmd",
      "kind": "lesson",
      "title": "Files, Terminal, and Permissions",
      "summary": "Navigate paths, inspect files, and use permissions safely.",
      "href": "../tej3-4/linux-operating-systems/files-terminal-permissions.html",
      "source": "tej3-4/linux-operating-systems/files-terminal-permissions.qmd",
      "course": "tej",
      "track": "linux-operating-systems",
      "strands": [
        "linux"
      ],
      "order": 5,
      "sequence_index": 68
    },
    {
      "id": "lesson-tej3-4-linux-operating-systems-git-version-control-qmd",
      "kind": "lesson",
      "title": "Git Version Control",
      "summary": "Record, inspect, and share changes with a safe Git workflow.",
      "href": "../tej3-4/linux-operating-systems/git-version-control.html",
      "source": "tej3-4/linux-operating-systems/git-version-control.qmd",
      "course": "tej",
      "track": "linux-operating-systems",
      "strands": [
        "linux"
      ],
      "order": 6,
      "sequence_index": 69
    },
    {
      "id": "lesson-tej3-4-linux-operating-systems-quarto-website-qmd",
      "kind": "lesson",
      "title": "Build a Quarto Website",
      "summary": "Turn Markdown, code, and media into a small technical website.",
      "href": "../tej3-4/linux-operating-systems/quarto-website.html",
      "source": "tej3-4/linux-operating-systems/quarto-website.qmd",
      "course": "tej",
      "track": "linux-operating-systems",
      "strands": [
        "linux"
      ],
      "order": 7,
      "sequence_index": 70
    },
    {
      "id": "lesson-tej3-4-linux-operating-systems-publish-github-pages-qmd",
      "kind": "lesson",
      "title": "Publish with GitHub Pages",
      "summary": "Publish a reviewed static site without exposing secrets or private files.",
      "href": "../tej3-4/linux-operating-systems/publish-github-pages.html",
      "source": "tej3-4/linux-operating-systems/publish-github-pages.qmd",
      "course": "tej",
      "track": "linux-operating-systems",
      "strands": [
        "linux"
      ],
      "order": 8,
      "sequence_index": 71
    },
    {
      "id": "lesson-tej3-4-linux-operating-systems-python-data-logging-qmd",
      "kind": "lesson",
      "title": "Python Measurement Logging",
      "summary": "Write a small Python program that records measurements with units and timestamps.",
      "href": "../tej3-4/linux-operating-systems/python-data-logging.html",
      "source": "tej3-4/linux-operating-systems/python-data-logging.qmd",
      "course": "tej",
      "track": "linux-operating-systems",
      "strands": [
        "linux"
      ],
      "order": 9,
      "sequence_index": 72
    },
    {
      "id": "lesson-tej3-4-linux-operating-systems-python-analysis-curve-fitting-qmd",
      "kind": "lesson",
      "title": "Python Analysis and Curve Fitting",
      "summary": "Inspect recorded data and fit a simple model.",
      "href": "../tej3-4/linux-operating-systems/python-analysis-curve-fitting.html",
      "source": "tej3-4/linux-operating-systems/python-analysis-curve-fitting.qmd",
      "course": "tej",
      "track": "linux-operating-systems",
      "strands": [
        "linux"
      ],
      "order": 10,
      "sequence_index": 73
    },
    {
      "id": "lesson-tej3-4-linux-operating-systems-networking-ssh-tmux-qmd",
      "kind": "lesson",
      "title": "Networking, SSH, and tmux",
      "summary": "Diagnose a network connection and manage a remote Linux session safely.",
      "href": "../tej3-4/linux-operating-systems/networking-ssh-tmux.html",
      "source": "tej3-4/linux-operating-systems/networking-ssh-tmux.qmd",
      "course": "tej",
      "track": "linux-operating-systems",
      "strands": [
        "linux"
      ],
      "order": 11,
      "sequence_index": 74
    },
    {
      "id": "lesson-tej3-4-linux-operating-systems-power-and-raspberry-pi-bridge-qmd",
      "kind": "lesson",
      "title": "Power and Raspberry Pi Bridge",
      "summary": "Connect computer power concepts to a future Raspberry Pi build without inventing a lab.",
      "href": "../tej3-4/linux-operating-systems/power-and-raspberry-pi-bridge.html",
      "source": "tej3-4/linux-operating-systems/power-and-raspberry-pi-bridge.qmd",
      "course": "tej",
      "track": "linux-operating-systems",
      "strands": [
        "linux"
      ],
      "order": 12,
      "sequence_index": 75
    },
    {
      "id": "lesson-tej3-4-networking-how-wifi-and-ethernet-connect-index-qmd",
      "kind": "lesson",
      "title": "How Wi-Fi and Ethernet Connect",
      "summary": "Trace data through an access point or cable, a switch, a router, and Internet service.",
      "href": "../tej3-4/networking/how-wifi-and-ethernet-connect/index.html",
      "source": "tej3-4/networking/how-wifi-and-ethernet-connect/index.qmd",
      "course": "tej",
      "track": "networking",
      "strands": [
        "systems"
      ],
      "order": 1,
      "sequence_index": 76
    },
    {
      "id": "lesson-tej3-4-networking-ethernet-cable-categories-index-qmd",
      "kind": "lesson",
      "title": "Ethernet Cable Categories and Speeds",
      "summary": "Compare Cat5e, Cat6, Cat6A, and Cat8 and identify the 8P8C plug commonly called RJ45.",
      "href": "../tej3-4/networking/ethernet-cable-categories/index.html",
      "source": "tej3-4/networking/ethernet-cable-categories/index.qmd",
      "course": "tej",
      "track": "networking",
      "strands": [
        "systems"
      ],
      "order": 2,
      "sequence_index": 77
    },
    {
      "id": "lesson-tej3-4-networking-build-and-test-ethernet-cable-index-qmd",
      "kind": "lesson",
      "title": "Build and Test an Ethernet Cable",
      "summary": "Terminate both ends in T568B order, inspect the crimp, and verify all eight conductors with a tester.",
      "href": "../tej3-4/networking/build-and-test-ethernet-cable/index.html",
      "source": "tej3-4/networking/build-and-test-ethernet-cable/index.qmd",
      "course": "tej",
      "track": "networking",
      "strands": [
        "systems"
      ],
      "order": 3,
      "sequence_index": 78
    },
    {
      "id": "lesson-tej3-4-computational-engineering-jupyterlite-qmd",
      "kind": "lesson",
      "title": "Python Engineering Notebooks with JupyterLite",
      "summary": "Open, run, edit, save, download, and submit engineering notebooks in a browser.",
      "href": "../tej3-4/computational-engineering/jupyterlite.html",
      "source": "tej3-4/computational-engineering/jupyterlite.qmd",
      "course": "tej",
      "track": "programming-interfacing",
      "strands": [
        "programming"
      ],
      "order": 1,
      "sequence_index": 79
    },
    {
      "id": "lesson-tej3-4-computational-engineering-circuit-quest-qmd",
      "kind": "lesson",
      "title": "Circuit Quest: Power the Grid",
      "summary": "Rotate circuit tiles, complete three paths, light lamps, and see how a branch carries power.",
      "href": "../tej3-4/computational-engineering/circuit-quest.html",
      "source": "tej3-4/computational-engineering/circuit-quest.qmd",
      "course": "tej",
      "track": "programming-interfacing",
      "strands": [
        "programming"
      ],
      "order": 2,
      "sequence_index": 80
    },
    {
      "id": "lesson-tej3-4-computational-engineering-python-first-steps-qmd",
      "kind": "lesson",
      "title": "Assignment: Python First Steps",
      "summary": "Start from zero with notebook cells, printing, calculator operations, variables, four basic types, lists, and one small NumPy array.",
      "href": "../tej3-4/computational-engineering/python-first-steps.html",
      "source": "tej3-4/computational-engineering/python-first-steps.qmd",
      "course": "tej",
      "track": "programming-interfacing",
      "strands": [
        "programming"
      ],
      "order": 3,
      "sequence_index": 81
    },
    {
      "id": "lesson-tej3-4-computational-engineering-local-python-jupyter-qmd",
      "kind": "lesson",
      "title": "Run Python and Jupyter on Your Own Computer",
      "summary": "Choose a Jupyter route for Windows with WSL, macOS, Linux, native Windows, or Google Colab.",
      "href": "../tej3-4/computational-engineering/local-python-jupyter.html",
      "source": "tej3-4/computational-engineering/local-python-jupyter.qmd",
      "course": "tej",
      "track": "programming-interfacing",
      "strands": [
        "programming"
      ],
      "order": 4,
      "sequence_index": 82
    },
    {
      "id": "lesson-tej3-4-computational-engineering-python-numpy-foundations-qmd",
      "kind": "lesson",
      "title": "Assignment: Python and NumPy Foundations",
      "summary": "Continue from Python basics to NumPy arrays, plotting, documentation lookup, and evidence-based debugging before circuit linear algebra.",
      "href": "../tej3-4/computational-engineering/python-numpy-foundations.html",
      "source": "tej3-4/computational-engineering/python-numpy-foundations.qmd",
      "course": "tej",
      "track": "programming-interfacing",
      "strands": [
        "programming"
      ],
      "order": 5,
      "sequence_index": 83
    },
    {
      "id": "lesson-tej3-4-computational-engineering-finding-documentation-and-asking-for-help-qmd",
      "kind": "lesson",
      "title": "Find Documentation and Ask for Programming Help",
      "summary": "Reproduce a problem, search official documentation and Stack Overflow, and ask a complete technical question.",
      "href": "../tej3-4/computational-engineering/finding-documentation-and-asking-for-help.html",
      "source": "tej3-4/computational-engineering/finding-documentation-and-asking-for-help.qmd",
      "course": "tej",
      "track": "programming-interfacing",
      "strands": [
        "programming"
      ],
      "order": 6,
      "sequence_index": 84
    },
    {
      "id": "lesson-tej3-4-computational-engineering-kirchhoff-jupyter-assignment-qmd",
      "kind": "lesson",
      "title": "Assignment: From Two Loops to a Matrix",
      "summary": "Derive two signed KVL equations, arrange them in matrix form, and solve the same system numerically and symbolically.",
      "href": "../tej3-4/computational-engineering/kirchhoff-jupyter-assignment.html",
      "source": "tej3-4/computational-engineering/kirchhoff-jupyter-assignment.qmd",
      "course": "tej",
      "track": "programming-interfacing",
      "strands": [
        "programming"
      ],
      "order": 7,
      "sequence_index": 85
    },
    {
      "id": "lesson-tej3-4-computational-engineering-jupyter-electronics-lab-qmd",
      "kind": "lesson",
      "title": "Jupyter Electronics Lab",
      "summary": "Complete a simulation-first electronics pathway while components, instruments, or soldered kits are unavailable.",
      "href": "../tej3-4/computational-engineering/jupyter-electronics-lab.html",
      "source": "tej3-4/computational-engineering/jupyter-electronics-lab.qmd",
      "course": "tej",
      "track": "programming-interfacing",
      "strands": [
        "programming"
      ],
      "order": 8,
      "sequence_index": 86
    },
    {
      "id": "lesson-tej3-4-computational-engineering-midterm-circuit-investigation-qmd",
      "kind": "lesson",
      "title": "Life Checkpoint Upgrade: Jupyter + Tinkercad",
      "summary": "Digitize and correct the Life Checkpoint, solve it with NumPy, and verify the same circuit in Tinkercad.",
      "href": "../tej3-4/computational-engineering/midterm-circuit-investigation.html",
      "source": "tej3-4/computational-engineering/midterm-circuit-investigation.qmd",
      "course": "tej",
      "track": "programming-interfacing",
      "strands": [
        "programming"
      ],
      "order": 9,
      "sequence_index": 87
    },
    {
      "id": "lesson-tej3-4-capstone-index-qmd",
      "kind": "lesson",
      "title": "Mission Control",
      "summary": "Choose a route, review prerequisites, and use one common evidence and equipment-return contract.",
      "href": "../tej3-4/capstone/index.html",
      "source": "tej3-4/capstone/index.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 1,
      "sequence_index": 88
    },
    {
      "id": "lesson-tej3-4-capstone-mission-bank-qmd",
      "kind": "lesson",
      "title": "Inventory-Based Mission Bank",
      "summary": "Match available classroom equipment to foundation, Linux, sensor, motion, lighting, sound, and automotive missions.",
      "href": "../tej3-4/capstone/mission-bank.html",
      "source": "tej3-4/capstone/mission-bank.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 2,
      "sequence_index": 89
    },
    {
      "id": "lesson-tej3-4-capstone-projects-git-first-save-qmd",
      "kind": "lesson",
      "title": "Git First Save",
      "summary": "Create a local repository, make one useful commit, and show the recoverable checkpoint in Git history.",
      "href": "../tej3-4/capstone/projects/git-first-save.html",
      "source": "tej3-4/capstone/projects/git-first-save.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits",
        "linux",
        "portfolio"
      ],
      "order": 3,
      "sequence_index": 90
    },
    {
      "id": "lesson-tej3-4-capstone-projects-quarto-course-site-qmd",
      "kind": "lesson",
      "title": "Build Your Course Website",
      "summary": "Open the prepared Quarto starter, choose the core profile, edit the home page, and render a working local site.",
      "href": "../tej3-4/capstone/projects/quarto-course-site.html",
      "source": "tej3-4/capstone/projects/quarto-course-site.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits",
        "linux",
        "portfolio"
      ],
      "order": 4,
      "sequence_index": 91
    },
    {
      "id": "lesson-tej3-4-capstone-projects-beginner-breadboard-pi-led-qmd",
      "kind": "lesson",
      "title": "Beginner Breadboard and Raspberry Pi LED",
      "summary": "Map a breadboard, calculate LED current, power one protected LED from the Pi's fixed 3.3 V rail, and verify the circuit with a meter.",
      "href": "../tej3-4/capstone/projects/beginner-breadboard-pi-led.html",
      "source": "tej3-4/capstone/projects/beginner-breadboard-pi-led.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 5,
      "sequence_index": 92
    },
    {
      "id": "lesson-tej3-4-capstone-platform-index-qmd",
      "kind": "lesson",
      "title": "Raspberry Pi and BeagleBone Platform Setup",
      "summary": "Prepare an offline Linux controller station and complete the software-first platform sequence.",
      "href": "../tej3-4/capstone/platform/index.html",
      "source": "tej3-4/capstone/platform/index.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 6,
      "sequence_index": 93
    },
    {
      "id": "lesson-tej3-4-capstone-platform-gpio-progression-qmd",
      "kind": "lesson",
      "title": "GPIO Progression",
      "summary": "Move from a simulated signal to an LED, button, state machine, and safely isolated external load.",
      "href": "../tej3-4/capstone/platform/gpio-progression.html",
      "source": "tej3-4/capstone/platform/gpio-progression.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 7,
      "sequence_index": 94
    },
    {
      "id": "lesson-tej3-4-capstone-projects-reaction-timer-qmd",
      "kind": "lesson",
      "title": "Reaction Timer",
      "summary": "Build a playable Python and GPIO reaction game and analyze five measured results.",
      "href": "../tej3-4/capstone/projects/reaction-timer.html",
      "source": "tej3-4/capstone/projects/reaction-timer.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits",
        "programming"
      ],
      "order": 8,
      "sequence_index": 95
    },
    {
      "id": "lesson-tej3-4-capstone-projects-water-sensor-warning-qmd",
      "kind": "lesson",
      "title": "Water Sensor Warning",
      "summary": "Identify a water sensor, verify its output with a multimeter, and create a safe warning output.",
      "href": "../tej3-4/capstone/projects/water-sensor-warning.html",
      "source": "tej3-4/capstone/projects/water-sensor-warning.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 9,
      "sequence_index": 96
    },
    {
      "id": "lesson-tej3-4-capstone-projects-water-pump-controller-qmd",
      "kind": "lesson",
      "title": "Water Pump Controller",
      "summary": "Control a low-voltage pump from a separate fused supply through an approved driver and flyback diode.",
      "href": "../tej3-4/capstone/projects/water-pump-controller.html",
      "source": "tej3-4/capstone/projects/water-pump-controller.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 10,
      "sequence_index": 97
    },
    {
      "id": "lesson-tej3-4-capstone-projects-dc-motor-controller-qmd",
      "kind": "lesson",
      "title": "Low-Voltage DC Motor Controller",
      "summary": "Characterize a classroom low-voltage motor, build one-direction driver control, add PWM, and optionally add safe direction control.",
      "href": "../tej3-4/capstone/projects/dc-motor-controller.html",
      "source": "tej3-4/capstone/projects/dc-motor-controller.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 11,
      "sequence_index": 98
    },
    {
      "id": "lesson-tej3-4-capstone-projects-automatic-night-light-qmd",
      "kind": "lesson",
      "title": "Automatic Night Light",
      "summary": "Use a light sensor and state logic to control an indicator or approved lamp driver.",
      "href": "../tej3-4/capstone/projects/automatic-night-light.html",
      "source": "tej3-4/capstone/projects/automatic-night-light.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 12,
      "sequence_index": 99
    },
    {
      "id": "lesson-tej3-4-capstone-projects-beaglebone-traffic-light-qmd",
      "kind": "lesson",
      "title": "BeagleBone Traffic Light",
      "summary": "Build and program a timed traffic-light state machine.",
      "href": "../tej3-4/capstone/projects/beaglebone-traffic-light.html",
      "source": "tej3-4/capstone/projects/beaglebone-traffic-light.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 13,
      "sequence_index": 100
    },
    {
      "id": "lesson-tej3-4-capstone-projects-linux-alarm-qmd",
      "kind": "lesson",
      "title": "Linux Alarm",
      "summary": "Use Linux and Python to monitor an input and produce a controlled alarm response.",
      "href": "../tej3-4/capstone/projects/linux-alarm.html",
      "source": "tej3-4/capstone/projects/linux-alarm.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 14,
      "sequence_index": 101
    },
    {
      "id": "lesson-tej3-4-capstone-projects-capacitor-sound-demo-qmd",
      "kind": "lesson",
      "title": "Capacitor Sound Demonstration",
      "summary": "Connect stored charge and RC timing to a buzzer or sound demonstration.",
      "href": "../tej3-4/capstone/projects/capacitor-sound-demo.html",
      "source": "tej3-4/capstone/projects/capacitor-sound-demo.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 15,
      "sequence_index": 102
    },
    {
      "id": "lesson-tej3-4-capstone-projects-led-strip-controller-qmd",
      "kind": "lesson",
      "title": "LED Strip Controller",
      "summary": "Verify a classroom LED strip, control one channel through a protected driver, and add PWM colour control.",
      "href": "../tej3-4/capstone/projects/led-strip-controller.html",
      "source": "tej3-4/capstone/projects/led-strip-controller.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits",
        "programming"
      ],
      "order": 16,
      "sequence_index": 103
    },
    {
      "id": "lesson-tej3-4-capstone-projects-automotive-relay-trainer-qmd",
      "kind": "lesson",
      "title": "Automotive Relay Trainer",
      "summary": "Use an automotive relay to separate a low-current control circuit from a fused 12 V load circuit.",
      "href": "../tej3-4/capstone/projects/automotive-relay-trainer.html",
      "source": "tej3-4/capstone/projects/automotive-relay-trainer.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 17,
      "sequence_index": 104
    },
    {
      "id": "lesson-tej3-4-capstone-projects-salvage-machine-detective-qmd",
      "kind": "lesson",
      "title": "Salvage Machine Detective",
      "summary": "Trace an unknown salvaged mechanism while it is unpowered and reconstruct its connectors and functional blocks.",
      "href": "../tej3-4/capstone/projects/salvage-machine-detective.html",
      "source": "tej3-4/capstone/projects/salvage-machine-detective.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 18,
      "sequence_index": 105
    },
    {
      "id": "lesson-tej3-4-capstone-projects-student-choice-project-qmd",
      "kind": "lesson",
      "title": "Student-Choice Mission",
      "summary": "Propose a project using the same approval, safety, evidence, checkout, and return requirements.",
      "href": "../tej3-4/capstone/projects/student-choice-project.html",
      "source": "tej3-4/capstone/projects/student-choice-project.qmd",
      "course": "tej",
      "track": "missions-physical-computing",
      "strands": [
        "circuits"
      ],
      "order": 19,
      "sequence_index": 106
    }
  ],
  "edges": [
    {
      "from": "commons-hub",
      "to": "course-design-fabrication",
      "type": "contains"
    },
    {
      "from": "commons-hub",
      "to": "course-tej",
      "type": "contains"
    },
    {
      "from": "course-design-fabrication",
      "to": "track-design-fabrication-culture-land",
      "type": "contains"
    },
    {
      "from": "course-design-fabrication",
      "to": "track-design-fabrication-design-process",
      "type": "contains"
    },
    {
      "from": "course-design-fabrication",
      "to": "track-design-fabrication-emotions-visual-communication",
      "type": "contains"
    },
    {
      "from": "course-design-fabrication",
      "to": "track-design-fabrication-logo-design",
      "type": "contains"
    },
    {
      "from": "course-design-fabrication",
      "to": "track-design-fabrication-logo-animation",
      "type": "contains"
    },
    {
      "from": "course-design-fabrication",
      "to": "track-design-fabrication-accessible-design",
      "type": "contains"
    },
    {
      "from": "course-design-fabrication",
      "to": "track-design-fabrication-fabrication-tools",
      "type": "contains"
    },
    {
      "from": "course-design-fabrication",
      "to": "track-design-fabrication-phone-holder-project",
      "type": "contains"
    },
    {
      "from": "course-design-fabrication",
      "to": "track-design-fabrication-advanced-making",
      "type": "contains"
    },
    {
      "from": "course-tej",
      "to": "track-tej-portfolio",
      "type": "contains"
    },
    {
      "from": "course-tej",
      "to": "track-tej-circuits-electronics",
      "type": "contains"
    },
    {
      "from": "course-tej",
      "to": "track-tej-computer-systems",
      "type": "contains"
    },
    {
      "from": "course-tej",
      "to": "track-tej-linux-operating-systems",
      "type": "contains"
    },
    {
      "from": "course-tej",
      "to": "track-tej-networking",
      "type": "contains"
    },
    {
      "from": "course-tej",
      "to": "track-tej-programming-interfacing",
      "type": "contains"
    },
    {
      "from": "course-tej",
      "to": "track-tej-missions-physical-computing",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-culture-land",
      "to": "lesson-design-fabrication-culture-land-based-learning-grandmother-moon-seasons-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-culture-land",
      "to": "lesson-design-fabrication-culture-land-based-learning-land-lettermark-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-design-process",
      "to": "lesson-design-fabrication-design-process-situation-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-design-process",
      "to": "lesson-design-fabrication-design-process-user-needs-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-design-process",
      "to": "lesson-design-fabrication-design-process-necessities-nice-to-haves-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-design-process",
      "to": "lesson-design-fabrication-design-process-rank-priorities-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-design-process",
      "to": "lesson-design-fabrication-design-process-investigate-inquire-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-design-process",
      "to": "lesson-design-fabrication-design-process-create-communicate-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-design-process",
      "to": "lesson-design-fabrication-design-process-evaluate-repeat-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-emotions-visual-communication",
      "to": "lesson-design-fabrication-emotions-fear-anxiety-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-emotions-visual-communication",
      "to": "lesson-design-fabrication-emotions-anger-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-emotions-visual-communication",
      "to": "lesson-design-fabrication-emotions-disgust-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-emotions-visual-communication",
      "to": "lesson-design-fabrication-emotions-envy-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-emotions-visual-communication",
      "to": "lesson-design-fabrication-emotions-jealousy-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-emotions-visual-communication",
      "to": "lesson-design-fabrication-emotions-guilt-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-emotions-visual-communication",
      "to": "lesson-design-fabrication-emotions-shame-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-emotions-visual-communication",
      "to": "lesson-design-fabrication-emotions-happiness-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-emotions-visual-communication",
      "to": "lesson-design-fabrication-emotions-love-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-emotions-visual-communication",
      "to": "lesson-design-fabrication-emotions-sadness-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-logo-design",
      "to": "lesson-design-fabrication-logo-design-nameplate-text-photopea-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-logo-design",
      "to": "lesson-design-fabrication-logo-design-rough-sketch-to-svg-photopea-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-logo-design",
      "to": "lesson-design-fabrication-logo-design-02b-advanced-multilayer-tracing-photopea-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-logo-design",
      "to": "lesson-design-fabrication-logo-design-03-combine-logo-nameplate-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-logo-design",
      "to": "lesson-design-fabrication-03-laser-cutting-01-name-logo-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-logo-animation",
      "to": "lesson-design-fabrication-02-digital-design-animate-your-logo-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-accessible-design",
      "to": "lesson-design-fabrication-accessible-design-access-and-alt-text-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-accessible-design",
      "to": "lesson-design-fabrication-accessible-design-fonts-and-text-effects-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-accessible-design",
      "to": "lesson-design-fabrication-accessible-design-understanding-colour-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-accessible-design",
      "to": "lesson-design-fabrication-accessible-design-contrast-and-output-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-fabrication-tools",
      "to": "lesson-design-fabrication-03-laser-cutting-02-make-it-stand-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-fabrication-tools",
      "to": "lesson-design-fabrication-03-laser-cutting-03-measure-place-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-fabrication-tools",
      "to": "lesson-design-fabrication-03-laser-cutting-04-material-fit-calibration-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-fabrication-tools",
      "to": "lesson-design-fabrication-03-laser-cutting-05-assemblies-hybrid-fabrication-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-fabrication-tools",
      "to": "lesson-design-fabrication-03-laser-cutting-assembly-adhesives-finishing-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-fabrication-tools",
      "to": "lesson-design-fabrication-03-laser-cutting-07-wall-bench-module-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-fabrication-tools",
      "to": "lesson-design-fabrication-03-laser-cutting-08-capstone-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-phone-holder-project",
      "to": "lesson-design-fabrication-cad-parametric-modeling-phone-holder-design-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-phone-holder-project",
      "to": "lesson-design-fabrication-cad-parametric-modeling-introduction-to-cad-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-phone-holder-project",
      "to": "lesson-design-fabrication-hand-tools-tools-machines-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-phone-holder-project",
      "to": "lesson-design-fabrication-hand-tools-phone-holder-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-advanced-making",
      "to": "lesson-design-fabrication-04-3d-printing-01-additive-cad-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-advanced-making",
      "to": "lesson-design-fabrication-04-3d-printing-logo-stamp-mission-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-advanced-making",
      "to": "lesson-design-fabrication-04-3d-printing-tinkercad-logo-stamp-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-advanced-making",
      "to": "lesson-design-fabrication-04-3d-printing-onshape-logo-stamp-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-advanced-making",
      "to": "lesson-design-fabrication-04-3d-printing-blender-stamp-handle-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-advanced-making",
      "to": "lesson-design-fabrication-04-3d-printing-tinkercad-faux-enamel-logo-qmd",
      "type": "contains"
    },
    {
      "from": "track-design-fabrication-advanced-making",
      "to": "lesson-design-fabrication-04-3d-printing-faux-enamel-pin-jewellery-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-portfolio",
      "to": "lesson-tej3-4-portfolio-index-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-electronics-library-components-schematic-basics-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-electronics-library-components-resistors-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-electronics-library-components-capacitors-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-electronics-library-components-rc-charge-discharge-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-electronics-library-components-rc-time-constant-design-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-electronics-library-components-diodes-leds-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-electronics-library-components-transistors-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-electronics-library-components-op-amps-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-circuits-parallel-circuits-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-circuits-series-circuits-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-circuits-series-parallel-circuits-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-circuits-kirchhoffs-laws-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-circuits-linear-algebra-circuits-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-circuits-electronics",
      "to": "lesson-tej3-4-circuits-tinkercad-circuits-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-computer-systems",
      "to": "lesson-tej3-4-computer-systems-safe-opening-and-parts-index-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-computer-systems",
      "to": "lesson-tej3-4-computer-systems-usb-and-cable-management-index-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-linux-operating-systems",
      "to": "lesson-tej3-4-linux-operating-systems-choosing-a-distribution-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-linux-operating-systems",
      "to": "lesson-tej3-4-linux-operating-systems-install-linux-mint-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-linux-operating-systems",
      "to": "lesson-tej3-4-linux-operating-systems-explore-linux-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-linux-operating-systems",
      "to": "lesson-tej3-4-linux-operating-systems-know-your-computer-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-linux-operating-systems",
      "to": "lesson-tej3-4-linux-operating-systems-files-terminal-permissions-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-linux-operating-systems",
      "to": "lesson-tej3-4-linux-operating-systems-git-version-control-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-linux-operating-systems",
      "to": "lesson-tej3-4-linux-operating-systems-quarto-website-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-linux-operating-systems",
      "to": "lesson-tej3-4-linux-operating-systems-publish-github-pages-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-linux-operating-systems",
      "to": "lesson-tej3-4-linux-operating-systems-python-data-logging-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-linux-operating-systems",
      "to": "lesson-tej3-4-linux-operating-systems-python-analysis-curve-fitting-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-linux-operating-systems",
      "to": "lesson-tej3-4-linux-operating-systems-networking-ssh-tmux-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-linux-operating-systems",
      "to": "lesson-tej3-4-linux-operating-systems-power-and-raspberry-pi-bridge-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-networking",
      "to": "lesson-tej3-4-networking-how-wifi-and-ethernet-connect-index-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-networking",
      "to": "lesson-tej3-4-networking-ethernet-cable-categories-index-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-networking",
      "to": "lesson-tej3-4-networking-build-and-test-ethernet-cable-index-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-programming-interfacing",
      "to": "lesson-tej3-4-computational-engineering-jupyterlite-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-programming-interfacing",
      "to": "lesson-tej3-4-computational-engineering-circuit-quest-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-programming-interfacing",
      "to": "lesson-tej3-4-computational-engineering-python-first-steps-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-programming-interfacing",
      "to": "lesson-tej3-4-computational-engineering-local-python-jupyter-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-programming-interfacing",
      "to": "lesson-tej3-4-computational-engineering-python-numpy-foundations-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-programming-interfacing",
      "to": "lesson-tej3-4-computational-engineering-finding-documentation-and-asking-for-help-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-programming-interfacing",
      "to": "lesson-tej3-4-computational-engineering-kirchhoff-jupyter-assignment-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-programming-interfacing",
      "to": "lesson-tej3-4-computational-engineering-jupyter-electronics-lab-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-programming-interfacing",
      "to": "lesson-tej3-4-computational-engineering-midterm-circuit-investigation-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-index-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-mission-bank-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-git-first-save-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-quarto-course-site-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-beginner-breadboard-pi-led-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-platform-index-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-platform-gpio-progression-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-reaction-timer-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-water-sensor-warning-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-water-pump-controller-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-dc-motor-controller-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-automatic-night-light-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-beaglebone-traffic-light-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-linux-alarm-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-capacitor-sound-demo-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-led-strip-controller-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-automotive-relay-trainer-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-salvage-machine-detective-qmd",
      "type": "contains"
    },
    {
      "from": "track-tej-missions-physical-computing",
      "to": "lesson-tej3-4-capstone-projects-student-choice-project-qmd",
      "type": "contains"
    },
    {
      "from": "lesson-design-fabrication-culture-land-based-learning-grandmother-moon-seasons-qmd",
      "to": "lesson-design-fabrication-culture-land-based-learning-land-lettermark-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-culture-land-based-learning-grandmother-moon-seasons-qmd",
      "to": "lesson-design-fabrication-culture-land-based-learning-land-lettermark-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-design-process-situation-qmd",
      "to": "lesson-design-fabrication-design-process-user-needs-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-design-process-user-needs-qmd",
      "to": "lesson-design-fabrication-design-process-necessities-nice-to-haves-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-design-process-necessities-nice-to-haves-qmd",
      "to": "lesson-design-fabrication-design-process-rank-priorities-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-design-process-rank-priorities-qmd",
      "to": "lesson-design-fabrication-design-process-investigate-inquire-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-design-process-investigate-inquire-qmd",
      "to": "lesson-design-fabrication-design-process-create-communicate-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-design-process-create-communicate-qmd",
      "to": "lesson-design-fabrication-design-process-evaluate-repeat-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-emotions-fear-anxiety-qmd",
      "to": "lesson-design-fabrication-emotions-anger-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-emotions-fear-anxiety-qmd",
      "to": "lesson-design-fabrication-emotions-anger-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-emotions-anger-qmd",
      "to": "lesson-design-fabrication-emotions-disgust-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-emotions-anger-qmd",
      "to": "lesson-design-fabrication-emotions-disgust-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-emotions-disgust-qmd",
      "to": "lesson-design-fabrication-emotions-envy-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-emotions-disgust-qmd",
      "to": "lesson-design-fabrication-emotions-envy-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-emotions-envy-qmd",
      "to": "lesson-design-fabrication-emotions-jealousy-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-emotions-envy-qmd",
      "to": "lesson-design-fabrication-emotions-jealousy-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-emotions-jealousy-qmd",
      "to": "lesson-design-fabrication-emotions-guilt-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-emotions-jealousy-qmd",
      "to": "lesson-design-fabrication-emotions-guilt-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-emotions-guilt-qmd",
      "to": "lesson-design-fabrication-emotions-shame-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-emotions-guilt-qmd",
      "to": "lesson-design-fabrication-emotions-shame-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-emotions-shame-qmd",
      "to": "lesson-design-fabrication-emotions-happiness-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-emotions-shame-qmd",
      "to": "lesson-design-fabrication-emotions-happiness-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-emotions-happiness-qmd",
      "to": "lesson-design-fabrication-emotions-love-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-emotions-happiness-qmd",
      "to": "lesson-design-fabrication-emotions-love-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-emotions-love-qmd",
      "to": "lesson-design-fabrication-emotions-sadness-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-emotions-love-qmd",
      "to": "lesson-design-fabrication-emotions-sadness-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-logo-design-nameplate-text-photopea-qmd",
      "to": "lesson-design-fabrication-logo-design-rough-sketch-to-svg-photopea-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-logo-design-nameplate-text-photopea-qmd",
      "to": "lesson-design-fabrication-logo-design-rough-sketch-to-svg-photopea-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-logo-design-nameplate-text-photopea-qmd",
      "to": "lesson-design-fabrication-logo-design-03-combine-logo-nameplate-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-logo-design-rough-sketch-to-svg-photopea-qmd",
      "to": "lesson-design-fabrication-logo-design-02b-advanced-multilayer-tracing-photopea-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-logo-design-rough-sketch-to-svg-photopea-qmd",
      "to": "lesson-design-fabrication-logo-design-02b-advanced-multilayer-tracing-photopea-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-logo-design-02b-advanced-multilayer-tracing-photopea-qmd",
      "to": "lesson-design-fabrication-logo-design-03-combine-logo-nameplate-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-logo-design-02b-advanced-multilayer-tracing-photopea-qmd",
      "to": "lesson-design-fabrication-logo-design-03-combine-logo-nameplate-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-logo-design-03-combine-logo-nameplate-qmd",
      "to": "lesson-design-fabrication-03-laser-cutting-01-name-logo-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-logo-design-03-combine-logo-nameplate-qmd",
      "to": "lesson-design-fabrication-logo-design-rough-sketch-to-svg-photopea-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-logo-design-03-combine-logo-nameplate-qmd",
      "to": "lesson-design-fabrication-03-laser-cutting-01-name-logo-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-01-name-logo-qmd",
      "to": "lesson-design-fabrication-logo-design-nameplate-text-photopea-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-01-name-logo-qmd",
      "to": "lesson-design-fabrication-logo-design-rough-sketch-to-svg-photopea-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-01-name-logo-qmd",
      "to": "lesson-design-fabrication-logo-design-02b-advanced-multilayer-tracing-photopea-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-accessible-design-access-and-alt-text-qmd",
      "to": "lesson-design-fabrication-accessible-design-fonts-and-text-effects-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-accessible-design-fonts-and-text-effects-qmd",
      "to": "lesson-design-fabrication-accessible-design-understanding-colour-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-accessible-design-understanding-colour-qmd",
      "to": "lesson-design-fabrication-accessible-design-contrast-and-output-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-02-make-it-stand-qmd",
      "to": "lesson-design-fabrication-03-laser-cutting-03-measure-place-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-02-make-it-stand-qmd",
      "to": "lesson-design-fabrication-03-laser-cutting-03-measure-place-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-03-measure-place-qmd",
      "to": "lesson-design-fabrication-03-laser-cutting-04-material-fit-calibration-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-03-measure-place-qmd",
      "to": "lesson-design-fabrication-03-laser-cutting-04-material-fit-calibration-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-04-material-fit-calibration-qmd",
      "to": "lesson-design-fabrication-03-laser-cutting-05-assemblies-hybrid-fabrication-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-04-material-fit-calibration-qmd",
      "to": "lesson-design-fabrication-03-laser-cutting-05-assemblies-hybrid-fabrication-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-05-assemblies-hybrid-fabrication-qmd",
      "to": "lesson-design-fabrication-03-laser-cutting-assembly-adhesives-finishing-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-assembly-adhesives-finishing-qmd",
      "to": "lesson-design-fabrication-03-laser-cutting-07-wall-bench-module-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-assembly-adhesives-finishing-qmd",
      "to": "lesson-design-fabrication-03-laser-cutting-07-wall-bench-module-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-07-wall-bench-module-qmd",
      "to": "lesson-design-fabrication-03-laser-cutting-08-capstone-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-03-laser-cutting-07-wall-bench-module-qmd",
      "to": "lesson-design-fabrication-03-laser-cutting-08-capstone-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-cad-parametric-modeling-phone-holder-design-qmd",
      "to": "lesson-design-fabrication-cad-parametric-modeling-introduction-to-cad-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-cad-parametric-modeling-phone-holder-design-qmd",
      "to": "lesson-design-fabrication-cad-parametric-modeling-introduction-to-cad-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-cad-parametric-modeling-introduction-to-cad-qmd",
      "to": "lesson-design-fabrication-hand-tools-tools-machines-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-cad-parametric-modeling-introduction-to-cad-qmd",
      "to": "lesson-design-fabrication-hand-tools-tools-machines-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-hand-tools-tools-machines-qmd",
      "to": "lesson-design-fabrication-hand-tools-phone-holder-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-hand-tools-tools-machines-qmd",
      "to": "lesson-design-fabrication-hand-tools-phone-holder-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-01-additive-cad-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-logo-stamp-mission-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-01-additive-cad-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-blender-stamp-handle-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-logo-stamp-mission-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-tinkercad-logo-stamp-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-logo-stamp-mission-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-tinkercad-logo-stamp-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-logo-stamp-mission-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-onshape-logo-stamp-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-logo-stamp-mission-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-01-additive-cad-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-logo-stamp-mission-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-tinkercad-faux-enamel-logo-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-logo-stamp-mission-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-faux-enamel-pin-jewellery-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-tinkercad-logo-stamp-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-onshape-logo-stamp-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-tinkercad-logo-stamp-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-01-additive-cad-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-tinkercad-logo-stamp-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-onshape-logo-stamp-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-tinkercad-logo-stamp-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-tinkercad-faux-enamel-logo-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-onshape-logo-stamp-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-blender-stamp-handle-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-onshape-logo-stamp-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-01-additive-cad-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-onshape-logo-stamp-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-tinkercad-faux-enamel-logo-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-blender-stamp-handle-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-tinkercad-faux-enamel-logo-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-blender-stamp-handle-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-logo-stamp-mission-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-tinkercad-faux-enamel-logo-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-faux-enamel-pin-jewellery-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-tinkercad-faux-enamel-logo-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-01-additive-cad-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-tinkercad-faux-enamel-logo-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-faux-enamel-pin-jewellery-qmd",
      "type": "related"
    },
    {
      "from": "lesson-design-fabrication-04-3d-printing-faux-enamel-pin-jewellery-qmd",
      "to": "lesson-design-fabrication-04-3d-printing-01-additive-cad-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-schematic-basics-qmd",
      "to": "lesson-tej3-4-electronics-library-components-resistors-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-resistors-qmd",
      "to": "lesson-tej3-4-electronics-library-components-capacitors-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-capacitors-qmd",
      "to": "lesson-tej3-4-electronics-library-components-rc-charge-discharge-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-capacitors-qmd",
      "to": "lesson-tej3-4-electronics-library-components-rc-charge-discharge-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-rc-charge-discharge-qmd",
      "to": "lesson-tej3-4-electronics-library-components-rc-time-constant-design-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-rc-charge-discharge-qmd",
      "to": "lesson-tej3-4-circuits-tinkercad-circuits-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-rc-charge-discharge-qmd",
      "to": "lesson-tej3-4-electronics-library-components-rc-time-constant-design-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-rc-time-constant-design-qmd",
      "to": "lesson-tej3-4-electronics-library-components-diodes-leds-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-rc-time-constant-design-qmd",
      "to": "lesson-tej3-4-electronics-library-components-diodes-leds-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-rc-time-constant-design-qmd",
      "to": "lesson-tej3-4-electronics-library-components-transistors-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-rc-time-constant-design-qmd",
      "to": "lesson-tej3-4-electronics-library-components-op-amps-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-diodes-leds-qmd",
      "to": "lesson-tej3-4-electronics-library-components-transistors-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-transistors-qmd",
      "to": "lesson-tej3-4-electronics-library-components-op-amps-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-electronics-library-components-op-amps-qmd",
      "to": "lesson-tej3-4-circuits-parallel-circuits-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-circuits-parallel-circuits-qmd",
      "to": "lesson-tej3-4-circuits-series-circuits-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-circuits-parallel-circuits-qmd",
      "to": "lesson-tej3-4-circuits-series-circuits-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-circuits-parallel-circuits-qmd",
      "to": "lesson-tej3-4-circuits-tinkercad-circuits-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-circuits-series-circuits-qmd",
      "to": "lesson-tej3-4-circuits-series-parallel-circuits-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-circuits-series-circuits-qmd",
      "to": "lesson-tej3-4-circuits-tinkercad-circuits-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-circuits-series-parallel-circuits-qmd",
      "to": "lesson-tej3-4-circuits-kirchhoffs-laws-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-circuits-series-parallel-circuits-qmd",
      "to": "lesson-tej3-4-circuits-tinkercad-circuits-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-circuits-kirchhoffs-laws-qmd",
      "to": "lesson-tej3-4-circuits-linear-algebra-circuits-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-circuits-kirchhoffs-laws-qmd",
      "to": "lesson-tej3-4-computational-engineering-kirchhoff-jupyter-assignment-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-circuits-kirchhoffs-laws-qmd",
      "to": "lesson-tej3-4-circuits-tinkercad-circuits-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-circuits-linear-algebra-circuits-qmd",
      "to": "lesson-tej3-4-circuits-tinkercad-circuits-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-circuits-linear-algebra-circuits-qmd",
      "to": "lesson-tej3-4-computational-engineering-jupyterlite-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computer-systems-safe-opening-and-parts-index-qmd",
      "to": "lesson-tej3-4-computer-systems-usb-and-cable-management-index-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-choosing-a-distribution-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-install-linux-mint-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-install-linux-mint-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-explore-linux-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-explore-linux-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-know-your-computer-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-know-your-computer-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-files-terminal-permissions-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-files-terminal-permissions-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-git-version-control-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-git-version-control-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-quarto-website-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-git-version-control-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-quarto-website-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-quarto-website-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-publish-github-pages-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-quarto-website-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-publish-github-pages-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-publish-github-pages-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-python-data-logging-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-python-data-logging-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-python-analysis-curve-fitting-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-python-data-logging-qmd",
      "to": "lesson-tej3-4-computational-engineering-jupyterlite-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-python-data-logging-qmd",
      "to": "lesson-tej3-4-computational-engineering-local-python-jupyter-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-python-analysis-curve-fitting-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-networking-ssh-tmux-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-python-analysis-curve-fitting-qmd",
      "to": "lesson-tej3-4-computational-engineering-local-python-jupyter-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-linux-operating-systems-networking-ssh-tmux-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-power-and-raspberry-pi-bridge-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-networking-how-wifi-and-ethernet-connect-index-qmd",
      "to": "lesson-tej3-4-networking-ethernet-cable-categories-index-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-networking-ethernet-cable-categories-index-qmd",
      "to": "lesson-tej3-4-networking-build-and-test-ethernet-cable-index-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-jupyterlite-qmd",
      "to": "lesson-tej3-4-computational-engineering-circuit-quest-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-jupyterlite-qmd",
      "to": "lesson-tej3-4-computational-engineering-python-first-steps-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-jupyterlite-qmd",
      "to": "lesson-tej3-4-computational-engineering-python-numpy-foundations-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-jupyterlite-qmd",
      "to": "lesson-tej3-4-computational-engineering-circuit-quest-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-jupyterlite-qmd",
      "to": "lesson-tej3-4-computational-engineering-jupyter-electronics-lab-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-jupyterlite-qmd",
      "to": "lesson-tej3-4-computational-engineering-local-python-jupyter-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-circuit-quest-qmd",
      "to": "lesson-tej3-4-computational-engineering-python-first-steps-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-circuit-quest-qmd",
      "to": "lesson-tej3-4-computational-engineering-midterm-circuit-investigation-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-python-first-steps-qmd",
      "to": "lesson-tej3-4-computational-engineering-local-python-jupyter-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-local-python-jupyter-qmd",
      "to": "lesson-tej3-4-computational-engineering-python-numpy-foundations-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-local-python-jupyter-qmd",
      "to": "lesson-tej3-4-computational-engineering-finding-documentation-and-asking-for-help-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-python-numpy-foundations-qmd",
      "to": "lesson-tej3-4-computational-engineering-finding-documentation-and-asking-for-help-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-python-numpy-foundations-qmd",
      "to": "lesson-tej3-4-computational-engineering-python-first-steps-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-python-numpy-foundations-qmd",
      "to": "lesson-tej3-4-computational-engineering-kirchhoff-jupyter-assignment-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-python-numpy-foundations-qmd",
      "to": "lesson-tej3-4-computational-engineering-local-python-jupyter-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-python-numpy-foundations-qmd",
      "to": "lesson-tej3-4-computational-engineering-finding-documentation-and-asking-for-help-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-finding-documentation-and-asking-for-help-qmd",
      "to": "lesson-tej3-4-computational-engineering-kirchhoff-jupyter-assignment-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-kirchhoff-jupyter-assignment-qmd",
      "to": "lesson-tej3-4-computational-engineering-jupyter-electronics-lab-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-kirchhoff-jupyter-assignment-qmd",
      "to": "lesson-tej3-4-computational-engineering-jupyterlite-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-kirchhoff-jupyter-assignment-qmd",
      "to": "lesson-tej3-4-computational-engineering-local-python-jupyter-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-jupyter-electronics-lab-qmd",
      "to": "lesson-tej3-4-computational-engineering-midterm-circuit-investigation-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-jupyter-electronics-lab-qmd",
      "to": "lesson-tej3-4-computational-engineering-finding-documentation-and-asking-for-help-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-jupyter-electronics-lab-qmd",
      "to": "lesson-tej3-4-computational-engineering-python-first-steps-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-jupyter-electronics-lab-qmd",
      "to": "lesson-tej3-4-computational-engineering-python-numpy-foundations-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-jupyter-electronics-lab-qmd",
      "to": "lesson-tej3-4-computational-engineering-local-python-jupyter-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-midterm-circuit-investigation-qmd",
      "to": "lesson-tej3-4-computational-engineering-jupyterlite-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-computational-engineering-midterm-circuit-investigation-qmd",
      "to": "lesson-tej3-4-circuits-tinkercad-circuits-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-mission-bank-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-mission-bank-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-beginner-breadboard-pi-led-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-git-first-save-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-quarto-course-site-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-platform-index-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-platform-gpio-progression-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-water-sensor-warning-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-water-pump-controller-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-automatic-night-light-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-dc-motor-controller-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-beaglebone-traffic-light-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-student-choice-project-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-reaction-timer-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-led-strip-controller-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-salvage-machine-detective-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-linux-alarm-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-capacitor-sound-demo-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-index-qmd",
      "to": "lesson-tej3-4-capstone-projects-automotive-relay-trainer-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-git-first-save-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-git-first-save-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-quarto-course-site-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-publish-github-pages-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-portfolio-index-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-computational-engineering-python-first-steps-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-platform-index-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-platform-gpio-progression-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-reaction-timer-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-beaglebone-traffic-light-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-linux-alarm-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-networking-build-and-test-ethernet-cable-index-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-beginner-breadboard-pi-led-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-water-sensor-warning-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-automatic-night-light-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-water-pump-controller-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-dc-motor-controller-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-salvage-machine-detective-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-capacitor-sound-demo-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-led-strip-controller-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-mission-bank-qmd",
      "to": "lesson-tej3-4-capstone-projects-automotive-relay-trainer-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-git-first-save-qmd",
      "to": "lesson-tej3-4-capstone-projects-quarto-course-site-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-git-first-save-qmd",
      "to": "lesson-tej3-4-capstone-projects-quarto-course-site-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-git-first-save-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-git-version-control-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-quarto-course-site-qmd",
      "to": "lesson-tej3-4-capstone-projects-beginner-breadboard-pi-led-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-quarto-course-site-qmd",
      "to": "lesson-tej3-4-linux-operating-systems-quarto-website-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-beginner-breadboard-pi-led-qmd",
      "to": "lesson-tej3-4-capstone-platform-index-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-beginner-breadboard-pi-led-qmd",
      "to": "lesson-tej3-4-capstone-projects-reaction-timer-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-beginner-breadboard-pi-led-qmd",
      "to": "lesson-tej3-4-capstone-platform-gpio-progression-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-platform-index-qmd",
      "to": "lesson-tej3-4-capstone-platform-gpio-progression-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-platform-index-qmd",
      "to": "lesson-tej3-4-capstone-platform-gpio-progression-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-platform-gpio-progression-qmd",
      "to": "lesson-tej3-4-capstone-projects-reaction-timer-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-reaction-timer-qmd",
      "to": "lesson-tej3-4-capstone-projects-water-sensor-warning-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-water-sensor-warning-qmd",
      "to": "lesson-tej3-4-capstone-projects-water-pump-controller-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-water-sensor-warning-qmd",
      "to": "lesson-tej3-4-capstone-projects-water-pump-controller-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-water-pump-controller-qmd",
      "to": "lesson-tej3-4-capstone-projects-dc-motor-controller-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-dc-motor-controller-qmd",
      "to": "lesson-tej3-4-capstone-projects-automatic-night-light-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-dc-motor-controller-qmd",
      "to": "lesson-tej3-4-capstone-projects-water-pump-controller-qmd",
      "type": "related"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-automatic-night-light-qmd",
      "to": "lesson-tej3-4-capstone-projects-beaglebone-traffic-light-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-beaglebone-traffic-light-qmd",
      "to": "lesson-tej3-4-capstone-projects-linux-alarm-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-linux-alarm-qmd",
      "to": "lesson-tej3-4-capstone-projects-capacitor-sound-demo-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-capacitor-sound-demo-qmd",
      "to": "lesson-tej3-4-capstone-projects-led-strip-controller-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-led-strip-controller-qmd",
      "to": "lesson-tej3-4-capstone-projects-automotive-relay-trainer-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-automotive-relay-trainer-qmd",
      "to": "lesson-tej3-4-capstone-projects-salvage-machine-detective-qmd",
      "type": "sequence"
    },
    {
      "from": "lesson-tej3-4-capstone-projects-salvage-machine-detective-qmd",
      "to": "lesson-tej3-4-capstone-projects-student-choice-project-qmd",
      "type": "sequence"
    }
  ]
};
