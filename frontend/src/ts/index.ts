import { Utils } from "@utils";
import { setupEventListeners } from "ui/setup";
import { Tooltip } from "bootstrap";

function test() {
    console.log("test")
    Utils.setupFileInputs()
}

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(trigger => new Tooltip(trigger));

setupEventListeners();

console.log("Hello");