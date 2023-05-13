export class Utils {
    static setupFileInputs() {
        document.querySelectorAll(".file-input").forEach((elem) => {
            elem.addEventListener("change", () => {
                let fileInput = <HTMLInputElement>elem;
        
                const fileCount = fileInput.files?.length ?? 0;
                const textbox = fileInput.previousElementSibling;
        
                console.log(fileCount);
            })
        });
    }
}