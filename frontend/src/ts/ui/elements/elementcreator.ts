import { Singleton } from "utils/singleton";

export class ElementCreator extends Singleton<ElementCreator>() {
    constructor() {
        super();
    }
    
    static createElement<T extends HTMLElement>(parent: Element, id: string, setup: (elem: T) => any): T {
        const elem = <T>document.querySelector(id)?.children[0].cloneNode(true);
        if (elem) {
            setup(elem);
            parent.appendChild(elem);
        }
        
        return elem;
    }
}
