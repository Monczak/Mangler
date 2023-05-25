import { Utils } from "@utils";
import { setupEventListeners } from "@events";

function test() {
    console.log("test")
    Utils.setupFileInputs()
}

setupEventListeners();

console.log("Hello");