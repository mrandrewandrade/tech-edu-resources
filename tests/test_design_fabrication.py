from __future__ import annotations

import re
import unittest
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CURRICULUM = SITE / "design-fabrication"


class DesignFabricationTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (SITE / relative).read_text(encoding="utf-8")

    def test_site_source_has_no_em_dashes(self) -> None:
        text_extensions = {
            ".bib", ".css", ".html", ".js", ".json", ".lua", ".md", ".qmd",
            ".scss", ".svg", ".txt", ".xml", ".yaml", ".yml",
        }
        for path in SITE.rglob("*"):
            relative = path.relative_to(SITE)
            if "_site" in relative.parts or ".quarto" in relative.parts:
                continue
            if not path.is_file() or path.suffix.lower() not in text_extensions:
                continue
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn("\u2014", path.read_text(encoding="utf-8"))

    def test_canonical_curriculum_structure_exists(self) -> None:
        required = [
            "index.qmd",
            "resources/index.qmd",
            "resources/work-in-progress/index.qmd",
            "01-nice-design-process/index.qmd",
            "systems-design-fabrication-track/index.qmd",
            "ai/index.qmd",
            "ai/07-ai-design-audit.qmd",
            "02-digital-design/index.qmd",
            "02-digital-design/06-blender-artistic-3d.qmd",
            "02-digital-design/07-website-ui-ux.qmd",
            "03-laser-cutting/index.qmd",
            "03-laser-cutting/holiday-ornament-reindeer.qmd",
            "03-laser-cutting/resources/reverse-engineer-improve.qmd",
            "04-3d-printing/index.qmd",
            "04-3d-printing/faux-enamel-pin-jewellery.qmd",
            "tools/tool-organizer-gallery/index.qmd",
            "tools/plate-builder/index.qmd",
            "tools/leg-builder/index.qmd",
            "05-cnc-digital-machining/index.qmd",
            "06-textiles-soft-goods/index.qmd",
            "07-other-fabrication/index.qmd",
            "applications/index.qmd",
            "applications/exploring-technologies/index.qmd",
            "applications/technological-design/index.qmd",
            "applications/manufacturing/index.qmd",
            "applications/construction/index.qmd",
            "applications/transportation/index.qmd",
            "applications/computer-technology/index.qmd",
            "applications/communications-technology/index.qmd",
            "applications/green-industries/index.qmd",
            "applications/hairstyling-aesthetics/index.qmd",
            "applications/hospitality-tourism/index.qmd",
            "applications/health-care/index.qmd",
        ]
        for relative in required:
            self.assertTrue((CURRICULUM / relative).is_file(), relative)

    def test_navigation_is_educator_first(self) -> None:
        config = self.read("_quarto.yml")
        educator = config.index("text: Educator Resources")
        classes = config.index("text: Classes")
        self.assertLess(educator, classes)
        ordered = ["General Slides", "General Materials", "General Design & Fabrication", "TEJ Notes"]
        positions = [config.index(item, educator) for item in ordered]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn('title: "TAS Notes"', config)

    def test_design_fabrication_sidebar_matches_the_public_collection(self) -> None:
        config = self.read("_quarto.yml")
        sidebar_start = config.index("- id: design-fabrication")
        sidebar_end = config.index("- id: tas2", sidebar_start)
        sidebar = config[sidebar_start:sidebar_end]
        ordered = [
            'text: "Design & Fabrication Home"',
            'text: "N.I.C.E. Design Process"',
            'text: "Logo Design"',
            'text: "Tool Organizer Project"',
            'section: "Fabrication Tools"',
        ]
        positions = [sidebar.index(item) for item in ordered]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("Systems Design & Fabrication Track", sidebar)
        self.assertNotIn("Ideas by Technology Area", sidebar)

    def test_retired_systems_track_is_not_published(self) -> None:
        config = self.read("_quarto.yml")
        self.assertNotIn("design-fabrication/systems-design-fabrication-track/index.qmd", config)
        landing = self.read("design-fabrication/index.qmd")
        self.assertNotIn("systems-design-fabrication-track/index.qmd", landing)

    def test_nice_create_communicate_and_evaluate_meanings_are_explicit(self) -> None:
        process = self.read("design-fabrication/design-process/index.qmd")
        for heading in (
            "## Situation: understand what is happening",
            "## N: Needs and Necessities",
            "## I: Investigate and Inquire",
            "## C: Create and Communicate",
            "## E: Evaluate",
            "## Repeat the cycle",
        ):
            self.assertIn(heading, process)
        for phrase in (
            "situation statement",
            "need statement",
            "evidence-based direction",
            "clear pitch",
            "revised solution supported by evidence",
        ):
            self.assertIn(phrase.lower(), process.lower())
        for worksheet in (
            "N.I.C.E. Needs Worksheet",
            "N.I.C.E. Inquiry Worksheet",
            "Communicate Worksheet Online",
            "Feedback Package",
            "N.I.C.E. Evaluate Worksheet",
            "N.I.C.E. Design Log",
        ):
            self.assertIn(worksheet, process)

    def test_public_pages_do_not_replace_local_safety_instruction(self) -> None:
        landing = self.read("design-fabrication/index.qmd")
        organizer = self.read("design-fabrication/laser-cutting/tool-organizer.qmd")
        self.assertNotIn("machine operating procedure", landing.lower())
        self.assertNotIn("machine operating procedure", organizer.lower())
        self.assertIn("safe handling", organizer)

    def test_homepage_prioritizes_reusable_resources(self) -> None:
        home = self.read("index.qmd")
        self.assertLess(home.index("Educator resources"), home.index("Current class slides"))
        self.assertLess(home.index("General Slides"), home.index("General Materials"))
        self.assertIn("design-fabrication/index.qmd", home)

    def test_laser_curriculum_distinguishes_core_from_extensions(self) -> None:
        laser = self.read("design-fabrication/03-laser-cutting/index.qmd")
        for name in ("Current TAS project", "Name + Logo Wood Name Tag", "Learn as the project requires", "Optional and general projects", "Holiday Ornament / Reindeer", "Tool Organizer"):
            self.assertIn(name, laser)
        self.assertIn("not a required TAS project", laser)

    def test_ai_literacy_sequence_is_complete_and_source_grounded(self) -> None:
        ai = self.read("design-fabrication/ai/index.qmd")
        for term in ("define the goal", "limited job", "meaningful versions", "privacy", "copyright", "Last reviewed: October 4, 2026"):
            self.assertIn(term, ai)
        for source in ("unesco.org", "unicef.org", "priv.gc.ca", "edu.gov.on.ca"):
            self.assertIn(source, ai)
        self.assertNotIn("peelschools.org", ai)
        audit = self.read("design-fabrication/ai/07-ai-design-audit.qmd")
        for term in ("flawed answer", "Measure the actual", "authoritative", "Rewrite the prompt", "Compare the two outputs", "AI-use disclosure"):
            self.assertIn(term, audit)

    def test_current_tas_projects_are_prominent_and_original(self) -> None:
        landing = self.read("design-fabrication/index.qmd")
        for project in (
            "N.I.C.E. Design Process",
            "Logo Design",
            "Tool Organizer Project",
        ):
            self.assertIn(project, landing)
        organizer = self.read("design-fabrication/laser-cutting/tool-organizer.qmd")
        for step in ("Measure the tools", "Make a small fit test", "build the prototype", "record the next revision"):
            self.assertIn(step, organizer)

    def test_digital_design_and_modelling_branches_are_explicit(self) -> None:
        digital = self.read("design-fabrication/02-digital-design/index.qmd")
        for term in ("Pencil2D", "Blender", "Website", "UI/UX"):
            self.assertIn(term, digital)
        modelling = self.read("design-fabrication/04-3d-printing/01-additive-cad.qmd")
        for term in ("Onshape", "parametric", "Blender", "STEP", "STL", "3MF", "editable source"):
            self.assertIn(term, modelling)

    def test_tool_organizer_gallery_preserves_evidence_status(self) -> None:
        gallery = self.read("design-fabrication/tools/tool-organizer-gallery/index.qmd")
        for term in ("DESIGN", "BUILD", "FEEDBACK", "REVISION", "TIJ1OR-E Knife Holder Design", "Revision 2", "March 22, 2024", "finished-project photo pending", "35°", "French cleat"):
            self.assertIn(term, gallery)
        self.assertIn("No substitute image has been invented", gallery)

    def test_curriculum_relevance_is_varied_and_compact(self) -> None:
        main = (CURRICULUM / "index.qmd").read_text(encoding="utf-8")
        self.assertLess(len(main.split()), 300)
        self.assertIn("A concise collection", main)
        self.assertIn("Fabrication tools", main)

    def test_curriculum_glossary_metadata_resolves(self) -> None:
        glossary = json.loads((ROOT / "glossary" / "glossary.json").read_text(encoding="utf-8"))
        canonical = set(glossary)
        integrated_pages = 0
        for page in CURRICULUM.rglob("*.qmd"):
            source = page.read_text(encoding="utf-8")
            if not source.startswith("---\n"):
                continue
            metadata = yaml.safe_load(source.split("---", 2)[1]) or {}
            terms = metadata.get("terms", [])
            highlighted = metadata.get("highlighted-terms", [])
            if terms:
                integrated_pages += 1
            self.assertLessEqual(set(terms), canonical, page)
            self.assertLessEqual(set(highlighted), set(terms), page)
        self.assertGreaterEqual(integrated_pages, 25)

    def test_application_layer_is_cross_process_and_substantial(self) -> None:
        landing = self.read("design-fabrication/applications/index.qmd")
        self.assertIn("The fabrication method is transferable", landing)
        for code in ("TIJ1O", "TDJ2O", "TMJ2O", "TCJ2O", "TTJ2O", "TEJ2O", "TGJ2O", "THJ2O", "TXJ2O", "TFJ2O", "TPJ2O"):
            self.assertIn(code, landing)
        pages = list((CURRICULUM / "applications").glob("*/index.qmd"))
        self.assertEqual(len(pages), 11)
        for page in pages:
            content = page.read_text(encoding="utf-8")
            self.assertGreaterEqual(content.count("ter-project-card"), 3, page)
            for field in ("<dt>Process", "<dt>Skills", "<dt>Material", "<dt>Structural", "<dt>Use boundary", "<dt>Library", "<dt>Lesson", "<dt>Extension"):
                self.assertIn(field, content, (page, field))

    def test_sensitive_application_pages_state_boundaries(self) -> None:
        hair = self.read("design-fabrication/applications/hairstyling-aesthetics/index.qmd").lower()
        hospitality = self.read("design-fabrication/applications/hospitality-tourism/index.qmd").lower()
        health = self.read("design-fabrication/applications/health-care/index.qmd").lower()
        self.assertIn("heat-safe", hair)
        self.assertIn("food-contact", hospitality)
        self.assertIn("not medical devices", health)

    def test_course_code_queries_have_specific_pages(self) -> None:
        expectations = {
            "tool organizer": "design-fabrication/laser-cutting/tool-organizer.qmd",
            "logo design": "design-fabrication/logo-design/index.qmd",
            "design process": "design-fabrication/design-process/index.qmd",
            "fabrication plate builder": "design-fabrication/tools/plate-builder/index.qmd",
        }
        for query, relative in expectations.items():
            words = re.findall(r"[a-z0-9]+", query.lower())
            content = self.read(relative).lower()
            self.assertTrue(all(word in content for word in words), (query, relative))

    def test_old_tas_route_is_redirect_only(self) -> None:
        old = self.read("tas2/index.qmd")
        self.assertIn("http-equiv=\"refresh\"", old)
        self.assertIn("rel=\"canonical\"", old)
        self.assertIn("design-fabrication", old)
        self.assertNotIn("TAS Notes", old)

    def test_library_and_curriculum_cross_link(self) -> None:
        library = self.read("teaching-materials/laser-cutting/index.qmd")
        curriculum = self.read("design-fabrication/laser-cutting/tool-organizer.qmd")
        self.assertIn("design-fabrication/laser-cutting/tool-organizer.qmd", library)
        self.assertIn("teaching-materials/laser-cutting", curriculum)

    def legacy_first_laser_projects_toolkit_is_complete(self) -> None:
        toolkit = self.read("design-fabrication/03-laser-cutting/resources/index.qmd")
        for label in ("Basic Geometry", "Hole", "Slot", "Structure", "Wall + Mounting", "Organizer"):
            self.assertIn(label, toolkit)
        for relative in (
            "design-fabrication/03-laser-cutting/resources/fabrication-planning-worksheet.qmd",
            "design-fabrication/03-laser-cutting/resources/paper-to-inkscape.qmd",
            "design-fabrication/03-laser-cutting/resources/pill-bottle-organizer.qmd",
            "design-fabrication/03-laser-cutting/resources/active-sequence-slides.qmd",
        ):
            self.assertTrue((SITE / relative).is_file(), relative)

        first_project = self.read("design-fabrication/03-laser-cutting/01-name-logo.qmd")
        self.assertIn("pre-cut", first_project)
        self.assertIn("Photopea", first_project)
        self.assertIn("export", first_project.lower())
        self.assertIn("PNG", first_project)
        for detail in (
            "3300 × 1200",
            "75 px",
            "Source Sans 3 Bold",
            "NDRADE",
            "JPG / JPEG",
            "WebP",
            "SVG",
            "0.25 inch safe margin",
            "Student submission checklist",
        ):
            self.assertIn(detail, first_project)
        for screenshot in (
            "01-create-canvas-inches.jpg",
            "02-safe-margin-guides.jpg",
            "03-place-transparent-pngs.jpg",
            "04-add-readable-name.jpg",
            "05-final-layout.jpg",
            "06-export-png.jpg",
            "07-raster-format-guide.svg",
            "08-variation-1-a-andrade.png",
            "09-variation-2-max-readability.png",
            "10-variation-3-aa-ndrade.png",
            "11-variation-3-alignment-check.png",
        ):
            self.assertIn(screenshot, first_project)
            self.assertTrue((SITE / "assets" / "name-tag-photopea" / screenshot).is_file(), screenshot)

        downloads = SITE / "assets" / "name-tag-photopea" / "downloads"
        for student_file in (
            "variation-1-commons-a-andrade.psd",
            "variation-1-commons-a-andrade.png",
            "variation-2-maximum-readability.psd",
            "variation-2-maximum-readability.png",
            "variation-3-thick-aa-ndrade.psd",
            "variation-3-thick-aa-ndrade.png",
            "name-tag-design-pack.zip",
        ):
            self.assertIn(student_file, first_project)
            self.assertTrue((downloads / student_file).is_file(), student_file)
            self.assertGreater((downloads / student_file).stat().st_size, 10_000, student_file)

        for worksheet in (
            "personal-logo-worksheet.pdf",
            "personal-logo-photopea-guide.pdf",
            "name-tag-paper-prototype.pdf",
        ):
            self.assertTrue((SITE / "assets" / "name-tag-photopea" / worksheet).is_file(), worksheet)
            self.assertGreater((SITE / "assets" / "name-tag-photopea" / worksheet).stat().st_size, 10_000, worksheet)

        logo_lesson = self.read("design-fabrication/02-digital-design/03-logos-lettermarks.qmd")
        for detail in (
            "Personal Logo",
            "three different ideas",
            "Vectorize Bitmap",
            "Export As > SVG",
            "personal-logo-worksheet.pdf",
            "personal-logo-photopea-guide.pdf",
            "Bitmap_VS_SVG.svg",
            "photographing or scanning a hand-drawn idea",
            "two or three colours at most",
            "landscape-to-logo.svg",
            "File > Open & Place",
            "Opacity to 30%",
            "Press **U** for a Shape tool",
            "Press **P** for the Pen tool",
            "Press **T** for the Type tool",
            "Ctrl+T",
            "scale-free logo master",
            "1amzmA_uCjCnRD1YX1KIoW8YhIvRrl10hZQvdADdNV8Y",
            "14Tu-Nq394PJ6q7XqGiKx-N0yA6PrIBK4M53pB01OFHw",
            "personal-logo-starting-idea.svg",
            "personal-logo-three-sketches.svg",
            "personal-logo-colour-example.svg",
            "personal-logo-four-tests.svg",
            "personal-logo-file-set.svg",
            "01-photopea-personal-logo.jpg",
            "06-photopea-personal-logo.jpg",
        ):
            self.assertIn(detail, logo_lesson)
        self.assertTrue((SITE / "assets" / "name-tag-photopea" / "landscape-to-logo.svg").is_file())
        for screenshot_number in range(1, 7):
            screenshots = list((SITE / "assets" / "personal-logo-photopea").glob(f"{screenshot_number:02d}-*.jpg"))
            self.assertEqual(len(screenshots), 1, screenshot_number)
            self.assertGreater(screenshots[0].stat().st_size, 10_000, screenshots[0].name)

        for clean_screenshot in (
            "02-safe-margin-guides.jpg",
            "03-place-transparent-pngs.jpg",
            "04-add-readable-name.jpg",
            "05-final-layout.jpg",
            "06-export-png.jpg",
        ):
            self.assertTrue((SITE / "assets" / "name-tag-photopea" / "clean" / clean_screenshot).is_file())
            self.assertIn(f"clean/{clean_screenshot}", first_project)

        organizer = self.read("design-fabrication/03-laser-cutting/resources/pill-bottle-organizer.qmd")
        for design in ("Simple shelf", "Dowel-supported", "Reinforced wall", "Removable wall / bench", "Captured bottle rack"):
            self.assertIn(design, organizer)
        self.assertIn("unverified", organizer)
        self.assertIn("Ideas, not answers", organizer)
        self.assertEqual(organizer.count('class="ter-assembly-card"'), 5)
        self.assertEqual(organizer.count("True-size parts sheet"), 5)
        self.assertEqual(organizer.count("Download parts SVG"), 5)

        for relative in ("exploded.svg", "parts.svg"):
            self.assertGreaterEqual(organizer.count(relative), 10)

        laser_home = self.read("design-fabrication/03-laser-cutting/index.qmd")
        self.assertIn("Open the Tool Organizer Gallery", laser_home)
        self.assertIn("removable-wall-bench-rack/exploded.svg", laser_home)

        nav = self.read("_quarto.yml")
        self.assertIn("Organizer Reference Assemblies", nav)
        self.assertIn("Tool Organizer Gallery", nav)
        self.assertIn("Fabrication Planning Sheet", nav)
        self.assertIn("Fabrication Plate Builder", nav)

    def test_first_laser_projects_toolkit_is_complete(self) -> None:
        landing = self.read("design-fabrication/index.qmd")
        organizer = self.read("design-fabrication/laser-cutting/tool-organizer.qmd")
        logo = self.read("design-fabrication/logo-design/index.qmd")
        nav = self.read("_quarto.yml")

        for label in (
            "Fabrication Plate Builder",
            "Laser-Cut Leg & Support Builder",
            "Tool Organizer Gallery",
            "Laser-Cutting Files and Resources",
        ):
            self.assertIn(label, landing)
            self.assertIn(label, nav)
        for tool in ("Photopea", "GIMP", "Adobe Photoshop"):
            self.assertIn(tool, logo)
        self.assertEqual(logo.count("youtube.com/watch"), 4)
        for phrase in (
            "measure real tools",
            "Fabrication Plate Builder",
            "Laser-Cut Leg & Support Builder",
            "small fit test",
            "record the next revision",
        ):
            self.assertIn(phrase, organizer)

    def test_reverse_engineering_assignment_is_originality_and_evidence_first(self) -> None:
        assignment = self.read("design-fabrication/03-laser-cutting/resources/reverse-engineer-improve.qmd")
        for quality in ("Faster", "Cheaper", "Better looking", "More ergonomic", "More positive", "More serviceable"):
            self.assertIn(quality, assignment)
        for evidence in ("three attributed references", "decision matrix", "critical-dimension coupon", "before-and-after comparison", "user test", "revision notes"):
            self.assertIn(evidence, assignment)
        for boundary in ("The goal is not to make a copy", "Do not trace product photographs", "Reuse a file only when its licence clearly permits"):
            self.assertIn(boundary, assignment)
        for source in ("etsy.com", "glowforge.com", "instructables.com", "printables.com", "thingiverse.com", "makerworld.com", "onshape.com", "sketchfab.com", "openverse.org", "thenounproject.com"):
            self.assertIn(source, assignment)

        toolkit = self.read("design-fabrication/03-laser-cutting/resources/index.qmd")
        self.assertIn("Good Idea, Better Product", toolkit)
        self.assertIn("reverse-engineer-improve.qmd", toolkit)

    def legacy_free_online_resource_directory_is_broad_and_careful(self) -> None:
        directory = self.read("design-fabrication/resources/work-in-progress/index.qmd")
        for heading in (
            "Find ideas and understand products",
            "Inclusive design, ergonomics, and accessibility",
            "Graphics, images, icons, fonts, and colour",
            "Laser cutting and 2D fabrication",
            "3D CAD and modelling tools",
            "Downloadable 3D models and scans",
            "Electronics, circuits, and physical computing",
            "Websites, UI/UX, and coding",
            "Textiles, patterns, and soft goods",
            "Repair, circular design, and responsible fabrication",
            "CNC and digital machining",
        ):
            self.assertIn(heading, directory)

        links = re.findall(r"https://[^)\s]+", directory)
        domains = {re.sub(r"^www\.", "", link.split("/", 3)[2].lower()) for link in links}
        self.assertGreaterEqual(len(links), 70)
        self.assertGreaterEqual(len(domains), 55)

        for domain in (
            "instructables.com", "ifixit.com", "w3.org", "inkscape.org",
            "openverse.org", "onshape.com", "freecad.org", "printables.com",
            "science.nasa.gov", "si.edu", "kicad.org", "microbit.org",
            "developer.mozilla.org", "freesewing.eu", "inkstitch.org",
            "preciousplastic.com", "linuxcnc.org",
        ):
            self.assertIn(domain, domains)

        for boundary in (
            "Free access is not the same as permission to copy",
            "Free account",
            "Mixed",
            "creator, page title, URL, access date, and licence",
            "Teacher review is required",
            "Online examples are not operating procedures",
            "Work in progress · Research notes · Not fully reviewed",
            "broad initial online research pass",
            "received complete editorial, technical, licensing, accessibility, age-suitability, or classroom review",
            "Entries are leads, not endorsements",
        ):
            self.assertIn(boundary, directory)

        nav = self.read("_quarto.yml")
        self.assertIn("Free Online Resource Directory · Work in Progress", nav)
        self.assertIn("design-fabrication/resources/work-in-progress/index.qmd", nav)

        redirect = self.read("design-fabrication/resources/index.qmd")
        self.assertIn('http-equiv="refresh"', redirect)
        self.assertIn("resources/work-in-progress/", redirect)

        for relative in (
            "design-fabrication/index.qmd",
            "design-fabrication/01-nice-design-process/index.qmd",
            "design-fabrication/02-digital-design/index.qmd",
            "design-fabrication/02-digital-design/07-website-ui-ux.qmd",
            "design-fabrication/03-laser-cutting/resources/index.qmd",
            "design-fabrication/03-laser-cutting/resources/reverse-engineer-improve.qmd",
            "design-fabrication/04-3d-printing/index.qmd",
            "design-fabrication/05-cnc-digital-machining/index.qmd",
            "design-fabrication/06-textiles-soft-goods/index.qmd",
            "design-fabrication/07-other-fabrication/index.qmd",
        ):
            content = self.read(relative)
            self.assertIn("resources/work-in-progress/index.qmd", content, relative)
            self.assertIn("Work in Progress", content, relative)

    def test_draft_resource_directory_is_not_published(self) -> None:
        config = self.read("_quarto.yml")
        landing = self.read("design-fabrication/index.qmd")
        self.assertNotIn("design-fabrication/resources/work-in-progress/index.qmd", config)
        self.assertNotIn("Free Online Resource Directory", config)
        self.assertNotIn("Free Online Resource Directory", landing)

    def test_public_classroom_kit_has_palettes_and_reference_assemblies(self) -> None:
        kit = SITE / "assets" / "laser-library" / "classroom-kit"
        self.assertTrue((kit / "manifest.json").is_file())
        self.assertEqual(len(list((kit / "palettes").glob("*.svg"))), 6)
        assembly = __import__("json").loads((kit / "pill-bottle" / "assemblies.json").read_text(encoding="utf-8"))
        self.assertEqual(len(assembly["designs"]), 5)
        self.assertIn("captured-bottle-rack", assembly["designs"])

    def test_plate_builder_and_calibration_workflow_are_connected(self) -> None:
        builder = self.read("design-fabrication/tools/plate-builder/index.qmd")
        for label in (
            "Rectangle", "Rounded rectangle", "Circle", "Ring", "Staggered grid", "Radial", "Perimeter",
            "Outer diameter", "Ring wall thickness", "Finished hole diameter", "Circle-of-centres radius",
            "Download cut SVG", "Download settings JSON", "Copy share link", "What the downloads contain",
        ):
            self.assertIn(label, builder)
        script = self.read("assets/plate-builder.js")
        for group in ("CUT_OUTER", "CUT_HOLES", "GUIDES"):
            self.assertIn(group, script)
        self.assertNotIn("<text", script.split("function buildSvg", 1)[1].split("function encodeState", 1)[0])

        calibration = self.read("design-fabrication/03-laser-cutting/04-material-fit-calibration.qmd")
        for asset in ("material-thickness", "ruler-check", "dimension-verification", "kerf-test", "tab-fit", "slot-fit", "four-fit-series", "hole-fit"):
            self.assertIn(asset, calibration)
        for source in ("support.brmlasers.com", "ponoko.com"):
            self.assertIn(source, calibration)
        self.assertIn("Printable calibration record", calibration)

    def test_leg_builder_and_easel_mechanics_are_connected(self) -> None:
        builder = self.read("design-fabrication/tools/leg-builder/index.qmd")
        for label in (
            "Straight tabbed pair", "Angled tabbed pair", "Triangular side cheeks",
            "Narrow hinged rear strut", "Wide single easel back", "Flat parts to cut",
            "How the selected support is used", "Which reference file do I use?",
            "Interlocking X-base", "Download SVG", "Copy share link",
            "Measured material thickness", "Body length", "Calculated overall height",
            "Body mating slot", "What the dimensions mean",
            'data-unit-button="mm"', 'data-unit-button="in"',
        ):
            self.assertIn(label, builder)
        for source in ("freepatternsarea.com", "nationalartcraft.com", "troteclaser.com", "victocraft.com", "dpmsign.com"):
            self.assertIn(source, builder)
        plate_builder = self.read("design-fabrication/tools/plate-builder/index.qmd")
        self.assertIn('data-unit-button="mm"', plate_builder)
        self.assertIn('data-unit-button="in"', plate_builder)
        script = self.read("assets/leg-builder.js")
        for group in ("CUT_PARTS", "CUT_HOLES", "MATING_SLOTS", "FIT_COUPON", "GUIDES"):
            self.assertIn(group, script)
        mechanics = self.read("design-fabrication/03-laser-cutting/02-make-it-stand.qmd")
        for concept in ("bending moment", "rear kickstand", "support footprint", "cross rail", "pivot"):
            self.assertIn(concept, mechanics)
        for worked_example in ("11 × 4 inch name plate", "two high supports", "one low centre support"):
            self.assertIn(worked_example, mechanics)
        self.assertIn("tools/leg-builder/index.qmd", mechanics)


if __name__ == "__main__":
    unittest.main()
