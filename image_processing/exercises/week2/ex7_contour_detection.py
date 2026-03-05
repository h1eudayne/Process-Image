# -*- coding: utf-8 -*-
"""
Bài Tập 7: Phát Hiện Đường Viền (Contour Detection)
Mục tiêu: Tìm, vẽ, và đếm vật thể bằng contour

- Contour = đường viền bao quanh vật thể
- Pipeline: Ảnh gốc → Grayscale → Blur → Threshold → findContours
- Phân loại hình dạng: 3 đỉnh = tam giác, 4 = vuông, >5 = tròn
- Nền tảng của object detection trong xử lý ảnh
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
    print("  BAI TAP 7: CONTOUR DETECTION")
    print("=" * 50)

    # === BƯỚC 1: Tiền xử lý ảnh ===

    # Chuyển sang grayscale (1 kênh)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Làm mờ để giảm nhiễu, giúp contour chính xác hơn
    # (5, 5) = kích thước kernel, 0 = tự động tính sigma
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold nghịch đảo: vật thể = trắng, nền = đen
    # THRESH_BINARY_INV: ngược lại với BINARY (đen/trắng đảo ngược)
    _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)

    print(f"\n[1] Tien xu ly:")
    print(f"    Anh goc -> Grayscale -> Blur -> Threshold (nghich dao)")
    print(f"    THRESH_BINARY_INV: vat the = trang, nen = den")

    # === BƯỚC 2: Tìm contour ===

    # findContours tìm đường viền trên ảnh nhị phân (trắng/đen)
    # RETR_EXTERNAL: chỉ lấy contour ngoài cùng (bỏ qua contour lồng nhau)
    # CHAIN_APPROX_SIMPLE: nén các đoạn thẳng thành 2 điểm đầu cuối
    contours, hierarchy = cv2.findContours(
        thresh,                      # Ảnh nhị phân đầu vào
        cv2.RETR_EXTERNAL,           # Chỉ lấy contour ngoài cùng
        cv2.CHAIN_APPROX_SIMPLE      # Nén điểm để tiết kiệm bộ nhớ
    )

    print(f"\n[2] Tim contour:")
    print(f"    So contour tim duoc: {len(contours)}")
    print(f"    Mode: RETR_EXTERNAL (chi lay contour ngoai cung)")

    # === BƯỚC 3: Phân tích từng contour ===

    print(f"\n[3] Phan tich tung contour:")
    print(f"    {'#':>3} | {'Dien tich':>10} | {'Chu vi':>10} | {'Dinh':>5} | Hinh dang")
    print(f"    {'-'*3}-+-{'-'*10}-+-{'-'*10}-+-{'-'*5}-+----------")

    # Tạo bản sao để vẽ lên (không làm hỏng ảnh gốc)
    img_contours = img.copy()  # Để vẽ đường viền
    img_boxes = img.copy()     # Để vẽ bounding box

    # Màu sắc cho từng contour (BGR)
    colors = [
        (255, 0, 0),    # Xanh dương
        (0, 255, 0),    # Xanh lá
        (0, 0, 255),    # Đỏ
        (255, 255, 0),  # Xanh nhạt (Cyan)
        (0, 255, 255),  # Vàng
        (255, 0, 255),  # Tím (Magenta)
    ]

    min_area = 100  # Lọc nhiễu: bỏ contour nhỏ hơn 100 pixel
    valid_contours = []

    for i, contour in enumerate(contours):
        # Tính diện tích contour (số pixel bên trong)
        area = cv2.contourArea(contour)

        # Bỏ qua contour quá nhỏ (nhiễu)
        if area < min_area:
            continue

        valid_contours.append(contour)

        # Tính chu vi (độ dài đường viền)
        # True = đường viền khép kín
        perimeter = cv2.arcLength(contour, True)

        # Xấp xỉ hình dạng contour
        # epsilon = độ chính xác xấp xỉ (nhỏ hơn = chính xác hơn)
        epsilon = 0.04 * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)
        vertices = len(approx)  # Số đỉnh của hình xấp xỉ

        # Phân loại hình dạng dựa trên số đỉnh
        if vertices == 3:
            shape = "Tam giac"        # 3 đỉnh = tam giác
        elif vertices == 4:
            # Kiểm tra vuông hay chữ nhật bằng tỉ lệ cạnh
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            shape = "Hinh vuong" if 0.9 <= aspect_ratio <= 1.1 else "Hinh chu nhat"
        elif vertices == 5:
            shape = "Ngu giac"        # 5 đỉnh = ngũ giác
        elif vertices > 5:
            shape = "Hinh tron / Ellipse"  # Nhiều đỉnh = tròn
        else:
            shape = "Khong xac dinh"

        # Chọn màu cho contour này
        color = colors[len(valid_contours) % len(colors)]

        print(f"    {len(valid_contours):3d} | {area:10,.0f} | {perimeter:10.1f} | {vertices:5d} | {shape}")

        # Vẽ đường viền contour lên ảnh
        # -1 = vẽ tất cả các điểm, 2 = độ dày nét vẽ
        cv2.drawContours(img_contours, [contour], -1, color, 2)

        # Vẽ bounding box (hình chữ nhật bao quanh)
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img_boxes, (x, y), (x + w, y + h), color, 2)

        # Thêm nhãn text phía trên bounding box
        cv2.putText(img_boxes, f"#{len(valid_contours)} {shape}",
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    # === BƯỚC 4: Tổng kết ===

    print(f"\n[4] Tong ket:")
    print(f"    Tong contour: {len(contours)}")
    print(f"    Contour hop le (area > {min_area}): {len(valid_contours)}")
    print(f"    So object detect duoc: {len(valid_contours)}")

    # === HIỂN THỊ KẾT QUẢ ===
    cv2.imshow("Original", img)
    cv2.imshow("Threshold", thresh)
    cv2.imshow("Contours", img_contours)
    cv2.imshow("Bounding Boxes + Labels", img_boxes)

    print(f"\n[*] Dang hien thi 4 cua so. Nhan phim bat ky de dong.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Lưu kết quả
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(os.path.join(output_dir, "ex7_contours.jpg"), img_contours)
    cv2.imwrite(os.path.join(output_dir, "ex7_bounding_boxes.jpg"), img_boxes)
    print(f"\n[DONE] Da luu ket qua vao thu muc output/")


if __name__ == "__main__":
    main()
