import { EventHandler } from "@events/eventhandler";

export class FileDropAreaHandler implements EventHandler {
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
        console.log(event.dataTransfer?.files);
    }
    
    setupEventListeners(): void {
        const areas = document.querySelectorAll(".file-drop-area");
        areas.forEach(area => this.eventHandlers(<HTMLElement>area));
    }
}