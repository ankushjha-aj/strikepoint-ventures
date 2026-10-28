"""Builds every page into ../pages. Run:  python tools/build_site.py"""
import os, re, sys, time
BUILD = str(int(time.time()))
sys.path.insert(0, os.path.dirname(__file__))
from arts import *

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "pages")
os.makedirs(OUT, exist_ok=True)
for _f in os.listdir(OUT):
    if _f.endswith(".html"):
        os.remove(os.path.join(OUT, _f))

EMAIL = "contact@strikepointventures.com"
SERVICES = [
    ("Research &amp; Technology", "/services/research-technology"),
    ("Atlas &amp; Helm", "/services/atlas-helm"),
    ("Proprietary Desk", "/services/proprietary-desk"),
]
NOTICE = [
    "No Financial Services Provided: StrikePoint Ventures is a financial technology and quantitative software provider.",
    "No Public Communication Channels: We do not operate any public WhatsApp, Telegram, or social media premium groups for trading tips or signals.",
    "Technology &amp; Strategy Tools Disclosure: Any software, terminal dashboards (including StrikePoint Atlas and StrikePoint Helm), backtesting metrics, or quantitative insights published on this website are for educational, informational, and research support purposes only. They do not constitute a direct recommendation, buy/sell advice, or financial solicitation.",
    "User Responsibility &amp; Broker Deployment: All automated rules, parameters, or strategies executed via our software are deployed at the user's sole discretion within their personal broker infrastructure. Users are entirely responsible for their own trading decisions, regulatory compliance, and risk exposures. Investments in the securities market are subject to market risks.",
]
FONTS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800"
         "&family=Source+Serif+4:ital,opsz,wght@0,8..60,500;0,8..60,600;1,8..60,500;1,8..60,600"
         "&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap")

# The logo mark, inline so it can animate: the frame draws, the bars rise, the gold strike slides in.
MARK = ('<svg class="mark" viewBox="0 0 86 100" fill="none" aria-hidden="true">'
        '<path class="mk-frame" pathLength="1" d="M76 42V9H9v82h36" stroke="#0B1F3A" stroke-width="8" stroke-linejoin="miter"/>'
        '<rect class="mk-bar mk-b1" x="20" y="56" width="8" height="24" fill="#0B1F3A"/>'
        '<rect class="mk-bar mk-b2" x="32" y="42" width="8" height="38" fill="#0B1F3A"/>'
        '<rect class="mk-bar mk-b3" x="44" y="26" width="8" height="54" fill="#0B1F3A"/>'
        '<path class="mk-strike" d="M52 91L70 50H81L63 91Z" fill="#C29B40"/></svg>')


def lockup(extra="", sub=True):
    # "VENTURES LLP" is laid out letter by letter so it spans exactly the width of "STRIKEPOINT"
    letters = "".join('<span class="sp"></span>' if ch == " " else "<span>%s</span>" % ch for ch in "VENTURES LLP")
    return ('<a class="brand%s" href="/" aria-label="StrikePoint Ventures LLP">%s'
            '<span class="brand__rule"></span><span class="brand__txt"><b>STRIKE<i>POINT</i></b>%s</span></a>') % (
        extra, MARK, ('<em aria-hidden="true">%s</em>' % letters) if sub else "")


def header(active):
    def a(href, label, key):
        return '<a href="%s"%s>%s</a>' % (href, ' class="on"' if active == key else "", label)
    drop = "".join('<a href="%s">%s</a>' % (h, n) for n, h in SERVICES)
    cta_cls = "menu__cta on" if active == "contact" else "menu__cta"
    return ('<header class="bar"><div class="bar__in">%s'
            '<button class="burger" aria-label="Menu"><span></span><span></span><span></span></button>'
            '<nav class="menu">%s%s<div class="drop"><button type="button"%s>Services ▾</button><div class="drop__panel">%s</div></div>%s'
            '<a href="/contact" class="%s">Contact</a></nav></div></header>') % (
        lockup(), a("/", "Home", "home"), a("/about", "About", "about"), ' class="on"' if active == "services" else "", drop, a("/blog", "Blog", "blog"), cta_cls)


def footer():
    legal = "".join('<button type="button" data-notice>%s</button>' % t for t in
                    ["Disclaimers", "Privacy Policy", "Terms &amp; Conditions", "Risk Profile", "Grievance Redressal"])
    return ('<footer class="foot">'
            '<div class="wrap">'
            '<div class="foot__grid">'
            '  <div class="foot__col foot__col--brand">'
            '    %s'
            '    <p class="foot__mission">Quantitative research, institutional-grade software systems, and proprietary execution models engineered for modern derivatives and capital markets.</p>'
            '  </div>'
            '  <div class="foot__col">'
            '    <h4>Solutions</h4>'
            '    <ul class="foot__links">'
            '      <li><a href="/services/research-technology">Research &amp; Technology</a></li>'
            '      <li><a href="/services/atlas-helm#atlas">StrikePoint Atlas Terminal</a></li>'
            '      <li><a href="/services/atlas-helm#helm">StrikePoint Helm Execution</a></li>'
            '      <li><a href="/services/proprietary-desk">Proprietary Trading Desk</a></li>'
            '      <li><a href="/services">All Services Directory</a></li>'
            '    </ul>'
            '  </div>'
            '  <div class="foot__col">'
            '    <h4>Firm &amp; Research</h4>'
            '    <ul class="foot__links">'
            '      <li><a href="/about">About Firm</a></li>'
            '      <li><a href="/about#principles">Method &amp; Philosophy</a></li>'
            '      <li><a href="/blog">Research &amp; Insights</a></li>'
            '      <li><a href="/contact">Schedule Scoping Call</a></li>'
            '    </ul>'
            '  </div>'
            '  <div class="foot__col">'
            '    <h4>Desk &amp; Offices</h4>'
            '    <div class="foot__contact-item"><b>Direct Desk Email</b><a href="mailto:%s" class="foot__mail">%s</a></div>'
            '    <div class="foot__contact-item"><b>Headquarters</b><span>Delhi, India</span></div>'
            '    <div class="foot__contact-item"><b>Market Hours</b><span>Mon – Fri · 09:00 – 18:00 IST</span></div>'
            '    <div style="margin-top:.8rem"><a class="chip" href="https://www.linkedin.com/" target="_blank" rel="noopener">Follow on LinkedIn ↗</a></div>'
            '  </div>'
            '</div>'
            '<div class="foot__legal">'
            '  <div class="foot__legal-links">%s</div>'
            '  <span class="foot__copy">© 2026 StrikePoint Ventures LLP. All rights reserved.</span>'
            '</div>'
            '</div>'
            '</footer>') % (lockup(), EMAIL, EMAIL, legal)


def notice():
    body = "".join("<p>%s</p>" % p for p in NOTICE)
    return ('<div class="gate" id="notice" role="dialog" aria-modal="true" aria-labelledby="noticeT"><div class="gate__card"><span class="tag">Attention</span>'
            '<h3 id="noticeT">Important Regulatory Notice &amp; Disclaimer</h3><div class="notice__body">%s</div>'
            '<div class="notice__act"><button class="btn btn--solid" data-notice-close>I Accept</button></div></div></div>') % body


def page(slug, title, desc, active, body):
    if slug in ("services", "research-technology", "atlas-helm", "proprietary-desk"):
        active = "services"
    html = ('<!DOCTYPE html>\n<html lang="en" data-theme="1">\n<head>\n<meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>%s</title>\n'
            '<meta name="description" content="%s">\n<link rel="icon" href="/assets/img/mark.svg">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link href="%s" rel="stylesheet">\n<link rel="stylesheet" href="/assets/css/site.css?v=@@V@@">\n</head>\n<body>\n%s\n<main>\n%s\n</main>\n%s\n%s\n'
            '<script src="/assets/js/site.js?v=@@V@@"></script>\n</body>\n</html>\n') % (title, desc, FONTS, header(active), body, footer(), notice())
    html = html.replace("@@V@@", BUILD)
    open(os.path.join(OUT, slug + ".html"), "w", encoding="utf-8").write(html)
    print("built", slug)


# ---------------------------------------------------------------- pieces
def tag(t):
    return '<span class="tag">%s</span>' % t


def cta(h, p, label="Get in touch →", href="/contact"):
    return '<section class="cta"><div class="wrap"><div class="rv"><h2>%s</h2><p>%s</p><a href="%s" class="btn btn--solid">%s</a></div></div></section>' % (h, p, href, label)


def aud(items):
    return '<div class="aud">%s</div>' % "".join('<div class="rv"><h4>%s</h4><p>%s</p></div>' % i for i in items)


WHY = [
    ("Institutional-Level Expertise", "Guided by quantitative market professionals with more than ten years of live trading experience."),
    ("Production-Ready Engineering", "Constructed on ultra-low latency pipelines, clean architecture and dependable infrastructure."),
    ("Validation Backed by Data", "We remove bias. Each strategy is thoroughly tested against extensive historical quantitative backtests."),
    ("End-to-end Infrastructure", "One team handles research, software, market data and execution, so you never have to piece together five different vendors."),
]


def why_section():
    head = ('<div class="statement__head rv">%s<h2>Grounded in discipline and experience.</h2>'
            '<p>Four pillars that define our approach to quantitative software and market infrastructure.</p></div>') % tag("Why us")
    return ('<section class="statement"><div class="wrap">%s%s</div></section>' % (head, aud(WHY)))


def detail(d):
    """Shared layout for the five service pages."""
    out = []
    sub = '<p class="sub" style="margin-top:1rem;color:var(--muted)">%s</p>' % d["sub"] if d.get("sub") else ""
    out.append('<section class="pp"><div class="wrap pp__grid"><div class="rv"><a href="/services" class="crumb">← All services</a><br>%s'
               '<h1>%s</h1><p class="lead">%s</p><div class="hero__act"><a href="/contact" class="btn btn--solid">%s →</a>'
               '<a href="/contact" class="btn btn--soft">Talk to us</a></div>%s</div><div class="pp__art rv">%s</div></div>'
               '<div class="wrap"><div class="chips">%s</div></div></section>' % (
                   tag(d["pill"]), d["h1"], d["lead"], d["cta1"], sub, d["art"], "".join("<span>%s</span>" % c for c in d["chips"])))
    if d.get("intro"):
        out.append('<section class="statement"><div class="wrap"><p class="big rv">%s</p>%s</div></section>' % (d["intro"], d.get("intro2", "")))
    cells = []
    for i, (cls, t, p) in enumerate(d["cells"], 1):
        star = "star" in cls
        lead = '<span class="cell__flag">%s</span>' % d["flag"] if star else '<span class="cell__no">0%d</span>' % i
        cells.append('<div class="cell %s rv">%s<h3>%s</h3><p>%s</p></div>' % (cls, lead, t, p))
    out.append('<section class="sec"><div class="wrap"><div class="sec__head rv">%s<h2>%s</h2></div><div class="bento">%s</div></div></section>' % (
        tag(d["b_tag"]), d["b_h2"], "".join(cells)))
    steps = "".join('<li><h3>%s%s</h3><p>%s</p></li>' % (t, ('<span class="pill">%s</span>' % pl) if pl else "", p) for t, p, pl in d["steps"])
    out.append('<section class="sec"><div class="wrap flow"><div class="flow__intro rv">%s<h2>%s</h2></div><ol class="flow__list rv">%s</ol></div></section>' % (
        tag(d["f_tag"]), d["f_h2"], steps))
    for block in d.get("extra", []):
        out.append(block)
    if d.get("w_text"):
        out.append('<section class="statement"><div class="wrap">%s<p class="big rv">%s</p>%s%s</div></section>' % (
            tag(d["w_tag"]), d["w_text"], d.get("w_aud", ""), ('<p class="note rv">%s</p>' % d["note"]) if d.get("note") else ""))
    out.append(cta(d["c_h"], d["c_p"], d["cta1"] + " →"))
    return "\n".join(out)


# ---------------------------------------------------------------- HOME
def build_home():
    hero = ('<section class="hero"><div class="wrap"><div class="hero__grid"><div class="rv">%s'
            '<h1>We research market edges, build the systems that trade them, and <em>back them with our own capital.</em></h1>'
            '<p class="lead">StrikePoint Ventures is a data-led quantitative firm with years of experience in live markets. One team can look after every layer of your trading infrastructure, from research through data to execution.</p>'
            '</div>'
            '<div class="hero__art rv">%s</div></div>'
            '</div></section>') % (
        tag("Quant software • Research • Own-capital trading"), ART_HERO)

    loop = ('<section class="sec" id="loop"><div class="wrap"><div class="sec__head rv">%s<h2>One loop, three disciplines.</h2>'
            '<p>Research an edge, build the system that trades it, then run it on real capital.</p></div>'
            '<div class="loop"><div class="loop__tabs" data-tabs><button data-t="r" class="on">Research</button><button data-t="b">Build</button><button data-t="t">Trade</button></div>'
            # research
            '<div class="loop__panel on" data-t="r"><div class="rv"><span class="tag">Research</span><h3>Strategies you can defend with statistics.</h3>'
            '<p>A strategy that should be doing more? We subject it to strict backtesting, statistical validation and careful edge research, then return a strategy you can back with statistics and fully own. Everything runs under NDA, and your strategy and IP remain yours.</p>'
            '<a class="btn btn--solid" href="/services/research-technology">See Research &amp; Technology →</a></div><div class="loop__art">%s</div></div>'
            # build
            '<div class="loop__panel" data-t="b"><div><span class="tag">Technology &amp; products</span><h3>Software that trades. Terminals that show.</h3>'
            '<p>Bespoke software for financial markets: execution systems, backtesting engines, analytics terminals and market data infrastructure, shaped around your workflow and connected to your broker. Created by a team that runs its own automated capital on these same systems.</p>'
            '<a class="more" href="/services/research-technology">See Research &amp; Technology →</a></div>'
            '<div class="mini"><div><h4>StrikePoint Atlas</h4><p>Market structure analytics for derivatives and cash: volatility surfaces and positioning flows. A hosted terminal for serious traders, offered as a subscription.</p>'
            '<div class="acts"><a class="btn btn--solid" href="/contact">Request a demo</a><a class="more" href="/services/atlas-helm#atlas">Learn more →</a></div></div>'
            '<div><h4>StrikePoint Helm</h4><p>The execution engine that trades our own capital each day. For clients we create custom builds around your strategy and hand over the code. You run it on your own infrastructure, so your funds and execution remain fully under your control.</p>'
            '<div class="acts"><a class="btn btn--solid" href="/contact">Request a demo</a><a class="more" href="/services/atlas-helm#helm">Learn more →</a></div></div>'
            '<p style="color:var(--muted);font-size:.9rem;margin:0">Live demos of both products will open soon. Request one today and we will hold your access for launch.</p></div></div>'
            # trade
            '<div class="loop__panel" data-t="t"><div><span class="tag">Proprietary Desk</span><h3>We trade our own money.</h3>'
            '<p>Tested proprietary strategies with an edge that has lasted for years. We trade our own capital using fully automated, risk managed systems that need very little human intervention. Real markets, not only backtests.</p>'
            '<a class="btn btn--solid" href="/services/proprietary-desk">See the Proprietary Desk →</a></div><div class="loop__art">%s</div></div>'
            '</div></div></section>') % (tag("How we work"), ART_VALIDATE, ART_PROP)

    blog = ('<section class="sec"><div class="wrap"><div class="sec__head rv">%s<h2>Latest from the blog</h2></div>'
            '<p class="empty rv">New posts are on the way. Check back soon.</p></div></section>') % tag("Latest")
    body = hero + loop + why_section() + blog + cta("Let's create your edge.",
        "Whether you are fine-tuning a strategy, automating execution, or building out your whole trading infrastructure, we would love to hear from you.")
    page("index", "StrikePoint Ventures — Quantitative Research &amp; Trading",
         "A data-led quant firm for research, software and automated trading systems.", "home", body)


# ---------------------------------------------------------------- ABOUT
def build_about():
    hero = (
        '<section class="about-hero"><div class="wrap"><div class="about-hero__grid">'
        '<div class="about-hero__text rv">'
        '%s'
        '<h1>Where market research becomes working systems.</h1>'
        '<p class="lead">Taking pure mathematical research all the way to automated trading across derivatives and capital markets.</p>'
        '<div class="hero__act" style="margin-top:1.4rem">'
        '<a href="/contact" class="btn btn--solid">Schedule a scoping call →</a>'
        '<a href="/services" class="btn btn--soft">Explore services</a>'
        '</div>'
        '</div>'
        '<div class="about-hero__stats rv">'
        '<div class="stat-card">'
        '<span class="stat-card__val">10+</span>'
        '<span class="stat-card__lbl">Years Live Trading</span>'
        '<p>Proprietary quantitative strategies tested across dynamic market regimes.</p>'
        '</div>'
        '<div class="stat-card">'
        '<span class="stat-card__val">100%%</span>'
        '<span class="stat-card__lbl">Automated Execution</span>'
        '<p>Low-latency algorithmic engines running on institutional infrastructure.</p>'
        '</div>'
        '<div class="stat-card">'
        '<span class="stat-card__val">Strict</span>'
        '<span class="stat-card__lbl">Risk Disciplines</span>'
        '<p>Deterministic multi-layer controls eliminating emotional bias.</p>'
        '</div>'
        '<div class="stat-card">'
        '<span class="stat-card__val">Full IP</span>'
        '<span class="stat-card__lbl">Client Ownership</span>'
        '<p>Strict NDA protection. Custom code deployed on your infrastructure.</p>'
        '</div>'
        '</div>'
        '</div></div></section>'
    ) % tag("About StrikePoint")

    chapters = [
        ("01", "How we trade", "Trading with total conviction.",
         "At StrikePoint, we firmly follow our own advice. We actively run our cutting-edge, in-house mathematical strategies using our own proprietary capital. Our trades are carried out by fully automated, high-performance systems built to run smoothly with very little human intervention. Since we trade our own capital under strict, multi-layered risk management rules, clients can be confident that our software has been tested against the toughest conditions of live financial markets.",
         ["Proprietary Capital", "Automated Execution", "Strict Risk Control"]),
        ("02", "What we build", "Alpha discovery to live execution.",
         "Our work covers the full lifecycle of systematic trading: statistical edge research, execution engines, and risk-managed infrastructure. By combining advanced statistical models with modern artificial intelligence, we find structural market anomalies across asset classes. From our real-time analytics terminal, <strong>StrikePoint Atlas</strong>, to our flagship execution software, <strong>StrikePoint Helm</strong>, we equip institutions and professional desks to scale securely.",
         ["StrikePoint Atlas", "StrikePoint Helm", "Low-Latency Infra"]),
        ("03", "Who we are", "Built with precision. Guided by data.",
         "STRIKEPOINT VENTURES is a leading quantitative research and technology company, data-driven and grounded in strong market discipline and more than ten years of live trading experience. We operate at the intersection of mathematical finance, advanced data science, and institutional-quality software engineering, building the enduring infrastructure behind modern systematic trading.",
         ["10+ Years Experience", "Mathematical Rigor", "Bespoke Engineering"]),
    ]

    cards_html = "".join(
        '<div class="about-card rv">'
        '<div class="about-card__top">'
        '<span class="about-card__no">%s</span>'
        '%s'
        '</div>'
        '<h3>%s</h3>'
        '<p>%s</p>'
        '<div class="about-card__badges">%s</div>'
        '</div>' % (
            n, tag(l), t, p, "".join("<span>%s</span>" % b for b in badges)
        )
        for n, l, t, p, badges in chapters
    )

    core = (
        '<section class="sec about-core"><div class="wrap">'
        '<div class="sec__head rv">'
        '%s'
        '<h2>How we operate, build and trade.</h2>'
        '<p>Three interconnected disciplines behind every quantitative system we deploy.</p>'
        '</div>'
        '<div class="about-grid">%s</div>'
        '</div></section>'
    ) % (tag("Core Principles"), cards_html)

    body = hero + core + why_section() + cta("Let's create your edge.", "Whether you are fine-tuning a strategy, automating execution, or building out your whole trading infrastructure, we would love to hear from you.")
    page("about", "About — StrikePoint Ventures", "Who we are, what we build and how we trade.", "about", body)


# ---------------------------------------------------------------- SERVICES HUB
def build_hub():
    items = [
        ("Research &amp; technology", "Research &amp; Technology", "/services/research-technology", "See Research &amp; Technology →", ART_RESEARCH,
         "From edge research to the software that trades it. We put strategies through strict backtesting, statistical validation and careful research, then build the execution systems, backtesting engines, analytics terminals and market data infrastructure to run them, shaped around your workflow and connected to your broker. Covered entirely by NDA."),
        ("Products", "Atlas &amp; Helm", "/services/atlas-helm", "See Atlas &amp; Helm →", ART_ATLAS,
         "Two products from our desk. Atlas is a hosted analytics terminal for derivatives and cash: volatility surfaces and positioning flows. Helm is the execution engine that trades our own capital every day, custom built around your strategy and run on your own infrastructure."),
        ("Proprietary desk", "Proprietary Desk", "/services/proprietary-desk", "See the Proprietary Desk →", ART_PROP,
         "Tested proprietary strategies with an edge that has lasted across regimes. We trade our own capital using fully automated, risk-managed systems that need very little human intervention."),
    ]
    nav = "".join('<button type="button" data-t="%d"%s><span>0%d</span>%s<i>→</i></button>' % (i, ' class="on"' if i == 0 else "", i + 1, it[1]) for i, it in enumerate(items))
    panels = "".join('<article class="hub__panel%s" data-t="%d">%s<span class="tag">%s</span><h2>%s</h2><p>%s</p><a href="%s" class="btn btn--solid">%s</a></article>' % (
        " on" if i == 0 else "", i, it[4], it[0], it[1], it[5], it[2], it[3]) for i, it in enumerate(items))
    head = ('<section class="head"><div class="wrap rv">%s<h1>Everything between an idea and a live trade.</h1>'
            '<p>From statistical edge research and backtesting engines to production low-latency execution and proprietary capital deployment, our team provides institutional derivatives solutions founded on mathematical rigor.</p></div></section>') % tag("What we offer")
    hub = '<section class="sec" style="padding-top:1rem"><div class="wrap hub"><div class="hub__nav" data-tabs data-hover>%s</div><div class="hub__stage rv">%s</div></div></section>' % (nav, panels)
    page("services", "Services — StrikePoint Ventures", "Research and technology, the Atlas and Helm products, and our proprietary desk.", "",
         head + hub + cta("Let's create your quantitative edge.", "Whether you are fine-tuning a strategy, automating execution, or deploying institutional capital, we would love to hear from you."))


# ---------------------------------------------------------------- DETAIL PAGES
def hero_block(pill, h1, lead, cta1, sub, art, chips):
    sub_html = '<p class="sub">%s</p>' % sub if sub else ""
    return ('<section class="pp"><div class="wrap pp__grid"><div class="rv"><a href="/services" class="crumb">← All services</a><br>%s<h1>%s</h1><p class="lead">%s</p>'
            '<div class="hero__act"><a href="/contact" class="btn btn--solid">%s →</a><a href="/contact" class="btn btn--soft">Talk to us</a></div>%s</div>'
            '<div class="pp__art rv">%s</div></div><div class="wrap"><div class="chips">%s</div></div></section>') % (
        tag(pill), h1, lead, cta1, sub_html, art, "".join("<span>%s</span>" % c for c in chips))


def bento_block(tag_, h2, cells, flag=""):
    out = []
    for i, (cls, t, p) in enumerate(cells, 1):
        lead = '<span class="cell__flag">%s</span>' % flag if "star" in cls else '<span class="cell__no">0%d</span>' % i
        out.append('<div class="cell %s rv">%s<h3>%s</h3><p>%s</p></div>' % (cls, lead, t, p))
    return '<section class="sec"><div class="wrap"><div class="sec__head rv">%s<h2>%s</h2></div><div class="bento">%s</div></div></section>' % (tag(tag_), h2, "".join(out))


def flow_block(tag_, h2, steps):
    li = "".join('<li><h3>%s%s</h3><p>%s</p></li>' % (t, ('<span class="pill">%s</span>' % pl) if pl else "", p) for t, p, pl in steps)
    return '<section class="sec"><div class="wrap flow"><div class="flow__intro rv">%s<h2>%s</h2></div><ol class="flow__list rv">%s</ol></div></section>' % (tag(tag_), h2, li)


def who_block(tag_, text, audience="", note=""):
    n = '<p class="note rv">%s</p>' % note if note else ""
    return '<section class="statement"><div class="wrap">%s<p class="big rv">%s</p>%s%s</div></section>' % (tag(tag_), text, audience, n)


def checks(items):
    return '<ul class="checks rv">%s</ul>' % "".join("<li><div><b>%s</b><span>%s</span></div></li>" % i for i in items)


def build_details():
    # ---------------- Research & Technology
    cells_research = [
        ("x4", "Signal &amp; Hypothesis Discovery", "We search for repeatable, tradable patterns that have a clear economic reason to exist. A candidate signal with no rationale other than a good backtest does not go live."),
        ("", "Strategy Building", "We take a loose idea to a fully specified rule set: entries, exits, sizing, risk limits and regime filters, written precisely enough to automate with no interpretation."),
        ("", "Validation &amp; Resilience Testing", "Walk forward testing, out of sample checks, Monte Carlo resampling, parameter sweeps and regime analysis. If your Sharpe holds up on only one parameter set, we say so before the market does."),
        ("x4 star", "Options &amp; Volatility Studies", "Volatility surfaces and Greeks behaviour. Signals based on IV percentile, volatility of volatility, model free implied volatility, realised volatility and the variance risk premium, covering index options and more."),
        ("x3", "Execution-Conscious Modelling", "Backtests that reflect reality: transaction costs, slippage, fill probability, margin and liquidity limits. A strategy that works only with free, instant fills does not really work."),
        ("x3", "Strategy Review &amp; Independent Opinion", "Already bought or built a strategy? We examine it for overfitting, look ahead bias, survivorship bias and blind spots in execution. Independent, direct and written down."),
    ]
    cells_tech = [
        ("x4", "Automated Execution Systems", "Signal handling, order routing for complex option structures, position management, real time risk checks, kill switches and full audit trails. Works across brokers and accounts, deployed on your own infrastructure."),
        ("", "Backtesting &amp; Simulation", "Event driven backtesters with realistic fills, slippage, costs and margin modelling. Designed for options: Greeks, IV surfaces and expiry mechanics all handled properly."),
        ("", "Market Data Pipelines", "Live and historical data ingestion, tick storage on TimescaleDB, data quality checks, corporate action adjustments and clean APIs for your research stack."),
        ("x4", "Dashboards &amp; Terminals", "Live P&amp;L and exposure monitoring along with volatility and positioning analytics. Web based, on your own servers or in the cloud, built on the same framework as our own Atlas terminal."),
        ("x3", "Broker &amp; Exchange Integrations", "Adapters for any venue that has an API: Indian brokers such as Kite, Shoonya and XTS, global gateways like Interactive Brokers, and crypto exchanges via Binance and CCXT."),
        ("x3", "Strategy Audit &amp; System Recovery", "Inherited a bot that fires orders twice? A backtest that looks too good to be true? We audit existing systems for execution bugs, overfitting and infrastructure risk, then fix them."),
    ]
    parts = [
        hero_block("Research &amp; Technology", "Research &amp; <em>Technology</em>",
                   "We convert trading ideas into strategies you can back with statistics, then build the software that trades them: execution systems, backtesting engines, analytics terminals, risk tools and market data infrastructure, for any asset class, broker or exchange API. Created by a team that runs its own automated capital on these same systems.",
                   "Schedule a free scoping call",
                   "Thirty minutes, no obligation. Come with an idea, a half built strategy, or just a market you want to take on. If we are not the right fit, we will tell you.",
                   ART_RESEARCH, ["Hypothesis research", "Backtesting", "Validation", "Execution systems", "Market data", "Independent audit"]),
        '<section class="statement"><div class="wrap"><p class="big rv" style="max-width:46ch">An edge you cannot validate is only a guess. Most strategies do not fail because the idea was poor. They fail because <mark>no one stress tested them honestly</mark> before real money was committed.</p></div></section>',
        bento_block("Research", "From a hypothesis to a strategy you can stand behind.", cells_research, "OUR STRONGEST SPECIALTY"),
        bento_block("Technology", "Everything your trading operation requires, from data through to execution.", cells_tech),
        flow_block("How a project runs", "No open ended billing. No unpleasant surprises.", [
            ("Scoping call", "Thirty minutes. You explain what you want to achieve and we raise the awkward questions early. We say upfront whether it can be done.", "FREE"),
            ("Written proposal", "Fixed scope, timeline, milestones and cost, in writing, before any work starts.", ""),
            ("Research &amp; backtesting", "Hypothesis testing on quality data using execution aware assumptions. You see interim results, not a black box.", ""),
            ("Validation gauntlet", "Walk forward, out of sample, sensitivity and regime tests. Most ideas fail here. That is the purpose.", ""),
            ("Build, deploy &amp; handover", "Working software at each stage, then deployed on your infrastructure with the report, code, backtest framework, documentation, tests and a support period. All of it is yours, under NDA.", ""),
        ]),
        '<section class="sec"><div class="wrap duo"><div class="rv">%s<h2>What you receive.</h2><p>Not a PDF of promises. A complete, working research package that belongs to you, and if you want it automated, the same team can build and run it.</p></div>%s</div></section>' % (
            tag("Deliverables"), checks([
                ("Written research report", "with candid statistics, covering what failed and the reasons"),
                ("Complete strategy codebase", "in documented, tested Python, with nothing hidden"),
                ("Reusable backtest framework", "set up for your market and yours to keep"),
                ("Live deployment specification", "ready to be automated on your broker")])),
        '<section class="sec"><div class="wrap duo"><div class="rv">%s<h2>Most ideas do not pass our validation. Good.</h2>'
        '<p>Most of the strategy ideas we study do not make it through the validation gauntlet. We treat that as a success, because the cheapest place to lose money is in a backtest.</p>'
        '<p>We will never inflate a Sharpe ratio, cherry pick a date range or conceal a drawdown to make a report look better. You pay for the truth about your strategy, not for flattery.</p></div><div class="diagram rv">%s</div></div></section>' % (tag("Our standard"), ART_FUNNEL),
        '<section class="sec"><div class="wrap duo duo--rev"><div class="rv">%s<h2>Made first for our own money.</h2>'
        '<p>Every framework we sell started inside our own proprietary trading operation. Our execution engine runs live automated options strategies on Indian index derivatives on every trading day. Our backtester has been checked against real fills, real slippage and real expiry day behaviour.</p>'
        '<p>When we call it production grade, we mean it is <b>running in production today</b>, with our own capital at stake.</p></div><div class="diagram rv">%s</div></div></section>' % (tag("Proof"), ART_ARCH),
        who_block("Who we work with", "If this describes you, we should speak.", aud([
            ("Independent systematic traders", "You have a proven manual strategy, or an idea, and want it validated and turned into disciplined, hands off automated execution."),
            ("Prop desks &amp; family offices", "You need research capacity, execution, risk or data infrastructure without having to hire a full quant and tech team."),
            ("Fintech &amp; advisory firms", "You need white label research, analytics dashboards or backtesting capability to offer your own clients."),
            ("Research teams", "You want clean, dependable market data pipelines that your models can trust."),
            ("Strategy buyers &amp; builders", "You bought or built a strategy and want an independent, direct audit.")]),
            "We do not sell tips, signals or guaranteed strategies. We do not manage capital or provide investment advice. Your strategy, your money, your broker, your call. Searching for tips, signals or managed accounts? We are not that kind of firm and never will be."),
        cta("Got an idea worth testing?", "Tell us your market, your timeframe and what you want to test or automate, even roughly. We reply within one business day with an honest assessment: whether it can be done, how we would approach it, what it would cost, and whether you actually need custom software at all.", "Schedule a free scoping call →"),
    ]
    page("research-technology", "Research &amp; Technology — StrikePoint Ventures",
         "Edge research, backtesting and validation, plus the execution software, market data and dashboards to run it.", "", "\n".join(parts))

    # ---------------- Atlas & Helm
    parts = [
        hero_block("Our products", "Atlas &amp; <em>Helm</em>",
                   "Two products from our desk. StrikePoint Atlas is a real-time analytics terminal for derivatives and cash. StrikePoint Helm is the execution engine that trades our own capital every day, built around your strategy and deployed straight to you.",
                   "Request a demo", "Live demos of both products will open soon. Request one now and we will hold your access for launch.",
                   ART_ARCH, ["Volatility surfaces", "Market structure", "Positioning flows", "Your broker", "Your infrastructure", "Custom builds"]),
        '<section class="sec" id="atlas"><div class="wrap duo"><div class="rv">%s<h2>StrikePoint Atlas</h2>'
        '<p>A real-time analytics terminal for financial markets, spanning derivatives and cash. We reveal what is truly going on behind the scenes using multi-layered financial data, as a hosted terminal offered on subscription.</p>%s'
        '<p style="margin-top:1.6rem"><a href="/contact" class="btn btn--solid">Request an Atlas demo →</a></p></div><div class="diagram rv">%s</div></div></section>' % (
            tag("Analytics terminal · Subscription"), checks([
                ("Volatility surfaces", "See how implied volatility bends across strikes and expiries, and where the market is pricing convexity."),
                ("Market structure", "See how the market is built underneath price, across derivatives and cash, so the pressure behind a move becomes visible."),
                ("Positioning flows", "Follow how positioning shifts through the session instead of guessing it from price alone."),
                ("Derivatives and cash, together", "One terminal that spans both, built for institutional clients, proprietary firms and active traders.")]), ART_ATLAS),
        '<section class="sec" id="helm"><div class="wrap duo duo--rev"><div class="rv">%s<h2>StrikePoint Helm</h2>'
        '<p>The execution engine that trades our own capital every day. Your capital, your broker, our advanced trading engine, deployed straight to you.</p>%s'
        '<p style="margin-top:1.6rem"><a href="/contact" class="btn btn--solid">Request a Helm demo →</a></p></div><div class="diagram rv">%s</div></div></section>' % (
            tag("Execution engine · Custom built"), checks([
                ("Plugged into your broker", "We deploy Helm directly for clients and integrate it smoothly with the brokers they already prefer."),
                ("Runs where you choose", "Locally on your own machines, or securely on remote servers."),
                ("Custom builds, code handed over", "Designed around your strategy, then the code is handed over to you."),
                ("Your funds stay in your control", "You run it on your own infrastructure, so your funds and execution remain fully under your control.")]), ART_HELM),
        flow_block("Getting started", "From request to running.", [
            ("Request a demo", "Live demos open soon. Ask now and we will hold your access for launch.", ""),
            ("Tell us what you need", "For Atlas, the access you want. For Helm, your strategy and your broker.", ""),
            ("We set you up", "Atlas is a hosted terminal on subscription. Helm is a custom build shaped to your strategy, with the code handed over, documentation, tests and a support period.", ""),
            ("You are live", "Atlas shows volatility and positioning in one place, in real time. Helm runs on your own machines or remote servers, with your own broker.", ""),
        ]),
        cta("Want to discuss specifics?", "Describe your strategy or research question and we'll explain how we can help.", "Request a demo →"),
    ]
    page("atlas-helm", "Atlas &amp; Helm — StrikePoint Ventures", "A hosted analytics terminal and a custom-built execution engine from the StrikePoint desk.", "", "\n".join(parts))

    prop = dict(
        pill="Our own capital", h1="Proprietary <em>Desk</em>", art=ART_PROP, cta1="Start a conversation",
        lead="Our own capital. Automated execution. Hands-free trading. We trade our in-house strategies and models through fully automated, high-performance, risk-managed systems that need minimal human intervention.",
        chips=["Own capital", "Fully automated", "Risk-managed", "Statistically validated", "Live markets"],
        b_tag="How we trade", b_h2="Conviction, with the risk managed.", flag="",
        cells=[("x4", "Our capital is on the line", "Proven proprietary strategies with an edge that has lasted across regimes, traded with our own money, not client money."),
               ("", "Backtest first", "Strategies are examined with robust statistical methods before any capital is put at risk."),
               ("", "Algo trade", "Trading ideas become fully automated, risk-managed trading systems."),
               ("x4", "Live markets, not just backtests", "Everything we sell began here, tested against real fills, real slippage and real expiry-day behaviour."),
               ("x6", "Minimal intervention", "High-performance systems that run on their own, under multi-layered risk management.")],
        f_tag="The cycle", f_h2="Idea to live capital.",
        steps=[("Validate", "Hypotheses are tested statistically before they ever see capital.", ""),
               ("Automate", "Strategies are turned into fully automated, risk-managed systems.", ""),
               ("Trade", "Systems run live on firm capital, with minimal human intervention.", "")],
        c_h="Want to discuss specifics?", c_p="Describe your strategy or research question and we'll explain how we can help.")
    page("proprietary-desk", "Proprietary Desk — StrikePoint Ventures", "How we trade our own capital with automated, risk-managed systems.", "", detail(prop))


# ---------------------------------------------------------------- BLOG / CONTACT
def build_blog():
    body = ('<section class="head"><div class="wrap rv">%s<h1>The blog</h1><p>Writing on research, market microstructure and the systems we build.</p></div></section>'
            '<section class="sec" style="padding-top:1rem"><div class="wrap"><div class="cats"><span class="on">All</span><span>Markets</span><span>Research</span><span>Software</span></div>'
            '<p class="empty rv">New posts are on the way. Check back soon.</p></div></section>') % tag("Insights")
    page("blog", "Blog — StrikePoint Ventures", "Writing on research, market microstructure and the systems we build.", "blog", body)


def build_contact():
    opts = "".join("<option>%s</option>" % o for o in ["Research &amp; Technology", "Atlas &amp; Helm", "Proprietary Desk", "Other"])
    body = ('<section class="head"><div class="wrap rv">%s<h1>Tell us what you are building.</h1><p>We are happy to help. Share your market, your idea or your question and we will take it from there.</p></div></section>'
            '<section class="sec" style="padding-top:1rem"><div class="wrap contact"><div class="contact__info rv"><h2>What happens next</h2>'
            '<ol class="next"><li><span><b>You write to us.</b> Tell us your market, your idea or your question.</span></li>'
            '<li><span><b>We reply within one business day.</b> With an honest assessment, and a call if it makes sense.</span></li>'
            '<li><span><b>We scope it together.</b> Written scope, timeline and cost before any work begins.</span></li></ol>'
            '<div class="reach"><a class="mail" href="mailto:%s">%s</a><p>StrikePoint Ventures LLP · Delhi, India</p><p>Monday to Friday, 9 AM to 6 PM</p>'
            '<p><a href="https://www.linkedin.com/" target="_blank" rel="noopener" style="display:inline">LinkedIn</a></p></div></div>'
            '<form class="form rv" id="contactForm"><label for="n">Name</label><input id="n" name="name" required placeholder="Your name">'
            '<label for="e">Email</label><input id="e" name="email" type="email" required placeholder="you@example.com">'
            '<label for="t">Regarding</label><select id="t" name="topic">%s</select><div class="other" id="otherBox"><label for="o">What would you like to discuss?</label><input id="o" name="other" placeholder="Tell us in a few words"></div>'
            '<label for="m">Message</label><textarea id="m" name="message" required placeholder="Tell us about your market, strategy or question"></textarea>'
            '<input class="hp" name="website" tabindex="-1" autocomplete="off"><button class="btn btn--solid" type="submit">Send message →</button><p class="ok" id="formMsg"></p></form></div></section>') % (
        tag("Contact"), EMAIL, EMAIL, opts)
    page("contact", "Contact — StrikePoint Ventures", "Talk to the StrikePoint team about research, software or our products.", "contact", body)


for fn in (build_home, build_about, build_hub, build_details, build_blog, build_contact):
    fn()
