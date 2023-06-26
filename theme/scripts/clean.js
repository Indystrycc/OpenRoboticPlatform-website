import { rmSync } from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const destPath = path.resolve(__dirname, "../dist");

rmSync(destPath, { recursive: true, force: true });
