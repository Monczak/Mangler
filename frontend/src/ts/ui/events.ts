import { Utils } from "../utils";

function onSeedTextChanged(elem: HTMLElement) {
    if (elem.textContent?.trim() === "")
        elem.classList.add("empty-span");
    else
        elem.classList.remove("empty-span");
}

function onSeedTextFocusedOut(elem: HTMLElement) {

}

function onSeedTextDoubleClicked(elem: HTMLElement) {
    Utils.selectElemText(elem);
}

function onTextAreaClicked(elem: HTMLElement) {
    const seedInput = document.querySelector("#seed-input") as HTMLElement;
    if (seedInput) {
        seedInput.focus();
        Utils.selectElemText(seedInput);
    }
}

function onTextAreaKeyDown(event: KeyboardEvent) {
    const span: HTMLSpanElement = event.target as HTMLSpanElement;

    if (event.key === "Enter") {
        if (span.innerHTML === "") {
            event.preventDefault();
            span.appendChild(document.createElement("br"));   
            span.appendChild(document.createElement("br"));

            Utils.setCaretPosition(span, -1);
        }
    }
    else if (event.key === "Backspace" || event.key === "Delete") {
        if (span.children.length == 2 && span.children[0].tagName === "BR" && span.children[1].tagName === "BR")
            span.innerHTML = "";
    }
}

export function setupEventListeners() {
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
                onSeedTextChanged(elem);
        }
    })

    const config = { characterData: true, subtree: true, childList: true };

    const seedInput = document.querySelector("#seed-input");
    if (seedInput) {
        seedInputObserver.observe(seedInput, config);
        seedInput.addEventListener("dblclick", event => onSeedTextDoubleClicked(<HTMLElement>event.target));
        seedInput.addEventListener("focusout", event => onSeedTextFocusedOut(<HTMLElement>event.target))
    }

    const textArea = document.querySelector("#text-area");
    textArea?.addEventListener("keydown", event => onTextAreaKeyDown(<KeyboardEvent>event));
}

