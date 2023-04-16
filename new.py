



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

    for num, tag in enumerate(tags_input, 1):
        tag.click()
        x = browser.find_element(By.ID, f'result{num}')
        if x.text:
            list_res.append(num)

        tag.send_keys(Keys.DOWN)

    #list_res = [i.text for i in browser.find_elements(By.ID, 'result')]
    print(sum(list_res))




