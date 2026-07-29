(function () {
  const input = document.getElementById("recipe-search");
  const emptyMsg = document.getElementById("search-empty");
  const blocks = document.querySelectorAll(".category-block");

  if (!input || !blocks.length) return;

  function normalize(text) {
    return text
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .trim();
  }

  function filterRecipes() {
    const query = normalize(input.value);
    let anyVisible = false;

    blocks.forEach(function (block) {
      const categoryName = normalize(block.querySelector("h2")?.textContent || "");
      const items = block.querySelectorAll(".recipe-list > li");
      let visibleInBlock = 0;

      items.forEach(function (li) {
        if (li.classList.contains("empty")) {
          li.hidden = Boolean(query);
          return;
        }

        const recipeName = normalize(li.textContent || "");
        const match =
          !query ||
          recipeName.includes(query) ||
          categoryName.includes(query);

        li.hidden = !match;
        if (match) visibleInBlock += 1;
      });

      const showBlock = query ? visibleInBlock > 0 : true;
      block.hidden = !showBlock;
      if (showBlock && (visibleInBlock > 0 || !query)) anyVisible = true;
    });

    if (emptyMsg) {
      emptyMsg.hidden = !query || anyVisible;
    }
  }

  input.addEventListener("input", filterRecipes);
  input.addEventListener("search", filterRecipes);
})();
