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
}

