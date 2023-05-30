import { Singleton } from "utils/singleton";

export type FileStorageUpdateCallback = (files: Array<File>) => void;

export class FileStorage extends Singleton<FileStorage>() {    
    private fileMap!: Map<string, File>;

    private updateCallbacks!: Set<FileStorageUpdateCallback>;

    constructor() {
        super();
        this.fileMap = new Map<string, File>();
        this.updateCallbacks = new Set<FileStorageUpdateCallback>();
    }

    private notifyUpdate() {
        this.updateCallbacks.forEach(callback => callback([...this.files()]));
    } 

    registerCallback(callback: FileStorageUpdateCallback): void {
        this.updateCallbacks.add(callback);
    }

    unregisterCallback(callback: FileStorageUpdateCallback): void {
        this.updateCallbacks.delete(callback);
    }

    addFile(file: File): boolean {
        if (this.fileMap.has(file.name))
            return false;
        
        this.fileMap.set(file.name, file);
        this.notifyUpdate();
        return true;
    }

    removeFile(file: File): void {
        console.log(file);
        this.fileMap.delete(file.name);
        this.notifyUpdate();
    }

    removeFileByName(fileName: string): void {
        let file = this.fileMap.get(fileName);
        if (file)
            this.removeFile(file);
    }

    files = () => this.fileMap.values();


}