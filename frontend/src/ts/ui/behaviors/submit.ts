import { TextAreaHandler } from "@elements/textarea";
import { FileStorage } from "@files";
import { ExampleFile } from "@files/sourcefile"
import { RequestManager } from "@requests";
import { ErrorResponse, StatusAnalyzingResponse, StatusGeneratingResponse, StatusSuccessResponse, StatusFailureResponse } from "@requests/responses";

export async function onSubmit() {
    if (FileStorage.getInstance().filesChanged) {
        FileStorage.getInstance().resetFilesChanged();
        await RequestManager.getInstance().upload([...FileStorage.getInstance().files()]);
    }
    await generateText();
}

async function generateText() {
    const [minTrainDepth, maxTrainDepth] = [...document.querySelectorAll("#slider-train-depths .slider-handle")]
        .map(elem => elem.getAttribute("aria-valuenow"))
        .sort()
        .map(n => n ? parseInt(n) : -1);
    const trainDepths = Array.from(Array(maxTrainDepth - minTrainDepth + 1), (v, k) => k + minTrainDepth);
    const genDepth = parseInt(document.querySelector("#slider-gen-depth .slider-handle")?.getAttribute("aria-valuenow") ?? "-1");
    const temperature = parseFloat(document.querySelector("#slider-temperature .slider-handle")?.getAttribute("aria-valuenow") ?? "1");

    const seed = document.querySelector("#seed-input")?.textContent ?? "";

    const exampleIds = FileStorage.getInstance().files()
        .filter(file => file instanceof ExampleFile)
        .map(file => file.id());

    console.log(FileStorage.getInstance().files());
    
    const response = await RequestManager.getInstance().generateText(trainDepths, genDepth, seed, temperature, exampleIds);
    const taskId = response.taskId;

    let notFoundAttempts = 10;

    const pollStatus = async (onSuccess?: (taskId: string) => any, onFailure?: (response: StatusFailureResponse) => any) => {
        const status = await RequestManager.getInstance().pollStatus(taskId);
        console.log(`${status instanceof StatusSuccessResponse} ${JSON.stringify(status)}`);

        if (status instanceof StatusSuccessResponse) {
            if (onSuccess) await onSuccess(taskId);
            return;
        }
        if (status instanceof StatusFailureResponse) {
            if (onFailure) await onFailure(status);
            return;
        }

        if (status instanceof StatusAnalyzingResponse || status instanceof StatusGeneratingResponse || status == null) {
            if (status == null && --notFoundAttempts < 0)
                throw new Error("Attempted to poll status for a non-existent ID")
            setTimeout(async () => pollStatus(onSuccess, onFailure), 500);
        }
    }

    await pollStatus(async taskId => {
        TextAreaHandler.getInstance().setGeneratedText(await RequestManager.getInstance().retrieveText(taskId));
    });
}