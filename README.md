🎬 Hệ thống Gợi ý Phim (Movie Recommender System)

- 🧠 Giới thiệu

    + Movie Recommender System là một ứng dụng web gợi ý phim dựa trên mô hình lọc cộng tác (Collaborative Filtering), sử dụng phân rã ma trận (Matrix Factorization) để đưa ra gợi ý chính xác cho từng người dùng.
    + Hệ thống dựa trên nguyên lý:

Nếu hai người có cùng sở thích xem phim (cùng thích một số bộ phim giống nhau), thì những bộ phim mà một người đã thích nhưng người kia chưa xem — có thể sẽ là gợi ý phù hợp cho người còn lại. 🎥

- 🖥️ Giao diện

🏠 Trang chủ: hiển thị danh sách phim và ô tìm kiếm.

<img width="1872" height="864" alt="image" src="https://github.com/user-attachments/assets/46c48ede-f3c9-4b0c-a683-2bf5eb272b89" />



⭐ Trang đánh giá: người dùng có thể chấm điểm phim.

<img width="1888" height="844" alt="image" src="https://github.com/user-attachments/assets/5fcfb3bc-92a5-4984-a2e4-6b9a21a5d6a5" />


🤖 Trang đề xuất: hiển thị danh sách các phim được gợi ý dựa trên hành vi đánh giá của người dùng.

<img width="1867" height="867" alt="image" src="https://github.com/user-attachments/assets/3abe7512-87eb-41e5-859d-cd4c1b603f85" />


- ⚙️ Công nghệ sử dụng
  
🔹 Web Framework & Frontend

Django (Python)

HTML, CSS, Bootstrap, JavaScript

🔹 Machine Learning

Numpy, Pandas, Scipy

Áp dụng thuật toán Collaborative Filtering dựa trên Matrix Factorization

🔹 Cơ sở dữ liệu

SQLite (có thể mở rộng sang PostgreSQL hoặc MySQL)

- 💡 Cách hoạt động

Người dùng đăng ký, đăng nhập và đánh giá một vài bộ phim.

Hệ thống ghi nhận dữ liệu đánh giá.

Sử dụng thuật toán học máy để dự đoán các bộ phim phù hợp nhất.

Hiển thị danh sách phim được đề xuất cá nhân hóa cho từng người.
