export class APIResponse {
    statusCode: number;

    constructor(statusCode: number) {
        this.statusCode = statusCode;
    }
}

export class ErrorResponse extends APIResponse {
    details?: any;

    constructor(statusCode: number, details?: any) {
        super(statusCode);
        this.details = details;
    }
}

export class UploadResponse extends APIResponse {
    id: string;
    ttl: number;

    constructor(statusCode: number, response: {id: string, ttl: number}) {
        super(statusCode);
        this.id = response.id;
        this.ttl = response.ttl;
    }
}

export class GenerateResponse extends APIResponse {
    taskId: string;
    
    constructor(statusCode: number, response: {task_id: string}) {
        super(statusCode);
        this.taskId = response.task_id;
    }
}

export class StatusResponse extends APIResponse {

}

export class StatusAnalyzingResponse extends StatusResponse {
    fileCurrent: number;
    fileTotal: number;
    textCurrent: number;
    textTotal: number;

    constructor(statusCode: number, fileCurrent: number, fileTotal: number, textCurrent: number, textTotal: number) {
        super(statusCode);
        this.fileCurrent = fileCurrent;
        this.fileTotal = fileTotal;
        this.textCurrent = textCurrent;
        this.textTotal = textTotal;
    }
}

export class StatusGeneratingResponse extends StatusResponse {
    current: number;
    total: number;

    constructor(statusCode: number, current: number, total: number) {
        super(statusCode);
        this.current = current;
        this.total = total;
    }
}

export class StatusSuccessResponse extends StatusResponse {

}

export class StatusFailureResponse extends StatusResponse {
    errorCode: number;
    reason: string;
    details: string;

    constructor(statusCode: number, errorCode: number, reason: string, details: string) {
        super(statusCode);
        this.errorCode = errorCode;
        this.reason = reason;
        this.details = details;
    }
}

export class StatusResponseFactory {
    static async makeResponse(response: Response): Promise<APIResponse | null> {
        const code = response.status;
        if (code == 404)
            return null;
        
        const json = await response.json();

        switch (code) {
            case 200:
                return new StatusSuccessResponse(code);
            case 202:
                switch (json.state) {
                    case "ANALYZING":
                        return new StatusAnalyzingResponse(code, json.file_current, json.file_total, json.text_current, json.text_total);
                    case "GENERATING":
                        return new StatusGeneratingResponse(code, json.current, json.total);
                    default: throw new Error("Unknown status");
                }
            case 400:
                if (json.state === "FAILURE") {
                    return new StatusFailureResponse(code, json.code, json.reason, json.details);
                }
                return new ErrorResponse(code, json);
            case 500:
                return new ErrorResponse(code);
            default: throw new Error(`Unexpected status code ${code}`);
        }
    }
}
