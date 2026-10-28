import random
# Illustrations used across pages.
ART_HELM = '''<svg viewBox="0 0 520 430" fill="none" aria-hidden="true">
  <defs><linearGradient id="g2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0B1F3A"/><stop offset="1" stop-color="#1B7F5C"/></linearGradient></defs>
  <path d="M128 215H205M325 215H395" stroke="#0B1F3A" stroke-opacity=".45" stroke-width="3.5" stroke-dasharray="1 10" stroke-linecap="round"/>
  <path d="M196 208l12 7-12 7M386 208l12 7-12 7" stroke="#0B1F3A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <g font-family="DM Sans,system-ui,sans-serif" font-weight="700" letter-spacing="1.6" font-size="12" text-anchor="middle">
    <rect x="30" y="165" width="90" height="100" rx="26" fill="#fff" stroke="#0B1F3A" stroke-opacity=".16"/>
    <path d="M52 238l16-28 14 14 20-34" stroke="#1B7F5C" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><text x="75" y="256" fill="#51647B" font-size="10">SIGNAL</text>
    <rect x="215" y="150" width="100" height="130" rx="30" fill="#0B1F3A"/>
    <path d="M265 178l22 9v18c0 14-9 24-22 30-13-6-22-16-22-30v-18z" stroke="#C29B40" stroke-width="3.5" stroke-linejoin="round" fill="none"/><text x="265" y="268" fill="#fff" font-size="10">RISK</text>
    <rect x="400" y="165" width="90" height="100" rx="26" fill="#fff" stroke="#0B1F3A" stroke-opacity=".16"/>
    <g fill="#0B1F3A"><rect x="420" y="214" width="9" height="16"/><rect x="434" y="202" width="9" height="28"/><rect x="448" y="188" width="9" height="42"/></g><rect x="462" y="226" width="6" height="6" fill="#C29B40"/><text x="445" y="256" fill="#51647B" font-size="10">BROKER</text>
  </g>
  <g stroke="#0B1F3A" stroke-opacity=".12"><path d="M75 300V360H445V300"/><path d="M265 280V360"/></g>
  <g font-family="DM Sans,system-ui,sans-serif" font-size="12" font-weight="700" letter-spacing="1.6">
    <rect x="120" y="345" width="280" height="40" rx="20" fill="#fff" stroke="#0B1F3A" stroke-opacity=".14"/>
    <circle cx="146" cy="365" r="5" fill="#1B7F5C"/><text x="162" y="369" fill="#0B1F3A">YOUR MACHINES  ·  YOUR BROKER</text>
  </g>
  <path d="M90 110Q265 20 440 110" stroke="#B38A2A" stroke-width="2" stroke-dasharray="3 7" opacity=".7"/>
</svg>'''

ART_PROP = '''<svg viewBox="0 0 520 430" fill="none" aria-hidden="true">
  <defs>
    <linearGradient id="g3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B7F5C" stop-opacity=".32"/><stop offset="1" stop-color="#1B7F5C" stop-opacity="0"/></linearGradient>
  </defs>
  <g stroke="#0B1F3A" stroke-opacity=".09"><path d="M30 90H490M30 170H490M30 250H490M30 330H490"/></g>
  <path d="M30 320L100 290L160 302L230 232L290 252L360 168L420 188L490 70V350H30Z" fill="url(#g3)"/>
  <path d="M30 320L100 290L160 302L230 232L290 252L360 168L420 188L490 70" stroke="#1B7F5C" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
  <g fill="#fff" stroke="#1B7F5C" stroke-width="3.5"><circle cx="230" cy="232" r="7"/><circle cx="360" cy="168" r="7"/><circle cx="490" cy="70" r="8"/></g>
  <path d="M30 350H490" stroke="#0B1F3A" stroke-width="3"/>
  <g font-family="DM Sans,system-ui,sans-serif" font-size="12" font-weight="700" letter-spacing="1.6">
    <rect x="44" y="52" width="148" height="34" rx="17" fill="#0B1F3A"/><circle cx="64" cy="69" r="5" fill="#C29B40"/><text x="78" y="73.5" fill="#fff">OWN CAPITAL</text>
    <rect x="44" y="378" width="170" height="34" rx="17" fill="#fff" stroke="#0B1F3A" stroke-opacity=".14"/><circle cx="64" cy="395" r="5" fill="#1B7F5C"/><text x="78" y="399.5" fill="#0B1F3A">LIVE, AUTOMATED</text>
  </g>
</svg>'''

def _research_art():
    # Normal distribution probability density functions in StrikePoint Brand Gold & Blue:
    # Widescreen viewBox: 580x350
    # Left curve (Navy / Deep Blue): mu=-2.4, var=1.0, peak at X=176.5 (#0B1F3A)
    # Center curve (Royal / Tech Blue): mu=0.0, var=0.42, peak at X=290.0 (#1A56A0, tall quantitative peak)
    # Right curve (Rich Gold): mu=+2.2, var=1.2, peak at X=394.0 (#C29B40)
    # Broad baseline curve (Champagne Gold): mu=0.0, var=7.0, spanning across entire width (#D9B45A)
    # Pure geometric/mathematical animation with zero text content and clean background (no grid lines).
    import math

    def normal_pdf(x, mu, var):
        sigma = math.sqrt(var)
        return (1.0 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-((x - mu) ** 2) / (2 * var))

    W, H = 580, 350
    base_y = 310.0

    def X(x):
        return 30.0 + (x + 5.5) * (520.0 / 11.0)

    # Site brand palette: Gold (#C29B40 / #D9B45A) and Blue (#1A56A0 / #0B1F3A)
    curves = [
        ("gold-wide", 0.0, 7.0, "#8E4A5C", "areaGoldWide", 3.2, 320.0),
        ("navy", -2.4, 1.0, "#1F7A55", "areaNavy", 3.6, 360.0),
        ("gold", 2.2, 1.2, "#C29B40", "areaGold", 3.6, 380.0),
        ("blue", 0.0, 0.42, "#1A56A0", "areaBlue", 4.0, 320.0)
    ]
    N = 64

    def smooth(pts):
        d = "M %.2f %.2f" % pts[0]
        for k in range(len(pts) - 1):
            p0 = pts[k - 1] if k else pts[k]
            p1, p2 = pts[k], pts[k + 1]
            p3 = pts[k + 2] if k + 2 < len(pts) else p2
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d += " C %.2f %.2f %.2f %.2f %.2f %.2f" % (c1 + c2 + p2)
        return d

    def curve_pts(mu, var, sy):
        return [(X(-5.5 + i * (11.0 / N)), base_y - normal_pdf(-5.5 + i * (11.0 / N), mu, var) * sy) for i in range(N + 1)]

    out = ['<svg class="eq-art dist-art anim-play" viewBox="0 0 580 350" fill="none" shape-rendering="geometricPrecision" aria-hidden="true">',
           '  <defs>',
           '    <radialGradient id="distBg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#9CC3EA" stop-opacity=".25"/><stop offset=".65" stop-color="#9CC3EA" stop-opacity=".08"/><stop offset="1" stop-color="#9CC3EA" stop-opacity="0"/></radialGradient>',
           '    <linearGradient id="areaBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A56A0" stop-opacity=".36"/><stop offset="1" stop-color="#1A56A0" stop-opacity="0"/></linearGradient>',
           '    <linearGradient id="areaNavy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1F7A55" stop-opacity=".26"/><stop offset="1" stop-color="#1F7A55" stop-opacity="0"/></linearGradient>',
           '    <linearGradient id="areaGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C29B40" stop-opacity=".34"/><stop offset="1" stop-color="#C29B40" stop-opacity="0"/></linearGradient>',
           '    <linearGradient id="areaGoldWide" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E4A5C" stop-opacity=".14"/><stop offset="1" stop-color="#8E4A5C" stop-opacity="0"/></linearGradient>',
           '    <filter id="distGlowBlue" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="2" stdDeviation="3.5" flood-color="#1A56A0" flood-opacity=".45"/></filter>',
           '    <filter id="distGlowGold" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#C29B40" flood-opacity=".4"/></filter>',
           '  </defs>',
           '  <rect x="0" y="0" width="580" height="350" rx="16" fill="url(#distBg)"/>',
           '  <!-- Clean baseline axis with subtle tick marks (background grid removed) -->',
           '  <path d="M20 310H560" stroke="#0B1F3A" stroke-opacity=".2" stroke-width="1.8" stroke-linecap="round"/>',
           '  <g stroke="#0B1F3A" stroke-opacity=".25" stroke-width="1.4" stroke-linecap="round"><path d="M30 310V315M82 310V315M134 310V315M186 310V317M238 310V315M290 310V319M342 310V315M394 310V317M446 310V315M498 310V315M550 310V315"/></g>',
           '  <g stroke-linecap="round">',
           '    <line class="dist-drop drop-navy" x1="176.5" y1="166.4" x2="176.5" y2="310" stroke="#1F7A55" stroke-width="1.6" stroke-dasharray="3 4" stroke-opacity=".4"/>',
           '    <line class="dist-drop drop-blue" x1="290.0" y1="113.0" x2="290.0" y2="310" stroke="#1A56A0" stroke-width="1.6" stroke-dasharray="3 4" stroke-opacity=".45"/>',
           '    <line class="dist-drop drop-gold" x1="394.0" y1="171.6" x2="394.0" y2="310" stroke="#C29B40" stroke-width="1.6" stroke-dasharray="3 4" stroke-opacity=".45"/>',
           '  </g>']

    # Filled areas under curves
    for name, mu, var, col, grad, w, sy in curves:
        d = smooth(curve_pts(mu, var, sy))
        out.append(f'  <path class="dist-area area-{name}" d="M 30.0 {base_y:.1f} L{d[1:]} L 550.0 {base_y:.1f} Z" fill="url(#{grad})"/>')

    # Curve paths (smooth splines, no raster filters, so edges stay crisp)
    for name, mu, var, col, grad, w, sy in curves:
        d = smooth(curve_pts(mu, var, sy))
        out.append(f'  <path class="dist-curve curve-{name}" pathLength="1" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

    # Peak nodes and halos in gold and blue palette (no text)
    out.append('  <circle class="dist-peak peak-gold-wide" cx="290.0" cy="261.7" r="4.5" fill="#fff" stroke="#8E4A5C" stroke-width="2.5"/>')
    out.append('  <circle class="dist-halo halo-gold" cx="394.0" cy="171.6" r="8" stroke="#C29B40" stroke-width="1.8" fill="none"/>')
    out.append('  <circle class="dist-peak peak-gold" cx="394.0" cy="171.6" r="5.5" fill="#fff" stroke="#C29B40" stroke-width="3"/>')
    out.append('  <circle class="dist-halo halo-navy" cx="176.5" cy="166.4" r="8" stroke="#1F7A55" stroke-width="1.8" fill="none"/>')
    out.append('  <circle class="dist-peak peak-navy" cx="176.5" cy="166.4" r="5.5" fill="#fff" stroke="#1F7A55" stroke-width="3"/>')
    out.append('  <circle class="dist-halo halo-blue" cx="290.0" cy="113.0" r="9.5" stroke="#1A56A0" stroke-width="2" fill="none"/>')
    out.append('  <circle class="dist-peak peak-blue" cx="290.0" cy="113.0" r="6.5" fill="#fff" stroke="#1A56A0" stroke-width="3.5"/>')
    out.append('</svg>')
    return "\n".join(out)


ART_RESEARCH = _research_art()

ART_SOFT = '''<svg viewBox="0 0 520 430" fill="none" aria-hidden="true">
  <rect x="60" y="60" width="400" height="290" rx="28" fill="#fff" stroke="#0B1F3A" stroke-opacity=".16"/>
  <path d="M60 112H460" stroke="#0B1F3A" stroke-opacity=".1"/>
  <g><circle cx="92" cy="86" r="6" fill="#C29B40"/><circle cx="114" cy="86" r="6" fill="#0B1F3A" opacity=".25"/><circle cx="136" cy="86" r="6" fill="#0B1F3A" opacity=".25"/></g>
  <g stroke-width="9" stroke-linecap="round">
    <path d="M96 150H210" stroke="#0B1F3A"/><path d="M226 150H300" stroke="#1B7F5C"/>
    <path d="M120 186H250" stroke="#0B1F3A" opacity=".5"/><path d="M266 186H330" stroke="#C29B40"/>
    <path d="M120 222H196" stroke="#1B7F5C"/><path d="M212 222H330" stroke="#0B1F3A" opacity=".5"/>
    <path d="M96 258H170" stroke="#C29B40"/><path d="M186 258H286" stroke="#0B1F3A"/>
    <path d="M96 294H150" stroke="#0B1F3A" opacity=".5"/><path d="M166 294H260" stroke="#1B7F5C"/>
  </g>
  <g font-family="DM Sans,system-ui,sans-serif" font-size="12" font-weight="700" letter-spacing="1.6">
    <rect x="300" y="332" width="180" height="40" rx="20" fill="#0B1F3A"/><circle cx="322" cy="352" r="5" fill="#1B7F5C"/><text x="336" y="356.5" fill="#fff">BUILT AROUND YOU</text>
  </g>
</svg>'''

ART_ATLAS = '''<svg viewBox="0 0 520 430" fill="none" aria-hidden="true">
  <path d="M120 46Q260 -4 400 46" stroke="#B38A2A" stroke-width="2" stroke-dasharray="3 7" opacity=".7"/>
  <g stroke="#0B1F3A" stroke-opacity=".45" stroke-width="3.5" stroke-dasharray="1 10" stroke-linecap="round">
    <path d="M144 112H190V195H205"/><path d="M376 112H330V195H315"/><path d="M144 318H190V235H205"/><path d="M376 318H330V235H315"/>
  </g>
  <g fill="#1B7F5C"><circle cx="205" cy="195" r="5"/><circle cx="315" cy="195" r="5"/><circle cx="205" cy="235" r="5"/><circle cx="315" cy="235" r="5"/></g>
  <g font-family="DM Sans,system-ui,sans-serif" font-weight="700" letter-spacing="1.6" font-size="10" text-anchor="middle">
    <rect x="205" y="150" width="110" height="130" rx="30" fill="#0B1F3A"/>
    <circle cx="260" cy="200" r="24" stroke="#C29B40" stroke-width="3.5"/><path d="M260 182l9 18-9 18-9-18z" fill="#C29B40"/>
    <text x="260" y="262" fill="#fff">ATLAS</text>

    <rect x="40" y="70" width="104" height="84" rx="24" fill="#fff" stroke="#0B1F3A" stroke-opacity=".16"/>
    <path d="M70 108l14-12 12 8 20-20" stroke="#1B7F5C" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="92" y="138" fill="#51647B">DERIVATIVES</text>

    <rect x="376" y="70" width="104" height="84" rx="24" fill="#fff" stroke="#0B1F3A" stroke-opacity=".16"/>
    <path d="M402 104q6-14 12 0t12 0t12 0t12 0" stroke="#0B1F3A" stroke-width="4" stroke-linecap="round"/>
    <text x="428" y="138" fill="#51647B">VOLATILITY</text>

    <rect x="40" y="276" width="104" height="84" rx="24" fill="#fff" stroke="#0B1F3A" stroke-opacity=".16"/>
    <circle cx="92" cy="308" r="15" stroke="#C29B40" stroke-width="4"/><circle cx="92" cy="308" r="4.5" fill="#C29B40"/>
    <text x="92" y="344" fill="#51647B">CASH</text>

    <rect x="376" y="276" width="104" height="84" rx="24" fill="#fff" stroke="#0B1F3A" stroke-opacity=".16"/>
    <g><rect x="408" y="304" width="9" height="14" fill="#0B1F3A"/><rect x="421" y="296" width="9" height="22" fill="#1B7F5C"/><rect x="434" y="288" width="9" height="30" fill="#0B1F3A"/><rect x="447" y="298" width="9" height="20" fill="#C29B40"/></g>
    <text x="428" y="344" fill="#51647B">POSITIONING</text>

    <rect x="130" y="382" width="260" height="40" rx="20" fill="#fff" stroke="#0B1F3A" stroke-opacity=".14"/>
    <circle cx="158" cy="402" r="5" fill="#1B7F5C"/><text x="270" y="406" fill="#0B1F3A" font-size="12">ONE VIEW OF THE MARKET</text>
  </g>
</svg>'''

def _hero_art():
    """Top: Research -> Software -> Capital with a return arrow (the loop).
    Middle: a profit/loss heartbeat line. Bottom: a single navy rule."""
    W, H = 480, 340
    ny = 92                      # node row
    xs = {"res": 80, "sw": 240, "cap": 400}
    base = 232                   # heartbeat baseline
    # --- heartbeat path: three beats, profit spikes up, loss dips down
    beats = [(52, 30), (40, 22), (64, 26)]   # (profit height, loss depth)
    x, seg = 24.0, ["M 24 %d" % base]
    def L(dx, dy):
        nonlocal_x[0] += dx
        seg.append("L %.1f %.1f" % (nonlocal_x[0], base - dy))
    nonlocal_x = [x]
    for up, down in beats:
        L(22, 0); L(10, 7); L(10, 0); L(8, 0)          # small bump, settle
        L(5, -8); L(7, up); L(8, -down); L(6, 0)       # sharp profit spike, loss dip
        L(12, 0); L(14, 12); L(14, 0); L(18, 0)        # recovery wave
    seg.append("L %d %d" % (W - 24, base))
    hb = " ".join(seg)
    out = ['<svg class="hx" viewBox="0 48 %d 232" fill="none" shape-rendering="geometricPrecision" aria-hidden="true">' % W,
           '<defs>',
           # green above the baseline, navy on it, red below
           '<linearGradient id="hxPL" gradientUnits="userSpaceOnUse" x1="0" y1="%d" x2="0" y2="%d">'
           '<stop offset="0" stop-color="#1F7A55"/><stop offset=".47" stop-color="#1F7A55"/>'
           '<stop offset=".47" stop-color="#0B1F3A"/><stop offset=".53" stop-color="#0B1F3A"/>'
           '<stop offset=".53" stop-color="#B04A3E"/><stop offset="1" stop-color="#B04A3E"/></linearGradient>' % (base - 70, base + 70),
           '<linearGradient id="hxGold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E2B95A"/><stop offset="1" stop-color="#A57A18"/></linearGradient>',
           '<marker id="hxArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           '<path d="M1 1 L9 5 L1 9" fill="none" stroke="#B08D3C" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>',
           '<path id="hxCycle" d="M %d %d H %d"/>' % (xs["res"], ny, xs["cap"]),
           '</defs>',
           # forward arrows (left to right)
           '<path class="hx-flow" d="M %d %d H %d" stroke="#B08D3C" stroke-width="1.8" stroke-dasharray="4 6" marker-end="url(#hxArrow)"/>' % (xs["res"] + 34, ny, xs["sw"] - 36),
           '<path class="hx-flow" d="M %d %d H %d" stroke="#B08D3C" stroke-width="1.8" stroke-dasharray="4 6" marker-end="url(#hxArrow)"/>' % (xs["sw"] + 34, ny, xs["cap"] - 36),
           # a gold dot travelling the loop, behind the nodes
           '<circle class="hx-runner" r="4.5" fill="#C29B40"><animateMotion dur="3s" begin="1.6s" repeatCount="indefinite"><mpath href="#hxCycle"/></animateMotion></circle>',
           ]
    def node(x, k, disc, icon, label):
        return ('<g transform="translate(%d %d)"><circle class="hx-halo hx-h%d" r="27" fill="none" stroke="#B08D3C" stroke-width="1.6"/>'
                '<g class="hx-node hx-n%d">%s%s</g></g>'
                '<text x="%d" y="%d" class="hx-lab">%s</text>') % (x, ny, k, k, disc, icon, x, ny + 50, label)
    navy = '<circle r="27" fill="#0B1F3A"/><circle r="22" fill="none" stroke="#B08D3C" stroke-opacity=".55"/>'
    gold = '<circle r="27" fill="url(#hxGold)"/><circle r="22" fill="none" stroke="#FFFDF7" stroke-opacity=".5"/>'
    bell = '<path d="M-13 7 C-7 7 -5 -10 0 -10 C5 -10 7 7 13 7" stroke="#D9BE7A" stroke-width="2.2" stroke-linecap="round"/><path d="M-15 9H15" stroke="#FFFDF7" stroke-opacity=".5" stroke-width="1.3"/>'
    code = '<path d="M-7 -8 L-14 0 L-7 8 M7 -8 L14 0 L7 8" stroke="#FFFDF7" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M3.5 -10.5 L-3.5 10.5" stroke="#D9BE7A" stroke-width="2.2" stroke-linecap="round"/>'
    bars = '<path d="M-10 10V3 M-3 10V-2 M4 10V-7" stroke="#0B1F3A" stroke-width="4" stroke-linecap="square"/><path d="M-12 -3 L-2 -9 L5 -6 L13 -13 M8 -13 H13 V-8" stroke="#0B1F3A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    out.append('<g font-family="IBM Plex Mono,ui-monospace,monospace" font-size="11" font-weight="600" letter-spacing="2" fill="#4A505C" text-anchor="middle">')
    out.append(node(xs["res"], 1, navy, bell, "RESEARCH"))
    out.append(node(xs["sw"], 2, navy, code, "SOFTWARE"))
    out.append(node(xs["cap"], 3, gold, bars, "CAPITAL"))
    out.append('</g>')
    # heartbeat: faint trace + animated sweep, plus a leading dot
    out.append('<path d="%s" stroke="#0B1F3A" stroke-opacity=".1" stroke-width="2" stroke-linejoin="round"/>' % hb)
    out.append('<path id="hxBeat" class="hx-beat" pathLength="1" d="%s" stroke="url(#hxPL)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>' % hb)
    out.append('<circle class="hx-blip" r="4" fill="#C29B40"><animateMotion dur="4.2s" begin="1s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.72;1" calcMode="linear"><mpath href="#hxBeat"/></animateMotion></circle>')
    out.append('</svg>')
    return "".join(out)


ART_HERO = _hero_art()


ART_FUNNEL = '''<svg class="fn-art" viewBox="0 0 520 430" fill="none" aria-hidden="true">
  <g font-family="DM Sans,system-ui,sans-serif" font-size="13" font-weight="700" letter-spacing="2" text-anchor="middle">
    <g class="fn-step"><rect x="30" y="40" width="460" height="62" rx="20" fill="#0B1F3A" opacity=".95"/><text x="260" y="77" fill="#fff">IDEAS</text></g>
    <g class="fn-step"><rect x="70" y="118" width="380" height="62" rx="20" fill="#0B1F3A" opacity=".8"/><text x="260" y="155" fill="#fff">HYPOTHESES</text></g>
    <g class="fn-step"><rect x="110" y="196" width="300" height="62" rx="20" fill="#0B1F3A" opacity=".62"/><text x="260" y="233" fill="#fff">BACKTESTS</text></g>
    <g class="fn-step"><rect x="150" y="274" width="220" height="62" rx="20" fill="#136548" opacity=".9"/><text x="260" y="311" fill="#fff">VALIDATED</text></g>
    <g class="fn-step"><rect x="190" y="352" width="140" height="62" rx="20" fill="#B38A2A"/><text x="260" y="389" fill="#fff">LIVE</text></g>
  </g>
</svg>'''

ART_ARCH = '''<svg viewBox="0 0 520 430" fill="none" aria-hidden="true">
  <g font-family="DM Sans,system-ui,sans-serif" font-size="13" font-weight="700" letter-spacing="2" text-anchor="middle">
    <rect x="110" y="24" width="300" height="56" rx="18" fill="#fff" stroke="#0B1F3A" stroke-opacity=".18"/><text x="260" y="58" fill="#0B1F3A">MARKET DATA</text>
    <rect x="110" y="108" width="300" height="56" rx="18" fill="#fff" stroke="#0B1F3A" stroke-opacity=".18"/><text x="260" y="142" fill="#0B1F3A">SIGNALS</text>
    <rect x="110" y="192" width="300" height="56" rx="18" fill="#0B1F3A"/><text x="260" y="226" fill="#fff">RISK CHECKS</text>
    <rect x="110" y="276" width="300" height="56" rx="18" fill="#fff" stroke="#0B1F3A" stroke-opacity=".18"/><text x="260" y="310" fill="#0B1F3A">EXECUTION</text>
    <rect x="110" y="360" width="300" height="56" rx="18" fill="#136548"/><text x="260" y="394" fill="#fff">YOUR BROKER</text>
  </g>
  <g stroke="#0B1F3A" stroke-opacity=".4" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M260 82v24M260 166v24M260 250v24M260 334v24"/><path d="M254 98l6 8 6-8M254 182l6 8 6-8M254 266l6 8 6-8M254 350l6 8 6-8"/></g>
  <path d="M440 220V52h-30M440 220v82h-30" stroke="#B38A2A" stroke-width="2.5" stroke-dasharray="2 8" stroke-linecap="round"/>
  <g font-family="DM Sans,system-ui,sans-serif" font-size="11" font-weight="700" letter-spacing="1.6"><rect x="428" y="196" width="80" height="48" rx="14" fill="#fff" stroke="#B38A2A"/><text x="468" y="216" text-anchor="middle" fill="#8a6a1c">KILL</text><text x="468" y="231" text-anchor="middle" fill="#8a6a1c">SWITCH</text></g>
</svg>'''



def _spline(pts):
    """Smooth Catmull-Rom path through points."""
    d = "M %.1f %.1f" % pts[0]
    for k in range(len(pts) - 1):
        p0 = pts[k - 1] if k else pts[k]
        p1, p2 = pts[k], pts[k + 1]
        p3 = pts[k + 2] if k + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += " C %.1f %.1f %.1f %.1f %.1f %.1f" % (c1 + c2 + p2)
    return d


def _validate_art():
    """Backtest validation: simulated paths fan out, the expected range fills in,
    the strategy's equity line draws through in-sample and out-of-sample periods,
    then a 'validated' seal appears. Loops."""
    import random
    x0, x1, y0, N = 44, 536, 262, 34
    xs = [x0 + i * (x1 - x0) / (N - 1) for i in range(N)]
    split = xs[22]

    def walk(seed, drift=4.2, vol=7.5):
        r = random.Random(seed)
        v, out = 0.0, [0.0]
        for _ in range(N - 1):
            v += drift + r.gauss(0, vol)
            out.append(v)
        return out

    sims = [walk(s) for s in range(1, 61)]
    lo = [sorted(s[i] for s in sims)[6] for i in range(N)]
    hi = [sorted(s[i] for s in sims)[53] for i in range(N)]
    main = walk(424, 4.6, 5.0)
    Y = lambda v: y0 - 14 - v * 1.02
    band = _spline([(x, Y(v)) for x, v in zip(xs, hi)]) + " L" + _spline([(x, Y(v)) for x, v in reversed(list(zip(xs, lo)))])[1:] + " Z"
    paths = "".join('<path class="vx-sim" style="--i:%d" pathLength="1" d="%s"/>' % (k, _spline([(x, Y(v)) for x, v in zip(xs, sims[s])]))
                    for k, s in enumerate([3, 8, 15, 22, 31, 40, 47, 55]))
    ex, ey = xs[-1], Y(main[-1])
    grid = "".join('<path d="M%d %.0fH%d"/>' % (x0, y, x1) for y in (102, 142, 182, 222))
    return (
        '<svg class="vx" viewBox="0 0 580 330" fill="none" shape-rendering="geometricPrecision" aria-hidden="true">'
        '<defs><linearGradient id="vxBand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C29B40" stop-opacity=".22"/>'
        '<stop offset="1" stop-color="#C29B40" stop-opacity=".06"/></linearGradient>'
        '<linearGradient id="vxSeal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E2B95A"/><stop offset="1" stop-color="#A57A18"/></linearGradient></defs>'
        # out-of-sample zone
        '<rect x="%.1f" y="44" width="%.1f" height="218" fill="#0B1F3A" fill-opacity=".035"/>'
        '<path d="M%.1f 44V262" stroke="#0B1F3A" stroke-opacity=".3" stroke-dasharray="3 5"/>'
        '<g font-family="IBM Plex Mono,ui-monospace,monospace" font-size="10" font-weight="600" letter-spacing="1.6" fill="#7A7F8A">'
        '<text x="%d" y="34">IN-SAMPLE</text><text x="%.1f" y="34">OUT-OF-SAMPLE</text></g>'
        '<g stroke="#0B1F3A" stroke-opacity=".07">%s</g>'
        '<path d="M%d 262H%d" stroke="#0B1F3A" stroke-opacity=".3" stroke-width="1.4"/>'
        '<path class="vx-band" d="%s" fill="url(#vxBand)"/>'
        '<g stroke="#6E8BB0" stroke-width="1.3" stroke-opacity=".55">%s</g>'
        '<path class="vx-main" pathLength="1" d="%s" stroke="#0B1F3A" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle class="vx-end-halo" cx="%.1f" cy="%.1f" r="7" stroke="#C29B40" stroke-width="1.6"/>'
        '<circle class="vx-end" cx="%.1f" cy="%.1f" r="5.5" fill="#C29B40" stroke="#FFFDF7" stroke-width="2"/>'
        '<g transform="translate(%.1f %.1f)"><g class="vx-seal">'
        '<circle r="23" fill="url(#vxSeal)"/><circle r="18.5" stroke="#FFFDF7" stroke-opacity=".6"/>'
        '<path d="M-8 0.5 L-2.5 6 L8.5 -5.5" stroke="#0B1F3A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g></g>'
        '</svg>') % (
        split, x1 - split, split, x0, split + 10, grid, x0, x1, band, paths,
        _spline([(x, Y(v)) for x, v in zip(xs, main)]), ex, ey, ex, ey, ex - 40, ey - 4 - 42)


ART_VALIDATE = _validate_art()
