export function Singleton<T>() {
    return class Singleton {
        private static instance: T;

        protected constructor() {

        }

        static getInstance(): T {
            if (!this.instance) {
                this.instance = new this() as T;
            }
            return this.instance;
        }
    }
} 