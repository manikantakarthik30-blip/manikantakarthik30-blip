# Multiverse Developer Portfolio

A lightweight, responsive portfolio site designed to complement the GitHub profile README. The visual language uses a near-black cosmic background, electric blue and violet accents, CSS-built orbital forms, and readable project detail sections.

## Stack

- HTML, CSS, and vanilla JavaScript
- CSS illustrations instead of a required Three.js/WebGL dependency
- Google Fonts (Manrope and DM Mono) with system-font fallbacks
- No build step, package installation, API key, or paid service required

The scene is deliberately CSS-based for reliable mobile performance and graceful fallback. The experience remains usable without WebGL or third-party JavaScript. GitHub README and project links lead to actual repositories.

## Run locally

Open `index.html` in a browser, or serve the folder with Python:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deploy with GitHub Pages

1. Push or merge the portfolio files into the repository's default branch.
2. In repository Settings, open **Pages**.
3. Select **Deploy from a branch**, select `main` and `/ (root)`, then save.
4. Once GitHub Pages reports deployment complete, use the published URL from the Pages settings.

You can also import this static repository into Vercel or Netlify. No build command is needed and the output directory is the repository root.

## Files

- `index.html` — landing page, universe navigation, identity, project details, skills and contact
- `styles.css` — responsive cosmic theme, CSS portal artwork, project mockups, focus indicators and reduced-motion support
- `script.js` — accessible mobile navigation and optional pointer interaction
- `README.md` — GitHub-rendered profile summary
- `assets/` — existing profile SVG banner and dividers retained from the original profile

## Accuracy and limitations

- The 3D-inspired portals are CSS illustrations, not a Three.js/WebGL scene. That keeps deployment dependency-free; a true interactive 3D scene could be added in a later iteration.
- The live URL, LinkedIn URL, email, and resume are not added because the inspected profile did not provide confirmed values.
- Project descriptions are summarized from repository READMEs. SCIS explicitly labels its detection labels and incident figures as demo data; the portfolio repeats that qualification.
- AI Print OS describes its Canva and Adobe integration requirements and says live credential-backed integration has not been verified. Cyber-OS integrations similarly depend on configured external services.
- No build/test runner is configured because this is a static site without a package manager. Verify responsive layouts in a real browser before treating the design as production-approved.
