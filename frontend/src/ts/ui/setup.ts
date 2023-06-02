import { SeedInputHandler } from "@elements/seedinput";
import { TextAreaHandler } from "@elements/textarea";
import { FileBadgeHandler } from "@elements/filebadges";
import { FilePanelHandler } from "@elements/filepanel";
import { FileDropAreaHandler } from "@elements/filedroparea";

import { FileStorage } from "@files";
import bootstrapSlider from "bootstrap-slider";
import { Tooltip, Modal } from "bootstrap";
import { onSubmit } from "@behaviors/submit";
import { ModalController } from "./elements/modalcontroller";

export function setupUI() {
    
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(trigger => new Tooltip(trigger));

    const trainDepthsSlider = new bootstrapSlider("#train-depths", {
        id: "slider-train-depths",
        min: 1,
        max: 10,
        range: true,
        value: [1, 3],
    });
    const genDepthSlider = new bootstrapSlider("#gen-depth", {
        id: "slider-gen-depth",
        min: 1,
        max: 10,
        value: 3,
    });
    const temperature = new bootstrapSlider("#temperature", {
        id: "slider-temperature",
        min: -5,
        max: 5,
        value: 1,
        step: 0.05,
    });
    
    for (let handler of [
        SeedInputHandler, 
        TextAreaHandler, 
        FileBadgeHandler, 
        FilePanelHandler,
        FileDropAreaHandler,
        ModalController
    ]) {
        let handlerInstance = handler.getInstance();
        handlerInstance.setupEventListeners();
    }

    document.querySelector("#submit-btn")?.addEventListener("click", onSubmit);

    FileStorage.getInstance().registerCallback(files => FileBadgeHandler.getInstance().setFrom(files));
}

