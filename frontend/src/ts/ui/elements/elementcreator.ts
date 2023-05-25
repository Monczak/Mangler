export class ElementCreator {
    static createElement<T extends HTMLElement>(parent: Element, id: string, setup: (elem: T) => any): T {
        const elem = <T>document.querySelector(id)?.children[0].cloneNode(true);
        console.log(elem);
        if (elem) {
            setup(elem);
            parent.appendChild(elem);
        }
        
        return elem;
    }
}