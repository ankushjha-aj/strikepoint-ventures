"""Builds a single self-contained HTML file with every page of the site plus a
background-palette picker, for sharing a review copy.

Usage:  python tools/build_share.py <output.html>
"""
import base64, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PAGES = os.path.join(ROOT, "pages")
OUT = sys.argv[1]

ORDER = [("home", "index", "StrikePoint Ventures"), ("about", "about", "About"), ("services", "services", "Services"),
         ("research-technology", "research-technology", "Research & Technology"), ("atlas-helm", "atlas-helm", "Atlas & Helm"),
         ("proprietary-desk", "proprietary-desk", "Proprietary Desk"), ("blog", "blog", "Blog"), ("contact", "contact", "Contact")]
LINKS = {"/": "#home", "/about": "#about", "/services": "#services", "/services/research-technology": "#research-technology",
         "/services/atlas-helm": "#atlas-helm", "/services/proprietary-desk": "#proprietary-desk", "/blog": "#blog", "/contact": "#contact"}


def read(p):
    return open(p, encoding="utf-8").read()


mark = "data:image/svg+xml;base64," + base64.b64encode(open(os.path.join(ROOT, "assets", "img", "mark.svg"), "rb").read()).decode()
counter = [0]


def fix(h):
    def link(m):  # "/services/atlas-helm#helm" -> the page, then scroll to the anchor
        path = LINKS.get(m.group(1), m.group(1))
        return 'href="%s"%s' % (path, ' data-scroll="%s"' % m.group(3) if m.group(3) and path in LINKS.values() else "")
    h = re.sub(r'href="(/[^"#]*)(#([^"]*))?"', link, h)
    h = h.replace('src="/assets/img/mark.svg"', 'src="%s"' % mark)
    h = h.replace('href="#loop"', 'href="#home" data-scroll="loop"')

    def uniq(m):  # keep SVG gradient / clip ids unique across pages
        counter[0] += 1
        s = m.group(0)
        for i in set(re.findall(r'id="([^"]+)"', s)):
            s = s.replace('id="%s"' % i, 'id="%s-%d"' % (i, counter[0])).replace("url(#%s)" % i, "url(#%s-%d)" % (i, counter[0]))
        return s
    return re.sub(r"<svg\b.*?</svg>", uniq, h, flags=re.S)


index = read(os.path.join(PAGES, "index.html"))
header = fix(re.search(r'<header class="bar">.*?</header>', index, re.S).group(0)).replace(' class="on"', "")
footer = fix(re.search(r'<footer class="foot">.*?</footer>', index, re.S).group(0))
notice = re.search(r'<div class="gate".*?</div></div></div>', index, re.S).group(0)

sections = []
for token, fname, _ in ORDER:
    h = read(os.path.join(PAGES, fname + ".html"))
    main = re.search(r"<main>\n(.*?)\n</main>", h, re.S).group(1)
    sections.append('<div class="page%s" data-page="%s">\n%s\n</div>' % (" on" if token == "home" else "", token, fix(main)))

css = read(os.path.join(ROOT, "assets", "css", "site.css")).replace('html[data-theme="', ':root[data-pal="')
css += """
/* review copy */
.page{display:none}.page.on{display:block}
body{display:block;min-height:0}
#site{min-height:100vh;display:flex;flex-direction:column}
.page.on{flex:1 0 auto}
.rv{opacity:1!important;transform:none!important;transition:none!important}
.bar{top:0}
.wrap{padding-left:max(24px,env(safe-area-inset-left,0px));padding-right:max(24px,env(safe-area-inset-right,0px))}
.pal{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));z-index:130;width:min(250px,calc(100% - 32px));
  background:#fff;border:1px solid rgba(11,31,58,.15);border-radius:18px;box-shadow:0 20px 50px -18px rgba(11,31,58,.5);font:600 13px/1.3 "Inter",system-ui,sans-serif;color:#0B1F3A}
.pal>button{width:100%;display:flex;justify-content:space-between;align-items:center;gap:8px;background:none;border:0;padding:12px 14px;cursor:pointer;font:inherit;color:inherit}
.pal__body{display:none;padding:0 8px 10px}.pal.open .pal__body{display:grid;gap:3px}
.pal__hint{padding:0 8px 8px;color:#51647B;font-weight:500}
.pal__opt{display:flex;align-items:center;gap:10px;border:1px solid transparent;background:none;border-radius:10px;padding:7px 8px;cursor:pointer;font:inherit;color:inherit;text-align:left}
.pal__opt:hover{background:#f1f5f3}.pal__opt.on{border-color:#1B7F5C;background:#eef8f3}
.pal__opt i{width:30px;height:18px;border-radius:6px;border:1px solid rgba(11,31,58,.18);flex:none}
"""

PALETTES = [("1", "Beige", "linear-gradient(#FFFCF5,#EDE5D3)"), ("2", "Sky", "linear-gradient(#FFFFFF,#DAE7F5)"),
            ("3", "Pearl", "linear-gradient(#FFFFFF,#EAEAE6)"), ("4", "Sage", "linear-gradient(#FFFFFF,#DEEBE2)")]
pal_html = ('<div class="pal" id="pal"><button type="button" id="palBtn"><span>Choose a background</span><span>▾</span></button>'
            '<div class="pal__body"><p class="pal__hint">Click through the pages, then pick the background you prefer.</p>%s</div></div>') % "".join(
    '<button type="button" class="pal__opt" data-v="%s"><i style="background:%s"></i>%s · %s</button>' % (v, g, v, n) for v, n, g in PALETTES)

names = [t for t, _, _ in ORDER]
titles = dict((t, n) for t, _, n in ORDER)
router = """
(function () {
  var names = %s, titles = %s;
  var pages = [].slice.call(document.querySelectorAll('.page'));
  function show(t) {
    if (names.indexOf(t) < 0) t = 'home';
    pages.forEach(function (p) { p.classList.toggle('on', p.getAttribute('data-page') === t); });
    [].forEach.call(document.querySelectorAll('.menu > a'), function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + t); });
    var svc = ['services','research-technology','atlas-helm','proprietary-desk'].indexOf(t) > -1; var db = document.querySelector('.drop > button'); if (db) db.classList.toggle('on', svc);
    try { document.title = titles[t] === 'StrikePoint Ventures' ? 'StrikePoint Ventures' : titles[t] + ' · StrikePoint Ventures'; } catch (e) {}
    window.scrollTo(0, 0);
  }
  window.addEventListener('hashchange', function () { show((location.hash || '').replace('#', '')); });
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!a) return;
    var t = a.getAttribute('href').slice(1);
    if (names.indexOf(t) < 0) return;
    e.preventDefault();
    try { history.replaceState(null, '', '#' + t); } catch (x) {}
    show(t);
    var m = document.querySelector('.menu'); if (m) m.classList.remove('on');
    var s = a.getAttribute('data-scroll');
    if (s) setTimeout(function () { var el = document.getElementById(s); if (el) el.scrollIntoView({ behavior: 'smooth' }); }, 40);
  });
  show((location.hash || '').replace('#', ''));

  // background palette picker
  var K = 'sp-review-palette-v2', pal = document.getElementById('pal');
  function get() { try { return localStorage.getItem(K); } catch (e) { return null; } }
  function put(v) { try { localStorage.setItem(K, v); } catch (e) {} }
  function apply(v) {
    document.documentElement.setAttribute('data-pal', v);
    [].forEach.call(pal.querySelectorAll('.pal__opt'), function (b) { b.classList.toggle('on', b.getAttribute('data-v') === v); });
  }
  pal.querySelector('#palBtn').addEventListener('click', function () { pal.classList.toggle('open'); });
  pal.addEventListener('click', function (e) { var b = e.target.closest('.pal__opt'); if (b) { var v = b.getAttribute('data-v'); put(v); apply(v); } });
  if (window.innerWidth > 900) pal.classList.add('open');
  apply(get() || '1');
})();
""" % (names, str(titles).replace("'", '"'))

js = "window.SP_REVIEW = true;\n" + read(os.path.join(ROOT, "assets", "js", "site.js"))

html = ('<title>StrikePoint Ventures</title>\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=Source+Serif+4:ital,opsz,wght@0,8..60,500;0,8..60,600;1,8..60,500;1,8..60,600&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap">\n'
        '<style>\n%s\n</style>\n<div id="site">\n%s\n%s\n%s\n%s\n%s\n</div>\n<script>\n%s\n%s\n</script>\n') % (
    css, header, "\n".join(sections), footer, notice, pal_html, js, router)

os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(html)
print("wrote", OUT, round(len(html.encode("utf-8")) / 1024), "KB")
