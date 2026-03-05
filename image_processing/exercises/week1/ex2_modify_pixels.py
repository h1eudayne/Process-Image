# -*- coding: utf-8 -*-
"""
Bài Tập 2: Tự Sửa Pixel
Mục tiêu: Hiểu cách thao tác trực tiếp lên pixel bằng NumPy

- Tô màu 1 vùng ảnh thành màu đỏ
- Chuyển nửa ảnh sang grayscale
- Hiểu cách dùng NumPy slicing để sửa vùng ảnh
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
    print("  BAI TAP 2: TU SUA PIXEL")
    print("=" * 50)

    h, w = img.shape[:2]  # Lấy chiều cao và chiều rộng

    # === PHẦN A: Tô vùng 100x100 pixel thành màu ĐỎ ===

    # Tạo bản sao để giữ nguyên ảnh gốc (copy() tạo bản độc lập)
    img_red = img.copy()

    # Trong OpenCV, màu đỏ = [B=0, G=0, R=255]
    # Cách truy cập vùng ảnh: img[y_bắt_đầu:y_kết_thúc, x_bắt_đầu:x_kết_thúc]
    # Vùng này là hình vuông 100x100 bắt đầu từ điểm (50, 50)
    img_red[50:150, 50:150] = [0, 0, 255]

    print(f"\n[A] Da to vung (50,50) -> (150,150) thanh mau DO")
    print(f"    Kich thuoc vung: 100x100 pixels")
    print(f"    Gia tri: [B=0, G=0, R=255]")

    # Hiển thị kết quả phần A
    cv2.imshow("A - Red Region (100x100)", img_red)

    # === PHẦN B: Chuyển nửa bên phải sang Grayscale ===

    img_half = img.copy()  # Tạo bản sao mới

    # Bước 1: Lấy nửa bên phải của ảnh
    mid = w // 2  # Tính vị trí giữa theo chiều ngang
    right_half = img_half[:, mid:]  # Lấy từ cột giữa đến hết

    # Bước 2: Chuyển nửa phải sang grayscale (1 kênh)
    # cvtColor đổi không gian màu, BGR2GRAY: từ 3 kênh xuống 1 kênh
    gray_half = cv2.cvtColor(right_half, cv2.COLOR_BGR2GRAY)

    # Bước 3: Chuyển ngược lại thành 3 kênh để ghép vào ảnh gốc
    # Vì ảnh gốc có 3 kênh, không thể ghép ảnh 1 kênh vào
    # GRAY2BGR nhân bản giá trị xám ra cả 3 kênh (B=G=R=gray)
    gray_half_bgr = cv2.cvtColor(gray_half, cv2.COLOR_GRAY2BGR)

    # Bước 4: Thay thế nửa phải bằng phiên bản grayscale
    img_half[:, mid:] = gray_half_bgr

    print(f"\n[B] Da chuyen nua ben phai sang Grayscale")
    print(f"    Nua trai: giu nguyen BGR (3 channels)")
    print(f"    Nua phai: grayscale -> BGR (gray values x3)")
    print(f"    Ranh gioi tai cot: {mid}")

    cv2.imshow("B - Half Grayscale", img_half)

    # === PHẦN C: So sánh trước/sau ===
    # cv2.hconcat() ghép 2 ảnh theo chiều ngang (horizontal)
    comparison = cv2.hconcat([img, img_half])
    cv2.imshow("C - So sanh: Goc (trai) vs Sua (phai)", comparison)

    print(f"\n[*] Dang hien thi 3 cua so. Nhan phim bat ky de dong.")
    cv2.waitKey(0)       # Đợi nhấn phím
    cv2.destroyAllWindows()  # Đóng tất cả cửa sổ

    # Lưu kết quả vào thư mục output
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "output")
    os.makedirs(output_dir, exist_ok=True)  # Tạo thư mục nếu chưa có
    cv2.imwrite(os.path.join(output_dir, "ex2_red_region.jpg"), img_red)
    cv2.imwrite(os.path.join(output_dir, "ex2_half_gray.jpg"), img_half)
    print(f"\n[DONE] Da luu ket qua vao thu muc output/")


if __name__ == "__main__":
    main()
