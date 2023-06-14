from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term=" 
    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print("Can't request website")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("section", class_="jobs")  # 다시 한번 상기하자면, 이건 string이 아니라 python의 데이터 구조, entitiy임 
                                                        # 이 경우 jobs는 우리가 찾은 모든 section의 list임
        for job_section in jobs:
            job_posts = job_section.find_all('li') 
            job_posts.pop(-1)  
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]
                link = anchor['href']   # 이 부분도 BeautifulSoup덕분에 html 태그를 가져오고 그걸 Python Dictionary로 바꿔줬기 때문에 
                                        # anchor['href']가 가능한 것
                company, kind, region = anchor.find_all("span", class_="company")       # find_all()은 찾은 모든 것들의 list를 주고
                title = anchor.find("span", class_="title")                             # find()는 기준에 맞는 첫 번째 항목을 찾아줌, 여기선 class가 title인 span태그 
                print(company.string, kind.string, region.string, title.string)
                print("=======================================================================")
                job_data = {
                    'link' : f"https://weworkremotely.com{link}",
                    'company' : company.string.replace(",", " "),
                    'location' : region.string.replace(",", " "),
                    'position' : title.string.replace(",", " "),
                }
                results.append(job_data)
        return results