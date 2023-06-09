import { IEventHandler } from "@events/eventhandler";
import { FileStorage } from "@files";
import { Singleton } from "utils/singleton";

export class FilePanelHandler extends Singleton<FilePanelHandler>() implements IEventHandler {
    constructor() {
        super();
    }
    
    rotateOn = "rotate-90-right";
    rotateOff = "rotate-none";   

    panelShow = "expanded";
    panelHide = "collapsed";

    panel = document.querySelector("#file-panel");
    examplesDropdownBtn = document.querySelector("#dropdown-examples");

    onOpenBtnClick(event: MouseEvent): void {
        const icon = <HTMLElement>(<HTMLButtonElement>event.target).firstChild;

        if (icon) {
            if (icon.classList.contains(this.rotateOn)) {
                icon.classList.replace(this.rotateOn, this.rotateOff);
                this.panel?.classList.replace(this.panelShow, this.panelHide);
                this.panel?.classList.remove("overflow-visible");
            }
            else {
                icon.classList.replace(this.rotateOff, this.rotateOn);
                this.panel?.classList.replace(this.panelHide, this.panelShow);
            }
        }
    }

    onExamplesDropdownClick(event: MouseEvent): void {
        const btn = <HTMLButtonElement>event.target;
        if (btn.getAttribute("aria-expanded") === "true") {
            this.panel?.classList.add("overflow-visible");
        }
        else {
            this.panel?.classList.remove("overflow-visible");
        }
    }

    onFileInputChange(event: Event): void {
        const target = event.target as HTMLInputElement;
        if (target && target.files) {
            for (let file of target.files) {
                FileStorage.getInstance().addUploadedFile(file);
            }
            target.value = "";  // Remove all files from the input
        }
    }

    onExampleItemClick(event: MouseEvent): void {
        const target = (event.target as HTMLElement).closest(".example-item");
        if (target) {
            const id = target.attributes.getNamedItem("data-example-id")?.value;
            const title = target.attributes.getNamedItem("data-example-title")?.value;
            if (id && title)
                FileStorage.getInstance().addExampleFile(id, title);
        }
    }
    
    setupEventListeners(): void {
        const openBtn = document.querySelector("#open-file-panel-btn");
        openBtn?.addEventListener("click", event => this.onOpenBtnClick(<MouseEvent>event));
        openBtn?.querySelector("i")?.classList.add(this.rotateOff);
        this.panel?.classList.add(this.panelHide);

        this.examplesDropdownBtn?.addEventListener("click", event => this.onExamplesDropdownClick(<MouseEvent>event));

        const fileInput = document.querySelector("#upload-file-input");
        fileInput?.addEventListener("change", event => this.onFileInputChange(event))

        const exampleItems = document.querySelectorAll(".example-item");
        exampleItems.forEach(item => item.addEventListener("click", event => this.onExampleItemClick(<MouseEvent>event)));
    }
    
}