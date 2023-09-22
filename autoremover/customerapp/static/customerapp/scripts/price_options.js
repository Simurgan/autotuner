function calculator(event) {
  // re-write this method

  var sum = 0;
  var selecteds = [];

  [...document.querySelectorAll(".price-option-check")].map((item) => {
    if (item.checked) {
      var name = document.getElementById(item.id + "-name-span").innerText;
      var price = Number(
        document.getElementById(item.id + "-price-span").innerText
      );
      var hash = {
        product: name,
        price: price,
      };

      selecteds.push(hash);
      sum += price;
    }
  });

  var ul = document.getElementById("selected-services");

  for (var i = 0; i < ul.children.length - 1; i++) {
    console.log("removing:");
    console.log(ul.firstChild);
    ul.removeChild(ul.firstChild);
  }

  if (sum !== 0) {
    var taxRate =
      Number(document.getElementById("tax-percentage-span").innerText) / 100;

    var tax = sum * taxRate;
    var total = sum + tax;

    document.getElementById("total-amount-span").innerText = total;
    document.getElementById("tax-amount-span").innerText = tax;

    for (const hash of selecteds) {
      var li = document.createElement("li");
      li.classList.add("price-li");

      var inner = `<div class="row apart-children"><span>${hash.product}</span><span>${hash.price}$</span></div>`;
      li.innerHTML = inner;
      if (!ul.contains(li)) {
        console.log("inserting:");
        console.log(li);
        ul.insertBefore(li, ul.firstChild);
      }
      document.getElementById("choice-content").style.display = "block";
      document.getElementById("no-choice-content").style.display = "none";
    }
  } else {
    document.getElementById("choice-content").style.display = "none";
    document.getElementById("no-choice-content").style.display = "block";
  }
}

function calculate(event) {
  var choiceContent = document.getElementById("choice-content");
  var noChoiceContent = document.getElementById("no-choice-content");

  var choiceUl = document.getElementById("selected-services");
  var taxLi = document.getElementById("tax-li");

  if (event.target.checked) {
    choiceContent.style.display = "block";
    noChoiceContent.style.display = "none";

    var newName = document.getElementById(
      event.target.id + "-name-span"
    ).innerText;
    var newAmount = Number(
      document.getElementById(event.target.id + "-price-span").innerText
    );

    var li = document.createElement("li");
    li.classList.add("price-li");
    li.id = event.target.id + "-li";

    li.innerHTML = `<div class="row apart-children"><span>${newName}</span><div><span class="price-span">${newAmount}</span>$</div></div>`;

    choiceUl.insertBefore(li, taxLi);

    let sum = 0;
    [...document.querySelectorAll(".price-span")].map((item) => {
      sum += Number(item.innerText);
    });
    let taxRate =
      Number(document.getElementById("tax-percentage-span").innerText) / 100;
    let newTax = sum * taxRate;
    document.getElementById("tax-amount-span").innerText = newTax;
    document.getElementById("total-amount-span").innerText = sum + newTax;
  } else {
    let oldLi = document.getElementById(event.target.id + "-li");
    choiceUl.removeChild(oldLi);

    let sum = 0;
    [...document.querySelectorAll(".price-span")].map((item) => {
      sum += Number(item.innerText);
    });

    if (sum !== 0) {
      let taxRate =
        Number(document.getElementById("tax-percentage-span").innerText) / 100;
      let newTax = sum * taxRate;
      document.getElementById("tax-amount-span").innerText = newTax;
      document.getElementById("total-amount-span").innerText = sum + newTax;
    } else {
      choiceContent.style.display = "none";
      noChoiceContent.style.display = "block";
    }
  }
}

function openCalculator() {
  document.getElementById("calculator-box").style.display = "flex";
  [...document.querySelectorAll(".price-option-check")].map((item) => {
    item.addEventListener("change", calculate);
  });
}
export { openCalculator };
