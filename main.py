from flask import Flask, render_template

app = Flask("JobScrapper")

@app.route("/")     # 데코레이터, syntactic sugar 문법은 간단해 보이지만 실제 일어나는 일은 좀 더 복잡
                    # /는 Homepage를 의미  =>  / route로 접근하면 밑의 함수를 실행
                    # decoraator를 함수 위에 두면 Flask는 user가 이 주소의 page를 방문했을 때 이 함수를 호출해야 하는 것을 알게 된다
def home():         # decorator와 함수는 바로 아래에 위치해야 함 => 만약 지금 home함수와 decorator 사이에 print()가 존재한다면, home은 작동되지 않는다
    return render_template("home.html", name="ivy") # requeste가 도착하면 Flask는 변수를 가져다가 HTML templates 안에 있는 변수를 가져온 것으로 replace하고 그렇게 만들어진 결과의 HTML이 user에게 전달 된다
                                                    # 이런걸 rendering이라고 한다
            
@app.route("/hello")
def hello():
    return "Hi there"



app.run("127.0.0.1")