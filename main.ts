// news-image-20261119 rev3 — Thursday 19 November 2026, 47 stories.
// Node 22, standard library only. The entry image is the entry.png
// beside this file (1024x1024, drawn in code by draw_rev3.py); this
// program copies it byte-for-byte to /output/entry.png, so the judge
// sees exactly the bytes in the repository. No network, no clock,
// no randomness: both grader runs write identical bytes.
//
// Local check (outside the grader's container):
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// The image must already exist beside this file: this program never
// draws, fetches, or invents anything — it only copies entry.png.

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
if (!existsSync(src)) {
  throw new Error('entry.png missing beside main.ts');
}

// The gate only accepts a whole 1024x1024 PNG of at most 1 MiB: read
// the header first and fail loudly here instead of shipping a bad file.
const png = readFileSync(src);
if (png.length < 33 || png.readUInt32BE(16) !== 1024
    || png.readUInt32BE(20) !== 1024) {
  throw new Error('entry.png is not a 1024 by 1024 PNG');
}
if (png.length > 1048576) {
  throw new Error('entry.png is over the 1 MiB cap');
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(src, dest);

// The copy must be whole: the judge sees exactly these bytes.
if (statSync(dest).size !== statSync(src).size) {
  throw new Error('entry.png copy is incomplete');
}
