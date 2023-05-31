import { IEventHandler } from "@events/eventhandler";
import { FileStorage } from "filestorage";
import { Singleton } from "utils/singleton";

export class FileDropAreaHandler extends Singleton<FileDropAreaHandler>() implements IEventHandler {
    constructor() {
        super();
    }

    preventDefault(event: Event): void {
        event.preventDefault();
        event.stopPropagation();
    }

    eventHandlers(area: HTMLElement): void {
        ["dragenter", "dragover", "dragleave", "drop"].forEach(event => {
            area.addEventListener(event, this.preventDefault, false);
            document.body.addEventListener(event, this.preventDefault, false);
        })

        area.addEventListener("drop", event => this.handleDrop(event));
    }

    handleDrop(event: DragEvent) {
        if (event.dataTransfer) {
            for (let file of event.dataTransfer.files) {
                console.log(FileStorage.getInstance().addUploadedFile(file));
            }
        }
    }
    
    setupEventListeners(): void {
        const areas = document.querySelectorAll(".file-drop-area");
        areas.forEach(area => this.eventHandlers(<HTMLElement>area));
    }
}