import { Singleton } from "utils/singleton";

export type FileStorageUpdateCallback = (files: Array<File>) => void;

export class FileStorage extends Singleton<FileStorage>() {    
    private fileSet!: Set<File>;

    private updateCallbacks!: Set<FileStorageUpdateCallback>;

    constructor() {
        super();
        this.fileSet = new Set<File>();
        this.updateCallbacks = new Set<FileStorageUpdateCallback>();
    }

    private notifyUpdate() {
        this.updateCallbacks.forEach(callback => callback([...this.fileSet]));
    } 

    registerCallback(callback: FileStorageUpdateCallback): void {
        this.updateCallbacks.add(callback);
    }

    unregisterCallback(callback: FileStorageUpdateCallback): void {
        this.updateCallbacks.delete(callback);
    }

    addFile(file: File): void {
        // TODO: This doesn't work the way it should (separate objects), need to ID the files somehow
        this.fileSet.add(file);
        this.notifyUpdate();
    }

    removeFile(file: File) : void {
        this.fileSet.delete(file);
        this.notifyUpdate();
    }

    files = () => this.fileSet.entries();


}