# -*- coding: utf-8 -*-
"""
Bài Tập 5: Threshold (Phân Ngưỡng - Trắng Đen)
Mục tiêu: Hiểu cách ngưỡng ảnh hưởng đến việc phân đoạn ảnh

- Threshold biến ảnh grayscale thành ảnh trắng/đen (binary)
- Pixel > ngưỡng → trắng (255), pixel <= ngưỡng → đen (0)
- Ngưỡng thấp: giữ nhiều chi tiết, ngưỡng cao: chỉ giữ vùng sáng
- Otsu: tự động tìm ngưỡng tối ưu
"""

import cv2          # Thư viện xử lý ảnh
import numpy as np  # Thư viện ma trận
import os           # Thao tác file

def main():
    # Đọc ảnh và chuyển sang grayscale
    img_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "sample.jpg")
    img = cv2.imread(img_path)

    if img is None:
        print("[LOI] Khong the doc anh! Hay chay sample_generator.py truoc.")
        return

    # Chuyển sang xám để threshold (chỉ hoạt động trên 1 kênh)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print("=" * 50)
    print("  BAI TAP 5: THRESHOLD (PHAN TRANG DEN)")
    print("=" * 50)

    # === HIỂU VỀ THRESHOLD ===
    # cv2.threshold(ảnh_xám, giá_trị_ngưỡng, giá_trị_max, kiểu)
    #   - Pixel > giá_trị_ngưỡng → đặt thành giá_trị_max (trắng 255)
    #   - Pixel <= giá_trị_ngưỡng → đặt thành 0 (đen)
    #   - Trả về: (ngưỡng_đã_dùng, ảnh_kết_quả)

    thresholds = [50, 100, 127, 200]  # 4 ngưỡng để so sánh

    print(f"\n[INFO] Anh grayscale: min={gray.min()}, max={gray.max()}")
    print(f"       Mean = {gray.mean():.1f}")
    print(f"\n       Nguong threshold anh huong nhu the nao:")
    print(f"       - Nguong THAP (50)  -> nhieu pixel trang (giu nhieu chi tiet)")
    print(f"       - Nguong CAO  (200) -> it pixel trang (chi giu vung sang)")

    results = []
    for thresh in thresholds:
        # Áp dụng threshold với từng giá trị ngưỡng
        _, binary = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)

        # Đếm số pixel trắng và đen
        white = np.sum(binary == 255)   # Số pixel trắng
        black = np.sum(binary == 0)     # Số pixel đen
        total = binary.size             # Tổng số pixel
        white_pct = white / total * 100 # Tỉ lệ phần trăm trắng

        print(f"\n[Nguong {thresh:3d}] Trang: {white:6,} ({white_pct:.1f}%) | Den: {black:6,} ({100-white_pct:.1f}%)")

        # Thêm nhãn để nhận biết khi hiển thị
        labeled = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        cv2.putText(labeled, f"Thresh={thresh}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        results.append(labeled)

    # === ADAPTIVE THRESHOLD (nâng cao) ===
    # Tự động điều chỉnh ngưỡng theo từng vùng cục bộ
    # Tốt hơn khi độ sáng không đều trên ảnh
    adaptive = cv2.adaptiveThreshold(
        gray, 255,                           # Ảnh đầu vào, giá trị max
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,      # Phương pháp tính ngưỡng cục bộ
        cv2.THRESH_BINARY, 11, 2             # Kiểu, kích thước vùng, hằng số
    )
    print(f"\n[Adaptive] Tu dong dieu chinh nguong cuc bo")
    print(f"           Phu hop khi do sang khong deu")

    # === OTSU THRESHOLD (tự động tìm ngưỡng tối ưu) ===
    # Otsu phân tích histogram để tìm ngưỡng tốt nhất
    otsu_val, otsu_result = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(f"\n[Otsu] Nguong toi uu tu dong: {otsu_val:.0f}")

    # === HIỂN THỊ DẠNG LƯỚI (GRID) ===
    # Hàng trên: ngưỡng 50 và 100
    # Hàng dưới: ngưỡng 127 và 200
    top_row = cv2.hconcat([results[0], results[1]])
    bottom_row = cv2.hconcat([results[2], results[3]])
    grid = cv2.vconcat([top_row, bottom_row])  # Ghép dọc

    cv2.imshow("Threshold Comparison (50 | 100 / 127 | 200)", grid)
    cv2.imshow("Original Grayscale", gray)
    cv2.imshow("Adaptive Threshold", adaptive)
    cv2.imshow(f"Otsu Threshold (auto={otsu_val:.0f})", otsu_result)

    print(f"\n[*] Dang hien thi anh. Nhan phim bat ky de dong.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Lưu kết quả
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(os.path.join(output_dir, "ex5_threshold_grid.jpg"), grid)
    print(f"\n[DONE] Da luu ket qua vao thu muc output/")


if __name__ == "__main__":
    main()
