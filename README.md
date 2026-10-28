# StrikePoint Ventures

Website for StrikePoint Ventures LLP: quantitative research, trading technology and a proprietary trading desk.

## Structure

| Path | What it is |
| :--- | :--- |
| `pages/` | The generated HTML pages the server sends |
| `assets/css/site.css` | The single stylesheet (palette themes are `html[data-theme="1".."3"]`) |
| `assets/js/site.js` | Menu, tabs, reveal-on-scroll, regulatory notice, contact form |
| `assets/img/mark.svg` | Logo mark |
| `tools/build_site.py` | Builds every page in `pages/` from shared header, footer and content |
| `tools/arts.py` | SVG illustrations used across pages |
| `src/server.ts` | Express server (compiled to `dist/server.js`) |

## Routes

`/`, `/about`, `/services`, `/services/research-technology`, `/services/atlas-helm`, `/services/proprietary-desk`, `/blog`, `/contact`, plus `GET /api/health` and `POST /api/contact`.

## Editing content

Page text lives in `tools/build_site.py`. After editing it, regenerate the pages:

```bash
python tools/build_site.py
```

## Running

```bash
npm install
npm run build
npm start        # http://localhost:9000
```

The default background palette is set in each page's `<html data-theme="1">` tag (1 Beige, 2 Sky, 3 Pearl, 4 Sage; visitors can also switch with the picker in the top-right corner). To change it site-wide, edit the `data-theme` value in `tools/build_site.py` and rebuild.
