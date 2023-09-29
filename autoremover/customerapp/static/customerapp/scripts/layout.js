import { turnOnModal, turnOffModal, getAndInject } from "./modals.js";

function winolsClick() {
  getAndInject(
    window.location.origin + "/app/winols_modal/",
    undefined,
    undefined,
    turnOnModal
  );
  turnOnModal();
}

document
  .getElementById("winols-sidebar-icon")
  .addEventListener("click", winolsClick);

function profileClick() {
  turnOnModal();
  document.getElementById("profile-card").classList.add("on-screen");

  document
    .getElementById("modal-background")
    .addEventListener("click", turnOffModal);
}

document
  .getElementById("profile-anchor")
  .addEventListener("click", profileClick);
