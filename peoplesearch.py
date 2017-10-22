import aiohttp
import asyncio
import async_timeout
import os
from selenium import webdriver
import time
import logging

def get_input_data (input_file):
    inputs= []
    with open(input_file) as f:
        input_data = f.readlines()
        # remove whitespace characters like `\n` at the end of each line
        input_data = [x.strip() for x in input_data]
    input_no_blank_lines =[]
    for x in input_data:
        if x != '':
            input_no_blank_lines.append(x)
    clean_input_data =[]
    for x in input_no_blank_lines:
        if x[0:1] != '#':
            clean_input_data.append(x)

    logging.debug(clean_input_data)
    logging.debug(len(clean_input_data))

    webdriver = (clean_input_data[0][clean_input_data[0].find('=') + 1:]).split(',')
    webdriver = webdriver[0].strip()
    inputs.append(webdriver)

    out_file = (clean_input_data[1][clean_input_data[1].find('=') + 1:]).split(',')
    out_file = out_file[0].strip()
    inputs.append(out_file)

    page_timeout = (clean_input_data[2][clean_input_data[2].find('=') + 1:]).split(',')
    page_timeout = page_timeout[0].strip()
    inputs.append(page_timeout)

    full_name = (clean_input_data[3][clean_input_data[3].find('=') + 1:]).split(',')
    full_name = [x.strip() for x in full_name]
    inputs.append(full_name)

    email = (clean_input_data[4][clean_input_data[4].find('=') + 1:]).split(',')
    email = [x.strip() for x in email]
    inputs.append(email)

    street = (clean_input_data[5][clean_input_data[5].find('=') + 1:]).split(',')
    street = [x.strip() for x in street]
    inputs.append(street)

    city = (clean_input_data[6][clean_input_data[6].find('=') + 1:]).split(',')
    city = [x.strip() for x in city]
    inputs.append(city)

    zip_code = (clean_input_data[7][clean_input_data[7].find('=') + 1:]).split(',')
    zip_code = [x.strip() for x in zip_code]
    inputs.append(zip_code)

    maiden_name = (clean_input_data[8][clean_input_data[8].find('=') + 1:]).split(',')
    maiden_name = [x.strip() for x in maiden_name]
    inputs.append(maiden_name)

    phone = (clean_input_data[9][clean_input_data[9].find('=') + 1:]).split(',')
    phone = [x.strip() for x in phone]
    inputs.append(phone)

    ssn = (clean_input_data[10][clean_input_data[10].find('=') + 1:]).split(',')
    ssn = [x.strip() for x in ssn]
    inputs.append(ssn)

    age = (clean_input_data[11][clean_input_data[11].find('=') + 1:]).split(',')
    age = [x.strip() for x in age]
    inputs.append(age)

    state = (clean_input_data[12][clean_input_data[12].find('=') + 1:]).split(',')
    state = [x.strip() for x in state]
    inputs.append(state)

    dob = (clean_input_data[13][clean_input_data[13].find('=') + 1:]).split(',')
    dob = [x.strip() for x in dob]
    inputs.append(dob)

    logging.debug(inputs)
    return(inputs)

async def my_coroutine(x):
    driver = webdriver.Chrome(webdriver_path)
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
    FORMAT='%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT, filename='bitcoin_value.log', level=logging.DEBUG)
#   logging.disable(logging.DEBUG)
#    driver = webdriver.Chrome("C:/Users/Greg/PycharmProjects/1369328/chromedriver_win32/chromedriver.exe")
# load webdriver_loc, out_file, page_timeout into global variables
    inputs = get_input_data('C:\\Users\\Greg\\PycharmProjects\\1369328\\input.txt')
    webdriver_path = inputs[0]
# read data from input file and get all combos for searching
    start = time.time()
    loop = asyncio.get_event_loop()
    tasks = []
    url = 'http://www.findpeoplesearch.com/'
    for i in range(3):
        task = asyncio.ensure_future(my_coroutine(i))
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
