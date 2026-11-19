# Nhẫn Giới Hải Vân

Game đấu tướng theo lượt chạy trên trình duyệt: 40 nhẫn giả (B đến SSS), đội 6 người, Nộ chung, combo Truy Kích, kỹ năng phụ, thiên phú, Điểm Tốc, ngũ hành tương khắc, chiêu mộ, trang bị, đột phá, thức tỉnh, Duyên, đồ giám, linh thú, vượt ải 5 chương, tháp 100 tầng, boss thế giới, phó bản, cửa hàng, đấu trường, nhiệm vụ và thành tựu.

Chơi tại: https://benphandz.github.io/nhan-gioi-hai-van/

- Toàn bộ nhân vật, làng và chiêu thức là sáng tác riêng, lấy cảm hứng từ địa danh Đà Nẵng và truyền thuyết dân gian Việt Nam.
- Tiến trình lưu trong trình duyệt của người chơi (localStorage).
- Chỉ gồm một tệp `index.html`, không cần cài đặt.

## Nhân vật 3D

- Mặc định: model low-poly dựng bằng Three.js (mặt phẳng góc cạnh, viền đậm, tô bóng hoạt hình), dựng trực tiếp mỗi khung hình theo tư thế trận đấu (thở, bước chạy, lấy đà, chém, niệm chú, cánh và hào quang chuyển động). Ảnh được dựng ở độ phân giải 1,25–2 lần theo màn hình để sắc nét. Máy yếu sẽ tự giảm số nhân vật dựng trực tiếp.
- Model ngoài (tuỳ chọn): đặt `models/<id>.glb` và khai báo trong `models/manifest.json`, ví dụ `{"long":{"file":"long.glb","h":1.95,"ry":0,"anims":{"run":"long_run.glb"}}}`. Game tự nạp GLB (kể cả có xương và animation; clip tên chứa idle/run/walk/attack được dùng cho đứng/chạy/ra đòn), chuyển sang cùng phong cách tô bóng và viền. Model ngoài chỉ nạp khi chạy qua http(s), không nạp khi mở tệp trực tiếp.
- Tạo GLB bằng Tripo hoặc Meshy: `node tools/tripo.mjs --ids giong,hungdao,longmau,sontinh,haibatrung [--rig]` hoặc `node tools/meshy.mjs --ids ... [--rig]` (khoá qua `TRIPO_API_KEY` / `MESHY_API_KEY`; `--dry` để xem prompt). Prompt dùng chung ở `tools/prompt.mjs`, tướng chủ lực có mô tả riêng.
- Model GLB vẫn giữ hiệu ứng thức tỉnh: I vòng nguyên tố + ánh phát sáng, II cánh, III cánh vàng + áo choàng + hào quang.

## Mô hình nhân vật VRoid
- `models/vroid_nam.glb`: mẫu do chủ dự án dựng bằng VRoid Studio (pixiv).
- `models/vroid_nu.glb`: mẫu chính thức `VRM1_Constraint_Twist_Sample` của pixiv Inc., giấy phép VRM Public License 1.0 (cho phép dùng thương mại, chỉnh sửa và phân phối lại; không bắt buộc ghi công). (c) 2022 pixiv Inc.
- Trang phục, kiểu tóc, râu, phụ kiện và chuyển động khớp được tạo bằng code trong `index.html` (mục 21).
