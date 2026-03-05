# -*- coding: utf-8 -*-
"""
Bài Tập 1: Đọc và Hiển Thị Ảnh
Mục tiêu: Hiểu ảnh là ma trận (matrix), cấu trúc pixel [B, G, R]

- Ảnh số = mảng NumPy 3 chiều (chiều cao, chiều rộng, kênh màu)
- Mỗi pixel gồm 3 giá trị: Blue, Green, Red (0-255)
- OpenCV dùng thứ tự BGR, KHÔNG phải RGB
"""

import cv2          # Thư viện xử lý ảnh OpenCV
import numpy as np  # Thư viện tính toán ma trận
import os           # Thư viện thao tác đường dẫn file

def main():
    # === BƯỚC 1: Đọc ảnh từ file ===
    # cv2.imread() đọc ảnh và trả về mảng NumPy
    # Mặc định đọc ảnh màu (3 kênh BGR)
    img_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "sample.jpg")
    img = cv2.imread(img_path)

    # Kiểm tra ảnh có đọc được không (None = thất bại)
    if img is None:
        print("[LOI] Khong the doc anh! Hay chay sample_generator.py truoc.")
        print(f"     Duong dan: {os.path.abspath(img_path)}")
        return

    # === BƯỚC 2: Khám phá thuộc tính của ảnh ===
    print("=" * 50)
    print("  BAI TAP 1: DOC VA HIEN THI ANH")
    print("=" * 50)

    # img.shape trả về (chiều_cao, chiều_rộng, số_kênh)
    # - chiều_cao = số hàng pixel (dọc)
    # - chiều_rộng = số cột pixel (ngang)
    # - số_kênh = 3 (BGR) hoặc 1 (grayscale)
    print(f"\n[1] img.shape = {img.shape}")
    print(f"    -> Height (chieu cao) : {img.shape[0]} pixels")
    print(f"    -> Width  (chieu rong): {img.shape[1]} pixels")
    print(f"    -> Channels (kenh mau): {img.shape[2]}")

    # img.dtype cho biết kiểu dữ liệu của mỗi giá trị pixel
    # uint8 = số nguyên không dấu 8-bit = giá trị từ 0 đến 255
    print(f"\n[2] img.dtype = {img.dtype}")
    print(f"    -> Moi gia tri pixel nam trong khoang [0, 255]")

    # Truy cập pixel tại vị trí (0, 0) = góc trái trên
    # OpenCV dùng thứ tự BGR, KHÔNG phải RGB!
    first_pixel = img[0][0]
    print(f"\n[3] Pixel dau tien img[0][0] = {first_pixel}")
    print(f"    -> B (Blue)  = {first_pixel[0]}")
    print(f"    -> G (Green) = {first_pixel[1]}")
    print(f"    -> R (Red)   = {first_pixel[2]}")

    # Truy cập pixel giữa ảnh
    h, w = img.shape[:2]  # Lấy chiều cao và chiều rộng
    center_pixel = img[h // 2][w // 2]
    print(f"\n[4] Pixel giua anh img[{h//2}][{w//2}] = {center_pixel}")

    # Tổng số pixel trong ảnh
    total_pixels = img.shape[0] * img.shape[1]
    print(f"\n[5] Tong so pixel: {total_pixels:,}")
    print(f"    Tong so gia tri: {img.size:,} (pixels x channels)")

    # === BƯỚC 3: Hiển thị ảnh lên màn hình ===
    print(f"\n[*] Dang hien thi anh... Nhan phim bat ky de dong.")

    # cv2.imshow() mở cửa sổ hiển thị ảnh
    # Tham số 1: tên cửa sổ, Tham số 2: mảng ảnh
    cv2.imshow("Bai Tap 1 - Original Image", img)

    # cv2.waitKey(0) đợi vô hạn cho đến khi nhấn phím
    # Trả về mã ASCII của phím đã nhấn
    key = cv2.waitKey(0)
    print(f"    Ban da nhan phim: {chr(key) if key > 0 else 'N/A'}")

    # Đóng tất cả cửa sổ OpenCV
    cv2.destroyAllWindows()
    print("\n[DONE] Hoan thanh Bai Tap 1!")


if __name__ == "__main__":
    main()
