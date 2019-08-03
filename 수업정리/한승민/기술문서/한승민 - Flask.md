# Flask

## 패키지 목록
```python
# app.py

from flask import Flask, render_template, redirect, url_for, flash, request
```

- Flask: Web Application 객체
- render_template: jinja2 template을 렌더링할 수 있도록 해주는 모듈
- redirect: 다른 url로 redirect 할 수 있도록 해주는 함수
- `url_for`: `url_for` 함수는 함수 이름으로 된 종단점(endpoint)의 URL을 생성해주는 함수이며, 예시는 다음과 같음.
  ```python
  # app.py
  
  @app.route('/board/view/<int: no>')
  def viewBoard(no):
      return render_template('/board/list.html', resultset=models.Board.query.filter_by(no=no).first())
  
  
  @app.route('/board/add/<int: no>')
  def addBoard(no):
      # source code ...
      return url_for('listBoard', resultset=models.Board.query.filter_by(no=no).first())
  ```
  > `endpoint` is an identifier that is used in determining what logical unit of your code should handle the request
    ([reference](https://stackoverflow.com/questions/19261833/what-is-an-endpoint-in-flask))
- flash: alert 메시지를 처리할 수 있도록 제공하는 모듈
- request: client가 보낸 request를 처리할 수 있도록 제공하는 모듈

## Configuration
기본적인 설정은 다음과 같이 구성했다.

```python
# config.py

import os


class Configuration:
    def __init__(self, host, user, password, db, *args, **kwargs):
        self._conf = {
            'host': os.environ.get('MYSQL_HOST', host),
            'user': os.environ.get('MYSQL_USER', user),
            'password': os.environ.get('MYSQL_PASS', password),
            'db': os.environ.get('MYSQL_DB', db)
        }
        self.CONFIG = f"mysql://{self._conf['user']}:{self._conf['password']}@{self._conf['host']}:3306/{self._conf['db']}?charset=utf8"

    def conf(self):
        return self.CONFIG

```

그 뒤, `app.py`에 다음과 같이 작성했다.

```python
# app.py

from config import Configuration


app = Flask(__name__)

conf = Configuration('host', 'user', 'password', 'db')
print(conf.conf())

app.config['SQLALCHEMY_DATABASE_URI'] = conf.conf()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

models.db.init_app(app)
```

## Model Class 정의
다음과 같이 `Board`라는 테이블이 정의가 되어있을 경우,

```sql
CREATE TABLE Board
(
    no      INT NOT NULL AUTO_INCREMENT,
    author  INT NOT NULL,
    title   VARCHAR(255) NOT NULL,
    date    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    content VARCHAR(5000) NULL,
    PRIMARY KEY (no)
);
```

아래처럼 `Board`에 대한 Model 클래스를 정의할 수 있다.

```python
# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Board(db.Model):
    __tablename__ = 'Board'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    no = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    author = db.Column(db.String(35), nullable=False)
    title = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    content = db.Column(db.Text)

    def __init__(self, author, title, date, content):
        self.author = author
        self.title = title
        self.date = date
        self.content = content
```

## CRUD
Model 클래스들을 `models.py`에 정의하고 다음과 같이 import 했다.

```python
import models
```

- Create
```python
title = request.form['title']
content = request.form['content']

newBoard = models.Board(title, content)

models.db.session.add(newBoard)
models.db.session.commit()
```

- Read
```python
resultset = models.Board.query.all()
```

- Update
```python
models.Board.query.filter_by(no=no).update(title=title, content=content)
models.db.session.commit()
```

- Delete
```python
models.db.session.delete(newBoard)
models.db.session.commit()
```

## Ubuntu 환경에서 MySQL 연동이 되지 않는 경우
만약 flask에서 orm 사용 시 ubuntu에서 mysql과 연동되지 않는다면 아래와 같은 명령어를 입력한다.

```dos
$ sudo apt install python3-dev
$ sudo apt install mysql-server
$ sudo apt install libmysqlclient-dev
```

그 다음 `pip`를 통해 `mysqlclient` 패키지를 설치한다.

```dos
$ pip install mysqlclient
```


## 참고
- [The Pallets Projects](https://palletsprojects.com/p/flask/)
- [Flask Official site](https://flask.palletsprojects.com/en/1.1.x/)
- [Flask SQLAlchemy Official site](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Flask SQLAlchemy CRUD](https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/)
- [jinja2 Template Official site](https://jinja.palletsprojects.com/en/master/)
- [Python Flask로 CRUD 만들어보기](https://medium.com/@feedbots/python-flask-%EB%A1%9C-crud-%EB%A7%8C%EB%93%A4%EC%96%B4-%EB%B3%B4%EA%B8%B0-3676b3b33d9)
- [Flask 공식 튜토리얼 따라하기](https://blog.outsider.ne.kr/1329)
- [높은 품질의 Flask 웹 애플리케이션 설계하기](https://prev.kr/posts/%EB%86%92%EC%9D%80-%ED%92%88%EC%A7%88%EC%9D%98-Flask-%EC%9B%B9-%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0/)
