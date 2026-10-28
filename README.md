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
| `tools/blog.py` | Reads blog posts from `content/blog/*.md` |
| `content/blog/` | Blog posts (Markdown with a small header) |
| `src/server.ts` | Express server (compiled to `dist/server.js`) |

## Routes

`/`, `/about`, `/services`, `/services/research-technology`, `/services/atlas-helm`, `/services/proprietary-desk`, `/blog`, `/contact`, plus `GET /api/health` and `POST /api/contact`.

## Editing content

Page text lives in `tools/build_site.py`. After editing it, regenerate the pages:

```bash
python tools/build_site.py
```

## Adding a blog post

1. Copy `content/blog/_example.md` to a new file, e.g. `content/blog/why-backtests-lie.md` (the file name becomes the URL: `/blog/why-backtests-lie`).
2. Fill in `title`, `date` (YYYY-MM-DD), `category` (Markets, Research or Software) and `summary`, then write the article in Markdown.
3. Run `python tools/build_site.py`, commit and push.

The post gets its own page, appears on `/blog` (newest first, with the category filter), and the three newest posts show in "Latest from the blog" on the home page. Files starting with `_` are ignored.

## Running

```bash
npm install
npm run build
npm start        # http://localhost:9000
```

The default background palette is set in each page's `<html data-theme="1">` tag (1 Beige, 2 Sky, 3 Pearl, 4 Sage, 5 Slate; visitors can also switch with the picker in the top-right corner). To change it site-wide, edit the `data-theme` value in `tools/build_site.py` and rebuild.
