import { readFileSync, writeFileSync, existsSync } from "fs";

// GTA 6 meme-x v2 entrypoint: hand in the X post that carries the meme.
// POST.json must name a real X post URL; anything else is refused so a
// placeholder or a non-X link can never be submitted by accident.

const POST_PATH = "POST.json";

function readPostUrl(): string {
  if (!existsSync(POST_PATH)) {
    throw new Error(
      "POST.json is missing: post the meme on X first, then set POST.json to its URL."
    );
  }
  const raw = readFileSync(POST_PATH, "utf8");
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    throw new Error("POST.json is not valid JSON.");
  }
  const url = (parsed as { url?: unknown }).url;
  if (typeof url !== "string") {
    throw new Error("POST.json must have a string field named url.");
  }
  return url;
}

function main(): void {
  const url = readPostUrl();
  const postPattern = /^https:\/\/x\.com\/[^/]+\/status\/\d+$/;
  if (!postPattern.test(url)) {
    throw new Error(`Not a real X post URL: ${url}`);
  }
  writeFileSync("output.txt", url + "\n", "utf8");
  console.log(`Entry post handed in: ${url}`);
}

main();
