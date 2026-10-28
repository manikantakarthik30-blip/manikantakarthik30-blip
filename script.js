(() => {
  const toggle = document.querySelector("#menu-toggle");
  const nav = document.querySelector("#primary-nav");
  if (toggle && nav) {
    const closeMenu = () => {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    };
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") !== "true";
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
    });
    nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeMenu();
        toggle.focus();
      }
    });
    document.addEventListener("click", (event) => {
      if (!nav.contains(event.target) && !toggle.contains(event.target)) closeMenu();
    });
  }

  // Motion is optional; the site remains navigable without WebGL or external JS libraries.
  const scene = document.querySelector(".orbit-scene");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (scene && !reducedMotion.matches && window.matchMedia("(pointer: fine)").matches) {
    scene.addEventListener("pointermove", (event) => {
      const bounds = scene.getBoundingClientRect();
      const x = (event.clientX - bounds.left) / bounds.width - 0.5;
      const y = (event.clientY - bounds.top) / bounds.height - 0.5;
      scene.style.setProperty("--scene-x", (x * 5).toFixed(2) + "deg");
      scene.style.setProperty("--scene-y", (y * -5).toFixed(2) + "deg");
    });
    scene.addEventListener("pointerleave", () => {
      scene.style.setProperty("--scene-x", "0deg");
      scene.style.setProperty("--scene-y", "0deg");
    });
  }
})();