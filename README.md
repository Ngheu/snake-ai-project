# Snake AI Project - Đồ án Trí tuệ nhân tạo

**Tên đồ án**: Snake game AI  
**Môn học**: Trí tuệ nhân tạo  
**Nhóm thực hiện**:  
1. Võ Duy Phước - 2351010169  
2. Đặng Hoàng Phúc - 2351010162  
3. Nguyễn Thanh Vinh - 2351010244  
4. Võ Thành Phi Long - 2351010117  

**Giảng viên hướng dẫn**: Lê Viết Tuấn  

## Tổng quan
Dự án triển khai hệ thống chơi trò chơi Snake tự động bằng trí tuệ nhân tạo với ba phương pháp khác nhau:
- **BFS** (Breadth-First Search): Tìm đường ngắn nhất an toàn.
- **Greedy Best-First Search**: Ưu tiên hướng gần thức ăn nhất (heuristic Manhattan distance).
- **Deep Q-Network với CNN** (Convolutional Neural Network): Học tăng cường từ môi trường, huấn luyện agent thông minh qua thử và sai.

Hệ thống hỗ trợ hai bản đồ:
- **Classic**: Không có tường.
- **Maze**: Có 50 tường ngẫu nhiên (đảm bảo khu vực khởi đầu an toàn).

## Tính năng chính
- Menu console chọn bản đồ và thuật toán.
- Chạy tự động với BFS/Greedy hoặc huấn luyện/lưu model CNN-DQN.
- Hiển thị đồ thị tiến trình huấn luyện realtime (score và mean score).
- Lưu model khi đạt record mới (`model/model_cnn.pth`).
- Tốc độ cao, giao diện Pygame mượt mà.

## Cấu trúc thư mục
SnakeTest/
├── main.py              # Menu chính và điều khiển chương trình
├── game.py              # Logic trò chơi (Pygame), bản đồ, va chạm, hiển thị
├── agent_logic.py       # BFS và Greedy Best-First Search
├── agent_cnn.py         # Agent DQN với CNN
├── model_cnn.py         # Kiến trúc mạng ConvQNet
├── helper.py            # Vẽ đồ thị huấn luyện (Matplotlib)
├── config.py            # Các hằng số cấu hình (kích thước lưới, learning rate, v.v.)
├── model/               # Thư mục lưu model đã huấn luyện (model_cnn.pth)
└── README.md            # Tài liệu này


## Yêu cầu hệ thống
- Python 3.8 trở lên
- Các thư viện:
  - pygame
  - torch
  - numpy
  - matplotlib

## Cài đặt
Mở terminal/command prompt trong thư mục dự án và chạy:
```bash
pip install pygame torch numpy matplotlib

Cách chạy chương trình
Bashpython main.py
Hướng dẫn sử dụng

Chương trình hiển thị menu:text--- SNAKE AI CONTROLLER ---

Select Map:
1. Classic
2. Maze (Walls)
Enter choice (1/2): 

Select Algorithm:
1. BFS
2. Greedy
3. Machine Learning (CNN)
Enter choice (1/2/3):
Nhập lựa chọn:
Nếu chọn 3 (CNN): Chương trình sẽ tự động huấn luyện hoặc tải model hiện có, hiển thị đồ thị training realtime.
Nếu chọn 1 hoặc 2: Chạy trực tiếp với BFS hoặc Greedy, game over thì reset tự động.

Đóng cửa sổ Pygame để thoát.

Kết quả đạt được

BFS & Greedy: Chơi ổn định, đạt score cao trên bản đồ Classic (gần tối đa), an toàn trên Maze.
CNN-DQN: Sau 300-500 games huấn luyện, đạt record cao hơn trên Maze, thể hiện hành vi linh hoạt và thích ứng tốt.

