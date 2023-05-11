import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import time

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

driver.get('http://prepssm.it/user/login')

driver.implicitly_wait(30)
driver.find_element(By.CSS_SELECTOR, '.cursor-pointer.text-theme-gray-two.text-12.text-right.underline').click()

driver.find_element(By.ID, 'mat-input-0').send_keys('.....')
driver.find_element(By.ID, 'mat-input-1').send_keys('.....')
driver.find_element(By.CSS_SELECTOR, '.mat-ripple.btn-nnki.btn-nnki-primary.btn-nnki-100.btn-nnki-uppercase.btn-nnki-i'
                                     'con-right.mat-ripple-unbounded.ng-star-inserted').click()

driver.implicitly_wait(30)
# driver.find_element(By.CSS_SELECTOR, 'nav > div.sidenav_nav > div.sidenav_menu > a:nth-child(3)').click()
driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH,
                                                                   '//*[@id="appComponentContent"]/app-logged-area/mat-sidenav'
                                                                   '-container/mat-sidenav/div/app-logged-side-nav/nav/div['
                                                                   '2]/div[2]/a[3]'))
driver.implicitly_wait(30)
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="appComponentContent"]/app-logged-area/mat-sidenav-container/mat-sidenav-content/div/app-exams-home/section/div[1]/div/div').click()
driver.find_element(By.CSS_SELECTOR, '#mat-checkbox-2').click()
driver.find_element(By.CLASS_NAME, 'filters-close').click()

time.sleep(10)
for i in range(30):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)

time.sleep(10)
soup = BeautifulSoup(driver.page_source, 'lxml')
elements = soup.select('app-exam-card')

prepQuiz = []
for element in elements:
    title = element.select_one('.card-title .ng-star-inserted').text
    # if title[:8] == 'PrepQUIZ':
    prepQuiz.append(element)

print(len(prepQuiz))
data = []

for i in range(1):
    row = {}
    #  switching between tabs
    exam = prepQuiz[i]
    driver.implicitly_wait(30)
    new_tab_link = exam.select_one('div.card.card--picto-corner a')['href']
    driver.execute_script(f"window.open('{new_tab_link}');")
    driver.switch_to.window(driver.window_handles[1])
    driver.implicitly_wait(30)
    driver.find_element(By.CSS_SELECTOR, '.mat-ripple.btn-nnki.btn-nnki-primary.btn-nnki-uppercase.btn-nnki-heavy.'
                                         'mat-ripple-unbounded.ng-star-inserted').click()

    try:
        button = WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'div.modal-buttons button'))
        )
        button.click()
    except:
        pass

    for i in range(30):
        buttons = driver.find_elements(By.CSS_SELECTOR,
                                       '.mat-ripple.btn-nnki.btn-nnki-white.btn-nnki-uppercase.btn-nnki-'
                                       'heavy.mat-ripple-unbounded.ng-star-inserted')
        driver.execute_script("arguments[0].click();", buttons[-1])

    driver.implicitly_wait(10)
    driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR,
                                                                       'div.modal-buttons > button.mat-ripple.btn-nnki.btn-nnki-primary.btn-nnki-uppercase.mat-ripple-unbounded'))

    driver.implicitly_wait(10)
    driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR,
                                                                       'div.modal_content.-large > div > div.modal-text > div.modal-buttons > button'))
    driver.implicitly_wait(30)
    driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR,
                                                                       'app-modal-end-exam > div.modal_content.-large > button'))

    driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR,
                                                                       '.card-row.mb-4.leading-snug.ng-star-inserted'))
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    item_code = soup.select('.min-w-\\[65px\\]')
    item_description = soup.select('.line-clamp-2')

    # correction link
    driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR,
                                                                       '.mat-tooltip-trigger.cursor-pointer.text-site-main-one.font-semibold.ng-star-inserted'))
    # If there is a premium
    try:
        button = WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, '.mat-modal-closer'))
        )
        button.click()
    except:
        pass

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    questions = soup.select('.card.card--nnki-question.ng-star-inserted')
    questions_driver = driver.find_elements(By.CSS_SELECTOR, '.card.card--nnki-question.ng-star-inserted')

    for index, question in enumerate(questions):
        row = {}
        row['Question'] = question.select_one('.question-description.select-text.nnki-no-select.ng-star-inserted').text
        alternatives = question.select('label > span.mat-radio-label-content')
        row['A'] = alternatives[0].text.replace('\xa0 A.\xa0 ', '')
        row['B'] = alternatives[1].text.replace('\xa0 B.\xa0 ', '')
        row['C'] = alternatives[2].text.replace('\xa0 C.\xa0 ', '')
        row['D'] = alternatives[3].text.replace('\xa0 D.\xa0 ', '')
        row['E'] = alternatives[4].text.replace('\xa0 E.\xa0 ', '')
        row['Correct Answer'] = question.select_one('.-answerShould').text.split()[0].replace('.', '')
        row['Correction'] = question.select_one('.-correction app-question-content').text

        time.sleep(1)
        driver.execute_script("arguments[0].click();", questions_driver[index].find_element(By.CSS_SELECTOR, 'div.ml-auto.mr-8.cursor-pointer.flex.items-center.text-12.space-x-2.ng-star-inserted > span'))
        driver.implicitly_wait(30)
        item_needed = driver.find_element(By.CSS_SELECTOR, '.mat-ripple.mat-tab-label.mat-focus-indicator.mat-tab-label-active.ng-star-inserted').text
        for jndex, item in enumerate(item_code):
            if item.text.lower().replace(' ', '') == item_needed.lower().replace(' ', ''):
                row['Item'] = item.text.strip()
                row['Item_topic'] = item_description[jndex].text.strip()
        driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR,  '.mat-modal-closer.-xs-black'))

        row['Question Image-src'] = ' '
        try:
            img_link = question.select_one('app-question-header+ .card-content .cursor-pointer')['src']
            row['Question Image-src'] = img_link
        except:
            pass

        correction_links = question.select('div.question-description.select-text.nnki-no-select.ng-star-inserted p a')

        for i in range(4):
            row['Correction link' + str(i + 1)] = ' '
            row['Correction link' + str(i + 1) + '-href'] = ' '
            try:
                row['Correction link' + str(i + 1)] = correction_links[i].text
                row['Correction link' + str(i + 1) + '-href'] = correction_links[i]['href']
            except:
                pass

        correction_image = question.select('.object-center , .-correction .relative')
        for i in range(4):
            row['Correction img' + str(i + 1) + '-srCorrection'] = ' '
            try:
                row['Correction img' + str(i + 1) + '-srCorrection'] = correction_image[i]['src']
            except:
                pass
        print(row)
        data.append(row)

    title = prepQuiz[i].select_one('.card-title .ng-star-inserted').text
    if len(data) == 30:
        df = pandas.DataFrame(data)
        with pandas.ExcelWriter("exams.xlsx") as writer:
            df.append(writer, sheet_name='test')

    driver.close()
    time.sleep(10)
    driver.switch_to.window(driver.window_handles[0])

df = pandas.DataFrame(data)
if len(data) == 31:
    df_old = pandas.read_excel('exams.xlsx')
    df_new = pandas.concat([df_old, df])
    df_new.to_excel('exams.xlsx', index=False)

driver.quit()
