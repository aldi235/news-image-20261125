/**
 * news-image-20261125 — entrypoint for make.fun.
 *
 * The image is fully pre-rendered by draw_news.py (PIL) and committed as
 * entry.png. This entrypoint only copies that file into the output
 * directory, so it works in the grader sandbox with no network access.
 * Stdlib only: fs + path + url.
 */
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = resolve(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  throw new Error("entry.png missing next to main.ts");
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// Verify the copy landed intact: same byte size as the committed image,
// and a valid PNG signature (89 50 4E 47 0D 0A 1A 0A) at the start — the
// gate refuses anything that is not a whole PNG under 1 MiB.
const srcBytes = statSync(source).size;
const outBytes = statSync(target).size;
if (srcBytes !== outBytes) {
  throw new Error(`copy mismatch: source ${srcBytes} bytes, output ${outBytes} bytes`);
}
const header = readFileSync(target).subarray(0, 8);
const pngSig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!header.equals(pngSig)) {
  throw new Error("output is not a valid PNG (bad signature)");
}
if (outBytes > 1048576) {
  throw new Error(`output exceeds the 1 MiB gate limit: ${outBytes} bytes`);
}
console.log(`copied entry.png -> ${target} (${outBytes} bytes, verified PNG)`);
