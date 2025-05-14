from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import yaml
import logging
import email
import aioimaplib
import asyncio
import time

browser = webdriver.Chrome()

def load_credentials(filepath):
    try:
        with open(filepath, 'r') as file:
            credentials = yaml.safe_load(file)
            user = credentials['user']
            password = credentials['password']
            print(user, password)
            return user, password
    except Exception as e:
        logging.error("Failed to load credentials: {}".format(e))
        raise

async def get_verification_mail():
    imap_client = aioimaplib.IMAP4_SSL(host='imap.gmail.com', timeout=30)
    await imap_client.wait_hello_from_server()

    await imap_client.login(*load_credentials("credentials.yaml"))
    await imap_client.select('INBOX')
    
    idle = await imap_client.idle_start(timeout=60)
    msg = await imap_client.wait_server_push()
    imap_client.idle_done()
    await asyncio.wait_for(idle, 30)

    print(msg, str(int(msg[0].split()[0])))
    _, data = await imap_client.fetch(str(int(msg[0].split()[0])), '(RFC822)')
    email_message = email.message_from_bytes(data[1])

    print(email_message.get_payload().split("Use verification code ")[1][0:6])

    await imap_client.logout()

    if email_message:
        return email_message.get_payload().split("Use verification code ")[1][0:6]
    return ""


def send_verification_code():
    browser.get('http://localhost:5173')
    assert 'AiFundTech' in browser.title

    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))
    btns = browser.find_elements(By.TAG_NAME, "button")
    browser.execute_script("arguments[0].click();", btns[0])

    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))
    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))
    userNameField = browser.find_element(By.ID, "UserId")
    passField = browser.find_element(By.ID, "password")
    siginBtn = browser.find_element(By.ID, "next")

    userNameField.send_keys("Harkit")
    passField.send_keys("Harkit@1234")
    browser.execute_script("arguments[0].click();", siginBtn)

    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "sendCode")))
    sendCodeBtn = browser.find_element(By.ID, "sendCode")
    browser.execute_script("arguments[0].click();", sendCodeBtn)
    
def create_application(message):
    print(message)
    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))
    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))
    verifCodeInput = browser.find_element(By.ID, "verificationCode")
    verifCodeBtn = browser.find_element(By.ID, "verifyCode")
    verifCodeInput.send_keys(message)
    browser.execute_script("arguments[0].click();", verifCodeBtn)

    # print(browser.current_url)
    WebDriverWait(browser, 10).until(EC.url_changes(browser.current_url))
    
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/pre-application']//button[text()='APPLY NEW ACCOUNT']")))
    newApplicationBtn = browser.find_element(By.XPATH, "//a[@href='/pre-application']//button[text()='APPLY NEW ACCOUNT']")
    browser.execute_script("arguments[0].click()", newApplicationBtn)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'New Investment Account')]")))
    invstTypeBtn = browser.find_element(By.XPATH, "//div[contains(text(), 'New Investment Account')]/../../..//button[text()='Apply']")
    print(invstTypeBtn.text)
    browser.execute_script("arguments[0].click()", invstTypeBtn)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Loan')]")))
    fundTypeBtn = browser.find_element(By.XPATH, "//div[contains(text(), 'Loan')]/../../..//button[text()='Apply']")
    print(fundTypeBtn.text)
    browser.execute_script("arguments[0].click()", fundTypeBtn)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Quick Loan')]")))
    loanTypeBtn = browser.find_element(By.XPATH, "//div[contains(text(), 'Quick Loan')]/../../..//button[text()='Apply']")
    print(loanTypeBtn.text)
    browser.execute_script("arguments[0].click()", loanTypeBtn)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '$200K')]")))
    loanAmtBtn = browser.find_element(By.XPATH, "//div[contains(text(), '$200K')]/../../..//button[text()='Select']")
    print(loanAmtBtn.text)
    browser.execute_script("arguments[0].click()", loanAmtBtn)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[normalize-space()='Requirements: Quick Loan']")))
    nextBtn = browser.find_element(By.XPATH, "//h1[normalize-space()='Requirements: Quick Loan']/following::button[normalize-space()='Next'][1]")
    print(nextBtn.text)
    browser.execute_script("arguments[0].click()", nextBtn)
    browser.implicitly_wait(2)
    agreeAndContBtn = browser.find_element(By.XPATH, "//div[@role='dialog']//div//div//button[text()='AGREE AND CONTINUE']")
    print(agreeAndContBtn.text)
    browser.execute_script("arguments[0].click()", agreeAndContBtn)

    time.sleep(5)

async def main():
    send_verification_code()
    message = await get_verification_mail()
    if len(message) != 0:
       create_application(message)
    
if __name__ == "__main__":
    asyncio.run(main())