// GTA 6 meme-x v2 entrypoint: hand in the X post that carries the meme.
// The grader checks the repo out at /bot and reads the gate input from
// /output, so POST.json is read from /bot and copied to /output/POST.json.
// POST.json must name a real X post URL; anything else is refused so a
// placeholder or a non-X link can never be submitted by accident.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const postPath = join(BOT_DIR, "POST.json");
let postUrl: string;
try {
  const post = JSON.parse(readFileSync(postPath, "utf8")) as { url?: unknown };
  postUrl = typeof post.url === "string" ? post.url : "";
} catch (err) {
  console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
if (!/^https:\/\/x\.com\/[^/]+\/status\/\d+$/.test(postUrl)) {
  console.error(`POST.json does not name a real X post URL: ${postUrl || "(empty)"}`);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(postPath, join(OUTPUT_DIR, "POST.json"));
  console.log(`Entry post handed in: ${postUrl}`);
} catch (err) {
  console.error(`POST.json could not be copied to ${OUTPUT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
