# -*- coding: utf-8 -*-
"""
Bài Tập 3: Resize và Crop
Mục tiêu: Làm chủ việc thay đổi kích thước và cắt vùng ảnh

- Resize (thay đổi kích thước) bằng cv2.resize()
- Crop (cắt vùng ảnh) bằng NumPy slicing
- Hiểu các phương pháp nội suy (interpolation)
"""

import cv2          # Thư viện xử lý ảnh
import numpy as np  # Thư viện ma trận
import os           # Thao tác file

def main():
    # Đọc ảnh mẫu
    img_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "sample.jpg")
    img = cv2.imread(img_path)

    if img is None:
        print("[LOI] Khong the doc anh! Hay chay sample_generator.py truoc.")
        return

    print("=" * 50)
    print("  BAI TAP 3: RESIZE VA CROP")
    print("=" * 50)

    h, w = img.shape[:2]  # Lấy chiều cao và rộng
    print(f"\n[INFO] Anh goc: {w}x{h} pixels")

    # === PHẦN A: Resize xuống 50% ===

    # cv2.resize(ảnh_gốc, (chiều_rộng_mới, chiều_cao_mới))
    # CHÚ Ý: resize nhận (width, height), KHÔNG phải (height, width)!
    new_w = w // 2  # Chiều rộng mới = 50%
    new_h = h // 2  # Chiều cao mới = 50%
    resized = cv2.resize(img, (new_w, new_h))

    print(f"\n[A] Resize 50%:")
    print(f"    Goc  : {w}x{h}")
    print(f"    Moi  : {resized.shape[1]}x{resized.shape[0]}")

    # Cách khác: dùng tỉ lệ fx, fy (0.5 = giảm 50%)
    resized_fx = cv2.resize(img, None, fx=0.5, fy=0.5)
    print(f"    (Cach fx/fy): {resized_fx.shape[1]}x{resized_fx.shape[0]}")

    cv2.imshow("A - Resized 50%", resized)

    # === PHẦN B: Các phương pháp nội suy (Interpolation) ===

    # INTER_NEAREST: nhanh nhất, hình vuông (tốt cho pixel art)
    # INTER_LINEAR : mặc định, cân bằng tốc độ và chất lượng
    # INTER_CUBIC  : chất lượng cao hơn, chậm hơn
    # INTER_AREA   : tốt nhất khi thu nhỏ ảnh
    resized_nearest = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
    resized_cubic = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    print(f"\n[B] Cac phuong phap noi suy (interpolation):")
    print(f"    INTER_NEAREST: Nhanh, hinh vuong (pixel art)")
    print(f"    INTER_LINEAR : Mac dinh, can bang")
    print(f"    INTER_CUBIC  : Chat luong cao, cham hon")

    # === PHẦN C: Crop vùng giữa ảnh ===

    # Crop chỉ là cắt mảng NumPy: img[y1:y2, x1:x2]
    # Ta muốn cắt vùng giữa 50% của ảnh
    crop_h = h // 4  # Bỏ 25% trên và 25% dưới
    crop_w = w // 4  # Bỏ 25% trái và 25% phải
    y1 = crop_h          # Điểm bắt đầu y
    y2 = h - crop_h      # Điểm kết thúc y
    x1 = crop_w          # Điểm bắt đầu x
    x2 = w - crop_w      # Điểm kết thúc x
    cropped = img[y1:y2, x1:x2]  # Cắt vùng giữa

    print(f"\n[C] Crop vung giua:")
    print(f"    Vung cat: ({x1},{y1}) -> ({x2},{y2})")
    print(f"    Kich thuoc: {cropped.shape[1]}x{cropped.shape[0]}")

    cv2.imshow("C - Cropped Center", cropped)

    # === PHẦN D: Crop góc trái trên ===

    # Lấy 1/4 ảnh phía trái trên
    quarter = img[0:h//2, 0:w//2]
    print(f"\n[D] Crop goc trai tren:")
    print(f"    Kich thuoc: {quarter.shape[1]}x{quarter.shape[0]}")

    cv2.imshow("D - Top-Left Quarter", quarter)

    # Hiển thị ảnh gốc để so sánh
    cv2.imshow("Original", img)

    print(f"\n[*] Dang hien thi 4 cua so. Nhan phim bat ky de dong.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Lưu kết quả
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(os.path.join(output_dir, "ex3_resized_50.jpg"), resized)
    cv2.imwrite(os.path.join(output_dir, "ex3_cropped_center.jpg"), cropped)
    print(f"\n[DONE] Da luu ket qua vao thu muc output/")


if __name__ == "__main__":
    main()
