import time

import pandas as pd
import undetected_chromedriver as uc
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from tabulate import tabulate
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-US")
options.add_argument('--blink-settings=imagesEnabled=false')
driver = uc.Chrome(options=options)
url = "https://www.linkedin.com/jobs/search?locale=en_US"
wait = WebDriverWait(driver, 5)

driver.get(url)


def get_jobs_url():
    if not driver.current_url.startswith(url):
        driver.get("https://www.linkedin.com/jobs/search?locale=en_US")
        time.sleep(3)


def scroll_down():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, -100);")
    time.sleep(1)


get_jobs_url()

job_title = input("Enter your Job : ")
job_place = input("Enter the location : ")

################Searching################
job_search = driver.find_element(By.CSS_SELECTOR, "section.dismissable-input input#job-search-bar-keywords")
job_search.send_keys(job_title)
location_search = driver.find_element(By.CSS_SELECTOR, "section.dismissable-input input#job-search-bar-location")
location_search.clear()
location_search.send_keys(job_place)
location_search.send_keys(Keys.ENTER)
#########################################
while True:
    df = pd.DataFrame(columns=['Title', 'Company', 'Location', 'Date', 'Seniority Level', 'Employment Type', 'Job Function', 'Industries', 'Link'])
    jobs_list = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li div.base-card")
    links = []
    try:
        load_more = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[2]/button')
        if load_more.is_displayed():
            load_more.click()
        scroll_down()
    except NoSuchElementException:
        pass

    jobs_length = len(jobs_list)
    print(f"{jobs_length} Results found for : {job_title} in {job_place}.")
    if jobs_length > 0:
        print("Loading... Please Wait")
    for c in jobs_list:
        c.click()
        time.sleep(2)
    for j in jobs_list:
        title = j.find_element(By.CSS_SELECTOR, "div h3").text
        company = j.find_element(By.CSS_SELECTOR, "div h4 a").text
        location = j.find_element(By.CSS_SELECTOR, "div div span.job-search-card__location").text
        date = j.find_element(By.CSS_SELECTOR, "div div time").text
        link = j.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        links.append(link)
        j.click()
        time.sleep(1)
        try:
            sen_lvl = driver.find_element(By.XPATH, "//h3[normalize-space()='Seniority level']/following-sibling::span").text
            if not sen_lvl.strip():
                sen_lvl = "_"
            emp_type = driver.find_element(By.XPATH, "//h3[normalize-space()='Employment type']/following-sibling::span").text
            if not emp_type.strip():
                emp_type = "_"
            job_func = driver.find_element(By.XPATH,"//h3[normalize-space()='Job function']/following-sibling::span").text
            if not job_func.strip():
                job_func = "_"
            ind = driver.find_element(By.XPATH,"//h3[normalize-space()='Industries']/following-sibling::span").text
            if not ind.strip():
                ind = "_"
        except NoSuchElementException:
            sen_lvl = "None"
            emp_type = "None"
            job_func = "None"
            ind = "None"

        data = pd.DataFrame(
            {'Title': [title], 'Company': [company], 'Location': [location], 'Date': [date],
             'Seniority Level': [sen_lvl], 'Employment Type': [emp_type], 'Job Function': [job_func],
             'Industries': [ind], 'Link': [link]}
        )
        df = pd.concat([df, data], ignore_index=True)

    print(tabulate(df, headers='keys', tablefmt='pretty'))
    df.to_csv('linkedin.csv', index=False)
    df.to_excel('linkedin.xlsx', index=False)
    break

driver.quit()
