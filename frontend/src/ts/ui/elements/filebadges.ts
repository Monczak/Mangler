import { IEventHandler } from "@events/eventhandler";
import { ElementCreator } from "@elements/elementcreator";
import { Singleton } from "utils/singleton";

export class FileBadgeHandler extends Singleton<FileBadgeHandler>() implements IEventHandler {
    constructor() {
        super();
    }
    
    parent = document.querySelector("#file-badge-container") as HTMLElement;
    
    onClick(event: MouseEvent) {
        console.log(this);
        const badge = (event.target as HTMLElement)?.closest(".file-badge");
        if (badge)
            badge.remove();
    }

    createNew(fileName: string) {
        let elem = ElementCreator.createElement<HTMLDivElement>(this.parent, "#file-badge-template", elem => {
            const span = elem.querySelector("span");
            if (span)
                span.textContent = fileName;
        });
        elem.addEventListener("click", event => this.onClick(<MouseEvent>event));
    }

    setFrom(files: Array<File>) {
        while (this.parent.firstChild)
            this.parent.removeChild(this.parent.lastChild as ChildNode);
        
        for (let file of files) {
            this.createNew(file.name)
        }
    }
    
    setupEventListeners() {
        document.querySelectorAll(".file-badge-close-btn").forEach(btn => {
            btn.addEventListener("click", event => this.onClick(<MouseEvent>event));
        });
    }
}