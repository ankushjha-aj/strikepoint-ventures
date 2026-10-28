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
    # Equity curves race: 14 strategy curves, one winner (gold line, green wins). site.js animates it;
    # this markup is the finished state, shown with no JS or reduced motion.
    N, L = 70, 14
    seed = 3
    while seed < 500:
        r = random.Random(seed)
        paths = []
        for k in range(L):
            v, a = 0.0, []
            d = 1.15 if k == 0 else (r.random() - .5) * 1.0
            for i in range(N):
                v += d + (r.random() - .5) * 5
                a.append(v)
            paths.append(a)
        if paths[0][-1] > max(a[-1] for a in paths[1:]) + 10:
            break
        seed += 1
    mn = min(min(a) for a in paths)
    mx = max(max(a) for a in paths)

    def X(i):
        return 40 + i * 450 / (N - 1)

    def Y(v):
        return 330 - (v - mn) / (mx - mn) * 250

    def pts(a):
        return " ".join("%.1f,%.1f" % (X(i), Y(v)) for i, v in enumerate(a))

    palette = ["#1A3F6D", "#4B86CE", "#8FB3E0", "#51647B", "#D9B45A", "#5FAE8C"]
    out = ['<svg class="eq-art" viewBox="0 0 520 400" fill="none" aria-hidden="true">',
           '  <defs>',
           '    <linearGradient id="eqArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B7F5C" stop-opacity=".45"/><stop offset="1" stop-color="#1B7F5C" stop-opacity="0"/></linearGradient>',
           '    <radialGradient id="eqBg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#9CC3EA" stop-opacity=".30"/><stop offset=".6" stop-color="#9CC3EA" stop-opacity=".14"/><stop offset="1" stop-color="#9CC3EA" stop-opacity="0"/></radialGradient>',
           '    <filter id="eqGlow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#B38A2A" flood-opacity=".45"/></filter>',
           '  </defs>',
           '  <rect x="0" y="0" width="520" height="400" fill="url(#eqBg)"/>',
           '  <g stroke="#0B1F3A" stroke-opacity=".16" stroke-width="1.5"><path d="M40 90H490M40 170H490M40 250H490M40 330H490"/></g>',
           '  <polygon class="eq-area" fill="url(#eqArea)" points="%s 490,330 40,330"/>' % pts(paths[0])]
    for k in range(1, L):
        out.append('  <polyline class="eq-l" points="%s" stroke="%s" stroke-opacity=".34" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' % (pts(paths[k]), palette[k % len(palette)]))
    for k in range(1, 5):
        out.append('  <circle class="eq-o" cx="%.1f" cy="%.1f" r="6" fill="#8A97A8" opacity="0"/>' % (X(N - 1), Y(paths[k][-1])))
    out.append('  <polyline class="eq-w" filter="url(#eqGlow)" points="%s" stroke="#B38A2A" stroke-width="5.6" stroke-linecap="round" stroke-linejoin="round"/>' % pts(paths[0]))
    for i in (5, 12, 19, 26, 33, 40, 47, 54, 61):
        out.append('  <circle class="eq-d" data-i="%d" cx="%.1f" cy="%.1f" r="8.5" fill="#1B7F5C" stroke="#fff" stroke-width="2.5"/>' % (i, X(i), Y(paths[0][i])))
    out.append('  <circle class="eq-halo" cx="%.1f" cy="%.1f" r="9" stroke="#B38A2A" stroke-width="1.8" fill="none" opacity="0"/>' % (X(N - 1), Y(paths[0][-1])))
    out.append('  <circle class="eq-tip" cx="%.1f" cy="%.1f" r="9.5" fill="#fff" stroke="#B38A2A" stroke-width="4.5"/>' % (X(N - 1), Y(paths[0][-1])))
    out.append('  <g font-family="DM Sans,system-ui,sans-serif" font-size="12" font-weight="700" letter-spacing="1.6">')
    out.append('    <g class="eq-pill"><rect x="40" y="356" width="150" height="34" rx="17" fill="#0B1F3A"/><circle cx="60" cy="373" r="5" fill="#C29B40"/><text x="74" y="377.5" fill="#fff">VALIDATED</text></g>')
    out.append('  </g>')
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

ART_HERO = '''<svg viewBox="0 0 460 400" fill="none" aria-hidden="true">
  <defs>
    <linearGradient id="nbFront" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1A3F6D"/>
      <stop offset="40%" stop-color="#133156"/>
      <stop offset="100%" stop-color="#0A182B"/>
    </linearGradient>
    <linearGradient id="nbTop" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="#2D5E99"/>
      <stop offset="100%" stop-color="#4B86CE"/>
    </linearGradient>
    <linearGradient id="nbSide" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F243E"/>
      <stop offset="100%" stop-color="#050C15"/>
    </linearGradient>

    <linearGradient id="gdFront" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#E2B038"/>
      <stop offset="40%" stop-color="#C59324"/>
      <stop offset="100%" stop-color="#91670E"/>
    </linearGradient>
    <linearGradient id="gdTop" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="#FCE58D"/>
      <stop offset="100%" stop-color="#ECC452"/>
    </linearGradient>
    <linearGradient id="gdSide" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#946C13"/>
      <stop offset="100%" stop-color="#593E05"/>
    </linearGradient>

    <filter id="lineGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#1B7F5C" flood-opacity="0.35"/>
    </filter>
  </defs>

  <path d="M20 322 H440" stroke="#0B1F3A" stroke-width="3" stroke-linecap="round"/>

  <!-- Bar 1 (Research, h=75, y=247) -->
  <g class="bar-3d bar-1">
    <ellipse class="bar-shadow" cx="64" cy="324" rx="26" ry="4.5" fill="#0B1F3A" fill-opacity="0.18"/>
    <path d="M32 247 H82 V318 Q82 322 78 322 H36 Q32 322 32 318 Z" fill="url(#nbFront)"/>
    <polygon points="82,247 96,237 96,312 82,322" fill="url(#nbSide)"/>
    <polygon points="32,247 46,237 96,237 82,247" fill="url(#nbTop)" stroke="rgba(255,255,255,0.2)" stroke-width="0.8"/>
  </g>

  <!-- Bar 2 (h=125, y=197) -->
  <g class="bar-3d bar-2">
    <ellipse class="bar-shadow" cx="140" cy="324" rx="26" ry="4.5" fill="#0B1F3A" fill-opacity="0.18"/>
    <path d="M108 197 H158 V318 Q158 322 154 322 H112 Q108 322 108 318 Z" fill="url(#nbFront)"/>
    <polygon points="158,197 172,187 172,312 158,322" fill="url(#nbSide)"/>
    <polygon points="108,197 122,187 172,187 158,197" fill="url(#nbTop)" stroke="rgba(255,255,255,0.2)" stroke-width="0.8"/>
  </g>

  <!-- Bar 3 (Software, h=175, y=147) -->
  <g class="bar-3d bar-3">
    <ellipse class="bar-shadow" cx="216" cy="324" rx="26" ry="4.5" fill="#0B1F3A" fill-opacity="0.18"/>
    <path d="M184 147 H234 V318 Q234 322 230 322 H188 Q184 322 184 318 Z" fill="url(#nbFront)"/>
    <polygon points="234,147 248,137 248,312 234,322" fill="url(#nbSide)"/>
    <polygon points="184,147 198,137 248,137 234,147" fill="url(#nbTop)" stroke="rgba(255,255,255,0.2)" stroke-width="0.8"/>
  </g>

  <!-- Bar 4 (Execution, h=230, y=92) -->
  <g class="bar-3d bar-4">
    <ellipse class="bar-shadow" cx="292" cy="324" rx="26" ry="4.5" fill="#0B1F3A" fill-opacity="0.18"/>
    <path d="M260 92 H310 V318 Q310 322 306 322 H264 Q260 322 260 318 Z" fill="url(#nbFront)"/>
    <polygon points="310,92 324,82 324,312 310,322" fill="url(#nbSide)"/>
    <polygon points="260,92 274,82 324,82 310,92" fill="url(#nbTop)" stroke="rgba(255,255,255,0.2)" stroke-width="0.8"/>
  </g>

  <!-- Bar 5 (Capital - Gold, h=285, y=37) -->
  <g class="bar-3d bar-5">
    <ellipse class="bar-shadow" cx="368" cy="324" rx="28" ry="5" fill="#A57A18" fill-opacity="0.22"/>
    <path d="M336 37 H386 V318 Q386 322 382 322 H340 Q336 322 336 318 Z" fill="url(#gdFront)"/>
    <polygon points="386,37 400,27 400,312 386,322" fill="url(#gdSide)"/>
    <polygon points="336,37 350,27 400,27 386,37" fill="url(#gdTop)" stroke="rgba(255,255,255,0.3)" stroke-width="0.8"/>
  </g>

  <!-- Ascending Green Trend Line -->
  <path class="trend-line" filter="url(#lineGlow)" d="M64 226 L140 176 L216 126 L292 71 L368 16" stroke="#1B7F5C" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Halo pulse on peak node 5 -->
  <circle class="dot-halo" cx="368" cy="16" r="10" stroke="#1B7F5C" stroke-width="1.8" fill="none"/>

  <!-- Glowing Nodes -->
  <g fill="#fff" stroke="#1B7F5C" stroke-width="3.5">
    <circle class="trend-dot dot-1" cx="64" cy="226" r="6"/>
    <circle class="trend-dot dot-2" cx="140" cy="176" r="6"/>
    <circle class="trend-dot dot-3" cx="216" cy="126" r="6"/>
    <circle class="trend-dot dot-4" cx="292" cy="71" r="6.5"/>
    <circle class="trend-dot dot-5" cx="368" cy="16" r="8"/>
  </g>

  <!-- Pillar labels -->
  <g font-family="DM Sans,system-ui,sans-serif" font-size="12" font-weight="700" letter-spacing="2" fill="#51647B">
    <text x="32" y="352">RESEARCH</text>
    <text x="184" y="352">SOFTWARE</text>
    <text x="336" y="352">CAPITAL</text>
  </g>
</svg>'''

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

