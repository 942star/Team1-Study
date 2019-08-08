## 설치
1. 환경설정 > `flask-dropzone` 설치
2. 깃허브의 examples > basic 을 참고함
 - https://github.com/greyli/flask-dropzone/tree/master/examples
 - flask-dropzone/examples/basic/app.py 내용 복붙
3. `basic > app.py` - app.config.update() 기본설정
 - UPLOADED_PATH : 업로드할 프로젝트폴더에 폴더명 지정(`미리 생성해놔야한다`)
 - DROPZONE_ALLOWED_FILE_TYPE : 보안상의 문제도 해결해주면서 업로드 유형 지정
 - DROPZONE_MAX_FILE_SIZE : 한번에 올릴 갯수?
 - DROPZONE_MAX_FILES : 최대 갯수?   

4. `basic/templates/index.html` 복붙
 - dropzone.load_css() : dropzone전용 css로딩 -> 페이지 소스보기에서 뜬 css을 url_for로 수정할 것
 - dropzone.style() : 마찬가지로 url_for style.css로 수정할 것
 - dropzone.create(action='upload') : 필수적인 것으로 **form태그를 자동생성**해준다.
    - dropzone에서의 action은 route밑에 있는 함수명을 지정. route('/') def `upload`(): ~
    - 소스보기에서 <form> 태그가 자동생성되어있는데, 내부의 `enctype="multipart/form-data"`가 반드시 있어야 파일이 업로드 된다.
    - action은 해당 라우트의 함수에 파일을 전송해준다.
 - dropzone.load_js() : url_for로 수정할 것
 - dropzone.config() : app.config에서 해준 설정을 여기에서??

5. app.py속 route
 - `request.files.get('file')`으로 업로드된 파일을 받을 수 있다.
 - f.save()로 미리지정했던 업로드폴더명 + f.filename으로 파일 저장
   `나중에는 파일이름 따로 처리해서 저장`하도록 해야한다.  
   
   

여기까지 하면, 화면에 이미지 업로드는 되나, 업로드 버튼이 없는 상태  
드래그하자마자 바로 서버에 저장된다.  
![](http://cfile27.uf.tistory.com/image/996B6A3C5D4C141405DCD7)

  

클릭버튼이 포함된 깃허브 `flask-dropzone/examples/click-upload/`
5. `app.py`의 config안에 
 - `DROPZONE_UPLOAD_ON_CLICK=True` 만 가져오기
6. `index.html`에서 
 - `<button id="upload">Upload</button>` 만 가져와 넣기
 - 이 때, id="라우트함수명"이다...
7. 기존에 있던
 - dropzone.create(`action='upload'`)에서 action속성은 빼기 = route로 보내주는 것 빼기
    - 라우트로 현재화면의 라우트를 적어준다. `{{ dropzone.create('/') }}`
 - 대신 업로드 버튼(id="갈 라우트함수명") 클릭시, 업로드 결과하면으로 redirect(`app.config`에서 설정한 라우트함수명)를 통해 다른 화면을 보여주어야한다.

`flask-dropzone/examples/complete-redirect/` 
8. 업로드 버튼 클릭-> upload함수(=업로드받는라우트) -> completed시 `app.config에 명시하여 자동이동`될 라우트 만들어주기
 - `DROPZONE_REDIRECT_VIEW='completed'`옵션에 찾아갈 route함수명 적어주기
 - redirect결과 라우트 만들어주기(def `completed`)

 

dropzone.create()가 아니라 직접 폼을 만드는   
`flask-dropzone/examples/in-form/`

9. `index.html`에서 직접 만든 폼태그 부분 가져오기
 - action에서는 url_for + 라우트명을 적어준다.
 - 맨 마지막 input type에는 submit +  `id=submit`으로 설정한다.
10. `app.py` 직접 폼을 만들때 넣어주는 in_form옵션
 - 업로드 처리할 route함수명 + 버튼id설정
    DROPZONE_UPLOAD_ACTION='handle_upload',#(라우트함수명)
    DROPZONE_UPLOAD_BTN_ID='submit',#(input type submit의 id)

11. 라우트 각각 분리하기..
 - 깃허브 html가져오는데 잘안된당..





이전에 했떤 form관련 처리

```python
@app.route('/debug')
def debug():
    # print(dir(request))
    # print(request.headers)
    # print(request.headers['User-Agent'])
    # if "Macintosh" in request.headers['User-Agent']:
    #     print('맥이군요')
    # print(request.path)
    print(request.method)
    return "디버그"

@app.route('/form')
def form():
    # print(url_for('debug'))
    # print(request.form)
    # print(request.path)

    # get 처리방식
    # if request.method=="GET": 를 쓸 필요없다.
    # route에 methods를 지정해줄 필요 없다.


    # get처리
    # print(request.args) # get으로 온 데이터를 빼낸다. 임뮤터플 딕트라 뜬다.
    # 받은 값은 key, value쌍이고, 오류없이 default를 가지기 위해서 get방식으로 빼낸다.
    # request.args.get('s', None)
    # t= request.args.get('s', None) #응용
    # if t == ?: # db에서 받은 값을 여기서 이렇게 받는다.
    return render_template('form.html')



@app.route('/form_post', )
def form():
    # print(url_for('debug'))
    # print(request.form)
    # print(request.path)

    # get 처리방식
    # if request.method=="GET": 를 쓸 필요없다.
    # route에 methods를 지정해줄 필요 없다.

    # get처리
    # print(request.args) # get으로 온 데이터를 빼낸다. 임뮤터플 딕트라 뜬다.
    # 받은 값은 key, value쌍이고, 오류없이 default를 가지기 위해서 get방식으로 빼낸다.
    # request.args.get('s', None)
    # t= request.args.get('s', None) #응용
    # if t == ?: # db에서 받은 값을 여기서 이렇게 받는다.

    return render_template('form.html')



@app.route('/form_result')
def form_result():
    # print(url_for('debug'))
    # print(request.form)
    # print(request.path)
    # print(request.path)
    return "form 결과처리 페이지입니다."
```

```html
    <form action="/form_result">
        <input type="text" name="search">
        <input type="submit">
        <input type="file">
    </form>

    {#겟#}
    <form action="/form_result">
        <input type="text" name="search">
        <input type="submit">
        <br>
        <input type="file">
    </form>

    {#포스트#}
    <form method=["GET","POST"]>
        <input type="text">
        <input type="submit">
        <br>
        <input type="file">
    </form>
```

