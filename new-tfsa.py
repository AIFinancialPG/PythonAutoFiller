from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
from utils import *
from helpers import *

browser = webdriver.Chrome(options=Options().add_argument("--disable-autofill"))
browser.maximize_window()
browser.implicitly_wait(10)
browser.execute_script("document.body.style.zoom='100%';")
helper = SeleniumHelper(browser)

def send_verification_code():
    browser.get('http://localhost:5173')
    assert 'AiFundTech' in browser.title

    login_btn = helper.wait_for_element_by_xpath('//button[text()="Log in"]')
    helper.click_btn(login_btn)

    user, password = load_credentials("internal-credentials.yaml")
    helper.enter_input('Username', user)
    helper.enter_input('Password', password)

    signin_btn = helper.wait_for_element_by_xpath('//button[@id="next"]')
    helper.click_btn(signin_btn)

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
    helper.wait_for_url_change()
    newApplicationBtn = helper.wait_for_element_by_xpath("//a[@href='/pre-application']//button[text()='APPLY NEW ACCOUNT']")
    helper.click_btn(newApplicationBtn)
    invstTypeBtn = helper.wait_for_element_by_xpath("//div[contains(text(), 'New Investment Account')]/../..//div//button[text()='Apply']")
    helper.click_btn(invstTypeBtn)
    personalFundDiv = helper.wait_for_element_by_xpath("//div[contains(text(), 'Personal Fund')]/../..")
    helper.scroll_to_element(personalFundDiv)
    fundTypeBtn = helper.wait_for_element_by_xpath("//div[contains(text(), 'Personal Fund')]/../..//div//button[text()='Apply']")
    helper.click_btn(fundTypeBtn)
    accTypeBtn = helper.wait_for_element_by_xpath("//div[contains(text(), 'TFSA')]/../../..//div//button[text()='Apply']")
    helper.click_btn(accTypeBtn)
    nextBtn = helper.wait_for_element_by_xpath("//h1[normalize-space()='Requirements: TFSA']/following::button[normalize-space()='Next'][1]")
    helper.scroll_to_element(nextBtn)
    helper.click_btn(nextBtn)
    agreeAndContBtn = helper.wait_for_element_by_xpath("//div[@role='dialog']//div//div//button[text()='AGREE AND CONTINUE']")
    helper.click_btn(agreeAndContBtn)
    time.sleep(1)
    skipBtn = helper.wait_for_element_by_xpath('//button[text()="Skip"]')
    helper.scroll_to_element(skipBtn)
    helper.click_btn(skipBtn)
    helper.click_next_btn()

def enter_personal_info():
    helper.wait_for_next_btn()
    helper.enter_input("personalInfo.Applicant.firstName", "test")
    helper.enter_input("personalInfo.Applicant.lastName", "test")
    helper.enter_input("personalInfo.Applicant.SIN", "485888473")
    helper.enter_drop_down("Gender", 0, 0)
    helper.select_first_date_picker('//label[text()="Date of Birth"]/..//div//div//button', 0)
    helper.click_next_btn()

def enter_contact_info():
    helper.wait_for_next_btn()
    helper.enter_input("contactInfo.Applicant.contact.email", "test@gmail.com")
    phoneNumField = helper.wait_for_element_by_xpath('//label[text()="Phone Number"]/..//div//div//input[@type="tel"]')
    phoneNumField.send_keys("1111111111")
    helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
    helper.scroll_to_next_btn()
    helper.enter_input("contactInfo.Applicant.currAddr.streetNumberC", "22352")
    helper.enter_input("contactInfo.Applicant.currAddr.cityC", "Toronto")
    helper.enter_input("contactInfo.Applicant.currAddr.postCodeC", "M5B 1N8")
    helper.enter_input("contactInfo.Applicant.currAddr.unitC", "75")
    helper.enter_input("contactInfo.Applicant.currAddr.streetNameC", "Paul Orchard")
    helper.enter_drop_down("Province", 0, 0)
    helper.click_next_btn()

def enter_id_info():
    helper.wait_for_next_btn()

    idDocumentDiv = helper.wait_for_element_by_xpath('//div[text()="ID Document"]')
    helper.click_btn(idDocumentDiv)
    helper.enter_input("identification.Applicant.id1.fullName", "test test")
    helper.enter_input("identification.Applicant.id1.idNumber", "11111")
    helper.enter_drop_down("ID Type", 0, 2)
    helper.enter_drop_down("Issuing Authority", 0, 2)
    helper.upload_file_to_input(0)
    helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
    helper.enter_drop_down("Issuing Country", 0, 1)
    helper.enter_input("identification.Applicant.id1.issueProvince", "Ontario")
    helper.select_today_date_picker('//label[text()="Issue Date"]/..//div//button', 0)
    saveBtns = helper.wait_for_all_elements_by_xpath('//button[text()="Save"]')
    helper.click_btn(saveBtns[0])
    
    idVerifyDocumentDiv = helper.wait_for_element_by_xpath('//div[text()="ID Verification Document"]')
    helper.click_btn(idVerifyDocumentDiv)
    helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
    helper.enter_drop_down("Verification Document Type", 0, 0)
    helper.enter_input("identification.Applicant.verification.issueAuthority", "Govt of Canada")
    helper.enter_input("identification.Applicant.verification.accountReference", "9999")
    helper.select_today_date_picker('//label[text()="ID Verification Document Date of Information"]/..//div//button', 0)
    helper.upload_file_to_input(0)
    saveBtns = helper.wait_for_all_elements_by_xpath('//button[text()="Save"]')
    helper.click_btn(saveBtns[0])
    
    helper.click_next_btn()

def enter_employment_info():
    helper.wait_for_next_btn()
    helper.enter_drop_down("Employment Status", 0, 0)
    helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
    helper.enter_input("employmentInfo.Applicant.commonInfo.responsibilities", "Website Development")
    helper.enter_input("employmentInfo.Applicant.commonInfo.jobTitle", "Software Developer")
    helper.enter_input("employmentInfo.Applicant.commonInfo.empName", "Some Company")
    helper.enter_input("employmentInfo.Applicant.commonInfo.empBusiness", "Ed-tech")
    helper.click_next_btn()

def enter_disclosure_info():
    helper.wait_for_next_btn()
    helper.click_next_btn()

def enter_source_contri_info():
    helper.wait_for_next_btn()
    helper.send_backspace_to_input("sourceOfContribution.amountApplied")
    helper.enter_input("sourceOfContribution.amountApplied", "1000000")
    noTypeBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="no"]')
    helper.click_btn(noTypeBtn)
    helper.click_next_btn()

def enter_contri_option_info():
    helper.wait_for_next_btn()
    helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
    helper.enter_drop_down("Bank / Institution Name", 0, 0)
    helper.enter_input("contributionOption.commonFields.transitNo", "04000")
    helper.enter_input("contributionOption.commonFields.accountNo", "99999999")
    helper.upload_file_to_input(0)
    helper.click_next_btn()

def enter_success_owner_info():
    time.sleep(3)
    confirmBtn = helper.wait_for_element_by_xpath('//button[text()="Confirm"]')
    helper.click_btn(confirmBtn)
    helper.click_next_btn()

def enter_primary_beneficiary_info():
    helper.wait_for_next_btn()
    helper.enter_input("pendingBeneficiary.commonInfo.firstName", "newTest")
    helper.enter_input("pendingBeneficiary.commonInfo.lastName", "newTest")
    helper.enter_drop_down("Relation to Annuitant", 0, 0)
    helper.enter_drop_down("Gender", 0, 0)
    helper.enter_drop_down("Beneficiary Type", 0, 0)
    helper.send_backspace_to_input("pendingBeneficiary.commonInfo.sharePercent")
    helper.enter_input("pendingBeneficiary.commonInfo.sharePercent", "100")
    helper.select_today_date_picker('//label[text()="Date of Birth"]/..//div//button', 0)
    time.sleep(2)
    helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-auto")]', 200)
    helper.enter_drop_down("Trustee Relation to Beneficiary", 0, 0)
    helper.enter_input("pendingBeneficiary.trusteeInfo.trusteeFirstname", "newTest1")
    helper.enter_input("pendingBeneficiary.trusteeInfo.trusteeLastname", "newTest1")
    helper.click_next_btn()
    time.sleep(2)
    helper.click_next_btn()

def enter_secondary_beneficiary_info():
    helper.wait_for_next_btn()
    helper.click_next_btn()

def enter_investor_profile_info():
    helper.wait_for_next_btn()
    helper.click_next_btn()

def enter_feedback_info():
    helper.wait_for_next_btn()
    helper.enter_drop_down("How did you hear about us?", 0, 0)
    helper.enter_input("specialInstructions.heardDetail", "Searching around on google")
    helper.click_next_btn()
    time.sleep(10)

def create_application():
    enter_personal_info()
    enter_contact_info()
    enter_id_info()
    enter_employment_info()
    enter_disclosure_info()
    enter_source_contri_info()
    enter_contri_option_info()
    enter_success_owner_info()
    enter_primary_beneficiary_info()
    enter_secondary_beneficiary_info()
    enter_investor_profile_info()
    enter_feedback_info()

def main():
    send_verification_code()
    pre_application_steps("")
    create_application()

if __name__ == "__main__":
    main()