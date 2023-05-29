import { EventHandler } from "@events/eventhandler";

export class FilePanelHandler implements EventHandler {
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
    
    setupEventListeners(): void {
        const openBtn = document.querySelector("#open-file-panel-btn");
        openBtn?.addEventListener("click", event => this.onOpenBtnClick(<MouseEvent>event));
        openBtn?.querySelector("i")?.classList.add(this.rotateOff);
        this.panel?.classList.add(this.panelHide);

        this.examplesDropdownBtn?.addEventListener("click", event => this.onExamplesDropdownClick(<MouseEvent>event));
    }
    
}