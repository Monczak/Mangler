import { IEventHandler } from "@events/eventhandler";
import { ElementCreator } from "@elements/elementcreator";
import { Singleton } from "utils/singleton";
import { FileStorage } from "filestorage";

export class FileBadgeHandler extends Singleton<FileBadgeHandler>() implements IEventHandler {
    badgeFileNames: Map<HTMLElement, string>;
    
    parent = document.querySelector("#file-badge-container") as HTMLElement;

    constructor() {
        super();

        this.badgeFileNames = new Map<HTMLElement, string>();
    }
    
    onClick(event: MouseEvent) {
        const badge = (event.target as HTMLElement)?.closest(".file-badge") as HTMLElement;
        if (badge)
            this.removeBadge(badge);
    }

    createNew(fileName: string): void {
        let elem = ElementCreator.createElement<HTMLDivElement>(this.parent, "#file-badge-template", elem => {
            const span = elem.querySelector("span");
            if (span)
                span.textContent = fileName;
        });
        elem.addEventListener("click", event => this.onClick(<MouseEvent>event));

        this.badgeFileNames.set(elem, fileName);
    }

    removeBadge(badge: HTMLElement): void {
        let fileName = this.badgeFileNames.get(badge);
        if (fileName) {
            FileStorage.getInstance().removeFileByName(fileName);
            this.badgeFileNames.delete(badge);
            badge.remove();
        }
    }

    setFrom(files: Array<File>): void {
        while (this.parent.firstChild)
            this.parent.removeChild(this.parent.lastChild as ChildNode);
        
        for (let file of files) {
            this.createNew(file.name)
        }
    }
    
    setupEventListeners(): void {
        document.querySelectorAll(".file-badge-close-btn").forEach(btn => {
            btn.addEventListener("click", event => this.onClick(<MouseEvent>event));
        });
    }
}