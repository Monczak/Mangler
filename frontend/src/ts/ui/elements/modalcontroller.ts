import { Singleton } from "utils/singleton";
import { Modal } from "bootstrap";
import { IEventHandler } from "@events/eventhandler";
import { ErrorBeautifier } from "@uiutils/errorbeautifier";

export class ModalController extends Singleton<ModalController>() implements IEventHandler {    
    private errorModal?: Modal;
    private errorModalElem?: HTMLElement | null;
    
    constructor() {
        super();
    }

    setupEventListeners(): void {
        const errorModalId = "#error-modal";
        this.errorModalElem = document.querySelector(errorModalId);
        this.errorModal = new Modal(errorModalId);
    }

    showErrorModal(error: {code: number, reason: string, details?: string}) {
        const errorText = this.errorModalElem?.querySelector("#error-desc") as HTMLParagraphElement;
        if (errorText)
            errorText.textContent = ErrorBeautifier.beautifyError(error);
        
        this.errorModal?.show();
    }

    
}