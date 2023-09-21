import { turnOnModal, getAndInject } from "./modals.js";
import { afterInjection } from "./pricing_modal.js";

function viewButtonClick(event) {
  getAndInject("pricing_modal/", undefined, undefined, afterInjection);
}

document
  .getElementById("view-pricing-button")
  .addEventListener("click", viewButtonClick);
