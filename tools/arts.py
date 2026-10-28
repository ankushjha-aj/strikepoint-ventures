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
        ("gold-wide", 0.0, 7.0, "#D9B45A", "areaGoldWide", 3.2, 320.0),
        ("navy", -2.4, 1.0, "#6E8BB0", "areaNavy", 3.6, 360.0),
        ("gold", 2.2, 1.2, "#C29B40", "areaGold", 3.6, 380.0),
        ("blue", 0.0, 0.42, "#1A56A0", "areaBlue", 4.0, 320.0)
    ]
    N = 110

    out = ['<svg class="eq-art dist-art anim-play" viewBox="0 0 580 350" fill="none" aria-hidden="true">',
           '  <defs>',
           '    <radialGradient id="distBg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#9CC3EA" stop-opacity=".25"/><stop offset=".65" stop-color="#9CC3EA" stop-opacity=".08"/><stop offset="1" stop-color="#9CC3EA" stop-opacity="0"/></radialGradient>',
           '    <linearGradient id="areaBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A56A0" stop-opacity=".36"/><stop offset="1" stop-color="#1A56A0" stop-opacity="0"/></linearGradient>',
           '    <linearGradient id="areaNavy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6E8BB0" stop-opacity=".3"/><stop offset="1" stop-color="#6E8BB0" stop-opacity="0"/></linearGradient>',
           '    <linearGradient id="areaGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C29B40" stop-opacity=".34"/><stop offset="1" stop-color="#C29B40" stop-opacity="0"/></linearGradient>',
           '    <linearGradient id="areaGoldWide" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9B45A" stop-opacity=".22"/><stop offset="1" stop-color="#D9B45A" stop-opacity="0"/></linearGradient>',
           '    <filter id="distGlowBlue" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="2" stdDeviation="3.5" flood-color="#1A56A0" flood-opacity=".45"/></filter>',
           '    <filter id="distGlowGold" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#C29B40" flood-opacity=".4"/></filter>',
           '  </defs>',
           '  <rect x="0" y="0" width="580" height="350" rx="16" fill="url(#distBg)"/>',
           '  <!-- Clean baseline axis with subtle tick marks (background grid removed) -->',
           '  <path d="M20 310H560" stroke="#0B1F3A" stroke-opacity=".2" stroke-width="1.8" stroke-linecap="round"/>',
           '  <g stroke="#0B1F3A" stroke-opacity=".25" stroke-width="1.4" stroke-linecap="round"><path d="M30 310V315M82 310V315M134 310V315M186 310V317M238 310V315M290 310V319M342 310V315M394 310V317M446 310V315M498 310V315M550 310V315"/></g>',
           '  <g stroke-linecap="round">',
           '    <line class="dist-drop drop-navy" x1="176.5" y1="166.4" x2="176.5" y2="310" stroke="#6E8BB0" stroke-width="1.6" stroke-dasharray="3 4" stroke-opacity=".4"/>',
           '    <line class="dist-drop drop-blue" x1="290.0" y1="113.0" x2="290.0" y2="310" stroke="#1A56A0" stroke-width="1.6" stroke-dasharray="3 4" stroke-opacity=".45"/>',
           '    <line class="dist-drop drop-gold" x1="394.0" y1="171.6" x2="394.0" y2="310" stroke="#C29B40" stroke-width="1.6" stroke-dasharray="3 4" stroke-opacity=".45"/>',
           '  </g>']

    # Filled areas under curves
    for name, mu, var, col, grad, w, sy in curves:
        pts = []
        for i in range(N + 1):
            x = -5.5 + i * (11.0 / N)
            pdf = normal_pdf(x, mu, var)
            px = X(x)
            py = base_y - pdf * sy
            pts.append(f"{px:.1f} {py:.1f}")
        d_pts = " ".join(("L " if i > 0 else "") + p for i, p in enumerate(pts))
        d_area = f"M 30.0 {base_y:.1f} L {d_pts} L 550.0 {base_y:.1f} Z"
        out.append(f'  <path class="dist-area area-{name}" d="{d_area}" fill="url(#{grad})"/>')

    # Curve paths
    for name, mu, var, col, grad, w, sy in curves:
        pts = []
        for i in range(N + 1):
            x = -5.5 + i * (11.0 / N)
            pdf = normal_pdf(x, mu, var)
            px = X(x)
            py = base_y - pdf * sy
            pts.append(f"{px:.1f} {py:.1f}")
        d_pts = " ".join(("L " if i > 0 else "") + p for i, p in enumerate(pts))
        d_line = f"M {d_pts}"
        filt = ' filter="url(#distGlowBlue)"' if name == "blue" else (' filter="url(#distGlowGold)"' if name == "gold" else '')
        out.append(f'  <path class="dist-curve curve-{name}"{filt} pathLength="1" d="{d_line}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

    # Peak nodes and halos in gold and blue palette (no text)
    out.append('  <circle class="dist-peak peak-gold-wide" cx="290.0" cy="261.7" r="4.5" fill="#fff" stroke="#D9B45A" stroke-width="2.5"/>')
    out.append('  <circle class="dist-halo halo-gold" cx="394.0" cy="171.6" r="8" stroke="#C29B40" stroke-width="1.8" fill="none"/>')
    out.append('  <circle class="dist-peak peak-gold" cx="394.0" cy="171.6" r="5.5" fill="#fff" stroke="#C29B40" stroke-width="3"/>')
    out.append('  <circle class="dist-halo halo-navy" cx="176.5" cy="166.4" r="8" stroke="#6E8BB0" stroke-width="1.8" fill="none"/>')
    out.append('  <circle class="dist-peak peak-navy" cx="176.5" cy="166.4" r="5.5" fill="#fff" stroke="#6E8BB0" stroke-width="3"/>')
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
    """The loop: Research -> Software -> Capital on a ring, with a growth curve drawing inside."""
    import math
    cx, cy, R = 230, 205, 140
    def at(deg, r=R):  # 0 deg = top, clockwise
        a = math.radians(deg - 90)
        return cx + r * math.cos(a), cy + r * math.sin(a)
    sw, cap, res = at(0), at(120), at(240)
    pts = [(140, 262), (156, 255), (170, 259), (184, 245), (198, 248), (212, 233), (226, 237), (240, 219),
           (254, 223), (268, 202), (282, 206), (296, 184), (310, 171), (322, 150)]
    line = "M" + " L".join("%d %d" % p for p in pts)
    area = line + " L322 300 L140 300 Z"
    grid = "".join('<path d="M%d 80V330"/>' % x for x in range(118, 345, 28)) + \
           "".join('<path d="M105 %dH355"/>' % y for y in range(93, 320, 28))
    out = ['<svg class="hx" viewBox="0 0 460 400" fill="none" aria-hidden="true">',
           '<defs>',
           '<clipPath id="hxClip"><circle cx="%d" cy="%d" r="112"/></clipPath>' % (cx, cy),
           '<linearGradient id="hxArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C29B40" stop-opacity=".38"/><stop offset="1" stop-color="#C29B40" stop-opacity="0"/></linearGradient>',
           '<linearGradient id="hxGold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E2B95A"/><stop offset="1" stop-color="#A57A18"/></linearGradient>',
           '<radialGradient id="hxCore" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFFDF7" stop-opacity=".9"/><stop offset="1" stop-color="#FFFDF7" stop-opacity="0"/></radialGradient>',
           '<filter id="hxGlow" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="0" dy="0" stdDeviation="3.5" flood-color="#C29B40" flood-opacity=".8"/></filter>',
           '</defs>',
           # soft light core + dial ticks
           '<circle cx="%d" cy="%d" r="125" fill="url(#hxCore)"/>' % (cx, cy),
           '<g class="hx-dial"><circle cx="%d" cy="%d" r="172" stroke="#0B1F3A" stroke-opacity=".22" stroke-width="6" stroke-dasharray="1.2 10.5"/>'
           '<circle cx="%d" cy="%d" r="172" stroke="#B08D3C" stroke-opacity=".6" stroke-width="10" stroke-dasharray="1.6 88.4"/></g>' % (cx, cy, cx, cy),
           # inner chart, clipped to a circle
           '<g clip-path="url(#hxClip)"><g class="hx-grid" stroke="#8A6A22" stroke-opacity=".12" stroke-width="1">%s</g>' % grid,
           '<path d="M100 275H360" stroke="#0B1F3A" stroke-opacity=".25" stroke-dasharray="3 5"/>',
           '<path class="hx-area" d="%s" fill="url(#hxArea)"/>' % area,
           '<path class="hx-line" pathLength="1" d="%s" stroke="#0B1F3A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>' % line,
           '<circle cx="%d" cy="%d" r="112" stroke="#0B1F3A" stroke-opacity=".12"/>' % (cx, cy),
           '<circle class="hx-peak-halo" cx="322" cy="150" r="7" stroke="#B08D3C" stroke-width="1.6"/>',
           '<circle class="hx-peak" cx="322" cy="150" r="5.5" fill="#B08D3C" stroke="#FFFDF7" stroke-width="2"/>',
           # the loop ring
           '<circle cx="%d" cy="%d" r="%d" stroke="#0B1F3A" stroke-opacity=".14" stroke-width="1.5"/>' % (cx, cy, R),
           '<circle class="hx-ring" pathLength="1" cx="%d" cy="%d" r="%d" stroke="#B08D3C" stroke-width="2.2" transform="rotate(-90 %d %d)"/>' % (cx, cy, R, cx, cy),
           # runner travelling the loop
           '<g class="hx-runner"><circle cx="%d" cy="%d" r="5.5" fill="#C29B40" filter="url(#hxGlow)"/>'
           '<circle cx="%.1f" cy="%.1f" r="3" fill="#C29B40" opacity=".45"/><circle cx="%.1f" cy="%.1f" r="2" fill="#C29B40" opacity=".25"/></g>' % (
               cx, cy - R, *at(-7), *at(-13)),
           ]
    def node(pos, cls, delay_cls, disc, icon):
        x, y = pos
        return ('<g transform="translate(%.1f %.1f)"><circle class="hx-halo %s" r="31" stroke="#B08D3C" stroke-width="1.6"/>'
                '<g class="hx-node %s">%s%s</g></g>') % (x, y, delay_cls, cls, disc, icon)
    navy = '<circle r="31" fill="#0B1F3A"/><circle r="26" stroke="#B08D3C" stroke-opacity=".55"/>'
    gold = '<circle r="31" fill="url(#hxGold)"/><circle r="26" stroke="#FFFDF7" stroke-opacity=".5"/>'
    bell = '<path d="M-15 8 C-8 8 -6 -12 0 -12 C6 -12 8 8 15 8" stroke="#D9BE7A" stroke-width="2.4" stroke-linecap="round"/><path d="M-17 10H17" stroke="#FFFDF7" stroke-opacity=".5" stroke-width="1.4"/><path d="M0 -12V10" stroke="#D9BE7A" stroke-opacity=".6" stroke-dasharray="2 2.5"/>'
    code = '<path d="M-8 -9 L-16 0 L-8 9 M8 -9 L16 0 L8 9" stroke="#FFFDF7" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 -12 L-4 12" stroke="#D9BE7A" stroke-width="2.4" stroke-linecap="round"/>'
    bars = '<path d="M-12 11V3 M-4 11V-3 M4 11V-8" stroke="#0B1F3A" stroke-width="4.5" stroke-linecap="square"/><path d="M-14 -4 L-2 -11 L6 -7 L15 -15 M9 -15 H15 V-9" stroke="#0B1F3A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    out.append(node(sw, "hx-n1", "hx-h1", navy, code))
    out.append(node(cap, "hx-n2", "hx-h2", gold, bars))
    out.append(node(res, "hx-n3", "hx-h3", navy, bell))
    lab = '<g font-family="IBM Plex Mono,ui-monospace,monospace" font-size="11.5" font-weight="600" letter-spacing="2.2" fill="#4A505C" text-anchor="middle">'
    lab += '<text x="%.1f" y="%.1f">RESEARCH</text>' % (res[0], res[1] + 52)
    lab += '<text x="%.1f" y="%.1f">SOFTWARE</text>' % (sw[0], sw[1] - 42)
    lab += '<text x="%.1f" y="%.1f">CAPITAL</text></g>' % (cap[0], cap[1] + 52)
    out.append(lab)
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

