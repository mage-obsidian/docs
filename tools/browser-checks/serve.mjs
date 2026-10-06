// This file is part of the MageObsidian - Documentation project.
//
// SPDX-FileCopyrightText: 2024 Jeanmarcos Juarez
// SPDX-License-Identifier: MIT
import { createServer } from "node:http";
import { createReadStream, statSync } from "node:fs";
import { createGzip } from "node:zlib";
import { extname, join, normalize, resolve } from "node:path";

const root = resolve(process.argv[2] ?? "site");
const port = Number(process.argv[3] ?? 8000);
const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json",
  ".xml": "application/xml",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".webp": "image/webp",
  ".woff2": "font/woff2",
  ".txt": "text/plain; charset=utf-8",
};
const compressible = new Set([".html", ".css", ".js", ".json", ".xml", ".svg", ".txt"]);

function resolveFile(urlPath) {
  const candidate = join(root, normalize(decodeURIComponent(urlPath)));
  if (!candidate.startsWith(root)) return null;
  try {
    const stat = statSync(candidate);
    return stat.isDirectory() ? join(candidate, "index.html") : candidate;
  } catch {
    return null;
  }
}

createServer((req, res) => {
  const file = resolveFile(new URL(req.url, "http://localhost").pathname);
  if (!file) {
    res.writeHead(404, { "content-type": "text/plain" }).end("not found");
    return;
  }
  const ext = extname(file);
  const headers = { "content-type": types[ext] ?? "application/octet-stream", "cache-control": "max-age=3600" };
  const stream = createReadStream(file);
  stream.on("error", () => res.writeHead(404).end());
  if (compressible.has(ext) && /\bgzip\b/.test(req.headers["accept-encoding"] ?? "")) {
    res.writeHead(200, { ...headers, "content-encoding": "gzip", vary: "accept-encoding" });
    stream.pipe(createGzip()).pipe(res);
    return;
  }
  res.writeHead(200, { ...headers, "content-length": statSync(file).size });
  stream.pipe(res);
}).listen(port, "127.0.0.1");
