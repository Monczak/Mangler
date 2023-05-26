import { SeedInputHandler } from "@elements/seedinput";
import { TextAreaHandler } from "@elements/textarea";
import { FileBadgeHandler } from "@elements/filebadges";
import { FilePanelHandler } from "@elements/filepanel";

export function setupEventListeners() {
    for (let handler of [SeedInputHandler, TextAreaHandler, FileBadgeHandler, FilePanelHandler]) {
        let handlerInstance = new handler();
        
        if (handlerInstance instanceof FileBadgeHandler) {
            handlerInstance.createNew("blah");
        }

        handlerInstance.setupEventListeners();
    }
}

