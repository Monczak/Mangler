import { IEventHandler } from "@events/eventhandler";
import { Singleton } from "@utils/singleton";
import { Tooltip } from "bootstrap";

export class SubmitButtonController extends Singleton<SubmitButtonController>() implements IEventHandler {
    private submitBtn?: HTMLButtonElement | null;
    private tooltipContainer?: HTMLElement | null;

    private forceDisable: boolean = false;
    private enabled: boolean = true;

    private enable(): void {
        this.submitBtn?.classList.remove("disabled");
    }

    private disable(): void {
        this.submitBtn?.classList.add("disabled");
    }

    private update(): void {
        if (!this.enabled || this.forceDisable) this.disable();
        else this.enable();
    }
    
    setEnabled(enabled: boolean): void {
        if (this.submitBtn && !this.forceDisable) {
            this.enabled = enabled;
            this.update();
        }
    }

    forceDisabled(disabled: boolean): void {
        this.forceDisable = disabled;
        this.update();
    }

    setTooltipText(text: string): void {
        if (this.tooltipContainer) {
            this.tooltipContainer.setAttribute("title", text);
            this.tooltipContainer.setAttribute("data-bs-original-title", text);

            // Need to recreate the tooltip to refresh the text in Bootstrap
            const newTooltip = new Tooltip(this.tooltipContainer);
        }
    }

    setupEventListeners(): void {
        this.submitBtn = document.querySelector("#submit-btn") as HTMLButtonElement;
        this.tooltipContainer = document.querySelector(".submit-btn-tooltip") as HTMLElement;
    }
}