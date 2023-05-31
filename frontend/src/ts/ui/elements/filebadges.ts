import { IEventHandler } from "@events/eventhandler";
import { ElementCreator } from "@elements/elementcreator";
import { Singleton } from "utils/singleton";
import { FileStorage } from "filestorage";
import { SourceFile } from "sourcefile";

export class FileBadgeHandler extends Singleton<FileBadgeHandler>() implements IEventHandler {
    badgeFileIds: Map<HTMLElement, string>;
    
    parent = document.querySelector("#file-badge-container") as HTMLElement;

    constructor() {
        super();

        this.badgeFileIds = new Map<HTMLElement, string>();
    }
    
    onClick(event: MouseEvent) {
        const badge = (event.target as HTMLElement)?.closest(".file-badge") as HTMLElement;
        if (badge)
            this.removeBadge(badge);
    }

    createNew(file: SourceFile): void {
        let elem = ElementCreator.createElement<HTMLDivElement>(this.parent, "#file-badge-template", elem => {
            const span = elem.querySelector("span");
            if (span)
                span.textContent = file.name();
        });
        elem.addEventListener("click", event => this.onClick(<MouseEvent>event));

        this.badgeFileIds.set(elem, file.id());
    }

    removeBadge(badge: HTMLElement): void {
        let fileName = this.badgeFileIds.get(badge);
        if (fileName) {
            FileStorage.getInstance().removeFileByName(fileName);
            this.badgeFileIds.delete(badge);
            badge.remove();
        }
    }

    setFrom(files: Array<SourceFile>): void {
        while (this.parent.firstChild)
            this.parent.removeChild(this.parent.lastChild as ChildNode);
        
        for (let file of files) {
            this.createNew(file);
        }

        const noFilesUploadedText = document.querySelector("#no-files-uploaded-text") as HTMLElement;
        if (files.length > 0)
            noFilesUploadedText.classList.add("display-none");
        else
            noFilesUploadedText.classList.remove("display-none");

    }
    
    setupEventListeners(): void {
        document.querySelectorAll(".file-badge-close-btn").forEach(btn => {
            btn.addEventListener("click", event => this.onClick(<MouseEvent>event));
        });
    }
}