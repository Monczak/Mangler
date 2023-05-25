import { setupEventListeners as setupSeedInput } from "@events/seedinput";
import { setupEventListeners as setupTextArea } from "@events/textarea";

export function setupEventListeners() {
    setupSeedInput();
    setupTextArea();
}

