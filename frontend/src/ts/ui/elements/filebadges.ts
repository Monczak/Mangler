import { EventHandler } from "@events/eventhandler";
import { ElementCreator } from "@elements/elementcreator";

export class FileBadgeHandler implements EventHandler {
    onClick(event: MouseEvent) {
        const badge = (event.target as HTMLElement)?.closest(".file-badge");
        if (badge)
            badge.remove();
    }

    createNew(fileName: string) {
        const parent = document.querySelector("#file-badge-container");
        if (parent) {
            ElementCreator.createElement<HTMLDivElement>(parent, "#file-badge-template", elem => {
                const span = elem.querySelector("span");
                if (span)
                    span.textContent = fileName;
            });
        }
    }
    
    setupEventListeners() {
        document.querySelectorAll(".file-badge-close-btn").forEach(btn => {
            btn.addEventListener("click", event => this.onClick(<MouseEvent>event));
        });
    }
}