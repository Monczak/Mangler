import { SeedInputHandler } from "@elements/seedinput";
import { TextAreaHandler } from "@elements/textarea";
import { FileBadgeHandler } from "@elements/filebadges";
import { FilePanelHandler } from "@elements/filepanel";
import { FileDropAreaHandler } from "@elements/filedroparea";

export function setupEventListeners() {
    for (let handler of [
        SeedInputHandler, 
        TextAreaHandler, 
        FileBadgeHandler, 
        FilePanelHandler,
        FileDropAreaHandler
    ]) {
        let handlerInstance = new handler();
        
        if (handlerInstance instanceof FileBadgeHandler) {
            handlerInstance.createNew("blah");
        }

        handlerInstance.setupEventListeners();
    }
}

