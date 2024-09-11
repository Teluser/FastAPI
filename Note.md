# Fast API


## 1. API schema (pydantic):

- dùng để validate input đầu vào của API chính xác như expect (thừa, thiếu params hay sai kiểu dữ liệu -> báo lỗi)

  -> dùng thay thế cho Body(...) (nhận bất kì kiểu dữ liệu nào)
- tự động convert dữ liệu user input theo kiểu như định nghĩa trong Schema
- Trường hợp k convert được -> Báo lỗi sai kiểu dữ liệu

```
class UserBase: # lưu các thuộc tính chung khi đọc/tạo User, (Khi đọc user k trả ra field password -> k bao gồm field password)
	email: str

class UserCreate(UserBase): # lưu thêm các dữ liệu cần có -> TẠO user so với class UserBase
	password: str

class User(UserBase): # lưu thêm các dữ liệu trả về -> khi ĐỌC từ DB. VD: id khi tạo rồi mới có giá trị 
	id: int
	is_active: bool
	class Config:
		orm_mode = True # giúp pydantic đọc được dữ liệu record trả về từ ORM(nếu k set nó chỉ đọc hiểu dữ liệu là dict)
```

## 2. Thứ tự xuất hiện API quan trọng

- Thứ tự xuất hiện API trong file là rất quan trọng -> nếu cả 2 API cùng match -> ưu tiên gọi API match đầu tiên
  ```
  @api.get("\posts\{id}")
  @api.get("\posts\lastest")

  # Nếu gọi \posts\lastest -> match vào schema @api.get("\posts\{id}")
  ```

## 3. Xử lý ngoại lệ trong API

- Nên sử dụng HTTPException()

```@app.get(
def get_post(id: int, response: Response):
    res = None
    if not res:
	# response.status_code = 404
	# return {"data": f"post with {id} does not exists"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"data": res}
```

## 4. ORM

* dùng thư viện SQLalchemy

## 5.Sự khác nhau giữa pydantic và orm

* SQLAlchemy *models* define attributes using `=`, and pass the type as a parameter to `Column`, like

`name = Column(String)`

* Pydantic *models* declare the types using `:`

```
name: str

```

- **Pydantic** để verify input, output format từ API -> gọi là **schemas**
- **ORM** để định nghĩa các table và kiểu dữ liệu, thao tác với DB -> gọi là models

## 6.Tổ chức folder

Tạo routers

```
# Tạo thư mục routers
# Tạo file .py cho từng API theo mục đích sử dụng 
# VD: 
# - posts.py
# - user.py
# Dùng APIRouter -> để create route, với 2 tham số 
# prefix -> tất cả các url trong file được thêm prefix 
# tag -> Nhóm các API với cùng mục đích sử dụng ở doc API  
# import route vào file main.py (file chạy uvicorn) bằng app.include_router(post.router)
# chi tiết tham khảo /Learn basic FastAPI/routers/post.py
```

## 7. Cách đọc tham số truyền vào func FastAPI

* Nếu tham số declared ở URL (**path)** -> sử dụng param được truyền vào từ url
* Nếu tham số truyền vào kiểu  `int`, `float`, `str`, `bool`, etc -> hiểu là **query** parameter.
* Nếu tham số tryền vào kiểu **Pydantic model** -> hiểu là request  **body** .

Tham số:

```
q: str  -> require
q: str = None -> hiểu là option, giá trị mặc định là None
q: str | None = None -> hiểu là option, giá trị mặc định là None
Chỉ dùng str = None -> fastapi cũng hiểu là option, nhưng cho thêm | None -> giúp cho IDE gợi ý và cảnh báo tốt hơn
```
