import { FileStorage } from "@files";
import { ExampleFile } from "@files/sourcefile"
import { RequestManager } from "requestmanager";

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
    
    await RequestManager.getInstance().generateText(trainDepths, genDepth, seed, temperature, exampleIds);

    // TODO: Poll /api/status periodically, display some sort of progress bar
}