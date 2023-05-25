import { Utils } from "@utils";
import { EventHandler } from "@events/eventhandler";

export class SeedInputHandler implements EventHandler {
    onChanged(elem: HTMLElement) {
        if (elem.textContent?.trim() === "")
            elem.classList.add("empty-span");
        else
            elem.classList.remove("empty-span");
    }
    
    onFocusedOut(elem: HTMLElement) {
    
    }
    
    onDoubleClicked(elem: HTMLElement) {
        Utils.selectElemText(elem);
    }
    
    setupEventListeners() {
        const seedInputObserver = new MutationObserver(mutations => {
            for (let mutation of mutations) {
                let elem: HTMLElement | null = null;
                switch (mutation.type) {
                    case "childList":
                        elem = mutation.target as HTMLElement;
                        break;
                    case "characterData":
                        elem = mutation.target.parentElement as HTMLElement;
                        break;
                    default:
                        break;
                }
                if (elem)
                    this.onChanged(elem);
            }
        })
    
        const config = { characterData: true, subtree: true, childList: true };
    
        const seedInput = document.querySelector("#seed-input");
        if (seedInput) {
            seedInputObserver.observe(seedInput, config);
            seedInput.addEventListener("dblclick", event => this.onDoubleClicked(<HTMLElement>event.target));
            seedInput.addEventListener("focusout", event => this.onFocusedOut(<HTMLElement>event.target))
    
            seedInput.addEventListener('copy', function (event) {
                event.preventDefault();
    
                const span: HTMLSpanElement = event.target as HTMLSpanElement;
                const text = span.innerText;
                (<ClipboardEvent>event).clipboardData?.setData('text/plain', text);
            });
    
            seedInput.addEventListener('paste', function (event) {
                event.preventDefault();
                const text = (<ClipboardEvent>event).clipboardData?.getData('text/plain') ?? "";
                document.getSelection()?.deleteFromDocument();
                const range = document.getSelection()?.getRangeAt(0);
                if (range) {
                    range.insertNode(document.createTextNode(text));
                    range.collapse(false);
                }
            });
        }
    }
}

