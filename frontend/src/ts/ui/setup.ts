import { SeedInputHandler } from "@elements/seedinput";
import { TextAreaHandler } from "@elements/textarea";
import { FileBadgeHandler } from "@elements/filebadges";
import { FilePanelHandler } from "@elements/filepanel";
import { FileDropAreaHandler } from "@elements/filedroparea";

import { FileStorage } from "filestorage";

export function setupEventListeners() {
    for (let handler of [
        SeedInputHandler, 
        TextAreaHandler, 
        FileBadgeHandler, 
        FilePanelHandler,
        FileDropAreaHandler
    ]) {
        let handlerInstance = handler.getInstance();
        handlerInstance.setupEventListeners();
    }

    console.log(FileBadgeHandler.getInstance());
    FileStorage.getInstance().registerCallback(files => FileBadgeHandler.getInstance().setFrom(files));
}

