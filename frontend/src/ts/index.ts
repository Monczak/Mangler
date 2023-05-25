import { Utils } from "@utils";
import { setupEventListeners } from "ui/setup";

function test() {
    console.log("test")
    Utils.setupFileInputs()
}

setupEventListeners();

console.log("Hello");