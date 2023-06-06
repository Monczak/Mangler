import { ModalController } from "@elements/modalcontroller";
import { ProgressBarController } from "@elements/progressbar";
import { SubmitButtonController } from "@elements/submitcontroller";
import { TextAreaHandler } from "@elements/textarea";
import { FileStorage } from "@files";
import { ExampleFile } from "@files/sourcefile"
import { RequestManager } from "@requests";
import { StatusAnalyzingResponse, StatusGeneratingResponse, StatusSuccessResponse, StatusFailureResponse, StatusResponse } from "@requests/responses";

const pollingInterval = 200;
const pollAttempts = 20;

export async function onSubmit() {
    TextAreaHandler.getInstance().setOverlayVisible(true);
    ProgressBarController.getInstance().setProgressBarValue(0, 1);

    SubmitButtonController.getInstance().forceDisabled(true);
    
    if (FileStorage.getInstance().filesChanged) {
        FileStorage.getInstance().resetFilesChanged();
        await RequestManager.getInstance().upload([...FileStorage.getInstance().files()]);
    }
    await generateText();
}

async function generateText() {
    const [minTrainDepth, maxTrainDepth] = [...document.querySelectorAll("#slider-train-depths .slider-handle")]
        .map(elem => elem.getAttribute("aria-valuenow"))
        .map(n => n ? parseInt(n) : -1)
        .sort((a: number, b: number) => a - b);
    console.log([minTrainDepth, maxTrainDepth])
    const trainDepths = Array.from(Array(maxTrainDepth - minTrainDepth + 1), (v, k) => k + minTrainDepth);
    const genDepth = parseInt(document.querySelector("#slider-gen-depth .slider-handle")?.getAttribute("aria-valuenow") ?? "-1");
    const temperature = parseFloat(document.querySelector("#slider-temperature .slider-handle")?.getAttribute("aria-valuenow") ?? "1");

    const seed = document.querySelector("#seed-input")?.textContent ?? "";

    const exampleIds = FileStorage.getInstance().files()
        .filter(file => file instanceof ExampleFile)
        .map(file => file.id());
    
    const response = await RequestManager.getInstance().generateText(trainDepths, genDepth, seed, temperature, exampleIds);
    const taskId = response.taskId;

    let notFoundAttempts = pollAttempts;

    ProgressBarController.getInstance().setProgressBarValue(0, 1);

    const pollStatus = async (onSuccess: (taskId: string) => any, onFailure: (response: StatusFailureResponse) => any, onProgress: (response: StatusResponse) => any, onNotFound: () => any) => {
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
            if (status == null && --notFoundAttempts < 0) {
                if (onNotFound) onNotFound();
                return;
            }
            if (onProgress && status) onProgress(status);
            setTimeout(async () => await pollStatus(onSuccess, onFailure, onProgress, onNotFound), pollingInterval);
        }
    }

    await pollStatus(async taskId => {
        TextAreaHandler.getInstance().setGeneratedText(await RequestManager.getInstance().retrieveText(taskId));
        reenableControls();
    }, async response => {
        ModalController.getInstance().showErrorModal({code: response.errorCode, reason: response.reason, details: response.details});
        reenableControls();
    }, response => {     
        let current, total;
        let text;

        if (response instanceof StatusAnalyzingResponse) {
            current = response.textCurrent;
            total = response.textTotal;
            text = `Analyzing (${response.fileCurrent + 1}/${response.fileTotal}) at depth ${response.currentDepth}`;
        }
        else if (response instanceof StatusGeneratingResponse) {
            current = response.current;
            total = response.total;
            text = `Generating text`;
        }
        else throw new Error("Unexpected status response");

        ProgressBarController.getInstance().setProgressBarText(text);
        ProgressBarController.getInstance().setProgressBarValue(current, total);
    }, () => {
        ModalController.getInstance().showErrorModal({code: -1, reason: "not found"});
        reenableControls();
    });

    function reenableControls() {
        TextAreaHandler.getInstance().setOverlayVisible(false);
        SubmitButtonController.getInstance().forceDisabled(false);
    }
}