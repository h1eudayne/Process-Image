# -*- coding: utf-8 -*-
"""
Mini Project 1: Chụp Ảnh Từ Camera
Mục tiêu: Mở webcam, hiển thị hình ảnh trực tiếp, lưu ảnh bằng bàn phím

Điều khiển:
    s - Chụp và lưu ảnh vào thư mục output/
    q - Thoát chương trình

Kiến thức:
- VideoCapture: đọc frame liên tục từ camera
- Vòng lặp real-time xử lý từng frame
- Xử lý sự kiện bàn phím (keyboard event)
- Quản lý tài nguyên: release() camera khi kết thúc
"""

import cv2          # Thư viện xử lý ảnh
import os           # Thao tác file và thư mục
from datetime import datetime  # Lấy thời gian hiện tại (đặt tên file)


def try_open_camera():
    """Thử nhiều backend để mở camera (fix lỗi trên Windows).

    OpenCV 4.10 trên Windows có thể gặp lỗi với backend mặc định.
    Hàm này thử lần lượt: DSHOW → MSMF → Default với nhiều index.
    """

    # Fix cho OpenCV 4.10.x trên Windows: tắt hardware transforms
    # Thiết lập này giúp tránh lỗi "Camera index out of range"
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

    # Danh sách các backend và index để thử
    # (tên_backend, index_camera, mã_backend)
    attempts = [
        ("DSHOW",   0, cv2.CAP_DSHOW),   # DirectShow - phổ biến trên Windows
        ("MSMF",    0, cv2.CAP_MSMF),     # Media Foundation
        ("Default", 0, cv2.CAP_ANY),      # Tự động chọn backend
        ("DSHOW",   1, cv2.CAP_DSHOW),    # Thử index 1 (camera thứ 2)
        ("MSMF",    1, cv2.CAP_MSMF),     # Thử index 1 với MSMF
    ]

    for name, idx, backend in attempts:
        print(f"    Thu {name} (index={idx})...", end=" ")

        # Mở camera với backend và index cụ thể
        cap = cv2.VideoCapture(idx, backend)

        if cap.isOpened():
            # Camera mở được, thử đọc 1 frame để xác nhận
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"-> OK!")
                return cap  # Trả về camera đã mở thành công
            else:
                print(f"-> Mo duoc nhung khong doc duoc frame")
                cap.release()  # Giải phóng camera
        else:
            print(f"-> Khong kha dung")

    return None  # Không tìm thấy camera nào


def main():
    print("=" * 50)
    print("  MINI PROJECT 1: CAMERA CAPTURE")
    print("=" * 50)

    # === BƯỚC 1: Mở webcam ===
    print("\n[*] Dang tim camera...")
    cap = try_open_camera()

    # Kiểm tra camera có mở được không
    if cap is None:
        print("\n[LOI] Khong the mo camera!")
        print("      Thu kiem tra:")
        print("      - Camera co duoc ket noi khong?")
        print("      - Co ung dung nao khac dang dung camera?")
        print("      - Vao Settings > Privacy > Camera > bat quyen truy cap")
        return

    # Lấy thông tin camera
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # Chiều rộng frame
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Chiều cao frame
    fps = cap.get(cv2.CAP_PROP_FPS)                     # Số frame/giây

    print(f"\n[OK] Camera da mo thanh cong!")
    print(f"     Do phan giai: {frame_w}x{frame_h}")
    print(f"     FPS: {fps}")
    print(f"\n     Phim 's' = Luu anh")
    print(f"     Phim 'q' = Thoat")
    print(f"-" * 50)

    # Tạo thư mục output nếu chưa có
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(output_dir, exist_ok=True)

    save_count = 0  # Đếm số ảnh đã lưu

    # === BƯỚC 2: Vòng lặp chính - đọc và hiển thị frame ===
    while True:
        # cap.read() trả về:
        # - ret: True/False (đọc frame thành công hay không)
        # - frame: mảng NumPy của frame (giống như imread)
        ret, frame = cap.read()

        if not ret:
            print("[LOI] Khong the doc frame tu camera!")
            break

        # Tạo bản sao để vẽ text lên (không làm hỏng frame gốc)
        display_frame = frame.copy()

        # Thêm text hướng dẫn lên góc trái trên
        cv2.putText(display_frame, "Press 's' to SAVE | 'q' to QUIT",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Hiển thị số ảnh đã lưu
        cv2.putText(display_frame, f"Saved: {save_count}",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)

        # Hiển thị frame lên cửa sổ
        cv2.imshow("Camera - Mini Project 1", display_frame)

        # === BƯỚC 3: Xử lý phím nhấn ===
        # waitKey(1) đợi 1ms cho phím nhấn (giữ vòng lặp chạy liên tục)
        # & 0xFF lấy 8 bit cuối (cần thiết trên một số hệ thống)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            # Phím 's': Lưu frame hiện tại với tên file theo thời gian
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"capture_{timestamp}.jpg"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, frame)  # Lưu frame gốc (không có text)
            save_count += 1
            print(f"[SAVED] {filename} ({frame.shape[1]}x{frame.shape[0]})")

        elif key == ord('q'):
            # Phím 'q': Thoát vòng lặp
            print(f"\n[QUIT] Thoat chuong trinh.")
            break

    # === BƯỚC 4: Dọn dẹp tài nguyên ===
    # QUAN TRỌNG: Luôn giải phóng camera và đóng cửa sổ khi kết thúc
    cap.release()            # Giải phóng camera
    cv2.destroyAllWindows()  # Đóng tất cả cửa sổ OpenCV

    print(f"\n[DONE] Da luu {save_count} anh vao thu muc output/")
    print(f"       Camera da duoc giai phong.")


if __name__ == "__main__":
    main()
