"""Blog posts live in content/blog/*.md. Files starting with "_" are ignored (templates/drafts).

Each post starts with a small header, then the article in Markdown:

    ---
    title: Why most backtests lie
    date: 2026-11-02
    category: Research          (Markets, Research or Software)
    summary: One or two sentences shown on the cards.
    ---
    Your article text...
"""
import datetime, html, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
POSTS_DIR = os.path.join(ROOT, "content", "blog")
CATEGORIES = ["Markets", "Research", "Software"]


def _inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: '<a href="%s">%s</a>' % (html.escape(m.group(2)), m.group(1)), t)
    return t


def markdown(src):
    """A small Markdown subset: headings, paragraphs, lists, quotes, code blocks, bold/italic/code/links."""
    out, para, lst, code = [], [], None, None

    def flush():
        nonlocal para, lst
        if para:
            out.append("<p>%s</p>" % _inline(" ".join(para)))
            para = []
        if lst:
            tag, items = lst
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % _inline(i) for i in items), tag))
            lst = None

    for line in src.splitlines():
        if code is not None:
            if line.strip().startswith("```"):
                out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(code)))
                code = None
            else:
                code.append(line)
            continue
        s = line.strip()
        if s.startswith("```"):
            flush(); code = []
        elif not s:
            flush()
        elif re.match(r"#{1,4} ", s):
            flush()
            level = min(4, len(s.split(" ")[0]) + 1)  # "#" -> h2, so the post title stays the only h1
            out.append("<h%d>%s</h%d>" % (level, _inline(s.lstrip("#").strip()), level))
        elif s.startswith("> "):
            flush(); out.append("<blockquote><p>%s</p></blockquote>" % _inline(s[2:]))
        elif re.match(r"[-*] ", s):
            if para: flush()
            if not lst or lst[0] != "ul": flush(); lst = ("ul", [])
            lst[1].append(s[2:])
        elif re.match(r"\d+\. ", s):
            if para: flush()
            if not lst or lst[0] != "ol": flush(); lst = ("ol", [])
            lst[1].append(re.sub(r"^\d+\.\s+", "", s))
        else:
            if lst: flush()
            para.append(s)
    flush()
    return "\n".join(out)


def _slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def load_posts():
    """All published posts, newest first."""
    posts = []
    if not os.path.isdir(POSTS_DIR):
        return posts
    for fn in sorted(os.listdir(POSTS_DIR)):
        if not fn.endswith(".md") or fn.startswith("_"):
            continue
        raw = open(os.path.join(POSTS_DIR, fn), encoding="utf-8").read()
        m = re.match(r"\s*---\s*\n(.*?)\n---\s*\n(.*)", raw, re.S)
        if not m:
            raise SystemExit("content/blog/%s: missing the --- header --- block" % fn)
        meta = {}
        for ln in m.group(1).splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                meta[k.strip().lower()] = v.strip()
        for need in ("title", "date"):
            if not meta.get(need):
                raise SystemExit("content/blog/%s: '%s' is required" % (fn, need))
        date = datetime.date.fromisoformat(meta["date"])
        cat = meta.get("category", "Research").title()
        if cat not in CATEGORIES:
            raise SystemExit("content/blog/%s: category must be one of %s" % (fn, ", ".join(CATEGORIES)))
        body = m.group(2)
        words = len(re.findall(r"\w+", body))
        posts.append({
            "slug": meta.get("slug") or _slug(fn[:-3]),
            "title": meta["title"],
            "date": date,
            "date_label": "%d %s %d" % (date.day, date.strftime("%B"), date.year),
            "category": cat,
            "summary": meta.get("summary", ""),
            "html": markdown(body),
            "minutes": max(1, round(words / 220)),
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts
