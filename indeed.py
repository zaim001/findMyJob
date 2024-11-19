import time
import pandas as pd
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from tabulate import tabulate
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument("--headless")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-US")
driver = uc.Chrome(options=options)
driver.get("https://www.indeed.com/")

wait = WebDriverWait(driver, 5)

job = input("Enter Job Title : ")
location = input("Enter your Location : ")
n_page = int(input("Enter number of pages to scrap : "))

search_job = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='text-input-what']"))
)
search_job.send_keys(job)

search_location = driver.find_element(By.ID, "text-input-where")
search_location.send_keys(location)

search_location.send_keys(Keys.ENTER)
time.sleep(3)


df = pd.DataFrame(columns=['Job Title', 'Company', 'Date', 'Location', 'Job Type', 'Link'])

for page in range(n_page):
    print(f"Scraping page {page + 1}...")
    try:
        boxes = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
        for b in boxes:
            link = b.find_element(By.CSS_SELECTOR, "a.jcs-JobTitle").get_attribute('href')
            job_title = b.find_element(By.CSS_SELECTOR, "span[title]").text
            try:
                company = b.find_element(By.CSS_SELECTOR, "span[data-testid='company-name']").text
            except NoSuchElementException:
                company = "_"
            try:
                date_posted = b.find_element(By.CSS_SELECTOR, "span[data-testid='myJobsStateDate']").text
                date_posted = date_posted.replace("Posted", "").strip()
                date_posted = date_posted.replace("Employer", "").strip()
            except NoSuchElementException:
                date_posted = "_"
            job_location = b.find_element(By.CSS_SELECTOR, "div[data-testid='text-location']").text
            try:
                job_type = b.find_element(By.CSS_SELECTOR, "div[data-testid='attribute_snippet_testid']").text
            except NoSuchElementException:
                job_type = "_"

            data = pd.DataFrame({'Job Title': [job_title], 'Company': [company],
                                 'Date': [date_posted], 'Location': [job_location],
                                 'Job Type': [job_type], 'Link': [link]})
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
                pass  # No dialog appeared
            time.sleep(2)
        except NoSuchElementException:
            print("No more pages found.")
            break

    except Exception as e:
        print(f"Error on page {page + 1}: {e}")
        break

if df.empty:
    print(f"No data found for {job} in {location}.")
else:
    print(tabulate(df, headers='keys', tablefmt='pretty'))
    df.to_csv('indeed.csv', index=False)
    df.to_excel('indeed.xlsx', index=False)

driver.quit()