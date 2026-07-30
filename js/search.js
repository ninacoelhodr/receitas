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
      const lists = block.querySelectorAll(".recipe-list");
      let visibleInBlock = 0;

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
            li.hidden = Boolean(query);
            return;
          }

          const recipeName = normalize(li.textContent || "");
          const match =
            !query ||
            recipeName.includes(query) ||
            categoryName.includes(query) ||
            subName.includes(query);

          li.hidden = !match;
          if (match) {
            visibleInList += 1;
            visibleInBlock += 1;
          }
        });

        const showList = query ? visibleInList > 0 : true;
        list.hidden = !showList;
        if (subHeading && subHeading.classList.contains("subcategory")) {
          subHeading.hidden = !showList;
        }
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
