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

    getFileId(file: File): string {
        // We need to ID the files somehow, making them unique by name & last modified date is not the best way to do this
        // Sadly browsers don't keep the original paths of uploaded files
        return file.name + file.lastModified;
    }

    addFile(file: File): boolean {
        const id = this.getFileId(file);
        if (this.fileMap.has(id))
            return false;
        
        this.fileMap.set(id, file);
        this.notifyUpdate();
        return true;
    }

    removeFile(file: File): void {
        const id = this.getFileId(file);
        this.fileMap.delete(id);
        this.notifyUpdate();
    }

    removeFileByName(fileId: string): void {
        let file = this.fileMap.get(fileId);
        if (file)
            this.removeFile(file);
    }

    files = () => this.fileMap.values();


}