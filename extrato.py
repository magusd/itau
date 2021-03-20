import sys, time, subprocess
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
import os

def wait_for_css(browser, selector):
    print(f"Waiting for: {selector}")
    try:
        element = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
    except:
        browser.quit()
        sys.exit(1)


def password_keypad(browser, password):
    try:
        chain_actions = ActionChains(browser)
        password_keys = browser.find_elements(By.CLASS_NAME, 'campoTeclado')
        for c in password:
            for k in password_keys:
                if c in k.text:
                    chain_actions.click(k)
        chain_actions.click(browser.find_element_by_id('acessar'))
        chain_actions.perform()
    except Exception as e:
        print(e)

def simple_click(browser, selector):
    chain_actions = ActionChains(browser)
    chain_actions.click(browser.find_element_by_css_selector(selector))
    chain_actions.perform()

def handle_stuff():
    opts = Options()
    # opts.headless = True
    ### Pre Login
    profile = FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2) # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', '/Users/magusd/Downloads/itau_extrato')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream;charset=UTF-8')
    browser = Firefox(profile, options=opts)
    browser.get('https://itau.com.br')
    ag = browser.find_element_by_id('agencia')
    ag.send_keys(os.environ.get('ITAU_AGENCY'))
    cc = browser.find_element_by_id('conta')
    cc.send_keys(os.environ.get('ITAU_ACCOUNT'),Keys.ENTER)
    ### Input password
    wait_for_css(browser, ".campoTeclado")
    password_keypad(browser,os.environ.get('ITAU_PASSWORD'))
    ### Navigate to extrato
    wait_for_css(browser, "#VerExtrato")
    simple_click(browser, "#VerExtrato")
    ### Select date
    wait_for_css(browser, "#extrato-filtro-lancamentos")
    wait_for_css(browser, "#select-filtrarPeriodo")
    time.sleep(5)
    selects = browser.find_elements_by_tag_name('select')
    for select in selects:
        if "mês completo (desde 1999)" in select.text:
            select = Select(select)
            select.select_by_visible_text('mês completo (desde 1999)')
    return browser

def download_by_date(browser, month_date):
    wait_for_css(browser, '#month-range-picker')
    browser.find_element_by_id('month-range-picker').find_element_by_tag_name('button').click()
    time.sleep(1)
    browser.find_element_by_class_name('month-picker__dropdown').find_element_by_tag_name('input').send_keys(Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE)
    browser.find_element_by_class_name('month-picker__dropdown').find_element_by_tag_name('input').send_keys(month_date)
    browser.find_element_by_class_name('month-picker__dropdown').find_element_by_tag_name('button').click()
    time.sleep(10)
    wait_for_css(browser, '#botao-opcoes-lancamentos')
    browser.find_element_by_id('botao-opcoes-lancamentos').click()
    links = browser.find_elements_by_tag_name('a')
    for link in links:
        if 'salvar em arquivo de texto' == link.text:
            link.click()
    time.sleep(1)
    download_path = '/Users/magusd/Downloads/itau_extrato/'
    f = subprocess.run(['ls',download_path], stdout=subprocess.PIPE)
    f = f.stdout.decode("utf-8").replace('saved','').replace('\n','')
    subprocess.run(['mv',f'{f}',f'saved/{month_date}.txt'], stdout=subprocess.PIPE, cwd=download_path)
    

    

browser = handle_stuff()
for y in range(2013, 2022):
    for m in range(1,13):
        if y == 2013 and m < 9:
            continue
        if y == 2021 and m > 2:
            continue
        month_date = "{:02d}{:04d}".format(m,y)
        print(f"downloading {month_date}")
        download_by_date(browser, month_date)
        time.sleep(5)


# 
# exportarExtratoArquivo('formExportarExtrato','txt');
#botao-opcoes-lancamentos
# select.select_by_visible_text('mês completo (desde 1999)')
# wait_for_css(browser, "#select-247")
# wait_for_css(browser, "#inputDate248")
# select_filter_date('02/2020')

# browser.close()
# browser.quit()