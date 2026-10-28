# Developer Portfolio

A responsive static portfolio website that complements the GitHub profile. The design uses a dark navy background, restrained blue and violet accents, and clear technology-focused illustrations.

## Stack

- HTML, CSS, and vanilla JavaScript
- CSS illustrations and lightweight pointer interaction
- Google Fonts (Manrope and DM Mono) with system-font fallbacks
- No build step, API key, backend, or paid service required

## Run locally

Open `index.html` in a browser, or serve the folder with Python:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deploy with GitHub Pages

1. Open repository Settings and select **Pages**.
2. Choose **Deploy from a branch**, select `main` and `/(root)`, and save.
3. After deployment succeeds, use the published URL shown in Settings → Pages.

These static files can also be hosted using Vercel or Netlify. No build command is required.

## Files

- `index.html` — landing page, selected projects, skills, and contact links
- `styles.css` — responsive theme, technology-logo area, project visuals, focus states, and reduced-motion support
- `script.js` — accessible mobile navigation and optional pointer interaction
- `README.md` — profile summary and automatically refreshed public repository index
- `assets/` — profile banner and supporting SVG graphics

## Accuracy and limitations

- CSS illustrations are visual elements, not a live WebGL simulation.
- The public repository index is refreshed automatically by GitHub Actions.
- The Smart Canal Intelligence System repository labels detection labels and incident figures as demo data; the profile preserves that qualification.
- External integrations in AI Print OS and Cyber-OS require configured services and should be verified before being described as production-ready.
- Check the site in a browser at desktop and mobile widths before treating its rendering as fully tested.
