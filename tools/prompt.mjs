// Mô tả (prompt) tiếng Anh cho dịch vụ tạo 3D, dựng từ dữ liệu nhân vật trong tools/heroes.json.
// Tướng chủ lực có mô tả viết tay trong SPECIAL; các tướng khác ghép tự động từ ngoại hình.
const HAIR = { spiky: 'spiky', long: 'long straight', wild: 'wild messy', pony: 'ponytail', bun: 'bun', short: 'short', twin: 'twin-tail', hood: 'hooded', shave: 'shaved head with red headband', hat: 'conical Vietnamese non la hat', dragon: 'dragon-horned helmet', crane: 'top-knot with white crane feather', flame: 'flaming spiky', helm: 'warrior helmet with red crest', crown: 'golden crown over', tiara: 'long hair with golden tiara,', khan: 'traditional Vietnamese khan dong turban' };
const WPN = { sword: 'straight sword', fan: 'war fan', staff: 'wooden staff with glowing orb', katana: 'curved sword', scroll: 'military strategy scroll', claw: 'claw blades', pins: 'throwing kunai', tube: 'scroll tube', lantern: 'red paper lantern', kunai: 'kunai', fist: 'armored gauntlets', oar: 'wooden boat oar', shuriken: 'large shuriken', bow: 'longbow', hammer: 'war hammer', orb: 'glowing orb', trident: 'trident', crane: 'crane-feather fan', bamboo: 'long bamboo staff', scythe: 'scythe', axe: 'axe', melon: 'glowing watermelon orb', branch: 'magic branch staff', net: 'fishing net fan', bell: 'bronze bell', disc: 'throwing disc', bowl: 'magic bowl', crossbow: 'crossbow', pillar: 'stone pillar hammer', banh: 'rice-cake scroll', spear: 'spear', glaive: 'glaive', flag: 'battle banner', brush: 'giant calligraphy brush' };
const ELN = { kim: 'metal', moc: 'wood and leaves', thuy: 'water', hoa: 'fire', tho: 'earth and stone' };
export const STYLE = 'chibi proportions with big head and small body, full body, standing A-pose, facing forward, stylized low-poly game asset, sharp angular planes, hard edges, crisp silhouette, clean topology, flat cel-shaded colors, no base, no background';
// Nhân vật dân gian / lịch sử Việt Nam (không có bản quyền); mô tả theo hình tượng truyền thống, phong cách riêng của game.
export const SPECIAL = {
  giong: 'Young Vietnamese folk-legend hero boy in dark iron armor and iron helmet, gripping a long bamboo stalk as a staff, small flames rising at his feet, golden scarf',
  hungdao: 'Vietnamese Tran-dynasty grand general, dignified older man with short black beard, dark red robe over lamellar armor, small golden crown, holding a rolled military strategy scroll',
  longmau: 'Original dragon-mother river goddess heroine, flowing red hair like flames, dark crimson robe with gold trim, small dragon horns, holding a golden trident, water-and-fire motifs',
  sontinh: 'Vietnamese mountain-god hero from folklore, earthy green and brown robe with stone-plate shoulder guards, golden crown, holding a wooden staff topped with a glowing mountain gem',
  haibatrung: 'Vietnamese heroine queen general of the Trung sisters legend, black twin-tail hair with gold ornaments, red armored robe with gold trim, holding a straight sword',
};
export function colorName(hex) {
  const n = parseInt(hex.slice(1), 16), r = (n >> 16) / 255, g = (n >> 8 & 255) / 255, b = (n & 255) / 255;
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, d = mx - mn;
  if (d < 0.08) return l > 0.85 ? 'white' : l > 0.55 ? 'light grey' : l > 0.25 ? 'grey' : 'black';
  let h = mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; h = (h * 60 + 360) % 360;
  const base = h < 15 ? 'red' : h < 40 ? 'orange' : h < 65 ? 'yellow' : h < 160 ? 'green' : h < 195 ? 'cyan' : h < 250 ? 'blue' : h < 290 ? 'purple' : h < 340 ? 'pink' : 'red';
  return (l < 0.3 ? 'dark ' : l > 0.72 ? 'light ' : '') + base;
}
export function prompt(h) {
  if (SPECIAL[h.id]) return `${SPECIAL[h.id]}, ${STYLE}`;
  const [hair, hc, , out, acc, wpn, fem] = h.look;
  return [
    `Stylized ${fem ? 'girl' : 'boy'} ninja warrior`,
    `${colorName(hc)} ${HAIR[hair] || hair} hair`,
    `${colorName(out)} ninja outfit with ${colorName(acc)} scarf and belt`,
    `holding a ${WPN[wpn] || wpn}`,
    `${ELN[h.el] || h.el} element motifs, Vietnamese folklore inspired`,
    STYLE,
  ].join(', ');
}
