
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


class ChromeWebDriver(object):
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument('--headless=new')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument("--remote-debugging-port=9222")

    def start_driver(self, driver_path):
        self.driver_path = driver_path
        self.driver = webdriver.Chrome(
            self.driver_path, chrome_options=self.chrome_options)
        return self.driver


class PageElement(ChromeWebDriver):
    '''
    This class has the objective to check if the element was loaded in the page
    and after that try the action triggered.
    '''

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=timeout)

    def element_loaded(self, by):
        not_loaded = True
        while not_loaded:
            try:
                element = self.wait.until(EC.visibility_of_element_located(by))
                print('Element loaded')
                not_loaded = False
            except (StaleElementReferenceException, TimeoutException) as e:
                print('-' * 50)
                print("ERROR:", e.__class__, "Trying again")
                print(f'Not Founded: {by}')
                print('-' * 50)
        return element

    def file_loaded(self, by):
        not_loaded = True
        while not_loaded:
            try:
                element = self.wait.until(
                    EC.invisibility_of_element_located(by))
                print('Arquivo carregado')
                not_loaded = False
            except (StaleElementReferenceException, TimeoutException) as e:
                print('-' * 50)
                print("Esperando pelo carregamento do arquivo...")
                print('-' * 50)
        return element

    def every_downloads_chrome(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        if not self.driver.current_url.startswith("chrome://downloads"):
            self.driver.get("chrome://downloads/")
        downloading = True
        print("Esperando pelo início do download...")
        while downloading:
            try:
                result = self.driver.execute_script("""
                    var items = document.querySelector('downloads-manager')
                        .shadowRoot.getElementById('downloadsList').items;
                    if (items.every(e => e.state === "COMPLETE"))
                        return items.map(e => e.filePath || e.file_path || e.fileUrl || e.file_url);
                    """)
                if result is None:
                    sleep(5)
                    print("Esperando pelo fim do download...")
                    continue
                elif len(result) != 0:
                    print("Download concluído!")
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    downloading = False
            except Exception as e:
                raise e.__class__
        return result
