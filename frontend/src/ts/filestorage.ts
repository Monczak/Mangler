import { Singleton } from "utils/singleton";
import { ExampleFile, SourceFile, UploadedFile } from "sourcefile";

export type FileStorageUpdateCallback = (files: Array<SourceFile>) => void;

export class FileStorage extends Singleton<FileStorage>() {    
    private fileMap!: Map<string, SourceFile>;    // TODO: Support examples somehow

    private updateCallbacks!: Set<FileStorageUpdateCallback>;

    constructor() {
        super();
        this.fileMap = new Map<string, SourceFile>();
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

    addUploadedFile(file: File): boolean {
        const uploadedFile = new UploadedFile(file);
        const id = uploadedFile.id();
        if (this.fileMap.has(id))
            return false;
        
        this.fileMap.set(id, uploadedFile);
        this.notifyUpdate();
        return true;
    }

    addExampleFile(id: string, title: string): boolean {
        const uploadedFile = new ExampleFile(id, title);
        if (this.fileMap.has(id))
            return false;
        
        this.fileMap.set(id, uploadedFile);
        this.notifyUpdate();
        return true;
    }

    removeFile(file: SourceFile): void {
        const id = file.id();
        this.fileMap.delete(id);
        this.notifyUpdate();
    }

    removeFileByName(fileId: string): void {
        const file = this.fileMap.get(fileId);
        if (file)
            this.removeFile(file);
    }

    files = () => this.fileMap.values();


}