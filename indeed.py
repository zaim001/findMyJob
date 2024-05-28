import time
import pandas as pd
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from tabulate import tabulate
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-US")
driver = uc.Chrome(options=options)
driver.get("https://www.indeed.com/")

wait = WebDriverWait(driver, 5)

time.sleep(5)
job = input("Enter Job Title : ")
location = input("Enter your Location : ")

search_job = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input#text-input-what"))
)
search_job.send_keys(job)

search_location = driver.find_element(By.ID, "text-input-where")
search_location.send_keys(location)

search_button = driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
search_button.click()


df = pd.DataFrame(columns=['Job Title', 'Company', 'Date', 'Location', 'Job Type', 'Link'])

while True:
    boxes = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
    for b in boxes:
        link = b.find_element(By.CSS_SELECTOR, "table tbody tr td div h2 a").get_attribute('href')
        job_title = b.find_element(By.CSS_SELECTOR, "table tbody tr td div h2 a span[title]").text
        company = b.find_element(By.CSS_SELECTOR, "table tbody tr td div div span[data-testid='company-name']").text
        date_posted = b.find_element(By.CSS_SELECTOR, "div.underShelfFooter div span").text
        date_posted = date_posted.replace("Posted", "")
        date_posted = date_posted.replace("Employer", "")
        job_location = b.find_element(By.CSS_SELECTOR, "table tbody tr td div div div").text
        try:
            job_type = b.find_element(By.CSS_SELECTOR, "table.big6_visualChanges tbody tr td div.jobMetaDataGroup div div div").text
        except NoSuchElementException:
            job_type = "None"

        data = pd.DataFrame({'Job Title': [job_title], 'Company': [company],'Date': [date_posted], 'Location':[job_location], 'Job Type': [job_type], 'Link': [link]})
        df = pd.concat([df, data], ignore_index=True)
    try:
        next_page = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next Page']").get_attribute('href')
        driver.get(next_page)
        try:
            dialog = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#mosaic-desktopserpjapopup div button"))
            )
            dialog.click()
        except TimeoutException:
            pass

        time.sleep(1)
    except NoSuchElementException:
        print("No more pages")
        break
    break

if df.empty:
    print(f"No Data Found for {job} in {location}")
else:
    print(tabulate(df, headers='keys', tablefmt='pretty'))
    df.to_csv('indeed.csv', index=False)
    df.to_excel('indeed.xlsx', index=False)

driver.quit()