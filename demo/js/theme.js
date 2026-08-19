(function () {
  var STORAGE_KEY = "demo-theme";
  var DEFAULT_THEME = "classic";

  function getTheme() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved === "classic" || saved === "modern") return saved;
    } catch (e) {
      /* ignore */
    }
    return DEFAULT_THEME;
  }

  function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {
      /* ignore */
    }
    document.querySelectorAll("[data-theme-set]").forEach(function (btn) {
      var active = btn.getAttribute("data-theme-set") === theme;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  function backHref() {
    var path = window.location.pathname.replace(/\\/g, "/");
    if (path.indexOf("/demo/na-cozinha/") !== -1) return "../../index.html";
    if (path.indexOf("/demo/") !== -1) return "../index.html";
    return "./index.html";
  }

  function mountPreviewBar() {
    if (document.querySelector(".demo-preview-bar")) return;

    var bar = document.createElement("div");
    bar.className = "demo-preview-bar no-print";
    bar.setAttribute("role", "banner");
    bar.innerHTML =
      '<span class="demo-preview-badge">Prévia — não é o site final</span>' +
      '<div class="demo-theme-toggle" role="group" aria-label="Tema da prévia">' +
      '<button type="button" data-theme-set="classic" aria-pressed="false">Clássico</button>' +
      '<button type="button" data-theme-set="modern" aria-pressed="false">Moderno</button>' +
      "</div>" +
      '<a class="demo-back-link" href="' +
      backHref() +
      '">Voltar ao site atual</a>';

    document.body.insertBefore(bar, document.body.firstChild);

    bar.querySelectorAll("[data-theme-set]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        setTheme(btn.getAttribute("data-theme-set"));
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      setTheme(getTheme());
      mountPreviewBar();
      setTheme(getTheme());
    });
  } else {
    setTheme(getTheme());
    mountPreviewBar();
    setTheme(getTheme());
  }
})();
