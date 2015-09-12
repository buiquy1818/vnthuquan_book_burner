# vnthuquan_book_burner

Xuất phát từ nhu cầu đi tìm ebook để đọc nhưng không tìm được hoặc định dạng file pdf( đọc trên smart phone rất khó chịu).
Trong khi đó nguồn nội dung trên nhiều trang web rất phong phú như vnthuquan.net. Tuy nhiên việc đọc
trên vnthuquan.net mình gặp hạn chế( cũng là lợi thế của việc đọc ebook).
- Trải nghiệm đọc web khó chịu, như chuyển trang, đánh dấu, ghi nhớ...
- Máy tính, điện thoại luôn phải đảm bảo kết nối internet. Như vậy luôn bị lệ thuộc vào mạng internet trong lúc đọc( không có internet thì nghỉ) cũng như tiêu hao pin điện thoại rất nhanh.
Nên mình tạo tool này phục vụ nhu cầu cá nhân cũng như để mọi người tham khảo sử dụng.

Chú ý: 

Việc sử dụng ebook có thể vi phạm quyền tác giả nên quyền sử dụng phần mềm này cũng như trách nhiệm pháp lý nếu có thuộc về người sử dụng phần mềm.
Trong trường hợp có điều kiện mua sách thì nên mua sách của chính tác giả để đảm bảo nguồn tài chính cho tác giả tái đầu tư.


## Trạng thái hiện tại của project.
Hiện tại phần mềm mới ở dạng beta. 
- Tải vào tạo được một ebook từ một số sách nhất định như cuốn "Trần Đức Thảo - Những Lời Trăng Trối"
- Giao diện commandline.


## Các gạch đầu dòng cần/sẽ giải quyết:
- Chuẩn hóa code, bổ sung comment, chuyển comment sang tiếng V
- Khả năng cho nhiều định dạng. Ban đầu tối thiểu 2 định dạng, về sau sẽ cập nhật khi có thêm bug
- Khả năng chạy portable GUI trên nền Window để ứng dụng phổ cập hơn


## Chạy môi trường commandline(Ubuntu)
### Cài đặt các thư viện phụ thuộc
```
pip install -r requirements.txt
```
### Chạy script chính của chương trình
```
python main.py http://vnthuquan.net/truyen/truyen.aspx?tid=2qtqv3m3237n3nmnqn2n31n343tq83a3q3m3237nvn
```

