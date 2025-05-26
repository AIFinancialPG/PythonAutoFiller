from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import asyncio
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
    invstTypeBtn = helper.wait_for_element_by_xpath("//div[contains(text(), 'New Investment Account')]/../../..//button[text()='Apply']")
    helper.click_btn(invstTypeBtn)
    fundTypeBtn = helper.wait_for_element_by_xpath("//div[contains(text(), 'Personal Fund')]/../../..//button[text()='Apply']")
    helper.click_btn(fundTypeBtn)
    loanTypeBtn = helper.wait_for_element_by_xpath("//div[contains(text(), 'Quick Loan')]/../../..//button[text()='Apply']")
    helper.click_btn(loanTypeBtn)
    loanAmtBtn = helper.wait_for_element_by_xpath("//div[contains(text(), '$200K')]/../../..//button[text()='Select']")
    helper.click_btn(loanAmtBtn)
    nextBtn = helper.wait_for_element_by_xpath("//h1[normalize-space()='Requirements: Quick Loan']/following::button[normalize-space()='Next'][1]")
    helper.scroll_to_element(nextBtn)
    helper.click_btn(nextBtn)
    agreeAndContBtn = helper.wait_for_element_by_xpath("//div[@role='dialog']//div//div//button[text()='AGREE AND CONTINUE']")
    helper.click_btn(agreeAndContBtn)
    time.sleep(1)
    helper.click_next_btn()

def enter_personal_info():
    helper.wait_for_next_btn()
    helper.enter_input("personalInfo.Applicant.firstName", "test")
    helper.enter_input("personalInfo.Applicant.lastName", "test")
    helper.enter_drop_down("Gender", 0, 0)
    helper.enter_drop_down("Marital Status", 0, 0)
    helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
    helper.scroll_to_next_btn()
    helper.select_first_date_picker('//label[text()="Date of Birth"]/..//div//div//button', 0)
    helper.enter_drop_down("Country of Birth", 0, 1)
    helper.enter_input("personalInfo.Applicant.provinceOfBirth", "Ontario")
    helper.enter_input("personalInfo.Applicant.SIN", "485888473")
    helper.enter_drop_down("Citizenship", 0, 1)
    helper.click_next_btn()

def enter_contact_info():
    helper.wait_for_next_btn()
    helper.enter_input("contactInfo.Applicant.contact.email", "test@gmail.com")
    phoneNumField = helper.wait_for_element_by_xpath('//label[text()="Phone Number"]/..//div//div//input[@type="tel"]')
    phoneNumField.send_keys("1111111111")
    homePhoneField = helper.wait_for_element_by_xpath('//label[text()="Home Phone"]/..//div//div//input[@type="tel"]')
    homePhoneField.send_keys("2222222222")
    workPhoneField = helper.wait_for_element_by_xpath('//label[text()="Work Phone"]/..//div//div//input[@type="tel"]')
    workPhoneField.send_keys("3333333333")
    helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
    helper.scroll_to_next_btn()
    helper.enter_input("contactInfo.Applicant.currAddr.streetNumberC", "22352")
    helper.enter_input("contactInfo.Applicant.currAddr.cityC", "Toronto")
    helper.enter_input("contactInfo.Applicant.currAddr.postCodeC", "M5B 1N8")
    helper.enter_input("contactInfo.Applicant.currAddr.streetNameC", "Paul Orchard")
    helper.enter_drop_down("Province", 0, 0)
    helper.select_today_date_picker('//label[text()="Living Here Since"]/..//div//div//button', 0)
    helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
    helper.enter_input("contactInfo.Applicant.prevAddr.streetNumberP", "15063")
    helper.enter_input("contactInfo.Applicant.prevAddr.cityP", "Toronto")
    helper.enter_input("contactInfo.Applicant.prevAddr.postCodeP", "M4N 1T7")
    helper.enter_input("contactInfo.Applicant.prevAddr.streetNameP", "Schroeder Villages")
    helper.enter_drop_down("Province", 1, 0)
    helper.select_today_date_picker('//label[text()="Living Here Since"]/..//div//div//button', 1)
    helper.click_next_btn()

def enter_id_info():
    helper.wait_for_next_btn()
    mainApplicantID1Div = helper.wait_for_element_by_xpath('//div[text()="Main Applicant ID 1"]')
    helper.click_btn(mainApplicantID1Div)
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
    helper.scroll_up_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
    
    mainApplicantID2Div = helper.wait_for_element_by_xpath('//div[text()="Main Applicant ID 2"]')
    helper.click_btn(mainApplicantID2Div)
    helper.enter_input("identification.Applicant.id2.fullName", "test test")
    helper.enter_input("identification.Applicant.id2.idNumber", "22222")
    helper.enter_drop_down("ID Type", 0, 2)
    helper.enter_drop_down("Issuing Authority", 0, 2)
    helper.upload_file_to_input(0)
    helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 250)
    helper.enter_drop_down("Issuing Country", 0, 1)
    helper.enter_input("identification.Applicant.id2.issueProvince", "Ontario")
    helper.select_today_date_picker('//label[text()="Issue Date"]/..//div//button', 0)
    helper.select_today_date_picker('//label[text()="Expiry Date"]/..//div//button', 0)
    saveBtns = helper.wait_for_all_elements_by_xpath('//button[text()="Save"]')
    helper.click_btn(saveBtns[0])

    mainApplicantVerification = helper.wait_for_element_by_xpath('//div[text()="Main Applicant Verification"]')
    helper.click_btn(mainApplicantVerification)
    yesRadioBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="Yes"]')
    helper.click_btn(yesRadioBtn)
    saveBtns = helper.wait_for_all_elements_by_xpath('//button[text()="Save"]')
    helper.click_btn(saveBtns[0])

    helper.click_next_btn()

def enter_tax_status():
    helper.wait_for_next_btn()
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
    time.sleep(3)
    disclosureFormBtn = helper.wait_for_element_by_xpath('//button[text()="Disclosure Form"]')
    helper.click_btn(disclosureFormBtn)
    helper.click_next_btn()

def enter_source_contri_info():
    helper.wait_for_next_btn()
    helper.click_next_btn()

def enter_contri_option_info():
    helper.wait_for_next_btn()
    helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
    helper.enter_drop_down("Bank / Institution Name", 0, 0)
    helper.enter_input("contributionOption.commonFields.transitNo", "04000")
    helper.enter_input("contributionOption.commonFields.accountNo", "99999999")
    helper.upload_file_to_input(0)
    helper.click_next_btn()

def enter_policy_guarantee_lvl_info():
    helper.wait_for_next_btn()
    guaranteeLvlOption = helper.wait_for_element_by_xpath('//button[@role="radio"]')
    helper.click_btn(guaranteeLvlOption)
    helper.click_next_btn()

def enter_resi_status_info():
    helper.wait_for_next_btn()
    otherResiStatusOption = helper.wait_for_element_by_xpath('//button[contains(text(), "I live with others.")]')
    helper.click_btn(otherResiStatusOption)
    helper.click_next_btn()

def ans_canadian_real_estate_ques():
    helper.wait_for_next_btn()
    noQuesOption = helper.wait_for_element_by_xpath('//button[contains(text(), "No")]')
    helper.click_btn(noQuesOption)
    helper.click_next_btn()

def enter_fin_analysis_info():
    helper.wait_for_next_btn()
    # because of window.reload()
    helper.wait_for_next_btn()
    
    helper.scroll_to_next_btn()
    addLiabilityBtn = helper.wait_for_element_by_xpath('//p[contains(text(), "Add Liabilities")]/following-sibling::div//button')
    helper.click_btn(addLiabilityBtn)
    helper.wait_for_element_by_xpath('//input[@name="commonFields.liabilityBalance"]')
    helper.enter_drop_down("Owner", 0, 0)
    helper.enter_drop_down("Liability Type", 0, 2)
    helper.enter_input("commonFields.liabilityBalance", "100")
    helper.enter_input("commonFields.liabilityMonthlyPayment", "5")
    addLiabilityDialogBtn = helper.wait_for_element_by_xpath('//div[@role="dialog"]//div//button[contains(text(), "Add Liability")]')
    helper.click_btn(addLiabilityDialogBtn)
    time.sleep(0.5)
    # WebDriverWait(browser, 10).until_not(EC.visibility_of_element_located((By.NAME, 'commonFields.liabilityBalance')))
    helper.click_next_btn()

    helper.scroll_to_next_btn()
    addAssetBtn = helper.wait_for_element_by_xpath('//p[contains(text(), "Add assets")]/following-sibling::div//button')
    helper.click_btn(addAssetBtn)
    helper.wait_for_element_by_xpath('//input[@name="commonFields.assetMarketValue"]')
    helper.enter_drop_down("Owner", 0, 0)
    helper.enter_input("commonFields.assetMarketValue", "1000000")
    helper.enter_drop_down("Asset Type", 0, 0)
    addAssetDialogBtn = helper.wait_for_element_by_xpath('//div[@role="dialog"]//div//button[contains(text(), "Add Asset")]')
    helper.click_btn(addAssetDialogBtn)
    time.sleep(0.5)
    # WebDriverWait(browser, 10).until_not(EC.visibility_of_element_located((By.NAME, 'commonFields.assetMarketValue')))
    helper.click_next_btn()

    helper.scroll_to_next_btn()
    addIncomeBtn = helper.wait_for_element_by_xpath('//p[contains(text(),"TFSA, RRSP")]/following-sibling::div//button')
    helper.click_btn(addIncomeBtn)
    helper.wait_for_element_by_xpath('//input[@name="commonFields.annualIncome"]')
    helper.enter_drop_down("Owner", 0, 0)
    helper.enter_drop_down("Income Type", 0, 7)
    helper.enter_input("commonFields.annualIncome", "100000")
    helper.enter_input("commonFields.incomeTypeOther", "Social Media")
    addIncomeDialogBtn = helper.wait_for_element_by_xpath('//div[@role="dialog"]//div//button[contains(text(), "Add Income")]')
    helper.click_btn(addIncomeDialogBtn)
    time.sleep(0.5)
    # WebDriverWait(browser, 10).until_not(EC.visibility_of_element_located((By.NAME, 'commonFields.annualIncome')))
    helper.click_next_btn()

    helper.wait_for_element_by_xpath('//p[text()="Great Job!"]')
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

def enter_credit_report_info():
    helper.wait_for_next_btn()
    confirmRadioBtns = helper.wait_for_all_elements_by_xpath('//button[@role="radio"]')
    helper.click_btn(confirmRadioBtns[0])
    helper.upload_file_to_input(0)
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
    send_verification_code()
    message = "@" # await get_verification_mail()
    if len(message) != 0:
       pre_application_steps(message)
       create_application()
    
if __name__ == "__main__":
    asyncio.run(main())