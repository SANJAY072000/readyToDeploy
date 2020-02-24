from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from flask import Flask, request, jsonify, render_template
from selenium.common.exceptions import StaleElementReferenceException
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    url = [str(x) for x in request.form.values()]
    url=url[0]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


    # options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument("--test-type")
    # options.add_argument("--headless")
    # options.binary_location = "/usr/bin/chromium"
    # driver = webdriver.Chrome("./chromedriver_win32/chromedriver.exe")


    driver.get(url)
    lst2,allemnts=list(),list()

    # sleep for 3 seconds
    time.sleep(3)

    driver.refresh()
    # if url != driver.current_url:
    driver.get(driver.current_url)

    allemnts = driver.find_elements()


    # # JS pages take time to load and sometimes after we scroll down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"
                          "var lenOfPage=document.body.scrollHeight;return lenOfPage;")


    # lst1 is the list of all urls
    lst1 = list()


    # select all urls based on href attribute through XPATH
    lst2 += driver.find_elements_by_xpath('//a[@href]')


    # all hoverable elements
    for i in allemnts:
        actionchains = ActionChains(driver)
        actionchains.move_to_element(i).perform()
        lst2 += driver.find_elements_by_xpath('//a[@href]')

    # all clickable elements
        for i in allemnts:
            actionchains = ActionChains(driver)
            actionchains.click(i).perform()
            lst2 += driver.find_elements_by_xpath('//a[@href]')


    for i in lst2:
            try:
                lst1.append(i.get_attribute('href'))
            except StaleElementReferenceException as Exception:
                print('StaleElementReferenceException while trying to type password,\
                 trying to find element again')


    time.sleep(3)
    driver.close()
    data = list(set(lst1))

    return render_template('index.html', prediction_text=data)


if __name__ == "__main__":
    app.run(debug=True)
