import { Singleton } from "@utils/singleton";
import { SourceFile, UploadedFile } from "@files/sourcefile";

export class RequestManager extends Singleton<RequestManager>() {
    private _inputId: string | undefined;
    public get inputId(): string | undefined {
        return this._inputId;
    }
    private set inputId(value: string | undefined) {
        this._inputId = value;
    }

    async upload(files: Array<SourceFile>) {
        const uploadedFiles = files.filter(file => file instanceof UploadedFile) as Array<UploadedFile>;
        
        const formData = new FormData();
        for (let [i, file] of uploadedFiles.entries()) {
            formData.append(`file${i}`, file.file);
        }

        const response = await fetch("api/upload", {
            method: "POST",
            body: formData
        });
        const json = await response.json();
        this.inputId = json.id;
    }

    async generateText(trainDepths: Array<number>, genDepth: number, seed: string, temperature: number, examples?: Array<string>) {        
        let payload = {
            input_id: this.inputId,
            train_depths: trainDepths, 
            gen_depth: genDepth, 
            seed: seed, 
            temperature: temperature, 
            examples: examples ?? []
        };
        
        const response = await fetch("api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
        const json = await response.json();
        console.log(json);
    }
}