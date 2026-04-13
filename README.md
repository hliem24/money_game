<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
   Money Game - Hand Tracking Project 
</h2>
<div align="center">
    <p align="center">
        <img src="docs/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

## 📝 1. Giới thiệu hệ thống

Ứng dụng **Money Game** sử dụng công nghệ nhận diện bàn tay thời gian thực, cho phép người chơi tương tác với thế giới ảo mà không cần chuột hay bàn phím.

- **Cơ chế**: Sử dụng Webcam để bắt tọa độ bàn tay, điều khiển giỏ hứng vật phẩm rơi từ trên màn hình.
- **Chế độ chơi**: 
    - **Vô tận (Endless)**: Thử thách khả năng phản xạ với độ khó tăng dần.
    - **Theo màn (Level)**: Hệ thống 4 màn chơi với độ khó khác nhau và cốt truyện dẫn dắt.
- **Tính năng đặc biệt**: 
    - **Boss Mode**: Xuất hiện ở các màn cao, yêu cầu người chơi vừa hứng vật phẩm vừa tấn công Boss và né đạn.
    - **Hệ thống Item**: Đa dạng từ vật phẩm tăng điểm, hồi máu đến các hiệu ứng hỗ trợ như đóng băng thời gian, tăng tốc độ.

## 🛠 2. Công nghệ sử dụng

- **Ngôn ngữ**: Python 3.9+
- **Thư viện chính**:
    - **OpenCV**: Xử lý luồng video và đồ họa 2D.
    - **MediaPipe**: Thư viện AI hỗ trợ nhận diện 21 điểm mốc (landmarks) trên bàn tay.
    - **NumPy**: Tính toán ma trận hình ảnh và xử lý hiệu ứng.
    - **ctypes**: Tối ưu giao diện theo độ phân giải màn hình thực tế.

## 📂 3. Cấu trúc thư mục

- `main.py`: Tệp thực thi chính, quản lý vòng lặp và trạng thái trò chơi.
- `hand_tracking.py`: Xử lý logic AI nhận diện bàn tay từ Webcam.
- `game.py`: Chứa logic lõi (tính điểm, va chạm, quản lý vật phẩm).
- `ui.py`: Định nghĩa giao diện người dùng (nút bấm, thanh máu, bảng điểm).
- `story.py`: Chứa dữ liệu kịch bản và lời thoại nhân vật.
- `assets/`: Thư mục chứa tài nguyên ảnh (.png) và âm thanh.
*/


## 🚀 4. Hình ảnh các chức năng

<p align="center">
  <img src="docs/project photo/1..png" alt="Ảnh 1" width="800"/>
</p>

<p align="center">
  <em>Các mode trong GAME  </em>
</p>

<p align="center">
  <img src="docs/project photo/2..png" alt="Ảnh 2" width="700"/>
</p>
<p align="center">
  <em>Client hướng dẫn  </em>
</p>


<p align="center">
  <img src="docs/project photo/3..png" alt="Ảnh 3" width="500"/>
 
</p>
<p align="center">
  <em> Client chơi màn  </em>
</p>

<p align="center">
    <img src="docs/project photo/4..png" alt="Ảnh 4" width="450"/>
</p>
<p align="center">
  <em> Giao diện khi vào chơi  </em>
</p>
<p align="center">
    <img src="docs/project photo/5...png" alt="Ảnh 5" width="450"/>
</p>
<p align="center">
  <em> Màn khi mình thua   </em>
</p>
<p align="center">
    <img src="docs/project photo/6..png" alt="Ảnh 6" width="450"/>
</p>
<p align="center">
  <em> Client thoại nhân vật    </em>
</p>
<p align="center">
    <img src="docs/project photo/7..png" alt="Ảnh 7" width="450"/>
</p>
<p align="center">
  <em> Giao diện màn đánh BOSS   </em>
</p>


## 📝 4. Hướng dẫn cài đặt và sử dụng

### 🔧 Yêu cầu hệ thống

- **Python**: Phiên bản 3.9 trở lên
- **Hệ điều hành**: Windows 10/11 (khuyên dùng), macOS, hoặc Linux
- **Môi trường phát triển**: IDE (VS Code, PyCharm) hoặc terminal/command prompt
- **Bộ nhớ**: Tối thiểu 4GB RAM
- **Phần cứng**: Webcam hoạt động tốt (để nhận diện bàn tay)
- **Mạng**: Không yêu cầu (chơi Offline)

### 📦 Cài đặt và triển khai

#### Bước 1: Chuẩn bị môi trường

1. **Kiểm tra Python**: Mở terminal/command prompt và chạy:
   ```bash
   python --version

2. **Cài đặt thư viện**: Chạy lệnh cài đặt các gói cần thiết:
  ```bash
   pip install opencv-python numpy mediapipe

#### Bước 2: Kiểm tra cấu trúc thư mục

Đảm bảo các tệp tin được đặt đúng vị trí (như ảnh cấu trúc thư mục):

Các file logic: main.py, game.py, hand_tracking.py, ui.py, sound.py, story.py.

Dữ liệu AI: hand_landmarker.task.

Tài nguyên: Thư mục assets/ (chứa ảnh .png và âm thanh).
3. **Kiểm tra kết quả**: Nếu biên dịch thành công, sẽ tạo ra các file `.class` tương ứng.

#### Bước 3: Chạy ứng dụng

**Khởi động trò chơi:**:

- python main.py

- Trò chơi sẽ khởi động ở chế độ toàn màn hình
- Webcam sẽ tự động kích hoạt để bắt đầu nhận diện cử chỉ.
- Nhạc nền sẽ tự động phát khi vào Menu.

### 🚀 Sử dụng ứng dụng

1. **Kết nối**: Chỉ cần đưa bàn tay vào khung hình Webcam để hệ thống bắt đầu tracking (Hand Tracking).
2. **Chơi game**: Di chuyển tay sang trái/phải để điều khiển chiếc giỏ hứng vật phẩm , Hứng Tiền, Sao để tích lũy điểm; né tránh Bom để không bị mất máu (HP).
3. **Vật phẩm hỗ trợ**: Hứng các Item như Tăng tốc, Đóng băng thời gian để có lợi thế.
4. **Chiến đấu**: Trong màn Boss, hứng các vật phẩm Tấn công để gây sát thương lên Boss.
5. **Cốt truyện**:Nhấn nút TIẾP trên màn hình để theo dõi lời thoại và diễn biến câu chuyện giữa các màn.
6. **Thoát**: Nhấn phím Esc để đóng ứng dụng ngay lập tức.

## 👜Thông tin cá nhân
**Họ tên**: Nguyễn Hoàng Liêm.  
**Lớp**: CNTT 16-03.  
**Email**: liemnguyenhoang22@gmail.com.

© 2026 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.

---
