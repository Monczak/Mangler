import { IEventHandler } from "@events/eventhandler";
import { Singleton } from "@utils/singleton";


export class ProgressBarController extends Singleton<ProgressBarController>() implements IEventHandler {
    progressBar?: HTMLElement | null;
    progressBarLabel?: HTMLSpanElement | null;

    constructor() {
        super();
    }

    setProgressBarText(text: string) {
        if (this.progressBarLabel) {
            this.progressBarLabel.textContent = text;
        }
    }

    setProgressBarValue(current: number, total: number): void {
        if (this.progressBar) {
            const percentage = Math.round(current / total * 100);
            const noTransition = percentage < parseInt(this.progressBar.getAttribute("aria-valuenow") ?? "0");
            
            if (noTransition) {
                this.progressBar.classList.add("no-transition");
            }
           
            this.progressBar.style.width = `${percentage}%`;
            this.progressBar.setAttribute("aria-valuenow", `${percentage}`);

            if (noTransition) {
                setTimeout(() => this.progressBar?.classList.remove("no-transition"), 100);
            }
        }
        
    }
    
    setupEventListeners(): void {
        this.progressBar = document.querySelector("#mangle-progress");
        this.progressBarLabel = document.querySelector("#mangle-progress-info")
    }

}