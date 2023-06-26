import { fileURLToPath } from "node:url";
import { copyFileSync } from "node:fs";
import * as path from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const srcPath = path.resolve(__dirname, "../dist/styles.css");
const targetPath = path.resolve(__dirname, "../../website/static/css/theme.css");

export function copyTheme() {
    copyFileSync(srcPath, targetPath);
}
