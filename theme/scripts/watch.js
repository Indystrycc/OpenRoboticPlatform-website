import { watch } from "node:fs/promises";
import * as path from "node:path";
import { fileURLToPath } from "node:url";
import { copyTheme } from "./copy-theme.js";
import { renderSCSS } from "./render-scss.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const sourcesDir = path.resolve(__dirname, "../scss");

const ac = new AbortController();
const { signal } = ac;

const watcher = watch(sourcesDir, { recursive: true, signal });

process.on("SIGINT", () => {
    console.log("Stopping");
    ac.abort();
});

async function buildAndCopy() {
    await renderSCSS();
    copyTheme();
}

try {
    process.stdout.write("Compiling...");
    await buildAndCopy();
    console.log(" done");
} catch (e) {
    console.log();
    console.error(e);
}

try {
    for await (const event of watcher) {
        try {
            const { eventType, filename } = event;
            process.stdout.write(`${eventType}: ${filename} `);
            await buildAndCopy();
            console.log("rebuilt");
        } catch (e) {
            console.log();
            console.error(e);
        }
    }
} catch (e) {
    if (e.name === "AbortError") process.exit(0);
    throw e;
}
