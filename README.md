# Nhẫn Giới Hải Vân

Game đấu tướng theo lượt chạy trên trình duyệt: 40 nhẫn giả (B đến SSS), đội 6 người, Nộ chung, combo Truy Kích, kỹ năng phụ, thiên phú, Điểm Tốc, ngũ hành tương khắc, chiêu mộ, trang bị, đột phá, thức tỉnh, Duyên, đồ giám, linh thú, vượt ải 5 chương, tháp 100 tầng, boss thế giới, phó bản, cửa hàng, đấu trường, nhiệm vụ và thành tựu.

Chơi tại: https://benphandz.github.io/nhan-gioi-hai-van/

- Toàn bộ nhân vật, làng và chiêu thức là sáng tác riêng, lấy cảm hứng từ địa danh Đà Nẵng và truyền thuyết dân gian Việt Nam.
- Tiến trình lưu trong trình duyệt của người chơi (localStorage).
- Chỉ gồm một tệp `index.html`, không cần cài đặt.

## Nhân vật 3D

- Mặc định: model low-poly dựng bằng Three.js (mặt phẳng góc cạnh, viền đậm, tô bóng hoạt hình), dựng trực tiếp mỗi khung hình theo tư thế trận đấu (thở, bước chạy, lấy đà, chém, niệm chú, cánh và hào quang chuyển động). Ảnh được dựng ở độ phân giải 1,25–2 lần theo màn hình để sắc nét. Máy yếu sẽ tự giảm số nhân vật dựng trực tiếp.
- Model ngoài (tuỳ chọn): đặt `models/<id>.glb` và khai báo trong `models/manifest.json`, ví dụ `{"long":{"file":"long.glb","h":1.95,"ry":0,"anims":{"run":"long_run.glb"}}}`. Game tự nạp GLB (kể cả có xương và animation; clip tên chứa idle/run/walk/attack được dùng cho đứng/chạy/ra đòn), chuyển sang cùng phong cách tô bóng và viền. Model ngoài chỉ nạp khi chạy qua http(s), không nạp khi mở tệp trực tiếp.
- Tạo GLB bằng Meshy: `MESHY_API_KEY=... node tools/meshy.mjs --ids long,khe [--rig]` (xem chú thích đầu tệp; `--dry` để xem prompt). Dữ liệu prompt lấy từ `tools/heroes.json`.
