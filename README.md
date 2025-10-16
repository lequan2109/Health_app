# 🏥 Health App - Ứng dụng Theo dõi Sức khỏe Cá nhân

Ứng dụng theo dõi sức khỏe cá nhân được phát triển bằng **Python** với giao diện **Tkinter**, giúp người dùng quản lý và theo dõi sức khỏe một cách hiệu quả.

---

## 📋 Mục lục
- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Cài đặt](#-cài-đặt)
- [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [License](#-license)
- [Tác giả](#-tác-giả)

---

## 🎯 Giới thiệu
**Health App** là ứng dụng desktop giúp người dùng:
- 📊 Theo dõi cân nặng và chỉ số BMI
- 🏃 Ghi nhận hoạt động thể thao hàng ngày
- ⚠️ Nhận cảnh báo sức khỏe thông minh
- 📈 Phân tích xu hướng sức khỏe qua biểu đồ
- 💾 Lưu trữ và xuất dữ liệu sức khỏe

---

## ✨ Tính năng

### 🎯 Tính năng chính
- 🔐 **Quản lý người dùng**: Đăng ký, đăng nhập an toàn  
- ⚖️ **Theo dõi cân nặng**: Nhập và theo dõi cân nặng hàng ngày  
- 📊 **Tính toán BMI**: Tự động tính chỉ số BMI và phân loại  
- 🏃 **Theo dõi hoạt động**: Ghi nhận các hoạt động thể thao  
- 📈 **Biểu đồ trực quan**: Hiển thị xu hướng sức khỏe  
- ⚠️ **Hệ thống cảnh báo**: Cảnh báo khi số liệu vượt ngưỡng  
- 📋 **Lịch sử dữ liệu**: Xem và quản lý lịch sử sức khỏe  
- 💾 **Xuất dữ liệu**: Export dữ liệu ra CSV, JSON  
- 📱 **Giả lập thiết bị**: Tạo dữ liệu mẫu để thử nghiệm  

### 🚀 Tính năng nổi bật
- 🎨 Giao diện thân thiện, dễ sử dụng  
- 📊 Biểu đồ đa dạng với **matplotlib**  
- 🗃️ Database **SQLite** nhẹ và hiệu quả  
- ⚡ Xử lý dữ liệu nhanh chóng  
- 🔒 Validation dữ liệu chặt chẽ  

---

## 🛠️ Cài đặt

### Yêu cầu hệ thống
- Python 3.8 hoặc cao hơn  
- Hệ điều hành: Windows / macOS / Linux  

### Các bước cài đặt

```bash
# Clone repository
git clone https://github.com/lequan2109/Health_app.git
cd Health_app

# Tạo môi trường ảo (khuyến nghị)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Cài đặt dependencies
pip install matplotlib

# Chạy ứng dụng
python main.py
```

---

## 📖 Hướng dẫn sử dụng

### 🚀 Khởi động
1. Chạy file `main.py`
2. Đăng ký tài khoản mới hoặc đăng nhập
3. Bắt đầu theo dõi sức khỏe!

### 📝 Sử dụng cơ bản
1. **Đăng ký tài khoản**  
   - Nhập: tên đăng nhập, mật khẩu, họ tên, chiều cao  
   - Tùy chọn: ngày sinh, giới tính  

2. **Nhập dữ liệu cân nặng**  
   - Tab `📝 Nhập liệu` → `⚖️ Cân nặng`  
   - Nhập cân nặng (kg), ngày, ghi chú  
   - Hệ thống tự động tính BMI và phân loại  

3. **Ghi nhận hoạt động**  
   - Tab `📝 Nhập liệu` → `🏃 Hoạt động`  
   - Chọn loại hoạt động, thời gian, cường độ  
   - Hệ thống tính calories đốt cháy  

4. **Xem tổng quan**  
   - Tab `🏠 Tổng quan` hiển thị thống kê hiện tại, cảnh báo, phân loại BMI, hoạt động gần đây  

5. **Phân tích biểu đồ**  
   - Tab `📊 Biểu đồ` cung cấp xu hướng cân nặng, biểu đồ BMI, phân tích hoạt động, tổng quan tuần  

6. **Quản lý lịch sử**  
   - Tab `📋 Lịch sử`: Xem, lọc, xuất dữ liệu ra file  

---

## 🎛️ Tính năng nâng cao

### 🧪 Giả lập thiết bị
- Tạo dữ liệu mẫu để thử nghiệm  
- Sinh dữ liệu cân nặng và hoạt động tự động  

### 💾 Xuất dữ liệu
- Xuất dữ liệu ra **CSV, JSON**  
- Tạo file ZIP chứa toàn bộ dữ liệu  
- Hỗ trợ phân tích ngoài ứng dụng  

---

## 📁 Cấu trúc dự án
```
health-App/
├── main.py                 
├── database/
│   ├── __init__.py
│   └── db_manager.py      
├── gui/
│   ├── __init__.py
│   ├── login_window.py    
│   ├── main_window.py     
│   └── components/
│       ├── __init__.py
│       ├── dashboard_tab.py    
│       ├── input_tab.py        
│       ├── charts_tab.py       
│       └── history_tab.py      
├── models/
│   ├── __init__.py
│   ├── user.py            
│   └── health_record.py   
├── utils/
│   ├── __init__.py
│   ├── bmi_calculator.py  
│   ├── alert_system.py    
│   ├── chart_generator.py 
│   ├── device_simulator.py 
│   └── validators.py      
├── tests/
│   ├── __init__.py
│   └── test_basic.py      
├── requirements.txt       
└── README.md             
```

---

## 🛠️ Công nghệ sử dụng
| Thành phần | Công nghệ |
|-------------|------------|
| Ngôn ngữ | Python 3.8+ |
| Giao diện | Tkinter |
| Cơ sở dữ liệu | SQLite |
| Vẽ biểu đồ | Matplotlib |
| Kiến trúc | OOP Architecture |

---

### Báo cáo lỗi / yêu cầu tính năng
- Sử dụng **GitHub Issues**
- Mô tả chi tiết lỗi và cách tái hiện
- Gửi đề xuất với mô tả rõ ràng

---

## 📄 License
Dự án được phân phối dưới **giấy phép MIT**.  
Xem file `LICENSE` để biết thêm chi tiết.

---

## 👨‍💻 Tác giả
**Nhóm 1**  
- GitHub: [@lequan2109](https://github.com/lequan2109)  
- Email: [lequan21092004@gmail.com](mailto:lequan21092004@gmail.com)

---

## 🙏 Acknowledgments
- Cảm ơn cộng đồng **Python** vì các thư viện tuyệt vời  
- Cảm ơn các **contributors** đã đóng góp cho dự án

---

## 📞 Hỗ trợ
- Tạo Issue  
- Liên hệ qua email: [lequan21092004@gmail.com](mailto:lequan21092004@gmail.com)

<div align="center">

⭐ **Hãy star repository này nếu bạn thấy hữu ích!**  

> “Sức khỏe là vàng - Hãy theo dõi nó một cách thông minh!” 💪

</div>

---

## 🚀 Quick Start

```bash
# Clone và chạy nhanh
git clone https://github.com/lequan2109/Health_app.git
cd Health_app
pip install matplotlib
python main.py
```

**Bắt đầu hành trình chăm sóc sức khỏe của bạn ngay hôm nay! 🏥✨**
