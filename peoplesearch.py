import aiohttp
import asyncio
import async_timeout
import os
from selenium import webdriver
import time
import logging

def read_file(input_file):
    with open(input_file) as f:
        input_data = f.readlines()
        # remove whitespace characters like `\n` at the end of each line
        input_data = [x.strip() for x in input_data]
        return input_data

def strip_blank_lines(input_list):
    input_no_blank_lines = []
    for x in input_list:
        if x != '':
            input_no_blank_lines.append(x)
    return input_no_blank_lines

def remove_comment_lines (input_list):
    clean_input_data = []
    for x in input_list:
        if x[0:1] != '#':
            clean_input_data.append(x)
    return clean_input_data

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
    logging.basicConfig(filename='bitcoin_value.log', level=DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
#   logging.disable(logging.DEBUG)
#    driver = webdriver.Chrome("C:/Users/Greg/PycharmProjects/1369328/chromedriver_win32/chromedriver.exe")
# load webdriver_loc, out_file, page_timeout into global variables
# read data from input file and get all combos for searching
    start = time.time()
    loop = asyncio.get_event_loop()
    tasks = []
    url = 'http://www.findpeoplesearch.com/'
    for i in range(3):
        task = asyncio.ensure_future(my_coroutine(i))
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
