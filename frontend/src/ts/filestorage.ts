export type FileStorageUpdateCallback = (files: Array<File>) => void;

export class FileStorage {
    private static instance: FileStorage; 
    
    private fileSet!: Set<File>;

    private updateCallbacks!: Set<FileStorageUpdateCallback>;

    constructor() {
        if (FileStorage.instance)
            return FileStorage.instance;
        
        FileStorage.instance = this;

        this.fileSet = new Set<File>();
        this.updateCallbacks = new Set<FileStorageUpdateCallback>();
    }

    static getInstance() {
        if (!FileStorage.instance)
            FileStorage.instance = new FileStorage();
        return FileStorage.instance;
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