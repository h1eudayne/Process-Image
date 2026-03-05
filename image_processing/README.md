## 📦 Cài Đặt (Chỉ Làm 1 Lần)

**Bước 1:** Mở PowerShell, di chuyển vào thư mục dự án:

```powershell
cd image_processing
```

**Bước 2:** Tạo và kích hoạt môi trường ảo:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Bước 3:** Cài thư viện:

```powershell
pip install -r requirements.txt
```

**Bước 4:** Tạo ảnh mẫu để dùng cho các bài tập:

```powershell
python assets/sample_generator.py
```

> ⚠️ Mỗi lần mở PowerShell mới, bạn cần chạy lại lệnh activate:
>
> ```powershell
> cd d:\Process_Image\image_processing
> .\venv\Scripts\activate
> ```

---

## 📚 TUẦN 1 — Pixel Thinking (Hiểu Ảnh Là Gì)

### Bài 1: Đọc và Hiển Thị Ảnh

```powershell
python exercises/week1/ex1_read_display.py
```

**Bạn sẽ học:** Ảnh = ma trận NumPy `(height, width, 3)`, mỗi pixel = `[B, G, R]` từ 0-255.

**Thao tác:** Nhấn **phím bất kỳ trên cửa sổ ảnh** để đóng.

---

### Bài 2: Tự Sửa Pixel

```powershell
python exercises/week1/ex2_modify_pixels.py
```

**Bạn sẽ học:** Thao tác pixel trực tiếp bằng NumPy slicing `img[y1:y2, x1:x2] = [B, G, R]`.

**Thao tác:** Nhấn **phím bất kỳ trên cửa sổ ảnh** để đóng. Kết quả lưu vào `output/`.

---

### Bài 3: Resize và Crop

```powershell
python exercises/week1/ex3_resize_crop.py
```

**Bạn sẽ học:** `cv2.resize()` thay đổi kích thước, crop bằng slicing `img[y1:y2, x1:x2]`.

**Thao tác:** Nhấn **phím bất kỳ trên cửa sổ ảnh** để đóng. Kết quả lưu vào `output/`.

---

### 🎯 Mini Project 1: Camera Capture

```powershell
python projects/mini_project_1_camera.py
```

**Bạn sẽ học:** `VideoCapture` đọc frame từ webcam, vòng lặp real-time, xử lý phím bấm.

**Thao tác:**

- Nhấn **`s`** trên cửa sổ camera → Chụp và lưu ảnh vào `output/`
- Nhấn **`q`** trên cửa sổ camera → Thoát chương trình

> 💡 Nếu camera không mở được: vào **Settings → Privacy → Camera** → bật **"Let desktop apps access your camera"**

---

## 📚 TUẦN 2 — Xử Lý Ảnh Cơ Bản

### Bài 4: Chuyển Ảnh Sang Grayscale

```powershell
python exercises/week2/ex4_grayscale.py
```

**Bạn sẽ học:** 3 cách chuyển grayscale, công thức `Y = 0.299R + 0.587G + 0.114B`, tách kênh B/G/R.

**Thao tác:** Nhấn **phím bất kỳ trên cửa sổ ảnh** để đóng.

---

### Bài 5: Threshold (Phân Ngưỡng)

```powershell
python exercises/week2/ex5_threshold.py
```

**Bạn sẽ học:** Phân ảnh trắng/đen với 4 ngưỡng (50, 100, 127, 200), Adaptive Threshold, Otsu tự động.

**Thao tác:** Nhấn **phím bất kỳ trên cửa sổ ảnh** để đóng.

---

### Bài 6: Edge Detection (Phát Hiện Cạnh)

```powershell
python exercises/week2/ex6_edge_detection.py
```

**Bạn sẽ học:** Canny edge với 3 bộ tham số, Gaussian Blur giảm nhiễu, tỉ lệ ngưỡng high/low.

**Thao tác:** Nhấn **phím bất kỳ trên cửa sổ ảnh** để đóng.

---

### Bài 7: Contour Detection (Phát Hiện Vật Thể)

```powershell
python exercises/week2/ex7_contour_detection.py
```

**Bạn sẽ học:** Tìm đường viền, vẽ bounding box, phân loại hình dạng (tam giác/vuông/tròn), đếm objects.

**Thao tác:** Nhấn **phím bất kỳ trên cửa sổ ảnh** để đóng.

---

## 📁 Cấu Trúc Thư Mục

```
image_processing/
├── assets/                  # Ảnh mẫu + script tạo ảnh
│   ├── sample_generator.py
│   └── sample.jpg           # (tạo khi chạy sample_generator)
├── exercises/
│   ├── week1/               # Bài tập tuần 1 (ex1-ex3)
│   └── week2/               # Bài tập tuần 2 (ex4-ex7)
├── projects/
│   └── mini_project_1_camera.py
├── output/                  # Kết quả ảnh (tự sinh khi chạy)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 💡 Kiến Thức Cốt Lõi

| Khái niệm         | Giải thích                                      |
| ----------------- | ----------------------------------------------- |
| **Ảnh = Ma trận** | Mảng NumPy `(height, width, channels)`          |
| **BGR**           | OpenCV dùng Blue-Green-Red, KHÔNG phải RGB      |
| **Pixel**         | `[B, G, R]`, mỗi giá trị 0-255                  |
| **Grayscale**     | 1 kênh, `Y = 0.299R + 0.587G + 0.114B`          |
| **Threshold**     | Phân ảnh trắng/đen dựa trên ngưỡng              |
| **Canny Edge**    | Phát hiện cạnh bằng 2 ngưỡng (low, high)        |
| **Contour**       | Đường viền bao quanh vật thể → object detection |

---

## 🔗 Pipeline Xử Lý Ảnh

```
Ảnh gốc → Grayscale → Threshold/Edge → Contour → Nhận dạng vật thể
  (EX1)     (EX4)       (EX5/EX6)       (EX7)        🎯
```
