from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    url = [str(x) for x in request.form.values()]
    url=url[0]

    options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(url)

    # JS pages take time to load and sometimes after we scroll down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"
                          "var lenOfPage=document.body.scrollHeight;return lenOfPage;")

    # sleep for 3 seconds
    time.sleep(3)

    # lst1 is the list of all urls
    lst1 = list()

    # lst2 is the list of all selenium selections based on regular expression
    lst2 = list()

    # select all urls based on href attribute through XPATH
    lst2 += driver.find_elements_by_xpath('//*[@href]')

    # select all urls based on src attribute through XPATH
    lst2 += driver.find_elements_by_xpath('//*[@src]')

    # select the elements
    btns, allemnts = list(), list()
    btns = driver.find_elements_by_name('button')
    allemnts = driver.find_elements()

    # button click
    for i in btns:
        actionchains = ActionChains(driver)
        actionchains.click(i).perform()
        lst2 += driver.find_elements_by_xpath('//*[@href]')
        lst2 += driver.find_elements_by_xpath('//*[@src]')

    # button hover
    for i in btns:
        actionchains = ActionChains(driver)
        actionchains.move_to_element(i).perform()
        lst2 += driver.find_elements_by_xpath('//*[@href]')
        lst2 += driver.find_elements_by_xpath('//*[@src]')

    # all hoverable elements
    for i in allemnts:
        actionchains = ActionChains(driver)
        actionchains.move_to_element(i).perform()
        lst2 += driver.find_elements_by_xpath('//*[@href]')
        lst2 += driver.find_elements_by_xpath('//*[@src]')

    # all clickable elements
        for i in allemnts:
            actionchains = ActionChains(driver)
            actionchains.click(i).perform()
            lst2 += driver.find_elements_by_xpath('//*[@href]')
            lst2 += driver.find_elements_by_xpath('//*[@src]')

    for i in lst2:
        lst1.append(i.get_attribute('href'))
        lst1.append(i.get_attribute('src'))

    # sleep for 1 seconds
    time.sleep(1)
    driver.close()
    data=list(set(lst1))

    return render_template('index.html', prediction_text=data)


if __name__ == "__main__":
    app.run(debug=True)
