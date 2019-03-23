import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_text(url):

    options = Options()
    options.add_argument('--headless')
    driver_path = './chromedriver'
    driver = webdriver.Chrome(driver_path, options=options)

    try:
        driver.get(url=url)
    except:
        print('URLNotFoundError: please input url when you use the programme.')

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    soup_list = soup.find_all("div", class_="body")

    names_messages = []
    for soup in soup_list:
        names_messages.extend(soup.text.split("\n"))

    dic = {}

    for names_message_ in names_messages:

        if re.match("^.*?「.*?」$", names_message_):
            try:
                names_, message_ = names_message_.split("「")
                message = message_[:-1]
            except:
                message = ""

            names = re.split(r"[＆\&・\+]", names_)

            for name in names:
                if name not in dic:
                    dic[name] = []

                dic[name].append(message)
        print(names_message_)

    driver.close()
    driver.quit()

    for name in dic:
        with open("resources/"+name+".txt", mode="a") as file:
            for message in dic[name]:
                file.write(message+"\n")

if __name__=="__main__":


    urls = [
        "http://lovegundam.dtiblog.com/blog-category-7.html",
        "http://lovegundam.dtiblog.com/category7-1.html",
        "http://lovegundam.dtiblog.com/category7-2.html",
        "http://lovegundam.dtiblog.com/category7-3.html",
        "http://lovegundam.dtiblog.com/category7-4.html",
    ]
    for url in urls:
        get_text(url)

