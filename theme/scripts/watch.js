import { watch } from "node:fs/promises";
import * as path from "node:path";
import { fileURLToPath } from "node:url";
import { renderSCSS } from "./render-scss.js";
import { copyTheme } from "./copy-theme.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const sourcesDir = path.resolve(__dirname, "../scss");

const ac = new AbortController();
const { signal } = ac;

const watcher = watch(sourcesDir, { recursive: true, signal });

process.on("SIGINT", () => {
    console.log("Stopping");
    ac.abort();
})

try {
    for await (const event of watcher) {
        const { eventType, filename } = event;
        process.stdout.write(`${eventType}: ${filename} `);
        await renderSCSS();
        copyTheme();
        console.log("rebuilt");
    }
} catch (e) {
    if (e.name === "AbortError") process.exit(0);
    throw e;
}
