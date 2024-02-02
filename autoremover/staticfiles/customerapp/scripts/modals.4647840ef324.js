const modal_back = document.getElementById("modal-background");
const profile_card = document.getElementById("profile-card");

function turnOnModal(event) {
  [...document.querySelectorAll("*:not(body):not(html):not(head)")].map(
    (item) => {
      if (
        !modal_back.contains(item) &&
        !profile_card.contains(item) &&
        item.id != "profile-card"
      ) {
        item.classList.add("disable");
        item.classList.add("disable-scroll");
      }
    }
  );

  document.querySelector("body").classList.add("disable-scroll");
  document.getElementById("modal-background").style.display = "flex";
}

function turnOffModal(event) {
  profile_card.classList.remove("on-screen");

  if (
    !(
      event.currentTarget.id == "modal-background" ||
      event.currentTarget.id == "modal-close"
    )
  ) {
    return;
  }
  [...document.querySelectorAll(".disable")].map((item) => {
    item.classList.remove("disable");
    item.classList.remove("disable-scroll");
  });

  document.querySelector("body").classList.remove("disable-scroll");
  document.getElementById("modal-background").style.display = "none";
}

function getAndInject(url, injectInId, preFunc, afterFunc) {
  if (preFunc === undefined) {
    document
      .getElementById("modal-background")
      .addEventListener("click", turnOffModal);
  } else {
    preFunc();
  }

  var id;

  if (injectInId === undefined) {
    id = "modal-background";
  } else {
    id = injectInId;
  }

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById(id).innerHTML = this.responseText;
      if (afterFunc !== undefined) {
        afterFunc();
      }
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}

export { turnOnModal, turnOffModal, getAndInject };
