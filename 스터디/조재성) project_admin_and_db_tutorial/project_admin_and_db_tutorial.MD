![](http://cfile21.uf.tistory.com/image/99A76D405D4E767A07A905)

## 미리 작성된 admin.py, model.py
1. 프로젝트 폴더에 복붙
2. flask-sqlalchemy 패키지 설치
3. flask-admin 패키지 설치
 
## app.py 설정
1. 모듈 불러오기 
```python
from model import db, Herb, Location, Category, Similaritygroup, News, Journal
from admin import admin, HerbView, LocationView, CategoryView, SimilaritygroupView, NewsView, JournalView
```
2. model로 db 생성할 db이름 및 경로 지정해주기
```python
app.config.update(
    SQLALCHEMY_DATABASE_URI = 'sqlite:///herb_medicine',
    FLASK_ADMIN_SWATCH = 'cosmo', # admin 테마 지정
    SECRET_KEY = 'my_secret_key' # admin권한을 위한 키생성
)
```

3. app객체에 admin과 sqlalchemy 연결해주기
```python
db.init_app(app)
admin.init_app(app)
```

4. 테이블과 Custom한 ModelView를 admin에 붙혀주기
```python
table_list= [ Herb, Location, Category, Similaritygroup, News, Journal ]
view_list = [ HerbView, LocationView, CategoryView, SimilaritygroupView, NewsView, JournalView ]
for table, view in zip(table_list, view_list):
    admin.add_view(view(table, db.session))
```

5. DB생성할 라우트 만들어주기
```python
# 테이블 생성
@app.route('/create_all')
def create_all():
    db.create_all()
    return "create OK"
```

6. 앱 실행시키고 `127.0.0.1:5000/create_all`로 DB생성

7. `127.0.0.1:5000/admin`