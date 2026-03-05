# -*- coding: utf-8 -*-
"""
Bài Tập 6: Phát Hiện Cạnh (Canny Edge Detection)
Mục tiêu: Hiểu cách phát hiện biên/cạnh với các tham số khác nhau

- Canny sử dụng 2 ngưỡng: thấp (low) và cao (high)
- Cạnh < low: bỏ qua, cạnh > high: giữ lại
- Cạnh giữa low-high: chỉ giữ nếu nối với cạnh mạnh
- Tỉ lệ lý tưởng: high/low = 2:1 hoặc 3:1
- Blur trước giúp giảm nhiễu (noise)
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

    # Canny chỉ hoạt động trên ảnh grayscale (1 kênh)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print("=" * 50)
    print("  BAI TAP 6: EDGE DETECTION (CANNY)")
    print("=" * 50)

    # === HIỂU VỀ CANNY EDGE DETECTION ===
    # cv2.Canny(ảnh, ngưỡng_thấp, ngưỡng_cao)
    #   - ngưỡng_thấp: cạnh dưới mức này bị bỏ (nhiễu)
    #   - ngưỡng_cao: cạnh trên mức này được giữ (cạnh mạnh)
    #   - giữa 2 ngưỡng: chỉ giữ nếu kết nối với cạnh mạnh

    # 3 bộ tham số để so sánh
    params = [
        (50, 150, "Nhieu canh (nguong thap)"),      # Nhạy → nhiều cạnh
        (100, 200, "Can bang (nguong trung binh)"),  # Cân bằng
        (100, 300, "It canh (nguong cao)"),           # Không nhạy → ít cạnh
    ]

    print(f"\n[INFO] Canny Edge Detection su dung 2 nguong:")
    print(f"       - Low threshold:  canh yeu (rejected neu < low)")
    print(f"       - High threshold: canh manh (accepted neu > high)")
    print(f"       - Giua low-high: chi accepted neu ket noi voi canh manh")

    results = []
    for low, high, desc in params:
        # Áp dụng Canny edge detection
        edges = cv2.Canny(gray, low, high)

        # Đếm số pixel cạnh (giá trị > 0 = là cạnh)
        edge_count = np.sum(edges > 0)
        total = edges.size
        edge_pct = edge_count / total * 100

        print(f"\n[Canny({low:3d}, {high:3d})] {desc}")
        print(f"    So pixel canh: {edge_count:,} ({edge_pct:.1f}%)")

        # Thêm nhãn text lên ảnh kết quả
        labeled = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cv2.putText(labeled, f"Canny({low}, {high})", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        results.append(labeled)

    # === GAUSSIAN BLUR TRƯỚC CANNY (giảm nhiễu) ===
    # Làm mờ ảnh trước khi detect cạnh sẽ giảm nhiễu đáng kể
    # GaussianBlur(ảnh, kích_thước_kernel, độ_lệch_chuẩn)
    blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
    edges_blurred = cv2.Canny(blurred, 100, 200)

    edge_count_blur = np.sum(edges_blurred > 0)
    print(f"\n[Blur + Canny(100, 200)] Voi Gaussian Blur truoc")
    print(f"    So pixel canh: {edge_count_blur:,}")
    print(f"    -> Blur giam nhieu (noise) truoc khi detect edge")

    labeled_blur = cv2.cvtColor(edges_blurred, cv2.COLOR_GRAY2BGR)
    cv2.putText(labeled_blur, "Blur+Canny(100,200)", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # === HIỂN THỊ DẠNG LƯỚI ===
    # Hàng trên: (50,150) và (100,200)
    # Hàng dưới: (100,300) và Blur+(100,200)
    top = cv2.hconcat([results[0], results[1]])
    bottom = cv2.hconcat([results[2], labeled_blur])
    grid = cv2.vconcat([top, bottom])

    cv2.imshow("Edge Detection Comparison", grid)
    cv2.imshow("Original", img)
    cv2.imshow("Grayscale", gray)

    print(f"\n[*] Dang hien thi anh. Nhan phim bat ky de dong.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Lưu kết quả
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(os.path.join(output_dir, "ex6_edges_grid.jpg"), grid)
    print(f"\n[DONE] Da luu ket qua vao thu muc output/")


if __name__ == "__main__":
    main()
