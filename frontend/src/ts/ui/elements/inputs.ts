import { IEventHandler } from "@events/eventhandler";
import { FileStorage } from "@files";
import { ExampleFile, UploadedFile } from "@files/sourcefile";
import { Singleton } from "@utils/singleton";
import { SubmitButtonController } from "./submitcontroller";
import bootstrapSlider from "bootstrap-slider";
import { SeedInputHandler } from "./seedinput";

export class InputHandler extends Singleton<InputHandler>() implements IEventHandler {
    trainDepthSlider!: bootstrapSlider;
    genDepthSlider!: bootstrapSlider;
    temperatureSlider!: bootstrapSlider;
    
    trainDepthHandles!: Array<HTMLElement>;
    genDepthHandle!: HTMLElement;
    temperatureHandle!: HTMLElement;

    seedInput!: HTMLElement;
    
    getInputs() {
        const [minTrainDepth, maxTrainDepth] = this.trainDepthHandles
            .map(elem => elem.getAttribute("aria-valuenow"))
            .map(n => n ? parseInt(n) : -1)
            .sort((a: number, b: number) => a - b);
        const trainDepths = Array.from(Array(maxTrainDepth - minTrainDepth + 1), (v, k) => k + minTrainDepth);
        const genDepth = parseInt(this.genDepthHandle.getAttribute("aria-valuenow") ?? "-1");
        const temperature = parseFloat(this.temperatureHandle.getAttribute("aria-valuenow") ?? "1");
    
        const seed = this.seedInput.textContent ?? "";
    
        const uploadIds = FileStorage.getInstance().files()
            .filter(file => file instanceof UploadedFile)
            .map(file => file.id());
        const exampleIds = FileStorage.getInstance().files()
            .filter(file => file instanceof ExampleFile)
            .map(file => file.id());
        
        return {
            trainDepths: trainDepths,
            genDepth: genDepth,
            temperature: temperature,
            seed: seed,
            uploadIds: uploadIds,
            exampleIds: exampleIds,
        }
    }

    validateInputs(): boolean {
        const inputs = this.getInputs();
    
        if (!inputs.trainDepths.includes(inputs.genDepth)) return false;
        if (inputs.seed.length <= inputs.genDepth) return false;
        if (inputs.uploadIds.length + inputs.exampleIds.length < 1) return false;
    
        return true;
    }

    setSubmitButtonEnabled() {
        SubmitButtonController.getInstance().setEnabled(this.validateInputs());
    }

    setupEventListeners(): void {
        this.trainDepthSlider = new bootstrapSlider("#train-depths", {
            id: "slider-train-depths",
            min: 1,
            max: 10,
            range: true,
            value: [1, 3],
        });
        this.genDepthSlider = new bootstrapSlider("#gen-depth", {
            id: "slider-gen-depth",
            min: 1,
            max: 10,
            value: 3,
        });
        this.temperatureSlider = new bootstrapSlider("#temperature", {
            id: "slider-temperature",
            min: -5,
            max: 5,
            value: 1,
            step: 0.05,
        });

        this.trainDepthHandles = [...document.querySelectorAll("#slider-train-depths .slider-handle")] as Array<HTMLElement>;
        this.genDepthHandle = document.querySelector("#slider-gen-depth .slider-handle") as HTMLElement;
        this.temperatureHandle = document.querySelector("#slider-temperature .slider-handle") as HTMLElement;
        this.seedInput = document.querySelector("#seed-input") as HTMLElement;

        this.trainDepthSlider.on("slide", () => this.setSubmitButtonEnabled());
        this.genDepthSlider.on("slide", () => this.setSubmitButtonEnabled());
        this.temperatureSlider.on("slide", () => this.setSubmitButtonEnabled());

        SeedInputHandler.getInstance().registerCallback(() => this.setSubmitButtonEnabled());
        FileStorage.getInstance().registerCallback(() => this.setSubmitButtonEnabled());

        this.setSubmitButtonEnabled();
    }
}



