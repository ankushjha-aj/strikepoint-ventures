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

  // Normal distribution curves animation controller.
  // Replays whenever it scrolls into view and when the research tab is selected.
  (function () {
    var svgs = $$("svg.dist-art");
    if (!svgs.length) return;

    function replay(svg) {
      svg.classList.remove("anim-play");
      void svg.offsetWidth; // trigger reflow
      svg.classList.add("anim-play");
    }

    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            replay(e.target);
          }
        });
      }, { threshold: 0.15 });

      svgs.forEach(function (svg) {
        io.observe(svg);
      });
    }

    // Trigger fresh animation on tab switches to Research panel
    document.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-t]");
      if (btn) {
        var t = btn.getAttribute("data-t");
        if (t === "r" || t === "0") {
          setTimeout(function () {
            svgs.forEach(replay);
          }, 35);
        }
      }
    });
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
    try { localStorage.setItem(KEY, "1"); } catch (e) { /* storage blocked: notice shows again next visit */ }
  }
  if (notice && !seen()) open();
  $$("[data-notice]").forEach(function (b) { b.addEventListener("click", open); });
  $$("[data-notice-close]").forEach(function (b) { b.addEventListener("click", close); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && notice && notice.classList.contains("on")) e.preventDefault();
  });

  // background theme picker (top-right)
  var picker = $("#theme");
  if (picker) {
    var pbtn = $(".theme__btn", picker);
    var mark = function () {
      var cur = document.documentElement.getAttribute("data-theme") || "1";
      $$(".theme__opt", picker).forEach(function (o) { o.classList.toggle("on", o.getAttribute("data-theme-set") === cur); });
    };
    var shut = function () { picker.classList.remove("open"); pbtn.setAttribute("aria-expanded", "false"); };
    pbtn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = picker.classList.toggle("open");
      pbtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    $$(".theme__opt", picker).forEach(function (o) {
      o.addEventListener("click", function () {
        var v = o.getAttribute("data-theme-set");
        document.documentElement.setAttribute("data-theme", v);
        try { localStorage.setItem("sp-theme", v); } catch (e) { /* storage blocked: theme lasts for this page only */ }
        mark(); shut();
      });
    });
    document.addEventListener("click", function (e) { if (!e.target.closest || !e.target.closest("#theme")) shut(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") shut(); });
    mark();
  }

  // blog category filter
  $$("[data-filter]").forEach(function (bar) {
    var scope = bar.parentNode, none = $(".posts__none", scope);
    $$("span[data-cat]", bar).forEach(function (chip) {
      chip.addEventListener("click", function () {
        var c = chip.getAttribute("data-cat"), shown = 0;
        $$("span[data-cat]", bar).forEach(function (x) { x.classList.toggle("on", x === chip); });
        $$(".post", scope).forEach(function (p) {
          var ok = c === "All" || p.getAttribute("data-cat") === c;
          p.hidden = !ok; if (ok) shown++;
        });
        if (none) none.hidden = shown > 0;
      });
    });
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
