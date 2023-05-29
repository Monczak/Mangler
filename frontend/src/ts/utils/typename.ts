import "reflect-metadata";

export function keepTypeName(target: any) {
    Reflect.defineMetadata("typeName", target.name, target.prototype);
}