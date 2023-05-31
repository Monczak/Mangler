export abstract class SourceFile {
    abstract name(): string;
    abstract id(): string;
}

export class UploadedFile extends SourceFile {
    file: File;
    
    constructor(file: File) {
        super();
        this.file = file;
    }
    
    name(): string {
        return this.file.name;
    }

    id(): string {
        // We need to ID the files somehow, making them unique by name & last modified date is not the best way to do this
        // Sadly browsers don't keep the original paths of uploaded files
        return this.file.name + this.file.lastModified;
    }
}

export class ExampleFile extends SourceFile {
    exampleId: string;
    exampleTitle: string;

    constructor(exampleId: string, exampleTitle: string) {
        super();
        this.exampleId = exampleId;
        this.exampleTitle = exampleTitle;
    }

    name(): string {
        return this.exampleTitle;
    }

    id(): string {
        return this.exampleId;
    }
}