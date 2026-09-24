/* Page config. Swap these before publishing. See README.md.
   Empty string = not confirmed yet.
   Required values render as a visible [PLACEHOLDER] chip until set.
   Optional values (MESSAGING_SLA, SEAT_COUNT, COHORT_DEADLINE) hide their rows until set. */
const PAGE_CONFIG = {
  PROGRAM_NAME: "New Build Coaching with Corey", // ASSUMED working title
  APPLICATION_URL: "https://www.lvrgd.co/book",   // primary CTA: application that leads into booking a call
  PROGRAM_PRICE: "",    // not shown on the page (pricing is covered on the call)
  PROGRAM_DURATION: "8 months",
  CALL_CADENCE: "whenever you need one",
  MESSAGING_SLA: "",     // optional, e.g. "1 business day"
  SEAT_COUNT: "",        // optional, only a real cap
  COHORT_DEADLINE: "",   // optional, only a real date
  VSL_URL: "https://www.lvrgd.co/book", // hero video link. Empty = placeholder image, not clickable
};

(function () {
  document.documentElement.classList.remove("no-js");
  const cfg = PAGE_CONFIG;

  // Text placeholders
  document.querySelectorAll("[data-ph]").forEach((el) => {
    const key = el.dataset.ph;
    const val = (cfg[key] || "").trim();
    if (val) {
      el.textContent = val;
      el.classList.remove("ph");
    } else {
      el.textContent = "[" + key + "]";
      el.classList.add("ph");
    }
  });

  // Optional rows hide until their value exists
  document.querySelectorAll("[data-optional]").forEach((el) => {
    el.hidden = !(cfg[el.dataset.optional] || "").trim();
  });

  // Primary CTA. Falls back to the final Apply section until APPLICATION_URL is set.
  const url = (cfg.APPLICATION_URL || "").trim();
  document.querySelectorAll("[data-apply]").forEach((a) => {
    if (url) {
      a.href = url;
      if (/^https?:/.test(url)) { a.target = "_blank"; a.rel = "noopener"; }
    } else {
      a.href = "#apply";
      a.title = "[APPLICATION_URL] not set yet";
    }
  });

  // Hero VSL. Clickable only once a real video URL exists.
  const vsl = document.querySelector("[data-vsl]");
  const vslUrl = (cfg.VSL_URL || "").trim();
  if (vsl && vslUrl) {
    vsl.href = vslUrl;
    vsl.target = "_blank";
    vsl.rel = "noopener";
  } else if (vsl) {
    vsl.classList.add("is-placeholder");
  }

  // Nav border on scroll
  const nav = document.querySelector(".nav");
  const onScroll = () => nav.classList.toggle("is-scrolled", window.scrollY > 8);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  if (!("IntersectionObserver" in window)) {
    document.querySelectorAll(".reveal").forEach((el) => el.classList.add("is-in"));
    return;
  }

  // Scroll reveal
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  // Mobile sticky CTA: show after the hero, hide over the final CTA
  const sticky = document.querySelector(".sticky");
  const hero = document.querySelector(".hero");
  const final = document.querySelector(".final");
  let heroOut = false, finalIn = false;
  const update = () => sticky.classList.toggle("is-visible", heroOut && !finalIn);
  new IntersectionObserver(([e]) => { heroOut = !e.isIntersecting; update(); }).observe(hero);
  new IntersectionObserver(([e]) => { finalIn = e.isIntersecting; update(); }).observe(final);
})();
