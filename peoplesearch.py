import os
import threading
from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import arrow
import time
import logging
import us_state_abbreviations
import itertools
import sys
import uuid
import csv
from pprint import pprint
from pprint import pformat
from bs4 import BeautifulSoup


# get the data from the input file
# add current date to name of output file
def get_input_data(input_file):
    inputs = []
    with open(input_file) as f:
        input_data = f.readlines()
        # remove whitespace characters like `\n` at the end of each line
        input_data = [x.strip() for x in input_data]
    input_no_blank_lines = []
    for x in input_data:
        if x != '':
            input_no_blank_lines.append(x)
    clean_input_data = []
    for x in input_no_blank_lines:
        if x[0:1] != '#':
            clean_input_data.append(x)

    logging.debug(clean_input_data)
    logging.debug(len(clean_input_data))

    webdriver = (clean_input_data[0][clean_input_data[0].find('=') + 1:])
    webdriver = webdriver.strip()
    logging.info('webdriver = ' + webdriver)
    inputs.append(webdriver)

    out_file = (clean_input_data[1][clean_input_data[1].find('=') + 1:]).split(',')
    out_file = out_file[0].strip()
    parts = out_file.split('.')
    date_string = arrow.now().format('MM_DD_YYYY_HH_mm')
    out_file = parts[0] + date_string + '.' + parts[1]
    logging.info('Output file = ' + out_file)
    inputs.append(out_file)

    page_timeout = (clean_input_data[2][clean_input_data[2].find('=') + 1:])
    page_timeout = page_timeout.strip()
    logging.info('page timeout = ' + page_timeout)
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

    max_browsers = (clean_input_data[14][clean_input_data[14].find('=') + 1:])
    max_browsers = max_browsers.strip()
    logging.info('max browsers = ' + max_browsers)
    inputs.append(max_browsers)

    level = (clean_input_data[15][clean_input_data[15].find('=') + 1:])
    level = level.strip()
    logging.info('log level = ' + level)
    inputs.append(level)

    logging.debug(inputs)
    return inputs


def validate_data(inputs):
    # data validation on email, zip, phone number, ssn, age, state, dob
    # if data is bad, log it, output message to console, and skip that value
    logging.debug("length of inputs = " + str(len(inputs)))
    logging.debug(type(inputs))
    for x in range(0, len(inputs)):
        logging.debug('input' + str(x) + ' = ' + str((inputs[x])))

    # email is inputs[4]
    if len(inputs[4]) == 1:
        pass
    else:
        remove_me = []
        for i in range(0, len(inputs[4])):
            if '@' not in inputs[4][i]:
                remove_me.append(inputs[4][i])
                logging.info('Invalid email address: ' + inputs[4][i])
        for j in range(0, len(remove_me)):
            inputs[4].remove(remove_me[j])

    # zip_code is inputs[7]
    if len(inputs[7]) == 1:
        pass
    else:
        remove_me = []
        for i in range(0, len(inputs[7])):
            if len(inputs[7][i]) != 5:
                remove_me.append(inputs[7][i])
        for k in range(0, len(remove_me)):
            logging.info('Invalid zip code: ' + remove_me[k])
            inputs[7].remove(remove_me[k])
        remove_me = []
        for i in range(0, len(inputs[7])):
            for j in range(0, len(inputs[7][i])):
                if not (inputs[7][i][j].isdigit()):
                    remove_me.append(inputs[7][i])
        for k in range(0, len(remove_me)):
            logging.info('Invalid zip code: ' + remove_me[k])
            inputs[7].remove(remove_me[k])

    # phone is inputs[9]
    if len(inputs[9]) == 1:
        pass
    else:
        remove_me = []
        for i in range(0, len(inputs[9])):
            if len(inputs[9][i]) != 12:
                remove_me.append(inputs[9][i])
        for k in range(0, len(remove_me)):
            logging.info('Invalid phone: ' + remove_me[k])
            inputs[9].remove(remove_me[k])
        remove_me = []
        for i in range(0, len(inputs[9])):
            phone_bool = True
            for j in range(0, len(inputs[9][i])):
                if j in (0, 1, 2, 4, 5, 6, 8, 9, 10, 11):
                    if not (inputs[9][i][j].isdigit()):
                        phone_bool = False
                if j in (3, 7):
                    if inputs[9][i][j] != '-':
                        phone_bool = False
            if not phone_bool:
                remove_me.append(inputs[9][i])
                logging.info('Invalid phone: ' + inputs[9][i])
        for k in range(0, len(remove_me)):
            inputs[9].remove(remove_me[k])

    # ssn is inputs[10]
    if len(inputs[10]) == 1:
        pass
    else:
        remove_me = []
        for i in range(0, len(inputs[10])):
            if len(inputs[10][i]) != 11:
                remove_me.append(inputs[10][i])
        for k in range(0, len(remove_me)):
            logging.info('Invalid SSN: ' + remove_me[k])
            inputs[10].remove(remove_me[k])
        remove_me = []
        for i in range(0, len(inputs[10])):
            ssn_bool = True
            for j in range(0, len(inputs[10][i])):
                if j in (0, 1, 2, 4, 5, 7, 8, 9, 10):
                    if not (inputs[10][i][j].isdigit()):
                        ssn_bool = False
                if j in (3, 7):
                    if inputs[10][i][j] != '-':
                        ssn = False
            if not ssn_bool:
                remove_me.append(inputs[10][i])
                logging.info('Invalid SSN: ' + inputs[10][i])
        for k in range(0, len(remove_me)):
            inputs[10].remove(remove_me[k])

    # age is inputs[11]
    if len(inputs[11]) == 1:
        pass
    else:
        remove_me = []
        for i in range(0, len(inputs[11])):
            if (int(inputs[11][i]) < 18) or (int(inputs[11][i]) > 95):
                logging.info('Invalid age: ' + inputs[11][i])
                remove_me.append(inputs[11][i])
        for k in range(0, len(remove_me)):
            inputs[11].remove(remove_me[k])

        # state is inputs[12]
        remove_me = []
        inputs[12] = [element.upper() for element in inputs[12]]
        for i in range(0, len(inputs[12])):
            if inputs[12][i] not in us_state_abbreviations.states:
                logging.info('Invalid state: ' + inputs[12][i])
                remove_me.append(inputs[12][i])
        for k in range(0, len(remove_me)):
            inputs[12].remove(remove_me[k])

    # dob is inputs[13]
    if len(inputs[13]) == 1:
        pass
    else:
        remove_me = []
        for i in range(0, len(inputs[13])):
            if (inputs[13][i]).count('/') != 2:
                remove_me.append(inputs[13][i])
        for k in range(0, len(remove_me)):
            logging.info('Invalid date: ' + remove_me[k])
            inputs[13].remove(remove_me[k])
        remove_me = []
        for i in range(0, len(inputs[13])):
            dob_bool = True
            the_date = inputs[13][i].split('/')
            month = the_date[0]
            day = the_date[1]
            year = the_date[2]
            if int(month) < 1 or int(month) > 12:
                dob_bool = False
            if int(day) < 1 or int(day) > 31:
                dob_bool = False
            if int(year) < 1900:
                dob_bool = False
            if not dob_bool:
                remove_me.append(inputs[13][i])
                logging.info('Invalid dob: ' + inputs[13][i])
        for k in range(0, len(remove_me)):
            inputs[13].remove(remove_me[k])
    return inputs


def get_input_scenarios(inputs):
    logging.debug(inputs)
    for i in range(3, 14):
        logging.debug('input ' + str(i))
        logging.debug(inputs[i])
    strs_of_scenarios = [','.join(str(y) for y in x) for x in itertools.product(inputs[3],
                                                                                inputs[4], inputs[5], inputs[6],
                                                                                inputs[7], inputs[8], inputs[9],
                                                                                inputs[10],
                                                                                inputs[11], inputs[12], inputs[13])]
    for j in range(len(strs_of_scenarios)):
        scenarios.append(strs_of_scenarios[j].split(','))
    logging.debug(pformat(scenarios))
    return scenarios


def my_search(my_scenario, tasknum):
    logging.basicConfig(format=FORMAT, filename=FILENAME, level=numeric_level)
    driver = webdriver.Chrome(WEBDRIVER_PATH)
    driver.get(URL)
    # click Expand Form button
    # the [0] is there because find_elements_by_id returns a list
    expand_form_button = driver.find_elements_by_id("more-btn")[0]
    expand_form_button.click()
    # <input type="text" name="full_name" id="full_name"
    try:
        driver.wait = WebDriverWait(driver, page_timeout)
    except TimeoutException:
        my_data[tasknum] = ['Error - webpage did not load within '
                            + str(page_timeout) + ' seconds', '']
        driver.quit()
        sys.exit()
    full_name_tbox = driver.wait.until(ec.presence_of_element_located((By.NAME, "full_name")))

    if my_scenario[0] != '':
        name = driver.find_element_by_id("full_name")
        name.send_keys(my_scenario[0])

    if my_scenario[1] != '':
        email = driver.find_element_by_name("email")
        email.send_keys(my_scenario[1])

    if my_scenario[2] != '':
        address = driver.find_element_by_name("address")
        address.send_keys(my_scenario[2])

    if my_scenario[3] != '':
        city = driver.find_element_by_name("city")
        city.send_keys(my_scenario[3])

    if my_scenario[4] != '':
        zip_code = driver.find_element_by_name("zip")
        zip_code.send_keys(my_scenario[4])

    if my_scenario[5] != '':
        akas = driver.find_element_by_id("akas")
        akas.send_keys(my_scenario[5])

    if my_scenario[6] != '':
        phone = driver.find_element_by_id("phone")
        phone.send_keys(my_scenario[6])

    if my_scenario[7] != '':
        ssn = my_scenario[7].split('-')
        ssn1 = driver.find_element_by_name("ssn1")
        ssn1.send_keys(ssn[0])
        ssn2 = driver.find_element_by_name("ssn2")
        ssn2.send_keys(ssn[1])
        ssn3 = driver.find_element_by_name("ssn3")
        ssn3.send_keys(ssn[2])

    if my_scenario[8] != '':
        age = driver.find_element_by_id("age")
        age.send_keys(my_scenario[8])

    if my_scenario[9] != '':
        select = Select(driver.find_element_by_name("state"))
        select.select_by_value(my_scenario[9])

    if my_scenario[10] != '':
        dob = my_scenario[10].split('/')
        logging.debug(dob[0], dob[1], dob[2])
        select = Select(driver.find_element_by_name("month"))
        select.select_by_value(dob[0])
        select = Select(driver.find_element_by_name("day"))
        select.select_by_value(dob[1])
        select = Select(driver.find_element_by_name("year"))
        select.select_by_value(dob[2])

    # <button type="submit" class="btn btn-success btn-lg" id="button-search" style="width: 75%">Search</button>
    search_button = driver.find_element_by_id("button-search")
    search_button.send_keys(Keys.ENTER)
    # wait for  <div class="alert alert-info col-md-8"><h4>Search Results for...</h4>
    start_time = time.time()
    try:
        driver.wait = WebDriverWait(driver, page_timeout)
    except TimeoutException:
        my_data[tasknum] = ['Error - webpage did not load within '
                            + str(page_timeout) + ' seconds', '']
        driver.quit()
        sys.exit()
    try:
        page_loaded = driver.wait.until(ec.presence_of_element_located((By.ID, "new-search2")))
    except TimeoutException:
        # if we get a timeout then there are 2 cases:
        # 1 - there were no results found
        # 2- something went wrong
        try:
            soup = BeautifulSoup(driver.page_source, "html5lib")
            no_results = soup.findAll("div", class_="panel panel-primary")
            my_data[tasknum] = ["No results found.", str(tasknum)]
            driver.quit()
            exit(101)
        except NoSuchElementException:
            my_data[tasknum] = ["Something went wrong.", str(tasknum)]
            driver.quit()
            exit(101)
    end_time = time.time()
    logging.info('Task' + str(tasknum) + ': ' + ' Elapsed time for first page = ' + str(end_time - start_time))

    soup = BeautifulSoup(driver.page_source, "html5lib")
    soups = [soup]
    more_pages = True
    while more_pages:
        try:
            next_page = driver.find_element_by_css_selector(
                '#search-results > div:nth-child(6) > div > nav > ul > li.next-page > a')
            logging.debug('Task' + str(tasknum) + ': ' + '  ' + 'next page link found')
        except NoSuchElementException:
            more_pages = False
            break
        start_time = time.time()
        next_page.send_keys(Keys.ENTER)
        try:
            driver.wait = WebDriverWait(driver, page_timeout)
        except TimeoutException:
            my_data[tasknum] = ['Error - webpage did not load within '
                                + str(page_timeout) + ' seconds', '']
            driver.quit()
            sys.exit()
        page_loaded = driver.wait.until(ec.presence_of_element_located((By.ID, "new-search2")))
        end_time = time.time()
        logging.info('Task' + str(tasknum) + ': ' + '  ' + 'Elapsed time = ' + str(end_time - start_time))
        soup = BeautifulSoup(driver.page_source, "html5lib")
        soups.append(soup)
        try:
            last_page = driver.find_element_by_css_selector(
                '#search-results > div:nth-child(6) > div > nav > ul > li.next-page.disabled > a')
            # search-results > div:nth-child(6) > div > nav > ul > li.next-page.disabled
            more_pages = False
            logging.debug('Task' + str(tasknum) + ': ' + '  ' + 'last page found')
            break
        except NoSuchElementException:
            logging.debug('Task' + str(tasknum) + ': ' + '  ' + 'more pages found')
            more_pages = True
    logging.info('Task' + str(tasknum) + ': ' + '  ' + str(len(soups)) + ' pages scraped')
    print("Pages scraped = " + str(len(soups)))

    # get all "panel panel-primary" from all pages (from each soup in soups)
    people = []
    for soup in soups:
        cols = soup.findAll("div", class_="panel panel-primary")
        for i in range(0, len(cols)):
            people.append(cols[i])
    print('number of persons found = ' + str(len(people)))
    logging.debug('Task' + str(tasknum) + ': ' + ' Number of persons found = ' + str(len(people)))
    # todo loop through people[] and get data:
    output = []
    for z in range(0, len(people)):
        one_person = people[z]
        tags = one_person.findAll('li')
        data_headers = one_person.findAll('span', class_='data_header')
        data_header_names = []
        for i in range(0, len(data_headers)):
            data_header_names.append(data_headers[i].text.split())
        logging.debug('Task' + str(tasknum) + ': ' + ' data headers = ')
        logging.debug(data_header_names)
        num_of_addresses = 0
        num_of_phones = 0
        num_of_emails = 0
        for i in range(0, len(data_header_names)):
            if data_header_names[i][1] == 'Street':
                num_of_addresses = int(data_header_names[i][0])
            elif data_header_names[i][1] == 'Phone':
                num_of_phones = int(data_header_names[i][0])
            elif data_header_names[i][1] == 'Email':
                num_of_emails = int(data_header_names[i][0])

        logging.info('Task' + str(tasknum) + ': ' +
                     ' Addresses=' + str(num_of_addresses) + '  Phones=' + str(num_of_phones) +
                     '  Emails=' + str(num_of_emails))

        for i in range(0, num_of_addresses):
            addy_data = str(tags[i])
            begin = addy_data.find('data-person="') + 13
            end = addy_data.find('" data-person-address')
            addy_data_1 = addy_data[begin:end]
            output.append(addy_data_1)
            logging.info('Task' + str(tasknum) + ': ' + addy_data_1)

        for j in range(num_of_addresses, num_of_addresses + num_of_phones):
            phone_data = str(tags[j])
            begin = phone_data.find('<b>Phone number: </b>') + 21
            end = phone_data.find('<br/><b>Company:')
            phone_data_1 = phone_data[begin:end]
            output.append(phone_data_1)
            logging.info('Task' + str(tasknum) + ': ' + phone_data_1)

        for j in range(num_of_addresses + num_of_phones, num_of_addresses + num_of_phones + num_of_emails):
            email_data = str(tags[j])
            begin = email_data.find('<a href="mailto:') + 16
            end = email_data.find('">')
            email_data_1 = email_data[begin:end]
            output.append(email_data_1)
            logging.info('Task' + str(tasknum) + ': ' + email_data_1)

    my_data[tasknum] = output
    driver.quit()


if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    FILENAME = 'peoplesearch' + arrow.now().format('MM_DD_YYYY_HH_mm') + '.log'
    log_level = 'DEBUG'
    with open('input.txt') as f:
        input_data = f.readlines()
    for x in input_data:
        if x.startswith('level='):
            log_level = x[x.find('=') + 1:]
            log_level = log_level.strip()
    numeric_level = getattr(logging, log_level)
    logging.basicConfig(format=FORMAT, filename=FILENAME, level=numeric_level)

    inputs = get_input_data('input.txt')
    logging.debug('inputs = ')
    logging.debug(inputs)
    WEBDRIVER_PATH = inputs[0]
    URL = 'http://www.findpeoplesearch.com/'
    output_file = inputs[1]
    page_timeout = int(inputs[2])
    max_browsers = int(inputs[14])
    clean_inputs = validate_data(inputs)
    logging.debug('clean_inputs = ' + str(clean_inputs))
    # read data from input file and get all combos for searching
    scenarios = []
    scenarios = get_input_scenarios(clean_inputs)
    num_scenarios = len(scenarios)
    logging.info('There are ' + str(len(scenarios)) + ' scenarios to be run')
    print('There are ' + str(len(scenarios)) + ' scenarios to be run')
    if len(scenarios) > max_browsers:
        logging.info('There are too many scenarios to run, please adjust input.txt file '
                     'so that the maximum number of scenarios is less than or equal to ' + str(max_browsers))
        print('There are too many scenarios to run, please adjust input.txt file '
              'so that the maximum number of scenarios is less than or equal to ' + str(max_browsers))
        sys.exit()

    my_data = []
    for i in range(num_scenarios):
        my_data.append(None)
        logging.debug(scenarios[i])
        logging.debug(type(scenarios[i]))
    logging.debug('data = ' + str(my_data))

    logging.info('Threading started')
    print('Threading started')
    scenario_uuid = []
    for j in range(num_scenarios):
        scenario_uuid.append(uuid.uuid4())
        t = Thread(target=my_search, args=(scenarios[j], j,))
        t.start()
        logging.info("Thread " + str(j) + ' started')
        print("Thread " + str(j) + ' started')

    # t.join() doesn't seem to work so I will roll my own
    while threading.active_count() > 1:
        print('Waiting for ' + str(threading.active_count() - 1) + ' threads to finish')
        time.sleep(5)

    with open(output_file, "w") as f_out:
        writer = csv.writer(f_out, lineterminator='\n')
        for z in range(0, len(scenarios)):
            writer.writerow((str(scenario_uuid[z]), str(scenarios[z])))
        for j in range(0, len(my_data)):
            if my_data[j] is not None:
                for k in range(0, len(my_data[j])):
                    out_line = my_data[j][k]
                    out_line = out_line.replace('+', ' ')
                    out_line = out_line.replace('&amp;', ':')
                    out_line = out_line.replace('%2C', ',')
                    writer.writerow((scenario_uuid[j], out_line))
                    print(out_line)
            else:
                writer.writerow((scenario_uuid[j], 'ERROR - no results returned '))
    print('Run completed')
