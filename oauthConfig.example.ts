
export class Config {
    conf = {
        "client": {
            "id": "banana",
            "secret": "psst, i like banana"
        }
    };

    get config() {
        return this.conf;
    }
}
