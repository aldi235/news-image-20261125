// Entry point for the news-image-20261125 bundle.
//
// Copies the committed entry.png into the directory given by
// MAKEFUN_OUTPUT_DIR (default /output) and verifies the copy before
// reporting success. Node standard library only — no dependencies.
//
//   node main.ts
//   MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024;

const here = resolve(fileURLToPath(new URL(".", import.meta.url)));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(resolve(outDir), "entry.png");

if (!existsSync(source)) {
  throw new Error(`source image missing: ${source} — run python3 draw_news.py first`);
}
const sourceBytes = readFileSync(source);
if (!sourceBytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("source entry.png does not start with the PNG signature");
}

mkdirSync(resolve(outDir), { recursive: true });
copyFileSync(source, target);

const before = sourceBytes;
const after = readFileSync(target);
const size = statSync(target).size;

if (size !== before.length || size !== after.length) {
  throw new Error(`size mismatch: source ${before.length} bytes, copy ${size} bytes`);
}
if (!after.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("copied file does not start with the PNG signature");
}
if (size >= MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
}
if (!before.equals(after)) {
  throw new Error("copied bytes differ from the source image");
}

console.log(
  `OK: entry.png (${size} bytes, ${(size / 1024).toFixed(1)} KiB) copied to ` +
    `${target} and verified (PNG signature, byte-identical, under 1 MiB)`,
);
