(function () {
  const input = document.getElementById("recipe-search");
  const emptyMsg = document.getElementById("search-empty");
  const indexRoot = document.getElementById("receitas");
  const categoryNav = document.getElementById("categorias");
  const breadcrumbs = document.getElementById("breadcrumbs");
  const blocks = document.querySelectorAll(".category-block");

  if (!indexRoot || !blocks.length) return;

  function normalize(text) {
    return String(text || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .trim();
  }

  function slugify(text) {
    return normalize(text)
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "");
  }

  function parseHash() {
    const raw = (location.hash || "").replace(/^#\/?/, "").trim();
    if (!raw) return { categoryId: null, subSlug: null };
    const parts = raw.split("/").filter(Boolean);
    const categoryId = parts[0] || null;
    if (categoryId === "categorias" || categoryId === "receitas") {
      return { categoryId: null, subSlug: null };
    }
    return {
      categoryId: categoryId,
      subSlug: parts[1] ? decodeURIComponent(parts[1]) : null,
    };
  }

  function setHash(categoryId, subSlug) {
    let next = "";
    if (categoryId && subSlug) {
      next = "#" + categoryId + "/" + subSlug;
    } else if (categoryId) {
      next = "#" + categoryId;
    } else {
      next = "#";
    }
    if ((location.hash || "#") === next || (!location.hash && next === "#")) {
      applyView();
      return;
    }
    location.hash = next === "#" ? "" : next;
  }

  /** @type {Map<string, { block: Element, title: string, subs: Array<{slug: string, label: string, heading: Element, list: Element}>, isLeaf: boolean }>} */
  const catalog = new Map();

  blocks.forEach(function (block) {
    const id = block.id;
    if (!id) return;
    const title = (block.querySelector("h2")?.textContent || id).trim();
    const lists = Array.from(block.querySelectorAll(":scope > .recipe-list"));
    const subs = [];

    lists.forEach(function (list) {
      const prev = list.previousElementSibling;
      const labelFromHeading =
        prev && prev.classList.contains("subcategory")
          ? (prev.textContent || "").trim()
          : "";
      const label =
        labelFromHeading ||
        (list.getAttribute("data-subcategory") || "").trim();
      if (!label) return;
      const slug = slugify(label);
      list.setAttribute("data-sub-slug", slug);
      if (prev && prev.classList.contains("subcategory")) {
        prev.setAttribute("data-sub-slug", slug);
      }
      subs.push({
        slug: slug,
        label: label,
        heading: prev && prev.classList.contains("subcategory") ? prev : null,
        list: list,
      });
    });

    const isLeaf = subs.length === 0;
    block.classList.toggle("is-leaf", isLeaf);
    block.setAttribute("data-has-subs", isLeaf ? "false" : "true");

    if (!isLeaf) {
      let subNav = block.querySelector(":scope > .subcategory-nav");
      if (!subNav) {
        subNav = document.createElement("nav");
        subNav.className = "subcategory-nav no-print";
        subNav.setAttribute("aria-label", "Subcategorias de " + title);
        const h2 = block.querySelector("h2");
        if (h2 && h2.nextSibling) {
          block.insertBefore(subNav, h2.nextSibling);
        } else {
          block.appendChild(subNav);
        }
      }
      subNav.innerHTML = "";
      subs.forEach(function (sub) {
        const a = document.createElement("a");
        a.href = "#" + id + "/" + sub.slug;
        a.textContent = sub.label;
        a.dataset.subSlug = sub.slug;
        subNav.appendChild(a);
      });
    }

    catalog.set(id, { block: block, title: title, subs: subs, isLeaf: isLeaf });
  });

  function clearItemVisibility() {
    blocks.forEach(function (block) {
      block.querySelectorAll(".recipe-list > li").forEach(function (el) {
        el.hidden = false;
      });
    });
    if (emptyMsg) emptyMsg.hidden = true;
  }

  function scrollToEl(el) {
    if (!el) return;
    requestAnimationFrame(function () {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  function goHome(e) {
    if (e) e.preventDefault();
    if (input) input.value = "";
    setHash(null, null);
  }

  function renderBreadcrumbs(categoryId, subSlug, searching) {
    if (!breadcrumbs) return;
    breadcrumbs.replaceChildren();

    if (searching) {
      breadcrumbs.hidden = false;
      const home = document.createElement("a");
      home.href = "./index.html";
      home.textContent = "Início";
      home.addEventListener("click", goHome);
      breadcrumbs.appendChild(home);
      breadcrumbs.appendChild(document.createTextNode(" › Busca"));
      return;
    }

    if (!categoryId || !subSlug) {
      breadcrumbs.hidden = true;
      return;
    }

    const entry = catalog.get(categoryId);
    if (!entry) {
      breadcrumbs.hidden = true;
      return;
    }

    const sub = entry.subs.find(function (s) {
      return s.slug === subSlug;
    });

    breadcrumbs.hidden = false;
    const home = document.createElement("a");
    home.href = "./index.html";
    home.textContent = "Início";
    home.addEventListener("click", goHome);
    breadcrumbs.appendChild(home);
    breadcrumbs.appendChild(document.createTextNode(" › "));

    const catLink = document.createElement("a");
    catLink.href = "#" + categoryId;
    catLink.textContent = entry.title;
    catLink.addEventListener("click", function (e) {
      e.preventDefault();
      if (input) input.value = "";
      setHash(categoryId, null);
    });
    breadcrumbs.appendChild(catLink);
    breadcrumbs.appendChild(document.createTextNode(" › "));

    const current = document.createElement("span");
    current.setAttribute("aria-current", "page");
    current.textContent = sub ? sub.label : subSlug;
    breadcrumbs.appendChild(current);
  }

  /** Home: all categories; with-subs show only sub links; leaves show recipes. */
  function showHome(scrollCategoryId) {
    indexRoot.dataset.nav = "home";
    if (categoryNav) categoryNav.hidden = false;
    clearItemVisibility();

    blocks.forEach(function (block) {
      block.hidden = false;
      block.classList.remove("is-active", "is-sub-active");
      const entry = catalog.get(block.id);
      const subNav = block.querySelector(":scope > .subcategory-nav");

      if (entry && !entry.isLeaf) {
        if (subNav) subNav.hidden = false;
        entry.subs.forEach(function (s) {
          if (s.heading) s.heading.hidden = true;
          s.list.hidden = true;
        });
      } else {
        if (subNav) subNav.hidden = true;
        block.querySelectorAll(":scope > .recipe-list").forEach(function (list) {
          list.hidden = false;
        });
        block.querySelectorAll(":scope > .subcategory").forEach(function (h) {
          h.hidden = false;
        });
      }
    });

    renderBreadcrumbs(null, null, false);

    if (scrollCategoryId) {
      const entry = catalog.get(scrollCategoryId);
      if (entry) scrollToEl(entry.block);
    }
  }

  /** Subcategory drill-down: recipes for one sub only. */
  function showSub(entry, categoryId, subSlug) {
    const sub = entry.subs.find(function (s) {
      return s.slug === subSlug;
    });
    if (!sub) {
      showHome(categoryId);
      return;
    }

    indexRoot.dataset.nav = "sub";
    if (categoryNav) categoryNav.hidden = true;
    clearItemVisibility();

    blocks.forEach(function (b) {
      const active = b === entry.block;
      b.hidden = !active;
      b.classList.toggle("is-active", active);
      b.classList.toggle("is-sub-active", active);
    });

    const subNav = entry.block.querySelector(":scope > .subcategory-nav");
    if (subNav) subNav.hidden = true;

    entry.subs.forEach(function (s) {
      const show = s === sub;
      if (s.heading) s.heading.hidden = !show;
      s.list.hidden = !show;
    });

    renderBreadcrumbs(categoryId, subSlug, false);
  }

  function applyView() {
    const query = input ? normalize(input.value) : "";
    if (query) {
      applySearch(query);
      return;
    }

    const { categoryId, subSlug } = parseHash();
    const entry = categoryId ? catalog.get(categoryId) : null;

    if (!categoryId || !entry) {
      showHome();
      return;
    }

    // #categoria alone → stay on full home, jump to that section
    if (!subSlug) {
      showHome(categoryId);
      return;
    }

    if (entry.isLeaf) {
      showHome(categoryId);
      return;
    }

    showSub(entry, categoryId, subSlug);
  }

  function applySearch(query) {
    indexRoot.dataset.nav = "search";
    if (categoryNav) categoryNav.hidden = true;
    let anyVisible = false;

    blocks.forEach(function (block) {
      block.classList.remove("is-active", "is-sub-active");
      block.hidden = false;
      const categoryName = normalize(block.querySelector("h2")?.textContent || "");
      const lists = block.querySelectorAll(":scope > .recipe-list");
      let visibleInBlock = 0;
      const subNav = block.querySelector(":scope > .subcategory-nav");
      if (subNav) subNav.hidden = true;

      lists.forEach(function (list) {
        const subHeading = list.previousElementSibling;
        const subName =
          subHeading && subHeading.classList.contains("subcategory")
            ? normalize(subHeading.textContent || "")
            : normalize(list.getAttribute("data-subcategory") || "");
        const items = list.querySelectorAll(":scope > li");
        let visibleInList = 0;

        items.forEach(function (li) {
          if (li.classList.contains("empty")) {
            li.hidden = true;
            return;
          }

          const recipeName = normalize(li.textContent || "");
          const match =
            recipeName.includes(query) ||
            categoryName.includes(query) ||
            subName.includes(query);

          li.hidden = !match;
          if (match) {
            visibleInList += 1;
            visibleInBlock += 1;
          }
        });

        const showList = visibleInList > 0;
        list.hidden = !showList;
        if (subHeading && subHeading.classList.contains("subcategory")) {
          subHeading.hidden = !showList;
        }
      });

      const showBlock = visibleInBlock > 0;
      block.hidden = !showBlock;
      if (showBlock) anyVisible = true;
    });

    if (emptyMsg) emptyMsg.hidden = anyVisible;
    renderBreadcrumbs(null, null, true);
  }

  function filterAndNavigate() {
    applyView();
  }

  // Top category chips: jump within the home structure
  if (categoryNav) {
    categoryNav.querySelectorAll("a[href^='#']").forEach(function (a) {
      a.addEventListener("click", function (e) {
        const href = a.getAttribute("href") || "";
        const id = href.replace(/^#\/?/, "").split("/")[0];
        if (!id || !catalog.has(id)) return;
        e.preventDefault();
        if (input) input.value = "";
        setHash(id, null);
      });
    });
  }

  indexRoot.addEventListener("click", function (e) {
    const link = e.target.closest(".subcategory-nav a");
    if (!link || !indexRoot.contains(link)) return;
    e.preventDefault();
    const href = link.getAttribute("href") || "";
    const m = href.match(/^#([^/]+)\/(.+)$/);
    if (!m) return;
    if (input) input.value = "";
    setHash(m[1], decodeURIComponent(m[2]));
  });

  if (input) {
    input.addEventListener("input", filterAndNavigate);
    input.addEventListener("search", filterAndNavigate);
  }

  window.addEventListener("hashchange", applyView);
  applyView();
})();
