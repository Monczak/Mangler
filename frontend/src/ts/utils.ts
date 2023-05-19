export class Utils {
    static setupFileInputs() {
        document.querySelectorAll(".file-input").forEach((elem) => {
            elem.addEventListener("change", () => {
                let fileInput = <HTMLInputElement>elem;
        
                const fileCount = fileInput.files?.length ?? 0;
                const textbox = fileInput.previousElementSibling;
        
                console.log(fileCount);
            })
        });
    }

    static findElement(node: Node): HTMLElement | null {
        let targetElement: HTMLElement | null = null;
        let currentNode: Node | null = node;

        while (currentNode && !targetElement) {
            if (currentNode instanceof HTMLElement) {
                targetElement = currentNode;
                break;
            }
            currentNode = currentNode.parentNode;
        }

        return targetElement;
    }

    static selectElemText(elem: HTMLElement) {
        let selection = window.getSelection();
        let range = document.createRange();
        range.selectNodeContents(elem);
        selection?.removeAllRanges();
        selection?.addRange(range);
    }

    static setCaretPosition(elem: HTMLElement, pos: number = -1) {        
        let selection = window.getSelection();
        let range = document.createRange();
        
        let node = elem.lastChild;
        if (node)
            range.setStart(node, node.textContent ? (pos == -1 ? node.textContent.length - 1 : pos) : 0);
        range.collapse(true);

        selection?.removeAllRanges();
        selection?.addRange(range);
    }
}