import { EventHandler } from "@events/eventhandler";

export class FilePanelHandler implements EventHandler {
    rotateOn = "rotate-90-right";
    rotateOff = "rotate-none";   

    panelShow = "expanded";
    panelHide = "collapsed";

    panel = document.querySelector("#file-panel");

    onClick(event: MouseEvent): void {
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
    
    setupEventListeners(): void {
        const openBtn = document.querySelector("#open-file-panel-btn");
        openBtn?.addEventListener("click", event => this.onClick(<MouseEvent>event));
        openBtn?.querySelector("i")?.classList.add(this.rotateOff);
        this.panel?.classList.add(this.panelHide);
    }
    
}