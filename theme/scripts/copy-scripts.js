import { fileURLToPath } from "node:url";
import { copyFileSync } from "node:fs";
import * as path from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const srcPath = path.resolve(__dirname, "../node_modules/bootstrap/dist/js/bootstrap.bundle.min.js");
const targetPath = path.resolve(__dirname, "../../website/static/js/bootstrap.bundle.min.js");

export function copyScript() {
    copyFileSync(srcPath, targetPath);
}
