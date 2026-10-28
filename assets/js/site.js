/* StrikePoint Ventures: site behaviour */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // mobile menu
  var burger = $(".burger"), menu = $(".menu");
  if (burger && menu) burger.addEventListener("click", function () { menu.classList.toggle("on"); });

  // tapping anywhere outside the open menu (or pressing Escape) closes it
  function closeMenu() { if (menu) menu.classList.remove("on"); $$(".drop").forEach(function (d) { d.classList.remove("open"); }); }
  document.addEventListener("click", function (e) {
    if (!menu || !menu.classList.contains("on")) return;
    if (e.target.closest && (e.target.closest(".menu") || e.target.closest(".burger"))) return;
    closeMenu();
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeMenu(); });

  // Services opens on click inside the collapsed menu
  $$(".drop > button").forEach(function (b) {
    b.addEventListener("click", function () { b.parentNode.classList.toggle("open"); });
  });
  if (burger && menu) burger.addEventListener("click", function () { if (!menu.classList.contains("on")) $$(".drop").forEach(function (d) { d.classList.remove("open"); }); });

  // close the Services dropdown after a choice (until the pointer leaves)
  $$(".drop").forEach(function (d) {
    d.addEventListener("click", function (e) {
      if (!e.target.closest || !e.target.closest(".drop__panel a")) return;
      d.classList.add("shut"); d.classList.remove("open");
      if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
    });
    d.addEventListener("mouseleave", function () { d.classList.remove("shut"); });
  });

  // header takes on the page colour at the current scroll position
  var bar = $(".bar");
  function hex(v) {
    v = (v || "").trim().replace("#", "");
    if (v.length === 3) v = v.replace(/(.)/g, "$1$1");
    var n = parseInt(v, 16);
    return isNaN(n) ? [255, 255, 255] : [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  function mix(a, b, t) { return a.map(function (x, i) { return Math.round(x + (b[i] - x) * t); }); }
  function tint() {
    if (!bar) return;
    var cs = getComputedStyle(document.documentElement);
    var A = hex(cs.getPropertyValue("--a")), M = hex(cs.getPropertyValue("--mid")), B = hex(cs.getPropertyValue("--b"));
    var h = Math.max(1, document.documentElement.scrollHeight);
    var t = Math.min(1, Math.max(0, (window.scrollY + 60) / h));
    var c = t < 0.5 ? mix(A, M, t * 2) : mix(M, B, (t - 0.5) * 2);
    bar.style.setProperty("--hdr", "rgb(" + c.join(",") + ")");
  }
  var ticking = false;
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(function () { tint(); ticking = false; }); }
  }, { passive: true });
  window.addEventListener("resize", tint);
  if ("MutationObserver" in window) new MutationObserver(tint).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  tint();

  // reveal on scroll
  var items = $$(".rv");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else items.forEach(function (el) { el.classList.add("in"); });

  // research chart: curves race, the winner turns gold, green dots mark its wins.
  // The markup is already the finished chart; this replays it while visible (and on every tab switch).
  (function () {
    var svgs = $$("svg.eq-art");
    if (!svgs.length || (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches)) return;
    var CYCLE = 9000, NAVY = [11, 31, 58], GOLD = [179, 138, 42];
    function S(t, a, b) { return Math.min(1, Math.max(0, (t - a) / (b - a))); }
    function E(x) { return 1 - Math.pow(1 - x, 3); }
    function B(x) { var c = 1.70158, d = c + 1; return 1 + d * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); }
    function mix(a, b, k) { return "rgb(" + a.map(function (v, i) { return Math.round(v + (b[i] - v) * k); }).join(",") + ")"; }
    function parse(el) { return el.getAttribute("points").trim().split(/\s+/); }
    function show(el, k) { el.setAttribute("opacity", k); el.setAttribute("transform", "translate(0," + ((1 - E(k)) * 10).toFixed(1) + ")"); }
    var items = svgs.map(function (svg) {
      var w = svg.querySelector(".eq-w"), tip = svg.querySelector(".eq-tip");
      var it = {
        svg: svg, w: w, wp: parse(w), glow: w.getAttribute("filter"), tip: tip, halo: svg.querySelector(".eq-halo"),
        area: svg.querySelector(".eq-area"), pill: svg.querySelector(".eq-pill"), start: performance.now(), visible: true,
        ls: $$(".eq-l", svg).map(function (el) { return { el: el, p: parse(el) }; }),
        os: $$(".eq-o", svg),
        ds: $$(".eq-d", svg).map(function (el) { el.style.transformBox = "fill-box"; el.style.transformOrigin = "center"; return { el: el, i: +el.getAttribute("data-i") }; })
      };
      it.N = it.wp.length;
      return it;
    });
    function render(it, t) {
      var n = Math.floor(S(t, .04, .56) * (it.N - 1)) + 1, f = E(S(t, .6, .78));
      it.ls.forEach(function (l) { l.el.setAttribute("points", l.p.slice(0, n).join(" ")); l.el.setAttribute("stroke-opacity", (.85 + (.34 - .85) * f).toFixed(3)); });
      it.w.setAttribute("points", it.wp.slice(0, n).join(" "));
      it.w.setAttribute("stroke", mix(NAVY, GOLD, f));
      it.w.setAttribute("stroke-width", (3.4 + 2.2 * f).toFixed(2));
      if (f > .05 && it.glow) it.w.setAttribute("filter", it.glow); else it.w.removeAttribute("filter");
      var head = it.wp[n - 1].split(",");
      it.tip.setAttribute("cx", head[0]); it.tip.setAttribute("cy", head[1]); it.tip.setAttribute("opacity", S(t, .04, .08));
      it.halo.setAttribute("cx", head[0]); it.halo.setAttribute("cy", head[1]);
      var ph = (t * CYCLE / 1600) % 1;
      it.halo.setAttribute("r", (8 + ph * 18).toFixed(1)); it.halo.setAttribute("opacity", (f * (1 - ph)).toFixed(3));
      it.ds.forEach(function (d) {
        var k = S(n - 1 - d.i, 0, 5);
        d.el.setAttribute("opacity", Math.min(1, k * 3)); d.el.style.transform = "scale(" + (k > 0 ? B(k) : 0).toFixed(3) + ")";
      });
      it.os.forEach(function (o) { o.setAttribute("opacity", (S(t, .56, .6) * (1 - f) * .7).toFixed(3)); });
      it.area.setAttribute("opacity", S(t, .72, .9).toFixed(3));
      show(it.pill, S(t, .8, .9));
    }
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          items.forEach(function (it) {
            if (it.svg !== e.target) return;
            if (e.isIntersecting && !it.visible) it.start = performance.now();
            it.visible = e.isIntersecting;
          });
        });
      }, { threshold: .15 });
      items.forEach(function (it) { io.observe(it.svg); });
    }
    function frame(now) {
      if (!document.hidden) items.forEach(function (it) { if (it.visible) render(it, ((now - it.start) % CYCLE) / CYCLE); });
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  })();

  // tab groups: [data-tabs] holds buttons[data-t], panels carry data-t
  $$("[data-tabs]").forEach(function (group) {
    var scope = group.parentNode;
    var btns = $$("button[data-t]", group), panels = $$("[data-t]:not(button)", scope);
    function show(t) {
      btns.forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-t") === t); });
      panels.forEach(function (p) { p.classList.toggle("on", p.getAttribute("data-t") === t); });
    }
    btns.forEach(function (b) {
      var t = b.getAttribute("data-t");
      b.addEventListener("click", function () { show(t); });
      if (group.hasAttribute("data-hover")) b.addEventListener("mouseenter", function () { show(t); });
    });
  });

  // regulatory notice: modal, blocks the page until accepted
  var notice = $("#notice"), KEY = "sp-notice-ack";
  var lockEls = $$("header.bar, main, .page, footer.foot");
  function seen() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function open() {
    if (!notice) return;
    notice.classList.add("on");
    document.documentElement.style.overflow = "hidden";
    document.body.style.overflow = "hidden";
    lockEls.forEach(function (el) { el.setAttribute("inert", ""); });
    var b = $("[data-notice-close]", notice);
    if (b) b.focus();
  }
  function close() {
    if (!notice) return;
    notice.classList.remove("on");
    document.documentElement.style.overflow = "";
    document.body.style.overflow = "";
    lockEls.forEach(function (el) { el.removeAttribute("inert"); });
    try { localStorage.setItem(KEY, "1"); } catch (e) {}
  }
  if (notice && !seen()) open();
  $$("[data-notice]").forEach(function (b) { b.addEventListener("click", open); });
  $$("[data-notice-close]").forEach(function (b) { b.addEventListener("click", close); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && notice && notice.classList.contains("on")) e.preventDefault();
  });

  // contact form -> /api/contact
  var form = $("#contactForm");
  var topic = $("#t"), otherBox = $("#otherBox"), otherIn = $("#o");
  function syncOther() {
    if (!topic || !otherBox) return;
    var on = topic.value === "Other";
    otherBox.classList.toggle("on", on);
    if (otherIn) otherIn.required = on;
  }
  if (topic) { topic.addEventListener("change", syncOther); syncOther(); }
  if (form) form.addEventListener("submit", function (e) {
    e.preventDefault();
    var f = new FormData(form);
    if (f.get("website")) return;
    if (window.SP_REVIEW) { $("#formMsg").textContent = "This is a review copy, so the form is not connected."; return; }
    var out = $("#formMsg"), btn = $("button[type=submit]", form);
    btn.disabled = true;
    fetch("/api/contact", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: f.get("name"), email: f.get("email"), topic: (f.get("topic") === "Other" && f.get("other")) ? "Other: " + f.get("other") : f.get("topic"), message: f.get("message") })
    }).then(function (r) { return r.json(); })
      .then(function (d) { out.textContent = d.message || "Thank you. We will reply within one business day."; form.reset(); })
      .catch(function () { out.textContent = "Something went wrong. Please email us directly."; })
      .then(function () { btn.disabled = false; });
  });
})();
