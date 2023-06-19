import autoprefixer from "autoprefixer";
import { mkdir, writeFile } from "fs/promises";
import * as path from "node:path";
import { fileURLToPath } from "node:url";
import postcss from "postcss";
import * as sass from "sass";
import packageJSON from "../package.json" assert { type: "json" };

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const stylesPath = '../scss/styles.scss';
const destPath = path.resolve(__dirname, "../dist/styles.css");

const entryPoint = `/*!
* Start Bootstrap - ${packageJSON.title} v${packageJSON.version} (${packageJSON.homepage})
* Copyright 2013-${new Date().getFullYear()} ${packageJSON.author}
* Licensed under ${packageJSON.license} (https://github.com/StartBootstrap/${packageJSON.name}/blob/master/LICENSE)
* Modified by Indystrycc
*/
@import "${stylesPath}"
`

const results = sass.compileString(entryPoint, {
    loadPaths: [
        path.resolve(__dirname, "../node_modules")
    ]
});

const destPathDirname = path.dirname(destPath);
await mkdir(destPathDirname, { recursive: true });
const prefixed = await postcss([autoprefixer]).process(results.css, { from: 'styles.css', to: 'styles.css' });
for (const warn of prefixed.warnings()) {
    console.warn(warn.toString());
}
await writeFile(destPath, prefixed.css.toString());
