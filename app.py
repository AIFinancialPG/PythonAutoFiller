from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import yaml
import logging
import email
import aioimaplib
import asyncio
import time
import os

browser = webdriver.Chrome(options=Options().add_argument("--disable-autofill"))

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

    user, password = load_credentials("internal-credentials.yaml")

    userNameField.send_keys(user)
    passField.send_keys(password)
    browser.execute_script("arguments[0].click();", siginBtn)

    # WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "sendCode")))
    # sendCodeBtn = browser.find_element(By.ID, "sendCode")
    # browser.execute_script("arguments[0].click();", sendCodeBtn)
    
def pre_application_steps(message):
    # print(message)
    # WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))
    # WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))
    # verifCodeInput = browser.find_element(By.ID, "verificationCode")
    # verifCodeBtn = browser.find_element(By.ID, "verifyCode")
    # verifCodeInput.send_keys(message)
    # browser.execute_script("arguments[0].click();", verifCodeBtn)

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
    nextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[normalize-space()='Requirements: Quick Loan']/following::button[normalize-space()='Next'][1]")))
    webdriver.ActionChains(browser).scroll_to_element(nextBtn).perform()
    print(nextBtn.text)
    browser.execute_script("arguments[0].click()", nextBtn)

    agreeAndContBtn = browser.find_element(By.XPATH, "//div[@role='dialog']//div//div//button[text()='AGREE AND CONTINUE']")
    print(agreeAndContBtn.text)
    browser.execute_script("arguments[0].click()", agreeAndContBtn)

    time.sleep(2)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    nextBtn2 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(nextBtn2).perform()
    print(nextBtn2.text)
    browser.execute_script("arguments[0].click()", nextBtn2)
    
    create_application()

def enter_personal_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))

    time.sleep(3)

    firstNameField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, "personalInfo.Applicant.firstName")))
    firstNameField.send_keys("test")

    lastNameField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, "personalInfo.Applicant.lastName")))
    lastNameField.send_keys("test")

    genderDropDown = browser.find_element(By.XPATH, '//label[text()="Gender"]/..//div//button[@role="combobox"]')
    browser.execute_script("arguments[0].click()", genderDropDown)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="option"]')))
    genderOptions = browser.find_elements(By.XPATH, '//div[@role="option"]')
    browser.execute_script("arguments[0].click()", genderOptions[0])

    maritalStatusDropDown = browser.find_element(By.XPATH, '//label[text()="Marital Status"]/..//div//button[@role="combobox"]')
    browser.execute_script("arguments[0].click()", maritalStatusDropDown)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="option"]')))
    maritalStatusOptions = browser.find_elements(By.XPATH, '//div[@role="option"]')
    browser.execute_script("arguments[0].click()", maritalStatusOptions[0])

    tbSrollDiv = browser.find_element(By.XPATH, '//div[contains(@class, "overflow-y-auto")]')
    webdriver.ActionChains(browser).move_to_element(tbSrollDiv).click().send_keys(Keys.PAGE_DOWN).perform()
    personalInfoNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(personalInfoNextBtn).perform()

    dobDatePicker = browser.find_element(By.XPATH, '//label[text()="Date of Birth"]/..//div//div//button')
    browser.execute_script("arguments[0].click()", dobDatePicker)
    
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="1"]')))
    firstDOBOption = browser.find_element(By.XPATH, '//button[text()="1"]')
    browser.execute_script("arguments[0].click()", firstDOBOption)
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    countryOfBirthDropDown = browser.find_element(By.XPATH, '//label[text()="Country of Birth"]/..//div//button[@role="combobox"]')
    browser.execute_script("arguments[0].click()", countryOfBirthDropDown)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="option"]')))
    countryOfBirthOptions = browser.find_elements(By.XPATH, '//div[@role="option"]')
    browser.execute_script("arguments[0].click()", countryOfBirthOptions[1])

    provinceOfBirthField = browser.find_element(By.NAME, "personalInfo.Applicant.provinceOfBirth")
    provinceOfBirthField.send_keys("Ontario")

    sinField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, "personalInfo.Applicant.SIN")))
    sinField.send_keys("485888473")

    citizenshipDropDown = browser.find_element(By.XPATH, '//label[text()="Citizenship"]/..//div//button[@role="combobox"]')
    browser.execute_script("arguments[0].click()", citizenshipDropDown)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="option"]')))
    citizenshipOptions = browser.find_elements(By.XPATH, '//div[@role="option"]')
    browser.execute_script("arguments[0].click()", citizenshipOptions[1])
    
    personalInfoNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    print(personalInfoNextBtn.text)
    browser.execute_script("arguments[0].click()", personalInfoNextBtn)

def enter_contact_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))

    time.sleep(3)

    emailField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, "contactInfo.Applicant.contact.email")))
    emailField.send_keys("test@gmail.com")

    phoneNumFiled = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//label[text()="Phone Number"]/..//div//div//input[@type="tel"]')))
    phoneNumFiled.send_keys("1111111111")

    homePhoneField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//label[text()="Home Phone"]/..//div//div//input[@type="tel"]')))
    homePhoneField.send_keys("2222222222")

    workPhoneField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//label[text()="Work Phone"]/..//div//div//input[@type="tel"]')))
    workPhoneField.send_keys("3333333333")

    tbSrollDiv = browser.find_element(By.XPATH, '//div[contains(@class, "overflow-y-auto")]')
    webdriver.ActionChains(browser).move_to_element(tbSrollDiv).click().send_keys(Keys.PAGE_DOWN).perform()
    contactInfoNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(contactInfoNextBtn).perform()

    streetNumberField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'contactInfo.Applicant.currAddr.streetNumberC')))
    streetNumberField.send_keys("22352")

    cityField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'contactInfo.Applicant.currAddr.cityC')))
    cityField.send_keys("Toronto")

    postalCodeField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'contactInfo.Applicant.currAddr.postCodeC')))
    postalCodeField.send_keys("M5B 1N8")

    streetNameField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'contactInfo.Applicant.currAddr.streetNameC')))
    streetNameField.send_keys("Paul Orchard")

    provinceDropDown = browser.find_element(By.XPATH, '//label[text()="Province"]/..//div//button[@role="combobox"]')
    browser.execute_script("arguments[0].click()", provinceDropDown)
    provinceOption = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", provinceOption)

    livingSinceDatePicker = browser.find_element(By.XPATH, '//label[text()="Living Here Since"]/..//div//div//button')
    browser.execute_script("arguments[0].click()", livingSinceDatePicker)
    firstLivingSinceOption = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="1"]')))
    browser.execute_script("arguments[0].click()", firstLivingSinceOption)
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    tbSrollDiv = browser.find_element(By.XPATH, '//div[contains(@class, "overflow-y-auto")]')
    webdriver.ActionChains(browser).move_to_element(tbSrollDiv).click().send_keys(Keys.PAGE_DOWN).perform()

    streetNumberField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'contactInfo.Applicant.prevAddr.streetNumberP')))
    streetNumberField.send_keys("15063")

    cityField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'contactInfo.Applicant.prevAddr.cityP')))
    cityField.send_keys("Toronto")

    postalCodeField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'contactInfo.Applicant.prevAddr.postCodeP')))
    postalCodeField.send_keys("M4N 1T7")

    streetNameField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'contactInfo.Applicant.prevAddr.streetNameP')))
    streetNameField.send_keys("Schroeder Villages")

    provinceDropDowns = WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//label[text()="Province"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", provinceDropDowns[1])
    provinceOption = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", provinceOption)

    livingSinceDatePickers = WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//label[text()="Living Here Since"]/..//div//div//button')))
    browser.execute_script("arguments[0].click()", livingSinceDatePickers[1])
    firstLivingSinceOption = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="1"]')))
    browser.execute_script("arguments[0].click()", firstLivingSinceOption)
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    contactInfoNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    print(contactInfoNextBtn.text)
    browser.execute_script("arguments[0].click()", contactInfoNextBtn)

def enter_id_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))

    time.sleep(3)

    mainApplicantID1Div = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="Main Applicant ID 1"]')))
    browser.execute_script("arguments[0].click()", mainApplicantID1Div)
    
    fullName1Field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'identification.Applicant.id1.fullName')))
    fullName1Field.send_keys("test test")

    idNum1Field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'identification.Applicant.id1.idNumber')))
    idNum1Field.send_keys("1111")

    idType1DropDown = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//label[text()="ID Type"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", idType1DropDown)
    idType1Options = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", idType1Options[2])

    issueAuth1DropDown = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//label[text()="Issuing Authority"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", issueAuth1DropDown)
    issueAuth1Options = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", issueAuth1Options[2])

    upload_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "test.jpg"))

    file_inputs = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@type="file"]')))
    file_inputs[0].send_keys(upload_file)

    tbScrollDiv = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "overflow-y-auto")]')))
    # webdriver.ActionChains(browser).move_to_element(tbSrollDiv).click().send_keys(Keys.PAGE_DOWN).perform()
    browser.execute_script("arguments[0].scrollTop += 200;", tbScrollDiv)

    time.sleep(1)

    issueCountry1DropDown = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//label[text()="Issuing Country"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", issueCountry1DropDown)
    issueCountry1Options = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", issueCountry1Options[1])

    issueProvince1Field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'identification.Applicant.id1.issueProvince')))
    issueProvince1Field.send_keys("Ontario")

    issueDatePickers = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//label[text()="Issue Date"]/..//div//button')))
    browser.execute_script("arguments[0].click()", issueDatePickers[0])
    todayIssueOption = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@aria-label, "Today")]')))
    browser.execute_script("arguments[0].click()", todayIssueOption)
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    # expireDatePickers = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//label[text()="Expiry Date"]/..//div//button')))
    # browser.execute_script("arguments[0].click()", expireDatePickers[0])
    # todayExpireOption = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@aria-label, "Today")]')))
    # browser.execute_script("arguments[0].click()", todayExpireOption)
    # webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    saveBtns = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//button[text()="Save"]')))
    browser.execute_script("arguments[0].click()", saveBtns[0])

    mainApplicantID2Div = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Main Applicant ID 2"]')))
    browser.execute_script("arguments[0].click()", mainApplicantID2Div)

    tbScrollDiv = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "overflow-y-auto")]')))
    browser.execute_script("arguments[0].scrollTop -= 200;", tbScrollDiv)

    time.sleep(1)

    fullName2Field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'identification.Applicant.id2.fullName')))
    fullName2Field.send_keys("test test")

    idNum2Field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'identification.Applicant.id2.idNumber')))
    idNum2Field.send_keys("2222")

    idType2DropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//label[text()="ID Type"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", idType2DropDown)
    idType2Options = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", idType2Options[2])

    issueAuth2DropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//label[text()="Issuing Authority"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", issueAuth2DropDown)
    issueAuth1Options = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", issueAuth1Options[2])

    file_inputs = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@type="file"]')))
    file_inputs[0].send_keys(upload_file)

    tbScrollDiv = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "overflow-y-auto")]')))
    browser.execute_script("arguments[0].scrollTop += 250;", tbScrollDiv)

    time.sleep(1)

    issueCountryDropDowns = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//label[text()="Issuing Country"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", issueCountryDropDowns[0])
    issueCountry2Options = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", issueCountry2Options[1])

    issueProvince2Field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'identification.Applicant.id2.issueProvince')))
    issueProvince2Field.send_keys("Ontario")

    issueDatePickers = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//label[text()="Issue Date"]/..//div//button')))
    browser.execute_script("arguments[0].click()", issueDatePickers[0])
    time.sleep(1)
    todayIssueOption = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(@aria-label, "Today")]')))
    browser.execute_script("arguments[0].click()", todayIssueOption)
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    expireDatePickers = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//label[text()="Expiry Date"]/..//div//button')))
    browser.execute_script("arguments[0].click()", expireDatePickers[0])
    time.sleep(1)
    todayExpireOption = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[contains(@aria-label, "Today")]')))
    browser.execute_script("arguments[0].click()", todayExpireOption)
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    saveBtns = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//button[text()="Save"]')))
    browser.execute_script("arguments[0].click()", saveBtns[0])

    mainApplicantVerification = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Main Applicant Verification"]')))
    browser.execute_script("arguments[0].click()", mainApplicantVerification)

    yesRadioBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@role="radio" and @value="Yes"]')))
    browser.execute_script("arguments[0].click()", yesRadioBtn)

    saveBtns = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//button[text()="Save"]')))
    browser.execute_script("arguments[0].click()", saveBtns[0])

    idInfoNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(idInfoNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", idInfoNextBtn)

def enter_tax_status():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)

    taxStatusInfoNextBtn = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(taxStatusInfoNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", taxStatusInfoNextBtn)

def enter_employment_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)

    employmentStatusDropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", employmentStatusDropDown)
    time.sleep(1)
    employmentStatusOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", employmentStatusOptions[0])

    tbSrollDiv = browser.find_element(By.XPATH, '//div[contains(@class, "overflow-y-auto")]')
    webdriver.ActionChains(browser).move_to_element(tbSrollDiv).click().send_keys(Keys.PAGE_DOWN).perform()    

    jobResField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'employmentInfo.Applicant.commonInfo.responsibilities')))
    jobResField.send_keys("Website Development")

    jobTitleField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'employmentInfo.Applicant.commonInfo.jobTitle')))
    jobTitleField.send_keys("Software Developer")

    employmentNameField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'employmentInfo.Applicant.commonInfo.empName')))
    employmentNameField.send_keys("Some Company")

    natureOfEmpField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'employmentInfo.Applicant.commonInfo.empBusiness')))
    natureOfEmpField.send_keys("Ed-tech")

    emplyInfoNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(emplyInfoNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", emplyInfoNextBtn)


def enter_disclosure_info():
    time.sleep(3)
    disclosureFormBtn = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[text()="Disclosure Form"]')))
    browser.execute_script('arguments[0].click()', disclosureFormBtn)

    disclosureInfoNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(disclosureInfoNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", disclosureInfoNextBtn)


def enter_source_contri_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)

    sourceContriInfoNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(sourceContriInfoNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", sourceContriInfoNextBtn)

def enter_contri_option_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)

    tbSrollDiv = browser.find_element(By.XPATH, '//div[contains(@class, "overflow-y-auto")]')
    webdriver.ActionChains(browser).move_to_element(tbSrollDiv).click().send_keys(Keys.PAGE_DOWN).perform()

    bankNameDropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@role="combobox"]')))
    browser.execute_script('arguments[0].click()', bankNameDropDown)
    bankNameOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script('arguments[0].click()', bankNameOptions[0])

    transitNumField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'contributionOption.commonFields.transitNo')))
    transitNumField.send_keys('04000')

    accountNumField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'contributionOption.commonFields.accountNo')))
    accountNumField.send_keys('99999999')

    upload_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "test.jpg"))

    file_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
    file_input.send_keys(upload_file)

    contriOptionInfoNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(contriOptionInfoNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", contriOptionInfoNextBtn)

def enter_policy_guarantee_lvl_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)

    guaranteeLvlOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@role="radio"]')))
    browser.execute_script("arguments[0].click()", guaranteeLvlOptions[0])

    policyGuaranteeLvlInfoNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(policyGuaranteeLvlInfoNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", policyGuaranteeLvlInfoNextBtn)

def enter_resi_status_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)

    otherResiStatusOption = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "I live with others.")]')))
    browser.execute_script("arguments[0].click()", otherResiStatusOption)

    resiStatusInfoNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(resiStatusInfoNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", resiStatusInfoNextBtn)

def ans_canadian_real_estate_ques():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)
 
    noQuesOption = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "No")]')))
    browser.execute_script("arguments[0].click()", noQuesOption)

    quesNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(quesNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", quesNextBtn)

def enter_fin_analysis_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)

    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)

    addLiabilityBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Liabilities"]/following-sibling::div//button')))
    browser.execute_script("arguments[0].click()", addLiabilityBtn)

    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'commonFields.liabilityBalance')))

    ownerDropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//label[text()="Owner"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", ownerDropDown)
    ownerOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", ownerOptions[0])

    liabilityTypeDropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//label[text()="Liability Type"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", liabilityTypeDropDown)
    liabilityTypeOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", liabilityTypeOptions[2])

    liablilityBalanceField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'commonFields.liabilityBalance')))
    liablilityBalanceField.send_keys("100")

    monthlyPaymentField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'commonFields.liabilityMonthlyPayment')))
    monthlyPaymentField.send_keys("5")

    addLiabilityDialogBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]//div//button[contains(text(), "Add Liability")]')))
    browser.execute_script('arguments[0].click()', addLiabilityDialogBtn)

    # WebDriverWait(browser, 10).until_not(EC.visibility_of_element_located((By.NAME, 'commonFields.liabilityBalance')))

    liabilityNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(liabilityNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", liabilityNextBtn)

    addAssetBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Assets"]/following-sibling::div//button')))
    browser.execute_script("arguments[0].click()", addAssetBtn)

    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'commonFields.assetMarketValue')))

    ownerDropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//label[text()="Owner"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", ownerDropDown)
    ownerOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", ownerOptions[0])

    assetMarketValueField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'commonFields.assetMarketValue')))
    assetMarketValueField.send_keys("1000000")

    assetTypeDropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//label[text()="Asset Type"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", assetTypeDropDown)
    assetTypeOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", assetTypeOptions[0])

    addAssestDialogBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]//div//button[contains(text(), "Add Asset")]')))
    browser.execute_script('arguments[0].click()', addAssestDialogBtn)

    # WebDriverWait(browser, 10).until_not(EC.visibility_of_element_located((By.NAME, 'commonFields.assetMarketValue')))

    assetNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(assetNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", assetNextBtn)

    addIncomeBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(),"TFSA, RRSP")]/following-sibling::div//button')))
    browser.execute_script("arguments[0].click()", addIncomeBtn)

    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'commonFields.annualIncome')))

    ownerDropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//label[text()="Owner"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", ownerDropDown)
    ownerOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", ownerOptions[0])

    incomeTypeDropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//label[text()="Income Type"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", incomeTypeDropDown)
    incomeTypeOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", incomeTypeOptions[7])

    annualIncomeField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'commonFields.annualIncome')))
    annualIncomeField.send_keys("100000")

    otherTypeIncomeField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'commonFields.incomeTypeOther')))
    otherTypeIncomeField.send_keys("Social Media")

    addIncomeDialogBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]//div//button[contains(text(), "Add Income")]')))
    browser.execute_script('arguments[0].click()', addIncomeDialogBtn)

    # WebDriverWait(browser, 10).until_not(EC.visibility_of_element_located((By.NAME, 'commonFields.annualIncome')))

    incomeNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(incomeNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", incomeNextBtn)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//p[text()="Great Job!"]')))

    finAnalysisNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(finAnalysisNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", finAnalysisNextBtn)

def enter_primary_beneficiary_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)

    beneficiaryFirstNameField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'pendingBeneficiary.commonInfo.firstName')))
    beneficiaryFirstNameField.send_keys("newTest")


    beneficiaryLastNameField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'pendingBeneficiary.commonInfo.lastName')))
    beneficiaryLastNameField.send_keys("newTest")


    relToAnnuitDropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//label[text()="Relation to Annuitant"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", relToAnnuitDropDown)
    relToAnnuitOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", relToAnnuitOptions[0])


    genderDropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//label[text()="Gender"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", genderDropDown)
    genderOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", genderOptions[0])


    beneficiaryTypeDropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//label[text()="Beneficiary Type"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", beneficiaryTypeDropDown)
    beneficiaryTypeOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", beneficiaryTypeOptions[0])


    sharePercentField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'pendingBeneficiary.commonInfo.sharePercent')))
    webdriver.ActionChains(browser).move_to_element(sharePercentField).click().send_keys(Keys.BACKSPACE).perform()
    sharePercentField.send_keys("100")


    dOBDatePickers = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//label[text()="Date of Birth"]/..//div//button')))
    browser.execute_script("arguments[0].click()", dOBDatePickers[0])
    todayDOBOption = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@aria-label, "Today")]')))
    browser.execute_script("arguments[0].click()", todayDOBOption)
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    time.sleep(2)

    tbScrollDiv = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "overflow-auto")]')))
    browser.execute_script("arguments[0].scrollTop += 200;", tbScrollDiv)

    trusteeRelToBeneficiaryDropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//label[text()="Trustee Relation to Beneficiary"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", trusteeRelToBeneficiaryDropDown)
    trusteeRelToBeneficiaryOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", trusteeRelToBeneficiaryOptions[0])

    trusteeFirstNameField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'pendingBeneficiary.trusteeInfo.trusteeFirstname')))
    trusteeFirstNameField.send_keys("newTest1")

    trusteeLastNameField = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'pendingBeneficiary.trusteeInfo.trusteeLastname')))
    trusteeLastNameField.send_keys("newTest1")

    primaryBeneficiaryNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(primaryBeneficiaryNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", primaryBeneficiaryNextBtn)
    time.sleep(2)
    primaryBeneficiaryInfoNextBtn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(primaryBeneficiaryNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", primaryBeneficiaryInfoNextBtn)

def enter_secondary_beneficiary_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)

    secondaryBeneficiaryInfoNextBtn = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(secondaryBeneficiaryInfoNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", secondaryBeneficiaryInfoNextBtn)

def enter_investor_profile_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)

    investorProfileInfoNextBtn = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(investorProfileInfoNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", investorProfileInfoNextBtn)

def enter_credit_report_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)

    confirmRadioBtns = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@role="radio"]')))
    browser.execute_script("arguments[0].click()", confirmRadioBtns[0])

    upload_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "test.jpg"))

    file_inputs = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@type="file"]')))
    file_inputs[0].send_keys(upload_file)

    creditReportInfoNextBtn = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(creditReportInfoNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", creditReportInfoNextBtn)

def enter_feedback_info():
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')))
    time.sleep(3)

    hearAboutDropDown = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//label[text()="How did you hear about us?"]/..//div//button[@role="combobox"]')))
    browser.execute_script("arguments[0].click()", hearAboutDropDown)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="option"]')))
    hearAboutOptions = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="option"]')))
    browser.execute_script("arguments[0].click()", hearAboutOptions[0])

    moreDetailsTextArea = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'specialInstructions.heardDetail')))
    moreDetailsTextArea.send_keys("Searching around on google")

    creditReportInfoNextBtn = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[text()="Next"]')))
    webdriver.ActionChains(browser).scroll_to_element(creditReportInfoNextBtn).perform()
    time.sleep(1)
    browser.execute_script("arguments[0].click()", creditReportInfoNextBtn)

    time.sleep(10)


def create_application():
    enter_personal_info()
    enter_contact_info()
    enter_id_info()
    enter_tax_status()
    enter_employment_info()
    enter_disclosure_info()
    enter_source_contri_info()
    enter_contri_option_info()
    enter_policy_guarantee_lvl_info()
    enter_resi_status_info()
    ans_canadian_real_estate_ques()
    enter_fin_analysis_info()
    enter_primary_beneficiary_info()
    enter_secondary_beneficiary_info()
    enter_investor_profile_info()
    enter_credit_report_info()
    enter_feedback_info()
    browser.quit()

async def main():
    browser.maximize_window()
    browser.implicitly_wait(10)
    browser.execute_script("document.body.style.zoom='100%';")
    send_verification_code()
    message = "a" # await get_verification_mail()
    if len(message) != 0:
       pre_application_steps(message)
    
if __name__ == "__main__":
    asyncio.run(main())