#!/usr/bin/env node
// Tạo model 3D chibi cho nhẫn giả bằng Tripo API rồi ghi vào models/ + models/manifest.json.
//
// Cách dùng (Node 18+):
//   TRIPO_API_KEY=tsk_... node tools/tripo.mjs --ids giong,hungdao,longmau,sontinh,haibatrung
//   ... --rig     gắn xương + animation đứng/chạy (tốn thêm credit)
//   ... --dry     chỉ in prompt, không gọi API
// Tuỳ chọn: --faces 12000 (giới hạn số mặt), --conc 2 (số tướng chạy song song).
// Trong phiên cloud có proxy tự chèn khoá: không cần đặt TRIPO_API_KEY.
// Tiến trình lưu ở tools/.tripo-state.json để chạy lại không tạo trùng (tốn credit).
//
// LƯU Ý: endpoint/trường theo tài liệu Tripo OpenAPI v2 (task text_to_model, animate_rig,
// animate_retarget); chưa chạy với khoá thật — lần đầu nên thử 1 tướng.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { prompt } from './prompt.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const API = 'https://api.tripo3d.ai/v2/openapi';
const KEY = process.env.TRIPO_API_KEY || 'tsk_proxy_injected';
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i < 0 ? d : (process.argv[i + 1] && !process.argv[i + 1].startsWith('--') ? process.argv[i + 1] : true); };
const IDS = String(arg('ids', '')).split(',').filter(Boolean);
const RIG = !!arg('rig', false), DRY = !!arg('dry', false);
const FACES = +arg('faces', 12000), CONC = +arg('conc', 2);

const heroes = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/heroes.json'), 'utf8'));
const statePath = path.join(ROOT, 'tools/.tripo-state.json');
const manPath = path.join(ROOT, 'models/manifest.json');
const state = fs.existsSync(statePath) ? JSON.parse(fs.readFileSync(statePath, 'utf8')) : {};
const man = fs.existsSync(manPath) ? JSON.parse(fs.readFileSync(manPath, 'utf8')) : {};
const saveState = () => fs.writeFileSync(statePath, JSON.stringify(state, null, 1));
const saveMan = () => fs.writeFileSync(manPath, JSON.stringify(man, null, 1) + '\n');
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function api(method, p, body) {
  for (let i = 0; ; i++) {
    const r = await fetch(API + p, { method, headers: { Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });
    if ((r.status === 429 || r.status >= 500) && i < 5) { await sleep(5000 * (i + 1)); continue; }
    const t = await r.text(); let j; try { j = JSON.parse(t); } catch { j = { raw: t }; }
    if (!r.ok || (j.code != null && j.code !== 0)) throw new Error(`${method} ${p} → ${r.status} ${t.slice(0, 300)}`);
    return j.data ?? j;
  }
}
async function task(body, tag) {
  const id = (await api('POST', '/task', body)).task_id;
  if (!id) throw new Error(tag + ': không nhận được task_id');
  return id;
}
async function wait(id, tag) {
  for (;;) {
    const d = await api('GET', '/task/' + id);
    process.stdout.write(`\r  ${tag}: ${d.status} ${d.progress ?? ''}%   `);
    if (d.status === 'success') { process.stdout.write('\n'); return d; }
    if (['failed', 'cancelled', 'banned', 'expired', 'unknown'].includes(d.status)) throw new Error(`${tag} ${d.status}: ${JSON.stringify(d).slice(0, 300)}`);
    await sleep(6000);
  }
}
const outUrl = d => { const o = d.output || d.result || {}; return o.pbr_model || o.model || o.base_model || (o.model && o.model.url); };
async function download(url, file) {
  const r = await fetch(url); if (!r.ok) throw new Error('tải ' + file + ' lỗi ' + r.status);
  const buf = Buffer.from(await r.arrayBuffer());
  if (buf.slice(0, 4).toString() !== 'glTF') throw new Error(file + ' không phải GLB (định dạng khác?)');
  fs.writeFileSync(path.join(ROOT, 'models', file), buf);
  console.log(`  ↓ models/${file} (${(buf.length / 1048576).toFixed(1)} MB)`);
}

async function make(h) {
  const s = state[h.id] = state[h.id] || {};
  const pr = prompt(h);
  console.log(`\n== ${h.id} · ${h.n}\n  ${pr}`);
  if (DRY) return;
  if (!s.model) { s.model = await task({ type: 'text_to_model', prompt: pr.slice(0, 1000), negative_prompt: 'realistic photo, base, pedestal, background, text', face_limit: FACES, texture: true, pbr: false }, 'model'); saveState(); }
  const md = await wait(s.model, 'model');
  const entry = { file: h.id + '.glb', h: 1.95, src: 'tripo' };
  const u = outUrl(md); if (!u) throw new Error('không có URL model: ' + JSON.stringify(md.output || md).slice(0, 200));
  await download(u, entry.file);
  if (RIG) {
    if (!s.rig) { s.rig = await task({ type: 'animate_rig', original_model_task_id: s.model, out_format: 'glb' }, 'rig'); saveState(); }
    const rd = await wait(s.rig, 'rig');
    await download(outUrl(rd), entry.file); // model đã gắn xương thay model tĩnh
    entry.anims = {};
    for (const [nm, preset] of [['idle', 'preset:idle'], ['run', 'preset:run']]) {
      const k = 'anim_' + nm;
      if (!s[k]) { s[k] = await task({ type: 'animate_retarget', original_model_task_id: s.rig, animation: preset, out_format: 'glb' }, nm); saveState(); }
      const ad = await wait(s[k], nm); const f = `${h.id}_${nm}.glb`; await download(outUrl(ad), f); entry.anims[nm] = f;
    }
  }
  man[h.id] = entry; saveMan(); s.done = true; saveState();
}

const list = IDS.map(id => heroes.find(h => h.id === id) || (console.warn('Không có id', id), null)).filter(Boolean);
if (!list.length) { console.log('Chọn tướng: --ids id1,id2  (danh sách id trong tools/heroes.json)'); process.exit(1); }
fs.mkdirSync(path.join(ROOT, 'models'), { recursive: true });
const q = [...list]; let fail = 0;
await Promise.all(Array.from({ length: Math.min(CONC, q.length) }, async () => {
  for (let h; (h = q.shift());) { try { await make(h); } catch (e) { fail++; console.error(`\n✗ ${h.id}: ${e.message}`); } }
}));
console.log(`\nXong: ${list.length - fail}/${list.length}. Manifest: models/manifest.json`);
process.exit(fail ? 2 : 0);
