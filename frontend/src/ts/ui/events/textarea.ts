import { Utils } from "@utils";

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
        if (span.children.length == 2 && 
            span.children[0].tagName === "BR" && 
            span.children[1].tagName === "BR" &&
            span.textContent?.trim() === "")
            span.innerHTML = "";
    }
}

export function setupEventListeners() {
    const textArea = document.querySelector("#text-area");
    textArea?.addEventListener("keydown", event => onTextAreaKeyDown(<KeyboardEvent>event));
}