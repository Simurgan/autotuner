import { turnOnModal, injectModal } from "./modals.js";

function winolsClick() {
  injectModal(window.location.origin + "/app/winols_modal/");
  turnOnModal();
}

document
  .getElementById("winols-sidebar-icon")
  .addEventListener("click", winolsClick);