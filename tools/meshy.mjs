#!/usr/bin/env node
// Tạo model 3D cho nhẫn giả bằng Meshy API rồi ghi vào models/ + models/manifest.json.
// Game tự nạp models/<id>.glb thay cho model dựng thủ tục (xem mục 18 trong index.html).
//
// Cách dùng (Node 18+):
//   MESHY_API_KEY=msy_... node tools/meshy.mjs --ids long,khe          # vài nhân vật
//   MESHY_API_KEY=msy_... node tools/meshy.mjs --ids long --rig        # kèm gắn xương + animation đi/chạy
//   node tools/meshy.mjs --ids long --dry                              # chỉ in prompt, không gọi API
// Tuỳ chọn: --poly 12000 (số tam giác mục tiêu), --conc 2 (số nhân vật chạy song song).
// Tiến trình lưu ở tools/.meshy-state.json để chạy lại không tạo trùng (tốn credit).
//
// LƯU Ý: tên trường/endpoint theo tài liệu Meshy (text-to-3d v2, rigging v1); chưa chạy thử
// với khoá thật — lần chạy đầu nên thử 1 nhân vật và đối chiếu https://docs.meshy.ai.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const API = 'https://api.meshy.ai/openapi';
// Trong phiên cloud có proxy tự chèn khoá: giá trị giả ở đây sẽ được thay thế.
const KEY = process.env.MESHY_API_KEY || 'msy_proxy_injected';
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i < 0 ? d : (process.argv[i + 1] && !process.argv[i + 1].startsWith('--') ? process.argv[i + 1] : true); };
const IDS = String(arg('ids', '')).split(',').filter(Boolean);
const RIG = !!arg('rig', false), DRY = !!arg('dry', false);
const POLY = +arg('poly', 12000), CONC = +arg('conc', 2);

const heroes = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/heroes.json'), 'utf8'));
const statePath = path.join(ROOT, 'tools/.meshy-state.json');
const manPath = path.join(ROOT, 'models/manifest.json');
const state = fs.existsSync(statePath) ? JSON.parse(fs.readFileSync(statePath, 'utf8')) : {};
const man = fs.existsSync(manPath) ? JSON.parse(fs.readFileSync(manPath, 'utf8')) : {};
const saveState = () => fs.writeFileSync(statePath, JSON.stringify(state, null, 1));
const saveMan = () => fs.writeFileSync(manPath, JSON.stringify(man, null, 1) + '\n');

import { prompt } from './prompt.mjs';

// ---------- gọi API ----------
async function api(method, p, body) {
  for (let i = 0; ; i++) {
    const r = await fetch(API + p, { method, headers: { Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });
    if (r.status === 429 && i < 5) { await sleep(5000 * (i + 1)); continue; }
    const t = await r.text(); let j; try { j = JSON.parse(t); } catch { j = { raw: t }; }
    if (!r.ok) throw new Error(`${method} ${p} → ${r.status} ${t.slice(0, 300)}`);
    return j;
  }
}
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function poll(p, tag) {
  for (;;) {
    const j = await api('GET', p);
    const st = j.status || (j.result && j.result.status);
    process.stdout.write(`\r  ${tag}: ${st} ${j.progress ?? ''}%   `);
    if (st === 'SUCCEEDED') { process.stdout.write('\n'); return j; }
    if (st === 'FAILED' || st === 'CANCELED' || st === 'EXPIRED') throw new Error(`${tag} ${st}: ${JSON.stringify(j.task_error || j).slice(0, 300)}`);
    await sleep(8000);
  }
}
// tìm mọi URL .glb trong kết quả (để không phụ thuộc cứng vào tên trường)
function glbUrls(o, pre = '', acc = {}) {
  if (o && typeof o === 'object') for (const [k, v] of Object.entries(o)) {
    if (typeof v === 'string' && /^https?:\/\/.*\.glb(\?|$)/i.test(v)) acc[(pre + k).replace(/_?glb_?url$/i, '').replace(/^model_urls\.?/, '') || 'model'] = v;
    else glbUrls(v, pre + k + '.', acc);
  }
  return acc;
}
async function download(url, file) {
  const r = await fetch(url); if (!r.ok) throw new Error('tải ' + file + ' lỗi ' + r.status);
  fs.writeFileSync(path.join(ROOT, 'models', file), Buffer.from(await r.arrayBuffer()));
  console.log(`  ↓ models/${file} (${(fs.statSync(path.join(ROOT, 'models', file)).size / 1048576).toFixed(1)} MB)`);
}

async function make(h) {
  const s = state[h.id] = state[h.id] || {};
  const pr = prompt(h);
  console.log(`\n== ${h.id} · ${h.n}\n  ${pr}`);
  if (DRY) return;
  if (!s.preview) { s.preview = (await api('POST', '/v2/text-to-3d', { mode: 'preview', prompt: pr.slice(0, 600), art_style: 'realistic', should_remesh: true, topology: 'triangle', target_polycount: POLY, symmetry_mode: 'on' })).result; saveState(); }
  await poll('/v2/text-to-3d/' + s.preview, 'preview');
  if (!s.refine) { s.refine = (await api('POST', '/v2/text-to-3d', { mode: 'refine', preview_task_id: s.preview, enable_pbr: false })).result; saveState(); }
  const ref = await poll('/v2/text-to-3d/' + s.refine, 'refine');
  const entry = { file: h.id + '.glb', h: 1.95 };
  if (RIG) {
    if (!s.rig) { s.rig = (await api('POST', '/v1/rigging', { input_task_id: s.refine, height_meters: 1.2 })).result; saveState(); }
    const rg = await poll('/v1/rigging/' + s.rig, 'rigging');
    const urls = glbUrls(rg); console.log('  GLB nhận được:', Object.keys(urls).join(', '));
    const main = Object.keys(urls).find(k => /rigged/i.test(k)) || Object.keys(urls)[0];
    if (!main) throw new Error('rigging không trả về GLB');
    await download(urls[main], entry.file);
    entry.anims = {};
    for (const [k, u] of Object.entries(urls)) {
      if (k === main) continue; const nm = /run/i.test(k) ? 'run' : /walk/i.test(k) ? 'walk' : k.split('.').pop();
      const f = `${h.id}_${nm}.glb`; await download(u, f); entry.anims[nm] = f;
    }
  } else {
    const u = (ref.model_urls && ref.model_urls.glb) || Object.values(glbUrls(ref))[0];
    if (!u) throw new Error('refine không có GLB');
    await download(u, entry.file);
  }
  man[h.id] = entry; saveMan(); s.done = true; saveState();
}

const list = IDS.length ? IDS.map(id => heroes.find(h => h.id === id) || (console.warn('Không có id', id), null)).filter(Boolean) : [];
if (!list.length) { console.log('Chọn nhân vật: --ids id1,id2  (danh sách id trong tools/heroes.json)'); process.exit(1); }
fs.mkdirSync(path.join(ROOT, 'models'), { recursive: true });
const q = [...list]; let fail = 0;
await Promise.all(Array.from({ length: Math.min(CONC, q.length) }, async () => {
  for (let h; (h = q.shift());) { try { await make(h); } catch (e) { fail++; console.error(`\n✗ ${h.id}: ${e.message}`); } }
}));
console.log(`\nXong: ${list.length - fail}/${list.length}. Manifest: models/manifest.json`);
process.exit(fail ? 2 : 0);
