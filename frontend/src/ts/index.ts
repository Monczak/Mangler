import { Utils } from "./utils";
import { setupEventListeners } from "./ui/events";

function test() {
    console.log("test")
    Utils.setupFileInputs()
}

setupEventListeners();

console.log("Hello");