# DB 가져오기 및 패키지 설치
1. 현재 프로젝트 폴더에 sqlite db 복붙
2. app.config.update()에 db_uri 붙혀주기
```python
app.config.update(
    SQLALCHEMY_DATABASE_URI = 'sqlite:///herb_medicine'
)
```
 - ///3개는 상대경로 ////4개는 절대경로
 - 경로에 .db 붙히지 말기
 
3. 패키지 2개 설치
    1. flask-sqlalchemy
    2. flask-sqlacodegen
4. `terminal`을 열어 `pip list`로 설치한 패키지 확인

## sqlacodegen 사용해보기
1. 터미널에서 `flask-sqlacodegen sqlite:///herb_medicine`
 - class 형태 확인하기
2. `flask-sqlacodegen sqlite:///herb_medicine --outfile models.py --flask`
 - models.py 파일로 빼기
 
## app.py에서 사용하기
1. from models import `db`, Herb # 테이블 싹다 해오기
2. app에 db 붙혀주기
 - `db.init_app(app)`
 
# db를 route에서 객체로 사용해보기
## 조회하기
* 라우트안에서
     - herb = Herb.query.all()
     - herb = Herb.query.filter_by(herb_name = '목통') 
     - return render_template('index.html', herb=herb)
* html에서 테이블안에 jinja로 받기
     1. jinja에서 for문으로 받은 변수 확인해보기
     2. table태그를 만들고 그안에 넣어주기
 ```python
@app.route('/select/<str>')
def select(str=None):
    # print(str)
    herb = Herb.query.filter_by(herb_name = str)
    # print(herb)
    return render_template('index.html', herb = herb)
```


# Admin
1. 패키지 설치
 - flask-admin 검색
2. `admins.py` 만들기
 - 객체랑 이름 정해주기(app객체는 app.py에서 연결)
   `from flask_admin import Admin`  
   `admin = Admin(name = "독약한방")`
 - db의 table을 admin에 붙혀줄 놈
   `from flask_admin.contrib.sqla import ModelView`
3. `app.py`에서 수정하기
 - `from admin import admin, ModelView`
 - app.config.update()에 테마 옵션, 권한을 위한 키 넣어주기
    1. `FLASK_ADMIN_SWATCH = 'cerulean'` : 테마
    2. `SECRET_KEY = 'my_secret_key'` : CRUD권한을 위한 키
 - `ModelView`로 models의 테이블과 admin을 연결
    1. `admin.add_view(ModelView(Herb, db.session))` 테이블 다 반복
    2. for문으로 수정
        ```python
        table_class_list = [ Herb, Location, Category, SimilarityGroup, News, Journal]
        for table in table_class_list:
            admin.add_view(ModelView(table, db.session))
        ```
4. admin에서 보이는 옵션 추가로 주기위해 custom ModelView 만들기
 - `admin.py`
    ```python
    class MyModelView(ModelView):
        can_delete = False # 삭제옵션 삭제
        can_view_details = True # 눈깔 자세히보기
        create_modal = True # 폼 생성->불편
    ```
 - `app.py`에서 import부터 모두 ModelView->MyModelView로 수정하기
