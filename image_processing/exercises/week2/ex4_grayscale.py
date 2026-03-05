# -*- coding: utf-8 -*-
"""
Bài Tập 4: Chuyển Ảnh Sang Grayscale
Mục tiêu: Hiểu cách chuyển đổi không gian màu và sự khác nhau giữa các kênh

- Grayscale = ảnh xám, chỉ có 1 kênh (0-255)
- Công thức: Y = 0.299*R + 0.587*G + 0.114*B
- Mắt người nhạy nhất với màu xanh lá → trọng số G lớn nhất
"""

import cv2          # Thư viện xử lý ảnh
import numpy as np  # Thư viện tính toán ma trận
import os           # Thao tác file

def main():
    # Đọc ảnh mẫu
    img_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "sample.jpg")
    img = cv2.imread(img_path)

    if img is None:
        print("[LOI] Khong the doc anh! Hay chay sample_generator.py truoc.")
        return

    print("=" * 50)
    print("  BAI TAP 4: CHUYEN ANH SANG GRAYSCALE")
    print("=" * 50)

    # === CÁCH 1: Dùng cvtColor (phổ biến nhất) ===
    # cv2.cvtColor() chuyển đổi giữa các không gian màu
    # BGR2GRAY áp dụng công thức: Y = 0.299*R + 0.587*G + 0.114*B
    # (trung bình có trọng số - mắt người nhạy nhất với xanh lá)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print(f"\n[1] cvtColor (BGR -> GRAY)")
    print(f"    Anh goc       : shape = {img.shape}, dtype = {img.dtype}")
    print(f"    Anh grayscale : shape = {gray.shape}, dtype = {gray.dtype}")
    print(f"    -> Tu 3 channels (BGR) xuong 1 channel (do sang)")

    # So sánh giá trị pixel trước và sau
    print(f"\n    Pixel goc [0][0]  : B={img[0][0][0]}, G={img[0][0][1]}, R={img[0][0][2]}")
    print(f"    Pixel gray [0][0] : {gray[0][0]}")
    print(f"    (Tinh: 0.299*{img[0][0][2]} + 0.587*{img[0][0][1]} + 0.114*{img[0][0][0]} ~= {gray[0][0]})")

    # === CÁCH 2: Đọc ảnh trực tiếp dạng grayscale ===
    # Truyền IMREAD_GRAYSCALE khi đọc file → ảnh chỉ có 1 kênh
    gray_direct = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    print(f"\n[2] Doc truc tiep bang IMREAD_GRAYSCALE:")
    print(f"    shape = {gray_direct.shape}")

    # === CÁCH 3: Tự tính bằng công thức (hiểu bản chất) ===
    # cv2.split() tách ảnh thành 3 kênh riêng biệt
    b, g, r = cv2.split(img)

    # Áp dụng công thức chuyển đổi thủ công
    gray_manual = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
    print(f"\n[3] Tu tinh bang cong thuc:")
    print(f"    Y = 0.299*R + 0.587*G + 0.114*B")
    print(f"    shape = {gray_manual.shape}")

    # === HIỂN THỊ TỪNG KÊNH MÀU ===
    # Mỗi kênh là ảnh grayscale riêng:
    # - Kênh B: sáng ở vùng màu xanh dương
    # - Kênh G: sáng ở vùng màu xanh lá
    # - Kênh R: sáng ở vùng màu đỏ
    print(f"\n[4] Cac kenh mau rieng le:")
    print(f"    Blue  channel: shape = {b.shape}")
    print(f"    Green channel: shape = {g.shape}")
    print(f"    Red   channel: shape = {r.shape}")

    # Hiển thị ảnh gốc và grayscale
    cv2.imshow("Original (BGR)", img)
    cv2.imshow("Grayscale (cvtColor)", gray)

    # Ghép 3 kênh cạnh nhau để so sánh
    # Phải chuyển GRAY→BGR vì imshow cần 3 kênh để hiển thị
    channels = cv2.hconcat([
        cv2.cvtColor(b, cv2.COLOR_GRAY2BGR),  # Kênh Blue
        cv2.cvtColor(g, cv2.COLOR_GRAY2BGR),  # Kênh Green
        cv2.cvtColor(r, cv2.COLOR_GRAY2BGR),  # Kênh Red
    ])
    cv2.imshow("Channels: B | G | R", channels)

    print(f"\n[*] Dang hien thi anh. Nhan phim bat ky de dong.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Lưu kết quả
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(os.path.join(output_dir, "ex4_grayscale.jpg"), gray)
    print(f"\n[DONE] Da luu ket qua vao thu muc output/")


if __name__ == "__main__":
    main()
