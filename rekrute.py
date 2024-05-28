import time
import undetected_chromedriver as uc
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from tabulate import tabulate
import pandas as pd
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)

driver.get("https://www.rekrute.com/offres-emploi-maroc.html")

job_keyword = input("Enter Job title/Keyword : ")

job_search = driver.find_element(By.ID, 'keywordSearch')
job_search.send_keys(job_keyword)
job_search.send_keys(Keys.ENTER)

df = pd.DataFrame(columns=['Titre', 'Entreprise', 'Secteur', 'Fonction', 'Experience', 'Niveau Etude', 'Date', 'Nombre Postes', 'Type', 'Link'])

while True:
    jobs_list = driver.find_elements(By.CSS_SELECTOR, "li.post-id")
    for j in jobs_list:
        title = j.find_element(By.CSS_SELECTOR, "div.section h2 a").text
        company = j.find_element(By.TAG_NAME, "img").get_attribute("title")

        if company == "":
            company = 'Confidential'

        secteur = j.find_element(By.CSS_SELECTOR, "div.section div.holder div.info ul li a").text
        fonction = j.find_element(By.CSS_SELECTOR, "div.section div.holder div.info ul li a[href*='/offres.html?positionId']").text
        experience = j.find_element(By.CSS_SELECTOR,"div.section div.holder div.info ul li a[href*='/offres.html?workExperience']").text
        Niveau_etude  = j.find_element(By.CSS_SELECTOR,"div.section div.holder div.info ul li a[href*='/offres.html?studyLevelId']").text
        date_du = j.find_element(By.CSS_SELECTOR, "div.section div.holder em.date span:nth-child(2)").text
        date_au = j.find_element(By.CSS_SELECTOR, "div.section div.holder em.date span:nth-child(3)").text
        date = date_du + "-" + date_au

        try:
            nbr_poste = j.find_element(By.CSS_SELECTOR, "div.section div.holder em.date span:nth-child(4)").text
        except NoSuchElementException:
            nbr_poste = 'N/A'

        type_contrat = j.find_element(By.CSS_SELECTOR,"div.section div.holder div.info ul li a[href*='/offres.html?contractType']").text
        link = j.find_element(By.CSS_SELECTOR, "div.section h2 a").get_attribute("href")
        data = pd.DataFrame({'Titre': [title], 'Entreprise': [company], 'Secteur': [secteur], 'Fonction': [fonction],
                             'Experience': [experience], 'Niveau Etude': [Niveau_etude], 'Date' : [date], 'Nombre Postes' : [nbr_poste] , 'Type': [type_contrat],
                             'Link': [link]})

        df = pd.concat([df, data], ignore_index=True)

    try:
        next = driver.find_element(By.CSS_SELECTOR, "div div.pagination div.section a.next").get_attribute("href")
        driver.get(next)
        time.sleep(1)
    except NoSuchElementException:
        break

if df.empty:
    print(f"No Data Found for {job_keyword}")
else:
    print(tabulate(df, headers='keys', tablefmt='pretty'))
    df.to_csv('rekrute.csv', index=False)
    df.to_excel('rekrute.xlsx', index=False)

driver.quit()