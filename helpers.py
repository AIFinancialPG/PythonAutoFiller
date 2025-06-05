import os
import time
import datetime
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class SeleniumHelper:
    def __init__(self, browser: webdriver.Chrome):
        self.browser = browser

    def browser_get(self, url: str):
        self.browser.get(url)

    def refresh(self):
        self.browser.execute_script("location.reload();")

    def wait_for_next_btn(self):
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
        time.sleep(3)

    def wait_for_url_change(self):
        WebDriverWait(self.browser, 20).until(EC.url_changes(self.browser.current_url))
    
    def wait_for_element_to_be_interactable_by_name(self, name: str):
        element = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.NAME, name)))
        self.click_btn(element)

    def wait_for_element_to_be_clickable(self, xpath: str) -> WebElement:
        return WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def wait_for_element_by_xpath(self, xpath: str) -> WebElement:
        return WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    def wait_for_all_elements_by_xpath(self, xpath: str) -> list[WebElement]:
        return WebDriverWait(self.browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    def scroll_down_div_by_pg_down(self, xpath: str):
        tbScrollDiv = self.wait_for_element_by_xpath(xpath)
        webdriver.ActionChains(self.browser).move_to_element(tbScrollDiv).click().send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(0.5)

    def scroll_up_div_by_pg_up(self, xpath: str):
        tbScrollDiv = self.wait_for_element_by_xpath(xpath)
        webdriver.ActionChains(self.browser).move_to_element(tbScrollDiv).click().send_keys(Keys.PAGE_UP).perform()
        time.sleep(0.5)
    
    def scroll_down_div_by_amt(self, xpath:str, amt: int):
        tbScrollDiv = self.wait_for_element_by_xpath(xpath)
        self.browser.execute_script(f"arguments[0].scrollTop += {amt};", tbScrollDiv)
        time.sleep(0.5)
    
    def scroll_up_div_by_amt(self, xpath:str, amt: int):
        tbScrollDiv = self.wait_for_element_by_xpath(xpath)
        self.browser.execute_script(f"arguments[0].scrollTop -= {amt};", tbScrollDiv)
        time.sleep(0.5)

    def scroll_down_page(self, amt: int):
        self.browser.execute_script(f"scroll(0, { amt });")
        time.sleep(0.5)

    def scroll_up_page(self, amt: int):
        self.browser.execute_script(f"scroll(0, -{ amt });")
        time.sleep(0.5)

    def scroll_to_element(self, element: WebElement):
        webdriver.ActionChains(self.browser).scroll_to_element(element).perform()
        time.sleep(0.5)

    def scroll_to_next_btn(self):
        nextBtn = self.wait_for_element_by_xpath('//button[text()="Next"]')
        self.scroll_to_element(nextBtn)
        time.sleep(1)

    def set_zoom(self, amt: int):
        self.browser.execute_script(f"document.body.style.zoom='{ amt }%';")
        time.sleep(0.5)

    def click_btn(self, element: WebElement):
        self.browser.execute_script("arguments[0].click()", element)

    def click_pres_btn(self, element: WebElement):
        webdriver.ActionChains(self.browser).move_to_element(element).click().perform()

    def switch_to_co_applicant_section(self):
        coAppBtn = self.wait_for_element_by_xpath('//button[@role="radio" and text()="Co-Applicant"]')
        self.click_btn(coAppBtn)
        time.sleep(0.5)

    def enter_input(self, name: str, data: str):
        element = WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.NAME, name)))
        element.send_keys(data)

    def send_keys(self, element: WebElement, data: str):
        element.send_keys(data)

    def quit_browser(self):
        self.browser.quit()

    def no_proceed_app(self):
        print("Application won't proceed ahead because an application stoping action got selected")
        time.sleep(3)
        self.quit_browser()

    def upload_file_to_input(self, idx: int):
        upload_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "test.jpg"))
        file_inputs = self.wait_for_all_elements_by_xpath('//input[@type="file"]')
        file_inputs[idx].send_keys(upload_file)

    def enter_drop_down(self, label: str, drop_down_idx: int, option_idx: int):
        dropDowns =  self.wait_for_all_elements_by_xpath(f'//label[text()="{label}"]/..//div//button[@role="combobox"]')
        self.click_btn(dropDowns[drop_down_idx])
        options = self.wait_for_all_elements_by_xpath('//div[@role="option"]')
        self.click_btn(options[option_idx])

    def select_today_date_picker(self, xpath: str, date_picker_idx: int):
        datePickers = self.wait_for_all_elements_by_xpath(xpath)
        self.click_btn(datePickers[date_picker_idx])
        time.sleep(0.5)
        todayOption = self.wait_for_element_by_xpath('//button[contains(@aria-label, "Today")]')
        self.click_btn(todayOption)
        webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()

    def select_first_date_picker(self, xpath: str, date_picker_idx: int):
        datePickers = self.wait_for_all_elements_by_xpath(xpath)
        self.click_btn(datePickers[date_picker_idx])
        time.sleep(0.5)
        firstOption = self.wait_for_element_by_xpath('//button[text()="1"]')
        self.click_btn(firstOption)
        webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()

    def select_first_at_least_12yrs_ago_date_selector(self, xpath: str, date_picker_idx: int):
        datePickers = self.wait_for_all_elements_by_xpath(xpath)
        self.click_btn(datePickers[date_picker_idx])
        time.sleep(0.5)
        now = datetime.datetime.now()
        monthBtn = self.wait_for_element_by_xpath(f'//button[text()="{ now.strftime("%B %Y") }"]')
        self.click_btn(monthBtn)
        leftChevBtn = self.wait_for_element_by_xpath('//button[@aria-label="Go to the previous 12 years"]')
        self.click_btn(leftChevBtn)
        firstYearBtn = self.wait_for_element_by_xpath(f'//div[@aria-label="{ now.strftime("%B %Y") }"]//button')
        self.click_btn(firstYearBtn)
        firstOption = self.wait_for_element_by_xpath('//button[text()="1"]')
        self.click_btn(firstOption)
        webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()

    def select_first_at_least_24yrs_ago_date_selector(self, xpath: str, date_picker_idx: int):
        datePickers = self.wait_for_all_elements_by_xpath(xpath)
        self.click_btn(datePickers[date_picker_idx])
        time.sleep(0.5)
        now = datetime.datetime.now()
        monthBtn = self.wait_for_element_by_xpath(f'//button[text()="{ now.strftime("%B %Y") }"]')
        self.click_btn(monthBtn)
        leftChevBtn = self.wait_for_element_by_xpath('//button[@aria-label="Go to the previous 12 years"]')
        self.click_btn(leftChevBtn)
        time.sleep(0.5)
        leftChevBtn = self.wait_for_element_by_xpath('//button[@aria-label="Go to the previous 12 years"]')
        self.click_btn(leftChevBtn)
        firstYearBtn = self.wait_for_element_by_xpath(f'//div[@aria-label="{ now.strftime("%B %Y") }"]//button')
        self.click_btn(firstYearBtn)
        firstOption = self.wait_for_element_by_xpath('//button[text()="1"]')
        self.click_btn(firstOption)
        webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
    
    def send_backspace_to_input(self, name: str):
        element = WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.NAME, name)))
        webdriver.ActionChains(self.browser).move_to_element(element).click().send_keys(Keys.BACKSPACE).perform()
    
    def click_next_btn(self):
        nextBtn = self.wait_for_element_by_xpath('//button[text()="Next"]')
        self.scroll_to_element(nextBtn)
        self.click_btn(nextBtn)