import { SeedInputHandler } from "@elements/seedinput";
import { TextAreaHandler } from "@elements/textarea";
import { FileBadgeHandler } from "@elements/filebadges";
import { FilePanelHandler } from "@elements/filepanel";
import { FileDropAreaHandler } from "@elements/filedroparea";

import { FileStorage } from "@files";
import bootstrapSlider from "bootstrap-slider";
import { Tooltip } from "bootstrap";
import { onSubmit } from "@behaviors/submit";
import { ModalController } from "./elements/modalcontroller";
import { ProgressBarController } from "@elements/progressbar";
import { SubmitButtonController } from "@elements/submitcontroller";
import { InputHandler } from "@elements/inputs";

export function setupUI() {
    
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(trigger => new Tooltip(trigger));
    
    for (let handler of [
        SeedInputHandler, 
        TextAreaHandler, 
        FileBadgeHandler, 
        FilePanelHandler,
        FileDropAreaHandler,
        ModalController,
        ProgressBarController,
        SubmitButtonController,
        InputHandler
    ]) {
        let handlerInstance = handler.getInstance();
        handlerInstance.setupEventListeners();
    }

    document.querySelector("#submit-btn")?.addEventListener("click", onSubmit);

    FileStorage.getInstance().registerCallback(files => FileBadgeHandler.getInstance().setFrom(files));
}

