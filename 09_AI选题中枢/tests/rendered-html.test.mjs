import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const projectRoot = new URL("../", import.meta.url);

test("builds the private topic compass product", async () => {
  const [page, board, layout, styles, hosting, migration] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/TopicBoard.tsx", projectRoot), "utf8"),
    readFile(new URL("app/layout.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
    readFile(new URL(".openai/hosting.json", projectRoot), "utf8"),
    readFile(new URL("drizzle/0000_shiny_vision.sql", projectRoot), "utf8"),
    access(new URL("dist/server/index.js", projectRoot)),
    access(new URL("public/og.png", projectRoot)),
  ]);

  assert.match(page, /<TopicBoard \/>/);
  assert.match(board, /选题罗盘/);
  assert.match(board, /今日主推/);
  assert.match(board, /收录选题/);
  assert.ok(board.includes('fetch("/api/topics"'));
  assert.match(layout, /私人 AI 内容中枢/);
  assert.match(layout, /og\.png/);
  assert.match(styles, /--lime:\s*#c8f36b/i);
  assert.match(hosting, /"d1":\s*"DB"/);
  assert.match(migration, /CREATE TABLE `topics`/);
  assert.doesNotMatch(page + board + layout, /codex-preview|SkeletonPreview/);
});
