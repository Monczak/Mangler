import { IEventHandler } from "@events/eventhandler";
import { Singleton } from "@utils/singleton";

export class SubmitButtonController extends Singleton<SubmitButtonController>() implements IEventHandler {
    private submitBtn?: HTMLButtonElement | null;

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

    setupEventListeners(): void {
        this.submitBtn = document.querySelector("#submit-btn") as HTMLButtonElement;
    }
}