(function () {
  function layoutRecipeCard(card) {
    if (card.dataset.layoutDone === "1") return;

    var ingredients = card.querySelector(":scope > .ingredients");
    var steps = card.querySelector(":scope > .steps");
    if (!ingredients || !steps) return;

    var ingHeading = ingredients.previousElementSibling;
    var stepsHeading = steps.previousElementSibling;
    if (
      !ingHeading ||
      ingHeading.tagName !== "H2" ||
      !stepsHeading ||
      stepsHeading.tagName !== "H2"
    ) {
      return;
    }

    var body = document.createElement("div");
    body.className = "recipe-body";

    var left = document.createElement("section");
    left.className = "recipe-section";

    var right = document.createElement("section");
    right.className = "recipe-section";

    // Insere o bloco ANTES de mover os títulos, senão ele fica solto fora da página.
    ingHeading.before(body);
    body.append(left, right);
    left.append(ingHeading, ingredients);
    right.append(stepsHeading, steps);
    card.dataset.layoutDone = "1";
  }

  document.querySelectorAll(".recipe-card").forEach(layoutRecipeCard);
})();
