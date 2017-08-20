import aiohttp
import asyncio
import async_timeout
import os
from selenium import webdriver
import time


async def my_coroutine(x):
    driver = webdriver.Chrome("C:/Users/Greg/PycharmProjects/1369328/chromedriver_win32/chromedriver.exe")
    driver.get('http://www.findpeoplesearch.com/')
    # click Expand Form button
    # the [0] is there because find_elements_by_id returns a list
    expand_form_button = driver.find_elements_by_id("more-btn")[0]
    expand_form_button.click()
    if (x == 1 ):
        await asyncio.sleep(20)
    driver.close()
    print('Closing driver ' + str(x))
    return



if __name__ == '__main__':
#    driver = webdriver.Chrome("C:/Users/Greg/PycharmProjects/1369328/chromedriver_win32/chromedriver.exe")
    start = time.time()
    loop = asyncio.get_event_loop()
    tasks = []
    url = 'http://www.findpeoplesearch.com/'
    for i in range(3):
        task = asyncio.ensure_future(my_coroutine(i))
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
