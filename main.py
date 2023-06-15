from flask import Flask, render_template, request, redirect, send_file          # request는 request에 대한 정보에 접근 할 수 있게 해준다
from extractors.indeed import extract_indeed_jobs                               # request란? 브라우저가 웹사이트에 가서 콘텐츠를 요청하는것을 말한다
from extractors.wwr import extract_wwr_jobs                                     # request는 어떤 정보를 갖고 있을까? => 요청하고 있는 URL이 무엇인지, IP주소가 무엇인지, cookies를 가지고 있는지
from extractors.save_file import save_to_file
app = Flask("JobScrapper") # Jobscrapper라고 불리는 새로운 Flask application인 app 변수를 생성

db = {}
                     # 가짜 DB를 만들거임(실제 DB는 아니지만 유사한 기능을 갖출 수 있게)
                     # 첫 extract 이후 다른 사용자가 오면 다시 extract하는 대신 이미 extract해둔 것을 보여줄 수 있게
                     # 예시로, 만약 첫 python에 대한 요청이 들어온다면 관련 jobs를 extract하고 해당 jobs를 key를 python으로해서 db(가짜)에 저장
                     # 다음 사용자가 python을 요청한다면 우리 db가 이미 python을 가지고 있는지 확인 => 존재한다면 다시 jobs를 extract하지 않고 jobs를 바로 제공
                     # Fake DB이기 때문에 서버가 켜져있을 때만 메모리에 존재(서버 중단 후 재시작하면 DB지워짐)

# 데코레이터, syntactic sugar 문법은 간단해 보이지만 실제 일어나는 일은 좀 더 복잡
# /는 Homepage를 의미  =>  / route로 접근하면 밑의 함수를 실행
# decoraator를 함수 위에 두면 Flask는 user가 이 주소의 page를 방문했을 때 이 함수를 호출해야 하는 것을 알게 된다
# decorator와 함수는 바로 아래에 위치해야 함 => 만약 지금 home함수와 decorator 사이에 print()가 존재한다면, home은 작동되지 않는다
@app.route("/")     
def home():         
    return render_template("home.html", name="ivy") # requeste가 도착하면 Flask는 변수를 가져다가 HTML templates 안에 있는 변수를 가져온 것으로 replace하고 그렇게 만들어진 결과의 HTML이 user에게 전달 된다
                                                    # 이런걸 rendering이라고 한다
                                                    # redering => 1) user에게 HTML을 전달하는 것
@app.route("/search")                                           # 2) 실제로 HTML 파일에 데이터를 보내는 것을 의미하기도 한다
def search():
    keyword = request.args.get("keyword") # request의 arguments에서 keyword를 가져와서(즉, URL의 ?뒤에 있는 arguments에서 keyword를 가져와서)그 keyword를 search.html에 보낸다
    if keyword == None:
        return redirect("/")
    elif keyword == "":
        return redirect("/")
   
    if keyword in db:
        jobs = db[keyword]
    else:
        indeed = extract_indeed_jobs(keyword) # keyword로 두 개의 function을 호출
        wwr = extract_wwr_jobs(keyword)
        jobs = indeed + wwr # 두 개의 함수 호출 결과로 나온 각각의 List 두 가지를 하나로 합친다
        db[keyword] = jobs  # db[keyword] => dictionary의 item에 접근할 수 있는 방법
    return render_template("search.html", keyword=keyword, jobs=jobs) # render_template은 Flask가 templates 폴더를 들여다 보게 한다
                                                           # 합친 하나의 List를 search.html로 보낸다


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}") # 데이터베이스에 없는 keyword로 export에 접근하는 것을 방지
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)



app.run("127.0.0.1",port=8000, debug=True) # 생성한 app변수를 이용해 run()함수를 호출하면 Flask application을 생성해준다
