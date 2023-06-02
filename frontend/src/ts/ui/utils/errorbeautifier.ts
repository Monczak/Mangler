export class ErrorBeautifier {
    private static errorCodes = {
        maxRetriesExceeded: 10,
        badSeed: 11,
        badSeedLength: 12,
        invalidDepth: 13,
        invalidLength: 14,
        badDepth: 15,
        badTemp: 16,
        timeout: 98,
        internal: 99,
        notFound: -1,
    };

    private static getSeed(errorDetails: string): string {
        const matches = errorDetails.match(/[Ss]eed "(?<seed>.*)"/);
        if (!matches || !matches.groups?.seed)
            throw new Error("Invalid API response");
        
        return matches.groups.seed;
    }

    private static getMinSeedLength(errorDetails: string): string {
        const matches = errorDetails.match(/(?<chars>[0-9]*) chars/);
        if (!matches || !matches.groups?.chars)
            throw new Error("Invalid API response");
        
        return matches.groups.chars;
    }

    private static getDepthInfo(errorDetails: string) {
        const matches = errorDetails.match(/Depth (?<depth>[0-9]*) is invalid, must be one of {(?<validDepths>.*)}/);
        if (!matches || !matches.groups?.depth || !matches.groups?.validDepths)
            throw new Error("Invalid API response");
        
        return {depth: matches.groups.depth, validDepths: matches.groups.validDepths}; 
    }

    private static getTempInfo(errorDetails: string) {
        const matches = errorDetails.match(/Temperature (?<temp>[-0-9.]*) is invalid, must be in range (?<minTemp>[-0-9.]*) - (?<maxTemp>[-0-9.]*)/);
        if (!matches || !matches.groups?.temp || !matches.groups?.minTemp || !matches.groups?.maxTemp)
            throw new Error("Invalid API response");
        
        return {temp: matches.groups.depth, minTemp: matches.groups.minTemp, maxTemp: matches.groups.maxTemp}; 
    }
    
    static beautifyError(errorData: {code: number, reason: string, details?: string}): string {
        switch (errorData.code) {
            case this.errorCodes.maxRetriesExceeded:
                return `We tried as hard as we could, but we could not generate text. Try a different seed.`;
            case this.errorCodes.badSeed:
                if (!errorData.details) throw new Error("Must specify details");
                return `Can't generate text with the seed "${this.getSeed(errorData.details)}". Try a different seed.`;
            case this.errorCodes.badSeedLength:
                if (!errorData.details) throw new Error("Must specify details");    
                return `The seed "${this.getSeed(errorData.details)}" is too short. It must be at least ${this.getMinSeedLength(errorData.details)} letters long.`;
            case this.errorCodes.badDepth:
                if (!errorData.details) throw new Error("Must specify details");
                const {depth, validDepths} = this.getDepthInfo(errorData.details);
                return `Generation depth of ${depth} is invalid. It must be one of ${validDepths}.`;
            case this.errorCodes.invalidDepth:
                return `Trying to generate text with an invalid depth. Check the depths and try again.`;
            case this.errorCodes.invalidLength:
                return `Trying to generate text with an invalid length. Check the length and try again.`;
            case this.errorCodes.badTemp:
                if (!errorData.details) throw new Error("Must specify details");
                const {temp, minTemp, maxTemp} = this.getTempInfo(errorData.details);
                return `Temperature of ${temp} is invalid. It must be between ${minTemp} and ${maxTemp}.`;
            case this.errorCodes.timeout:
                return `Text generation took too long. Try again with a smaller train depth range or less training files.`
            case this.errorCodes.internal:
                return `The server could not process your request. Try again later.`
            case this.errorCodes.notFound:
                return `It seems the server is taking too long to take on your request. Try again later or try different parameters.`
            default:
                return `I have no idea what happened. (error code ${errorData.code}, reason ${errorData.reason})`
        }
    }
}