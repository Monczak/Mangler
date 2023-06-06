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

    invalidDepthText = () => `The generation depth must be one of the training depths.`
    invalidSeedText = (length: number) => `The seed must be at least ${length} characters long.`
    noFilesText = () => `You must provide at least 1 file.`
    
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

    getValidationErrors(): Array<string> {
        const errors = [];

        if (!this.validateTrainDepths()) errors.push(this.invalidDepthText());
        if (!this.validateSeed()) errors.push(this.invalidSeedText(this.getInputs().genDepth + 1));
        if (!this.validateUploadIds()) errors.push(this.noFilesText());
    
        return errors;
    }

    validateTrainDepths(): boolean {
        const inputs = this.getInputs();
        return inputs.trainDepths.includes(inputs.genDepth);
    }

    validateSeed(): boolean {
        const inputs = this.getInputs();
        return inputs.seed.length > inputs.genDepth;
    }

    validateUploadIds(): boolean {
        const inputs = this.getInputs();
        return inputs.uploadIds.length + inputs.exampleIds.length >= 1;
    }
 
    setSubmitButtonStatus() {
        const errors = this.getValidationErrors();
        SubmitButtonController.getInstance().setEnabled(errors.length == 0);
        
        const tooltipText = errors.length == 0 ? "" : errors.join("<br>");
        SubmitButtonController.getInstance().setTooltipText(tooltipText);
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

        this.trainDepthSlider.on("slide", () => this.setSubmitButtonStatus());
        this.genDepthSlider.on("slide", () => this.setSubmitButtonStatus());
        this.temperatureSlider.on("slide", () => this.setSubmitButtonStatus());

        SeedInputHandler.getInstance().registerCallback(() => this.setSubmitButtonStatus());
        FileStorage.getInstance().registerCallback(() => this.setSubmitButtonStatus());

        window.addEventListener("DOMContentLoaded", () => this.setSubmitButtonStatus());
    }
}



