import { IEventHandler } from "@events/eventhandler";
import { Singleton } from "@utils/singleton";


export class ProgressBarController extends Singleton<ProgressBarController>() implements IEventHandler {
    progressBar?: HTMLElement | null;

    constructor() {
        super();
    }
    
    setupEventListeners(): void {
        this.progressBar = document.querySelector("#mangle-progress");
    }

}