(function () {
  const cfg = window.RECEITAS_CONFIG || {};
  const API_BASE = (cfg.API_BASE || "").replace(/\/$/, "");

  function recipeSlugFromPath() {
    const path = window.location.pathname.replace(/\\/g, "/");
    const marker = "/receitas/";
    const idx = path.indexOf(marker);
    if (idx === -1) return null;
    let slug = path.slice(idx + marker.length).replace(/\.html$/i, "");
    slug = slug.replace(/^\/+|\/+$/g, "");
    return slug || null;
  }

  async function api(path, options) {
    const res = await fetch(API_BASE + path, {
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
        ...(options && options.body
          ? { "Content-Type": "application/json" }
          : {}),
        ...((options && options.headers) || {}),
      },
      ...options,
    });
    let data = null;
    const text = await res.text();
    if (text) {
      try {
        data = JSON.parse(text);
      } catch {
        data = { error: text };
      }
    }
    if (!res.ok) {
      const err = new Error((data && data.error) || "Erro na API");
      err.status = res.status;
      err.data = data;
      throw err;
    }
    return data;
  }

  function el(tag, attrs, children) {
    const node = document.createElement(tag);
    if (attrs) {
      Object.entries(attrs).forEach(function ([k, v]) {
        if (v == null || v === false) return;
        if (k === "className") node.className = v;
        else if (k === "text") node.textContent = v;
        else if (k.startsWith("on") && typeof v === "function") {
          node.addEventListener(k.slice(2).toLowerCase(), v);
        } else if (k === "html") node.innerHTML = v;
        else node.setAttribute(k, v === true ? "" : String(v));
      });
    }
    (children || []).forEach(function (c) {
      if (c == null) return;
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  function focusLogin(panel) {
    if (!panel) return;
    panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
    const input = panel.querySelector('input[type="email"]');
    if (input) input.focus();
  }

  function updateNavLabel(user) {
    const btn = document.getElementById("caderno-nav-btn");
    if (!btn) return;
    btn.textContent = user ? "Meu caderno" : "Entrar";
    btn.setAttribute("aria-label", user ? "Meu caderno" : "Entrar no Meu caderno");
  }

  function ensureHeaderEntry(onActivate) {
    const header = document.querySelector(".site-header");
    if (!header || document.getElementById("caderno-nav-btn")) return;

    let nav = header.querySelector(".site-nav");
    if (!nav) {
      nav = el("nav", { className: "site-nav", "aria-label": "Principal" });
      header.appendChild(nav);
    }

    const btn = el("button", {
      type: "button",
      id: "caderno-nav-btn",
      className: "caderno-nav-btn",
      text: "Entrar",
      "aria-label": "Entrar no Meu caderno",
      onClick: function () {
        onActivate();
      },
    });
    nav.appendChild(btn);
  }

  function ensureRecipeJump(main) {
    const actions = main.querySelector(".recipe-actions");
    if (!actions || actions.querySelector(".caderno-jump")) return;
    actions.appendChild(
      el("a", {
        href: "#meu-caderno",
        className: "btn btn-ghost caderno-jump",
        text: "Meu caderno",
        onClick: function (e) {
          e.preventDefault();
          focusLogin(document.getElementById("meu-caderno"));
        },
      })
    );
  }

  function mountRecipePanel() {
    const slug = recipeSlugFromPath();
    if (!slug) return null;

    const main = document.querySelector("main.recipe-page");
    if (!main) return null;

    ensureRecipeJump(main);

    let panel = document.getElementById("meu-caderno");
    if (!panel) {
      panel = el("aside", {
        id: "meu-caderno",
        className: "caderno no-print",
        "aria-label": "Meu caderno",
      });
      const actions = main.querySelector(".recipe-actions");
      if (actions) {
        actions.insertAdjacentElement("afterend", panel);
      } else {
        main.insertBefore(panel, main.firstChild);
      }
    }

    render(panel, slug);
    return panel;
  }

  function mountIndexPanel() {
    if (recipeSlugFromPath()) return null;
    if (document.getElementById("meu-caderno")) {
      return document.getElementById("meu-caderno");
    }

    const header = document.querySelector(".site-header");
    const panel = el("aside", {
      id: "meu-caderno",
      className: "caderno caderno-index no-print",
      "aria-label": "Meu caderno",
      hidden: true,
    });

    if (header && header.parentNode) {
      header.insertAdjacentElement("afterend", panel);
    } else {
      document.body.insertBefore(panel, document.body.firstChild);
    }

    renderIndex(panel);
    return panel;
  }

  async function currentUser() {
    try {
      const me = await api("/api/auth/me");
      return me.user;
    } catch (err) {
      if (err.status === 401) return null;
      throw err;
    }
  }

  async function render(panel, slug) {
    panel.innerHTML = "";
    panel.appendChild(
      el("h2", { className: "caderno-title", text: "Meu caderno" })
    );
    const body = el("div", { className: "caderno-body" });
    panel.appendChild(body);
    body.textContent = "Carregando…";

    let user = null;
    try {
      user = await currentUser();
    } catch {
      body.textContent = "Não foi possível conectar ao caderno.";
      updateNavLabel(null);
      return;
    }

    updateNavLabel(user);

    if (!user) {
      body.innerHTML = "";
      body.appendChild(
        el("p", {
          className: "caderno-hint",
          text: "Entre para marcar receitas e guardar notas.",
        })
      );
      renderLogin(body, function () {
        render(panel, slug);
      });
      return;
    }

    let meta;
    try {
      meta = await api("/api/recipes/" + encodeURI(slug) + "/meta");
    } catch {
      body.textContent = "Erro ao carregar suas anotações.";
      return;
    }

    renderEditor(body, panel, slug, user, meta);
  }

  async function renderIndex(panel) {
    panel.innerHTML = "";
    panel.appendChild(
      el("h2", { className: "caderno-title", text: "Meu caderno" })
    );
    const body = el("div", { className: "caderno-body" });
    panel.appendChild(body);
    body.textContent = "Carregando…";

    let user = null;
    try {
      user = await currentUser();
    } catch {
      body.textContent = "Não foi possível conectar ao caderno.";
      updateNavLabel(null);
      panel.hidden = false;
      return;
    }

    updateNavLabel(user);

    if (!user) {
      body.innerHTML = "";
      body.appendChild(
        el("p", {
          className: "caderno-hint",
          text: "Entre para marcar receitas e guardar notas nas fichas.",
        })
      );
      renderLogin(body, function () {
        renderIndex(panel);
      });
      return;
    }

    body.innerHTML = "";
    body.appendChild(
      el("div", { className: "caderno-user" }, [
        el("span", { text: user.email }),
        el("button", {
          type: "button",
          className: "btn btn-ghost caderno-logout",
          text: "Sair",
          onClick: async function () {
            try {
              await api("/api/auth/logout", { method: "POST" });
            } catch {
              /* ignore */
            }
            renderIndex(panel);
          },
        }),
      ])
    );
    body.appendChild(
      el("p", {
        className: "caderno-hint",
        text: "Abra uma receita para marcar Quero fazer / Já fiz, estrelas e notas.",
      })
    );
  }

  function renderLogin(body, onSuccess) {
    const form = el("form", { className: "caderno-form" });
    const email = el("input", {
      type: "email",
      name: "email",
      required: true,
      autocomplete: "username",
      placeholder: "E-mail",
    });
    const password = el("input", {
      type: "password",
      name: "password",
      required: true,
      autocomplete: "current-password",
      placeholder: "Senha",
    });
    const msg = el("p", { className: "caderno-msg", hidden: true });
    const submit = el("button", {
      type: "submit",
      className: "btn",
      text: "Entrar",
    });

    form.append(email, password, msg, submit);
    body.appendChild(form);

    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      msg.hidden = true;
      submit.disabled = true;
      try {
        await api("/api/auth/login", {
          method: "POST",
          body: JSON.stringify({
            email: email.value,
            password: password.value,
          }),
        });
        onSuccess();
      } catch (err) {
        msg.textContent = (err.data && err.data.error) || "Falha no login";
        msg.hidden = false;
        submit.disabled = false;
      }
    });
  }

  function renderEditor(body, panel, slug, user, meta) {
    body.innerHTML = "";

    const head = el("div", { className: "caderno-user" }, [
      el("span", { text: user.email }),
      el("button", {
        type: "button",
        className: "btn btn-ghost caderno-logout",
        text: "Sair",
        onClick: async function () {
          try {
            await api("/api/auth/logout", { method: "POST" });
          } catch {
            /* ignore */
          }
          render(panel, slug);
        },
      }),
    ]);
    body.appendChild(head);

    const statusRow = el("div", { className: "caderno-status" }, [
      el("span", { className: "caderno-label", text: "Status" }),
    ]);
    const statuses = [
      { value: null, label: "—" },
      { value: "quero_fazer", label: "Quero fazer" },
      { value: "ja_fiz", label: "Já fiz" },
    ];
    statuses.forEach(function (s) {
      const btn = el("button", {
        type: "button",
        className:
          "caderno-chip" +
          ((meta.status || null) === s.value ? " is-active" : ""),
        text: s.label,
        onClick: function () {
          save({ status: s.value });
        },
      });
      statusRow.appendChild(btn);
    });
    body.appendChild(statusRow);

    const ratingWrap = el("div", {
      className:
        "caderno-rating" + (meta.status === "ja_fiz" ? "" : " is-disabled"),
    });
    ratingWrap.appendChild(
      el("span", { className: "caderno-label", text: "Nota" })
    );
    const stars = el("div", {
      className: "caderno-stars",
      role: "group",
      "aria-label": "Avaliação de 1 a 5",
    });
    for (let i = 1; i <= 5; i++) {
      stars.appendChild(
        el("button", {
          type: "button",
          className: "caderno-star" + (meta.rating >= i ? " is-on" : ""),
          "aria-label": i + " estrela" + (i > 1 ? "s" : ""),
          text: "★",
          onClick: function () {
            if (meta.status !== "ja_fiz") return;
            save({ rating: i });
          },
        })
      );
    }
    ratingWrap.appendChild(stars);
    body.appendChild(ratingWrap);

    const notesLabel = el("label", {
      className: "caderno-label",
      text: "Notas",
      for: "caderno-notes",
    });
    const notes = el("textarea", {
      id: "caderno-notes",
      className: "caderno-notes",
      rows: "3",
      placeholder: "Ex.: coloquei menos açúcar…",
    });
    notes.value = meta.notes || "";
    body.appendChild(notesLabel);
    body.appendChild(notes);

    const footer = el("div", { className: "caderno-footer" });
    const saveBtn = el("button", {
      type: "button",
      className: "btn",
      text: "Salvar notas",
    });
    const feedback = el("span", { className: "caderno-msg" });
    footer.append(saveBtn, feedback);
    body.appendChild(footer);

    saveBtn.addEventListener("click", function () {
      save({ notes: notes.value });
    });

    let saving = false;
    async function save(patch) {
      if (saving) return;
      saving = true;
      feedback.textContent = "Salvando…";
      try {
        meta = await api("/api/recipes/" + encodeURI(slug) + "/meta", {
          method: "PUT",
          body: JSON.stringify(patch),
        });
        feedback.textContent = "Salvo";
        renderEditor(body, panel, slug, user, meta);
      } catch (err) {
        feedback.textContent =
          (err.data && err.data.error) || "Erro ao salvar";
        saving = false;
      }
    }
  }

  function activateCaderno() {
    const slug = recipeSlugFromPath();
    if (slug) {
      const panel = document.getElementById("meu-caderno") || mountRecipePanel();
      focusLogin(panel);
      return;
    }

    const panel = document.getElementById("meu-caderno") || mountIndexPanel();
    if (!panel) return;
    panel.hidden = false;
    focusLogin(panel);
  }

  function boot() {
    ensureHeaderEntry(activateCaderno);

    if (recipeSlugFromPath()) {
      mountRecipePanel();
    } else {
      mountIndexPanel();
      // Na home, o painel só aparece ao clicar em Entrar (exceto se já logada).
      currentUser()
        .then(function (user) {
          updateNavLabel(user);
          const panel = document.getElementById("meu-caderno");
          if (panel && user) {
            panel.hidden = false;
            renderIndex(panel);
          }
        })
        .catch(function () {
          updateNavLabel(null);
        });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
