


import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


url = 'https://parsinger.ru/scroll/3/'


with webdriver.Chrome() as browser:
    browser.get(url)
    tags_input = browser.find_elements(By.TAG_NAME, 'input')
    list_res = []

    for tag in tags_input:
        tag.click()
        tag.send_keys(Keys.DOWN)

    list_res = [num for num, i in enumerate(browser.find_elements(By.CSS_SELECTOR, 'span'), 1) if i.text]
    print(list_res)
    print(sum(list_res))




