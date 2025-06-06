from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import asyncio
import time
from utils import *
from helpers import *

options: dict[str, str] = {}
helper: SeleniumHelper = None

def send_verification_code():
    helper.browser_get('http://localhost:5173')

    login_btn = helper.wait_for_element_by_xpath('//button[text()="Log in"]')
    helper.click_btn(login_btn)

    user, password = load_credentials("internal-credentials.yaml")
    helper.enter_input('Username', user)
    helper.enter_input('Password', password)

    signin_btn = helper.wait_for_element_by_xpath('//button[@id="next"]')
    helper.click_btn(signin_btn)
    helper.wait_for_url_change()

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
    if (len(options["personal_info_pref_name"]) > 0):
        helper.enter_input("personalInfo.Applicant.preferredName", options["personal_info_pref_name"])
    helper.enter_drop_down("Gender", 0, 0)
    helper.enter_drop_down("Marital Status", 0, 0)
    helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
    helper.scroll_to_next_btn()
    helper.select_first_date_picker('//label[text()="Date of Birth"]/..//div//div//button', 0)
    helper.enter_drop_down("Country of Birth", 0, 
        0 if options["personal_info_country_of_birth"] != "canada" else 1
    )
    helper.enter_input("personalInfo.Applicant.provinceOfBirth", "Ontario")
    helper.enter_input("personalInfo.Applicant.SIN", "485888473")
    if (options["personal_info_country_of_birth"] != "canada"):
        if (options["personal_info_resi_since"] == "first of month"):
            helper.select_first_date_picker('//label[text()="Resident of Canada Since"]/..//div//div//button', 0)
        else:
            helper.select_today_date_picker('//label[text()="Resident of Canada Since"]/..//div//div//button', 0)
    helper.enter_drop_down("Citizenship", 0, 1)

    if (options["personal_info_if_co_applicant"] == "yes"):
        yesOptionBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="true"]')
        helper.click_btn(yesOptionBtn)
        helper.scroll_up_div_by_pg_up('//div[contains(@class, "overflow-y-auto")]')
        helper.switch_to_co_applicant_section()
        
        helper.enter_input("personalInfo.Co-Applicant.firstName", "co test")
        helper.enter_input("personalInfo.Co-Applicant.lastName", "co test")
        if (len(options["personal_info_co_pref_name"]) > 0):
            helper.enter_input("personalInfo.Co-Applicant.preferredName", options["personal_info_co_pref_name"])
        helper.enter_drop_down("Gender", 0, 0)
        helper.enter_drop_down("Marital Status", 0, 0)
        helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
        helper.scroll_to_next_btn()
        helper.select_first_date_picker('//label[text()="Date of Birth"]/..//div//div//button', 0)
        helper.enter_drop_down("Country of Birth", 0, 
            0 if options["personal_info_co_country_of_birth"] != "canada" else 1
        )
        helper.enter_input("personalInfo.Co-Applicant.provinceOfBirth", "Ontario")
        helper.enter_input("personalInfo.Co-Applicant.SIN", "207694530")
        if (options["personal_info_co_country_of_birth"] != "canada"):
            if (options["personal_info_co_resi_since"] == "first of month"):
                helper.select_first_date_picker('//label[text()="Resident of Canada Since"]/..//div//div//button', 0)
            else:
                helper.select_today_date_picker('//label[text()="Resident of Canada Since"]/..//div//div//button', 0)
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
    if (options["contact_info_search_for_cur_address"] == "yes"):
        addressField = helper.wait_for_element_by_xpath('//label[text()="Current Address"]/..//div//div//div//div//input')
        helper.send_keys(addressField, "350 Hwy 7, Richmond Hill, ON L4B 3N2")
        optionDiv = helper.wait_for_element_by_xpath('//label[text()="Current Address"]/..//div//div//div//div//div//div//div//div[@data-value="350 Hwy 7, Richmond Hill, ON L4B 3N2"]')
        helper.click_btn(optionDiv)
    else:
        helper.enter_input("contactInfo.Applicant.currAddr.streetNumberC", "22352")
        helper.enter_input("contactInfo.Applicant.currAddr.cityC", "Toronto")
        helper.enter_input("contactInfo.Applicant.currAddr.postCodeC", "M5B 1N8")
        helper.enter_input("contactInfo.Applicant.currAddr.streetNameC", "Paul Orchard")
        if (options["contact_info_cur_province"] == "valid"):
            helper.enter_drop_down("Province", 0, 0)
        else:
            helper.enter_drop_down("Province", 0, 2)
            helper.no_proceed_app()
    if (options["contact_info_cur_living_since"] == "first of month"):
        helper.select_first_date_picker('//label[text()="Living Here Since"]/..//div//div//button', 0)
    elif (options["contact_info_cur_living_since"] == "today"):
        helper.select_today_date_picker('//label[text()="Living Here Since"]/..//div//div//button', 0)
    else:
        helper.select_first_at_least_12yrs_ago_date_selector('//label[text()="Living Here Since"]/..//div//div//button', 0)
    
    if (options["contact_info_cur_living_since"] != "first of month at least 12 yrs ago"):
        helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
        if (options["contact_info_search_for_prev_address"] == "yes"):
            addressField = helper.wait_for_element_by_xpath('//label[text()="Previous Address"]/..//div//div//div//div//input')
            helper.send_keys(addressField, "350 Hwy 7, Richmond Hill, ON L4B 3N2")
            optionDiv = helper.wait_for_element_by_xpath('//label[text()="Previous Address"]/..//div//div//div//div//div//div//div//div[@data-value="350 Hwy 7, Richmond Hill, ON L4B 3N2"]')
            helper.click_btn(optionDiv)
        else:
            helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
            helper.enter_input("contactInfo.Applicant.prevAddr.streetNumberP", "15063")
            helper.enter_input("contactInfo.Applicant.prevAddr.cityP", "Toronto")
            helper.enter_input("contactInfo.Applicant.prevAddr.postCodeP", "M4N 1T7")
            helper.enter_input("contactInfo.Applicant.prevAddr.streetNameP", "Schroeder Villages")
            helper.enter_drop_down("Province", 1, 0)
        if (options["contact_info_prev_living_since"] == "first of month"):
            helper.select_first_date_picker('//label[text()="Living Here Since"]/..//div//div//button', 1)
        elif (options["contact_info_prev_living_since"] == "today"):
            helper.select_today_date_picker('//label[text()="Living Here Since"]/..//div//div//button', 1)

    if (options["personal_info_if_co_applicant"] == "yes"):
        helper.scroll_up_div_by_pg_up('//div[contains(@class, "overflow-y-auto")]')
        helper.switch_to_co_applicant_section()
        helper.enter_input("contactInfo.Co-Applicant.contact.email", "test@gmail.com")
        phoneNumField = helper.wait_for_element_by_xpath('//label[text()="Phone Number"]/..//div//div//input[@type="tel"]')
        phoneNumField.send_keys("1111111111")
        homePhoneField = helper.wait_for_element_by_xpath('//label[text()="Home Phone"]/..//div//div//input[@type="tel"]')
        homePhoneField.send_keys("2222222222")
        workPhoneField = helper.wait_for_element_by_xpath('//label[text()="Work Phone"]/..//div//div//input[@type="tel"]')
        workPhoneField.send_keys("3333333333")

        if (options["contact_info_co_applicant_same_address"] == "yes"):
            yesOptionBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="true"]')
            yesOptionBtn.click()
        else:
            helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
            if (options["contact_info_co_search_for_cur_address"] == "yes"):
                addressField = helper.wait_for_element_by_xpath('//label[text()="Current Address"]/..//div//div//div//div//input')
                helper.send_keys(addressField, "3500 Steeles Ave E, Markham, ON L3R 0X1")
                optionDiv = helper.wait_for_element_by_xpath('//label[text()="Current Address"]/..//div//div//div//div//div//div//div//div[@data-value="3500 Steeles Ave E, Markham, ON L3R 0X1"]')
                helper.click_btn(optionDiv)
            else:
                helper.enter_input("contactInfo.Co-Applicant.currAddr.streetNumberC", "22352")
                helper.enter_input("contactInfo.Co-Applicant.currAddr.cityC", "Toronto")
                helper.enter_input("contactInfo.Co-Applicant.currAddr.postCodeC", "M5B 1N8")
                helper.enter_input("contactInfo.Co-Applicant.currAddr.streetNameC", "Paul Orchard")
                if (options["contact_info_co_cur_province"] == "valid"):
                    helper.enter_drop_down("Province", 0, 0)
                else:
                    helper.enter_drop_down("Province", 0, 2)
                    helper.no_proceed_app()
            if (options["contact_info_co_cur_living_since"] == "first of month"):
                helper.select_first_date_picker('//label[text()="Living Here Since"]/..//div//div//button', 0)
            elif (options["contact_info_co_cur_living_since"] == "today"):
                helper.select_today_date_picker('//label[text()="Living Here Since"]/..//div//div//button', 0)
            else:
                helper.select_first_at_least_12yrs_ago_date_selector('//label[text()="Living Here Since"]/..//div//div//button', 0)
            
            if (options["contact_info_co_cur_living_since"] != "first of month at least 12 yrs ago"):
                helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
                if (options["contact_info_co_search_for_prev_address"] == "yes"):
                    addressField = helper.wait_for_element_by_xpath('//label[text()="Previous Address"]/..//div//div//div//div//input')
                    helper.send_keys(addressField, "3500 Steeles Ave E, Markham, ON L3R 0X1")
                    optionDiv = helper.wait_for_element_by_xpath('//label[text()="Previous Address"]/..//div//div//div//div//div//div//div//div[@data-value="3500 Steeles Ave E, Markham, ON L3R 0X1"]')
                    helper.click_btn(optionDiv)
                else:
                    helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
                    helper.enter_input("contactInfo.Co-Applicant.prevAddr.streetNumberP", "15063")
                    helper.enter_input("contactInfo.Co-Applicant.prevAddr.cityP", "Toronto")
                    helper.enter_input("contactInfo.Co-Applicant.prevAddr.postCodeP", "M4N 1T7")
                    helper.enter_input("contactInfo.Co-Applicant.prevAddr.streetNameP", "Schroeder Villages")
                    helper.enter_drop_down("Province", 1, 0)
                if (options["contact_info_co_prev_living_since"] == "first of month"):
                    helper.select_first_date_picker('//label[text()="Living Here Since"]/..//div//div//button', 1)
                elif (options["contact_info_co_prev_living_since"] == "today"):
                    helper.select_today_date_picker('//label[text()="Living Here Since"]/..//div//div//button', 1)

    helper.click_next_btn()

def enter_id_info():
    helper.wait_for_next_btn()

    mainApplicantID1Div = helper.wait_for_element_by_xpath('//div[text()="Main Applicant ID 1"]')
    helper.click_btn(mainApplicantID1Div)
    helper.enter_input("identification.Applicant.id1.fullName", "test test")
    helper.enter_input("identification.Applicant.id1.idNumber", "11111")
    if (options["id_info_id1_type"] == "citizenship card"):
        helper.enter_drop_down("ID Type", 0, 2)
    else:
        helper.enter_drop_down("ID Type", 0, 0)
    helper.enter_drop_down("Issuing Authority", 0, 2)
    helper.upload_file_to_input(0)
    helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
    helper.enter_drop_down("Issuing Country", 0, 1)
    helper.enter_input("identification.Applicant.id1.issueProvince", "Ontario")
    if (options["id_info_id1_issue_date"] == "first of month"):
        helper.select_first_date_picker('//label[text()="Issue Date"]/..//div//button', 0)
    else:
        helper.select_today_date_picker('//label[text()="Issue Date"]/..//div//button', 0)
    if (options["id_info_id1_type"] != "citizenship card"):
        helper.select_today_date_picker('//label[text()="Expiry Date"]/..//div//button', 0)
    saveBtns = helper.wait_for_all_elements_by_xpath('//button[text()="Save"]')
    helper.click_btn(saveBtns[0])

    helper.scroll_up_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
    
    mainApplicantID2Div = helper.wait_for_element_by_xpath('//div[text()="Main Applicant ID 2"]')
    helper.click_btn(mainApplicantID2Div)
    helper.enter_input("identification.Applicant.id2.fullName", "test test")
    helper.enter_input("identification.Applicant.id2.idNumber", "22222")
    if (options["id_info_id2_type"] == "citizenship card"):
        helper.enter_drop_down("ID Type", 0, 1)
    else:
        helper.enter_drop_down("ID Type", 0, 0)
    helper.enter_drop_down("Issuing Authority", 0, 2)
    helper.upload_file_to_input(0)
    helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 250)
    helper.enter_drop_down("Issuing Country", 0, 1)
    helper.enter_input("identification.Applicant.id2.issueProvince", "Ontario")
    if (options["id_info_id2_issue_date"] == "first of month"):
        helper.select_first_date_picker('//label[text()="Issue Date"]/..//div//button', 0)
    else:
        helper.select_today_date_picker('//label[text()="Issue Date"]/..//div//button', 0)
    if (options["id_info_id2_type"] != "citizenship card"):
        helper.select_today_date_picker('//label[text()="Expiry Date"]/..//div//button', 0)
    saveBtns = helper.wait_for_all_elements_by_xpath('//button[text()="Save"]')
    helper.click_btn(saveBtns[0])

    mainApplicantVerification = helper.wait_for_element_by_xpath('//div[text()="Main Applicant Verification"]')
    helper.click_btn(mainApplicantVerification)
    if (options["id_info_in_person_verify"] == "no"):
        helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
        noRadioBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="No"]')
        helper.click_btn(noRadioBtn)
        if (options["id_info_id_verify_doc_type"] == "other option"):
            helper.enter_drop_down("Verification Document Type", 0, 8)
            helper.enter_input("identification.Applicant.verification.otherIdType", "Other Reason")
        else:
            helper.enter_drop_down("Verification Document Type", 0, 0)
        helper.enter_input("identification.Applicant.verification.issueAuthority", "Govt of Canada")
        helper.enter_input("identification.Applicant.verification.accountReference", "11111")
        if (options["id_info_id_verify_doc_date"] == "first of month"):
            helper.select_first_date_picker('//label[text()="ID Verification Document Date of Information"]/..//div//button', 0)
        else:
            helper.select_today_date_picker('//label[text()="ID Verification Document Date of Information"]/..//div//button', 0)
        helper.upload_file_to_input(0)
    else:
        yesRadioBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="Yes"]')
        helper.click_btn(yesRadioBtn)
    saveBtns = helper.wait_for_all_elements_by_xpath('//button[text()="Save"]')
    helper.click_btn(saveBtns[0])

    if (options["personal_info_if_co_applicant"] == "yes"):
        helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 500)
        helper.switch_to_co_applicant_section()

        mainApplicantID1Div = helper.wait_for_element_by_xpath('//div[text()="Co-Applicant ID 1"]')
        helper.click_btn(mainApplicantID1Div)
        helper.enter_input("identification.Co-Applicant.id1.fullName", "co test co test")
        helper.enter_input("identification.Co-Applicant.id1.idNumber", "11111")
        if (options["id_info_co_id1_type"] == "citizenship card"):
            helper.enter_drop_down("ID Type", 0, 2)
        else:
            helper.enter_drop_down("ID Type", 0, 0)
        helper.enter_drop_down("Issuing Authority", 0, 2)
        helper.upload_file_to_input(0)
        helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
        helper.enter_drop_down("Issuing Country", 0, 1)
        helper.enter_input("identification.Co-Applicant.id1.issueProvince", "Ontario")
        if (options["id_info_co_id1_issue_date"] == "first of month"):
            helper.select_first_date_picker('//label[text()="Issue Date"]/..//div//button', 0)
        else:
            helper.select_today_date_picker('//label[text()="Issue Date"]/..//div//button', 0)
        if (options["id_info_co_id1_type"] != "citizenship card"):
            helper.select_today_date_picker('//label[text()="Expiry Date"]/..//div//button', 0)
        saveBtns = helper.wait_for_all_elements_by_xpath('//button[text()="Save"]')
        helper.click_btn(saveBtns[0])

        helper.scroll_up_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
        
        mainApplicantID2Div = helper.wait_for_element_by_xpath('//div[text()="Co-Applicant ID 2"]')
        helper.click_btn(mainApplicantID2Div)
        helper.enter_input("identification.Co-Applicant.id2.fullName", "test test")
        helper.enter_input("identification.Co-Applicant.id2.idNumber", "22222")
        if (options["id_info_co_id2_type"] == "citizenship card"):
            helper.enter_drop_down("ID Type", 0, 1)
        else:
            helper.enter_drop_down("ID Type", 0, 0)
        helper.enter_drop_down("Issuing Authority", 0, 2)
        helper.upload_file_to_input(0)
        helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 250)
        helper.enter_drop_down("Issuing Country", 0, 1)
        helper.enter_input("identification.Co-Applicant.id2.issueProvince", "Ontario")
        if (options["id_info_co_id2_issue_date"] == "first of month"):
            helper.select_first_date_picker('//label[text()="Issue Date"]/..//div//button', 0)
        else:
            helper.select_today_date_picker('//label[text()="Issue Date"]/..//div//button', 0)
        if (options["id_info_co_id2_type"] != "citizenship card"):
            helper.select_today_date_picker('//label[text()="Expiry Date"]/..//div//button', 0)
        saveBtns = helper.wait_for_all_elements_by_xpath('//button[text()="Save"]')
        helper.click_btn(saveBtns[0])

        mainApplicantVerification = helper.wait_for_element_by_xpath('//div[text()="Co-Applicant Verification"]')
        helper.click_btn(mainApplicantVerification)
        if (options["id_info_co_in_person_verify"] == "no"):
            helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
            noRadioBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="No"]')
            helper.click_btn(noRadioBtn)
            if (options["id_info_co_id_verify_doc_type"] == "other option"):
                helper.enter_drop_down("Verification Document Type", 0, 8)
                helper.enter_input("identification.Co-Applicant.verification.otherIdType", "Other Reason")
            else:
                helper.enter_drop_down("Verification Document Type", 0, 0)
            helper.enter_input("identification.Co-Applicant.verification.issueAuthority", "Govt of Canada")
            helper.enter_input("identification.Co-Applicant.verification.accountReference", "11111")
            if (options["id_info_co_id_verify_doc_date"] == "first of month"):
                helper.select_first_date_picker('//label[text()="ID Verification Document Date of Information"]/..//div//button', 0)
            else:
                helper.select_today_date_picker('//label[text()="ID Verification Document Date of Information"]/..//div//button', 0)
            helper.upload_file_to_input(0)
        else:
            yesRadioBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="Yes"]')
            helper.click_btn(yesRadioBtn)
        saveBtns = helper.wait_for_all_elements_by_xpath('//button[text()="Save"]')
        helper.click_btn(saveBtns[0])

    helper.click_next_btn()

def enter_tax_status():
    helper.wait_for_next_btn()
    if (options["tax_status_info_tax_resi_of_canada"] == "no"):
        noOptionBtn = helper.wait_for_element_by_xpath('//label[text()="Are you a Canadian resident for tax purposes?"]/..//div//div//button[@role="radio" and @value="No"]')
        helper.click_btn(noOptionBtn)
        helper.no_proceed_app()
    if (options["tax_status_info_us_resi"] == "yes"):
        taxResiOfUSDiv = helper.wait_for_element_by_xpath('//div[text()="Tax Residence of the United States"]')
        helper.click_btn(taxResiOfUSDiv)
        yesOptionBtn = helper.wait_for_element_by_xpath('//label[text()="Are you a United States citizen or a U.S. resident for U.S. tax purposes?"]/..//div//div//button[@role="radio" and @value="Yes"]')
        helper.click_btn(yesOptionBtn)
        helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
        if (options["tax_status_info_tin_from_us"] == "yes"):
            yesOptionBtn = helper.wait_for_element_by_xpath('//label[text()="Do you have a Taxpayer Identification Number (TIN) from the U.S.?"]/..//div//div//button[@role="radio" and @value="Yes"]')
            helper.click_btn(yesOptionBtn)
            helper.enter_input("taxStatus.Applicant.residencyUnitedStates.tinUS", "99999")
        else:
            if (options["tax_status_info_reason_for_no_tin"] == "other"):
                helper.enter_drop_down("Reason why you don't have a TIN", 0, 2)
                helper.enter_input("taxStatus.Applicant.residencyUnitedStates.otherReasonOfNoTinUS", "Other Reason")
            else:
                helper.enter_drop_down("Reason why you don't have a TIN", 0, 0)
    if (options["tax_status_info_other_region"] == "yes"):
        taxResiOfOtherDiv = helper.wait_for_element_by_xpath('//div[text()="Tax Residence of a jurisdiction other than Canada or the United States"]')
        helper.click_btn(taxResiOfOtherDiv)
        yesOptionBtn = helper.wait_for_element_by_xpath('//label[text()="Are you a resident for tax purposes in a coutnry or region other than Canada or the United States?"]/..//div//div//button[@role="radio" and @value="Yes"]')
        helper.click_btn(yesOptionBtn)
        helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
        helper.enter_input("taxStatus.Applicant.residencyOther.countryName", "India")
        if (options["tax_status_info_tin_from_other"] == "yes"):
            yesOptionBtn = helper.wait_for_element_by_xpath('//label[text()="Do you have a Taxpayer Identification Number (TIN) outside the U.S. or Canada?"]/..//div//div//button[@role="radio" and @value="Yes"]')
            helper.click_btn(yesOptionBtn)
            helper.enter_input("taxStatus.Applicant.residencyOther.tinOther", "99999")
        else:
            if (options["tax_status_info_reason_for_no_other_tin"] == "other"):
                helper.enter_drop_down("Reason why you don't have a TIN", 0, 2)
                helper.enter_input("taxStatus.Applicant.residencyOther.otherReasonOfNoTinOther", "Other Reason")
            else:
                helper.enter_drop_down("Reason why you don't have a TIN", 0, 0)
    
    if (options["personal_info_if_co_applicant"] == "yes"):
        helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
        helper.switch_to_co_applicant_section()

        if (options["tax_status_info_co_tax_resi_of_canada"] == "no"):
            noOptionBtn = helper.wait_for_element_by_xpath('//label[text()="Are you a Canadian resident for tax purposes?"]/..//div//div//button[@role="radio" and @value="No"]')
            helper.click_btn(noOptionBtn)
            helper.no_proceed_app()
        if (options["tax_status_info_co_us_resi"] == "yes"):
            taxResiOfUSDiv = helper.wait_for_element_by_xpath('//div[text()="Tax Residence of the United States"]')
            helper.click_btn(taxResiOfUSDiv)
            yesOptionBtn = helper.wait_for_element_by_xpath('//label[text()="Are you a United States citizen or a U.S. resident for U.S. tax purposes?"]/..//div//div//button[@role="radio" and @value="Yes"]')
            helper.click_btn(yesOptionBtn)
            helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
            if (options["tax_status_info_co_tin_from_us"] == "yes"):
                yesOptionBtn = helper.wait_for_element_by_xpath('//label[text()="Do you have a Taxpayer Identification Number (TIN) from the U.S.?"]/..//div//div//button[@role="radio" and @value="Yes"]')
                helper.click_btn(yesOptionBtn)
                helper.enter_input("taxStatus.Co-Applicant.residencyUnitedStates.tinUS", "99999")
            else:
                if (options["tax_status_info_co_reason_for_no_tin"] == "other"):
                    helper.enter_drop_down("Reason why you don't have a TIN", 0, 2)
                    helper.enter_input("taxStatus.Co-Applicant.residencyUnitedStates.otherReasonOfNoTinUS", "Other Reason")
                else:
                    helper.enter_drop_down("Reason why you don't have a TIN", 0, 0)
        if (options["tax_status_info_co_other_region"] == "yes"):
            taxResiOfOtherDiv = helper.wait_for_element_by_xpath('//div[text()="Tax Residence of a jurisdiction other than Canada or the United States"]')
            helper.click_btn(taxResiOfOtherDiv)
            yesOptionBtn = helper.wait_for_element_by_xpath('//label[text()="Are you a resident for tax purposes in a coutnry or region other than Canada or the United States?"]/..//div//div//button[@role="radio" and @value="Yes"]')
            helper.click_btn(yesOptionBtn)
            helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-y-auto")]', 200)
            helper.enter_input("taxStatus.Co-Applicant.residencyOther.countryName", "India")
            if (options["tax_status_info_co_tin_from_other"] == "yes"):
                yesOptionBtn = helper.wait_for_element_by_xpath('//label[text()="Do you have a Taxpayer Identification Number (TIN) outside the U.S. or Canada?"]/..//div//div//button[@role="radio" and @value="Yes"]')
                helper.click_btn(yesOptionBtn)
                helper.enter_input("taxStatus.Co-Applicant.residencyOther.tinOther", "99999")
            else:
                if (options["tax_status_info_co_reason_for_no_other_tin"] == "other"):
                    helper.enter_drop_down("Reason why you don't have a TIN", 0, 2)
                    helper.enter_input("taxStatus.Co-Applicant.residencyOther.otherReasonOfNoTinOther", "Other Reason")
                else:
                    helper.enter_drop_down("Reason why you don't have a TIN", 0, 0)

    helper.click_next_btn()

def enter_employment_info():
    helper.wait_for_next_btn()
    if (options["emp_info_status"] == "employed"):
        helper.enter_drop_down("Employment Status", 0, 0)
        helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
        helper.enter_input("employmentInfo.Applicant.commonInfo.responsibilities", "Website Development")
        helper.enter_input("employmentInfo.Applicant.commonInfo.jobTitle", "Software Developer")
        helper.enter_input("employmentInfo.Applicant.commonInfo.empName", "Some Company")
        helper.enter_input("employmentInfo.Applicant.commonInfo.empBusiness", "Ed-tech")
    else:
        helper.enter_drop_down("Employment Status", 0, 2)
        helper.no_proceed_app()

    if (options["personal_info_if_co_applicant"] == "yes"):
        helper.switch_to_co_applicant_section()
        helper.scroll_up_div_by_pg_up('//div[contains(@class, "overflow-y-auto")]')
        if (options["emp_info_co_status"] == "employed"):
            helper.enter_drop_down("Employment Status", 0, 0)
            helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
            helper.enter_input("employmentInfo.Co-Applicant.commonInfo.responsibilities", "Website Development")
            helper.enter_input("employmentInfo.Co-Applicant.commonInfo.jobTitle", "Software Developer")
            helper.enter_input("employmentInfo.Co-Applicant.commonInfo.empName", "Some Company")
            helper.enter_input("employmentInfo.Co-Applicant.commonInfo.empBusiness", "Ed-tech")
    helper.click_next_btn()

def enter_disclosure_info():
    time.sleep(3)
    disclosureFormBtn = helper.wait_for_element_by_xpath('//button[text()="Disclosure Form"]')
    helper.click_btn(disclosureFormBtn)
    helper.click_next_btn()

def enter_source_contri_info():
    helper.wait_for_next_btn()
    if (options["source_of_contri_info_new_loan"] == "no"):
        noOptionBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="no"]')
        helper.click_btn(noOptionBtn)
        helper.enter_input("sourceOfContribution.existingAmount", "10000")
        helper.enter_input("sourceOfContribution.segAccount", "Seg Fund Account")
    helper.click_next_btn()

def enter_contri_option_info():
    helper.wait_for_next_btn()
    if (options["contri_option_requires_more_than_one_sign"] == "yes"):
        yesOptionBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="yes"]')
        helper.click_btn(yesOptionBtn)
        helper.enter_input("contributionOption.commonFields.jointAccountHolder", "joint test")
        helper.enter_input("contributionOption.commonFields.jointAccountHolderEmail", "joint-test@email.com")
    helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
    helper.enter_drop_down("Bank / Institution Name", 0, 0)
    helper.enter_input("contributionOption.commonFields.transitNo", "04000")
    helper.enter_input("contributionOption.commonFields.accountNo", "99999999")
    helper.upload_file_to_input(0)
    helper.click_next_btn()

def enter_policy_guarantee_lvl_info():
    helper.wait_for_next_btn()
    guaranteeLvlOption = helper.wait_for_element_by_xpath(f'//button[@role="radio" and @value="{ options["policy_guarantee_level"] }"]')
    helper.click_btn(guaranteeLvlOption)
    helper.click_next_btn()

def enter_resi_status_info():
    helper.wait_for_next_btn()
    if (options["resi_status_info_main_applicant_resi"] == "own home"):
        homeResiStatusOption = helper.wait_for_element_by_xpath('//button[text()="I own the home I live in."]')
        helper.click_btn(homeResiStatusOption)
    elif (options["resi_status_info_main_applicant_resi"] == "rented home"):
        rentedResiStatusOption = helper.wait_for_element_by_xpath('//button[contains(text(), "I live in a rented home")]')
        helper.click_btn(rentedResiStatusOption)
    elif (options["resi_status_info_main_applicant_resi"] == "live with parents"):
        parentsReiStatusOption = helper.wait_for_element_by_xpath('//button[text()="I live in my parent\'s home."]')
        helper.click_btn(parentsReiStatusOption)
    else:
        otherResiStatusOption = helper.wait_for_element_by_xpath('//button[contains(text(), "I live with others.")]')
        helper.click_btn(otherResiStatusOption)
    if (options["personal_info_if_co_applicant"] == "yes"):
        helper.switch_to_co_applicant_section()
        if (options["resi_status_info_co_applicant_resi"] == "own home"):
            homeResiStatusOption = helper.wait_for_element_by_xpath('//button[text()="I own the home I live in."]')
            helper.click_btn(homeResiStatusOption)
        elif (options["resi_status_info_co_applicant_resi"] == "rented home"):
            rentedResiStatusOption = helper.wait_for_element_by_xpath('//button[contains(text(), "I live in a rented home")]')
            helper.click_btn(rentedResiStatusOption)
        elif (options["resi_status_info_co_applicant_resi"] == "live with parents"):
            parentsReiStatusOption = helper.wait_for_element_by_xpath('//button[text()="I live in my parent\'s home."]')
            helper.click_btn(parentsReiStatusOption)
        else:
            otherResiStatusOption = helper.wait_for_element_by_xpath('//button[contains(text(), "I live with others.")]')
            helper.click_btn(otherResiStatusOption)
    if (options["resi_status_info_main_applicant_resi"] == "own home" or 
        (options["personal_info_if_co_applicant"] == "yes" and options["resi_status_info_co_applicant_resi"] == "own home")
        ):
        helper.click_next_btn()
        time.sleep(1)
        helper.wait_for_next_btn()
        if (options["resi_status_info_owner_of_home"] == "applicant"):
            mainAppOption = helper.wait_for_element_by_xpath('//button[text()="Main Applicant"]')
            helper.click_btn(mainAppOption)
        elif (options["resi_status_info_owner_of_home"] == "co applicant"):
            coAppOption = helper.wait_for_element_by_xpath('//button[text()="Co-Applicant"]')
            helper.click_btn(coAppOption)
        else:
            bothOption = helper.wait_for_element_by_xpath('//button[text()="Both"]')
            helper.click_btn(bothOption)
        helper.click_next_btn()
        time.sleep(1)
        helper.wait_for_next_btn()
        helper.set_zoom(80)
        helper.enter_input("residenceProperty.marketValue", "10000")
        helper.enter_input("residenceProperty.propertyTax", "1000")
        helper.click_next_btn()
        time.sleep(1)
        helper.wait_for_next_btn()
        helper.set_zoom(100)
        if (options["resi_status_info_is_mortgage"] == "yes"):
            yesOption = helper.wait_for_element_by_xpath('//button[text()="Yes"]')
            helper.click_btn(yesOption)
            helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
            helper.enter_input("residenceProperty.mortgageBalance", "10000")
            helper.enter_input("residenceProperty.mortgageMonthly", "1000")
            helper.enter_drop_down("Mortgage Financial Institution", 0, 0)
        helper.click_next_btn()
        time.sleep(1)
        helper.wait_for_next_btn()
        if (options["resi_status_info_is_maintenance_fee"] == "yes"):
            yesOption = helper.wait_for_element_by_xpath('//button[text()="Yes"]')
            helper.click_btn(yesOption)
            helper.enter_input("residenceProperty.monthlyMaintenanceFee", "1000")
    if (options["resi_status_info_main_applicant_resi"] == "rented home" or
        (options["personal_info_if_co_applicant"] and options["resi_status_info_co_applicant_resi"] == "rented home")
        ):
        helper.click_next_btn()
        time.sleep(1)
        helper.wait_for_next_btn()
        helper.enter_input("residenceRental.monthlyRentalFee", "1000")
    helper.click_next_btn()

def ans_canadian_real_estate_ques():
    helper.wait_for_next_btn()
    if (options["cad_real_estate_is_canadian_resi"] == "yes"):
        yesQuesOption = helper.wait_for_element_by_xpath('//button[contains(text(), "Yes")]')
        helper.click_btn(yesQuesOption)
        helper.click_next_btn()
        time.sleep(1)
        helper.wait_for_next_btn()
        if (options["cad_real_estate_owner_of_home"] == "applicant"):
            mainAppOption = helper.wait_for_element_by_xpath('//button[text()="Main Applicant"]')
            helper.click_btn(mainAppOption)
        elif (options["cad_real_estate_owner_of_home"] == "co applicant"):
            coAppOption = helper.wait_for_element_by_xpath('//button[text()="Co-Applicant"]')
            helper.click_btn(coAppOption)
        else:
            bothOption = helper.wait_for_element_by_xpath('//button[text()="Both"]')
            helper.click_btn(bothOption)
        helper.click_next_btn()
        time.sleep(1)
        helper.wait_for_next_btn()
        helper.set_zoom(80)
        helper.enter_input("residenceProperty.marketValue", "10000")
        helper.enter_input("residenceProperty.propertyTax", "1000")
        helper.click_next_btn()
        time.sleep(1)
        helper.wait_for_next_btn()
        helper.set_zoom(100)
        if (options["cad_real_estate_is_mortgage"] == "yes"):
            yesOption = helper.wait_for_element_by_xpath('//button[text()="Yes"]')
            helper.click_btn(yesOption)
            helper.enter_input("residenceProperty.mortgageBalance", "10000")
            helper.enter_input("residenceProperty.mortgageMonthly", "1000")
            helper.enter_drop_down("Mortgage Financial Institution", 0, 0)
        helper.click_next_btn()
        time.sleep(1)
        helper.wait_for_next_btn()
        if (options["cad_real_estate_is_maintenance_fee"] == "yes"):
            yesOption = helper.wait_for_element_by_xpath('//button[text()="Yes"]')
            helper.click_btn(yesOption)
            helper.enter_input("residenceProperty.monthlyMaintenanceFee", "1000")
        helper.click_next_btn()
        time.sleep(1)
        helper.wait_for_next_btn()
    
    noQuesOption = helper.wait_for_element_by_xpath('//button[contains(text(), "No")]')
    helper.click_btn(noQuesOption)
    helper.click_next_btn()

def enter_fin_analysis_info():
    helper.wait_for_next_btn()
    
    helper.scroll_to_next_btn()
    addLiabilityBtn = helper.wait_for_element_by_xpath('//div[text()="Liabilities"]/..//button')
    helper.click_btn(addLiabilityBtn)
    helper.wait_for_element_by_xpath('//input[@name="commonFields.liabilityBalance"]')

    if (options["personal_info_if_co_applicant"] == "yes"):
        if (options["fin_analysis_add_lib_owner"] == "applicant"):
            helper.enter_drop_down("Owner", 0, 0)
        elif (options["fin_analysis_add_lib_owner"] == "co applicant"):
            helper.enter_drop_down("Owner", 0, 1)
        else:
            helper.enter_drop_down("Owner", 0, 2)
    else:
        helper.enter_drop_down("Owner", 0, 0)

    enter_lib_inst_name: bool = True
    enter_lib_bal_and_monthly_pay: bool = True

    if (options["fin_analysis_add_lib_liability_type"] == "mortgage"):
        helper.enter_drop_down("Liability Type", 0, 0)
        if (options["fin_analysis_add_lib_no_mortgage"] == "yes"):
            noMortgageRadio = helper.wait_for_element_by_xpath('//label[@for="noMortgage"]/..//button')
            helper.click_btn(noMortgageRadio)
            enter_lib_inst_name = False
            enter_lib_bal_and_monthly_pay = False
        
        if (options["fin_analysis_add_lib_no_mortgage_maintain_fee"] == "no"):
            noMortgageMaintainFeedRadio = helper.wait_for_element_by_xpath('//label[@for="nomaintenanceFee"]/..//button')
            helper.click_btn(noMortgageMaintainFeedRadio)
            helper.send_backspace_to_input("mortgageFields.condoFeeMonthlyPayment")
            helper.enter_input("mortgageFields.condoFeeMonthlyPayment", "100")

        helper.enter_input("mortgageFields.annualPropertyTax", "10000")

    elif (options["fin_analysis_add_lib_liability_type"] == "rent"):
        helper.enter_drop_down("Liability Type", 0, 2)
        enter_lib_inst_name = False

    elif (options["fin_analysis_add_lib_liability_type"] == "other debts"):
        helper.enter_drop_down("Liability Type", 0, 7)
        helper.enter_input("commonFields.customDebtType", "Other Liability Type")

    if enter_lib_inst_name:
        helper.enter_drop_down("Institution Name", 0, 0)
    if enter_lib_bal_and_monthly_pay:
        helper.send_backspace_to_input("commonFields.liabilityBalance")
        helper.enter_input("commonFields.liabilityBalance", "100")
        helper.send_backspace_to_input("commonFields.liabilityMonthlyPayment")
        helper.enter_input("commonFields.liabilityMonthlyPayment", "5")

    addLiabilityDialogBtn = helper.wait_for_element_by_xpath('//div[@role="dialog"]//div//button[contains(text(), "Add Liability")]')
    helper.click_btn(addLiabilityDialogBtn)
    time.sleep(1)
    # WebDriverWait(browser, 10).until_not(EC.visibility_of_element_located((By.NAME, 'commonFields.liabilityBalance')))
    helper.click_next_btn()

    helper.scroll_to_next_btn()
    addAssetBtn = helper.wait_for_element_by_xpath('//div[text()="Assets"]/..//button')
    helper.click_btn(addAssetBtn)
    helper.wait_for_element_by_xpath('//input[@name="commonFields.assetMarketValue"]')

    if (options["personal_info_if_co_applicant"] == "yes"):
        if (options["fin_analysis_add_asset_owner"] == "applicant"):
            helper.enter_drop_down("Owner", 0, 0)
        elif (options["fin_analysis_add_asset_owner"] == "co applicant"):
            helper.enter_drop_down("Owner", 0, 1)
        else:
            helper.enter_drop_down("Owner", 0, 2)
    else:
        helper.enter_drop_down("Owner", 0, 0)

    helper.send_backspace_to_input("commonFields.assetMarketValue")
    helper.enter_input("commonFields.assetMarketValue", "1000000")

    enter_asset_inst_name: bool = True

    if (options["fin_analysis_add_asset_asset_type"] == "real estate"):
        helper.enter_drop_down("Asset Type", 0, 0)
        enter_asset_inst_name = False
    
    elif (options["fin_analysis_add_asset_asset_type"] == "other assets"):
        helper.enter_drop_down("Asset Type", 0, 13)
        helper.enter_input("commonFields.customAssetType", "Other Asset Type")

    if enter_asset_inst_name:
        helper.enter_drop_down("Institution Name", 0, 0)
    
    addAssetDialogBtn = helper.wait_for_element_by_xpath('//div[@role="dialog"]//div//button[contains(text(), "Add Asset")]')
    helper.click_btn(addAssetDialogBtn)
    time.sleep(1)
    # WebDriverWait(browser, 10).until_not(EC.visibility_of_element_located((By.NAME, 'commonFields.assetMarketValue')))
    helper.click_next_btn()

    helper.scroll_to_next_btn()
    addIncomeBtn = helper.wait_for_element_by_xpath('//div[text()="Incomes"]/..//button')
    helper.click_btn(addIncomeBtn)
    helper.wait_for_element_by_xpath('//input[@name="commonFields.annualIncome"]')

    helper.set_zoom(50)
    
    if (options["personal_info_if_co_applicant"] == "yes"):
        if (options["fin_analysis_add_income_owner"] == "applicant"):
            helper.enter_drop_down("Owner", 0, 0)
        elif (options["fin_analysis_add_income_owner"] == "co applicant"):
            helper.enter_drop_down("Owner", 0, 1)
        else:
            helper.enter_drop_down("Owner", 0, 2)
    else:
        helper.enter_drop_down("Owner", 0, 0)
    
    if (options["fin_analysis_add_income_income_type"] == "employment"):
        helper.enter_drop_down("Income Type", 0, 0)

        helper.enter_drop_down("Industry", 0, 0)
        helper.enter_drop_down("Occupation", 0, 0)
        helper.enter_input("currEmploymentFields.employmentInfo.employerName", "Employer Name")

        if (options["fin_analysis_add_income_search_for_cur_emp_address"] == "yes"):
            addressField = helper.wait_for_element_by_xpath('//label[text()="Current Employer Address"]/..//div//div//div//div//input')
            helper.send_keys(addressField, "350 Hwy 7, Richmond Hill, ON L4B 3N2")
            optionDiv = helper.wait_for_element_by_xpath('//label[text()="Current Employer Address"]/..//div//div//div//div//div//div//div//div[@data-value="350 Hwy 7, Richmond Hill, ON L4B 3N2"]')
            helper.click_btn(optionDiv)
        else:
            helper.enter_input("currEmploymentFields.addr.employerAddressStreetNumber", "201")
            helper.enter_input("currEmploymentFields.addr.employerAddressCity", "Hamilton")
            helper.enter_input("currEmploymentFields.addr.employerAddressPostalCode", "L8R 2L2")
            helper.enter_input("currEmploymentFields.addr.employerAddressStreetName", "James St N")
            helper.enter_input("currEmploymentFields.addr.employerAddressProvince", "ON")
        
        if (options["fin_analysis_add_income_cur_serving_since"] == "today"):
            helper.select_today_date_picker('//label[text()="Serving Since"]/..//div//button', 0)

            helper.set_zoom(100)
            time.sleep(1)
            prevIndustryDropDown = helper.wait_for_element_by_xpath('//label[text()="Previous Industry"]/..//div//button[@role="combobox"]')
            helper.click_btn(prevIndustryDropDown)
            helper.wait_for_element_by_xpath('//div[@role="option"]')
            time.sleep(1)
            agriIndustryOption = helper.wait_for_element_by_xpath('//div[@role="option"]//span[text()="Agriculture"]')
            helper.click_btn(agriIndustryOption)
            time.sleep(1)
            prevOccupationDropDown = helper.wait_for_element_by_xpath('//label[text()="Previous Occupation"]/..//div//button[@role="combobox"]')
            helper.click_btn(prevOccupationDropDown)
            helper.wait_for_element_by_xpath('//div[@role="option"]')
            time.sleep(1)
            hortiAgriOption = helper.wait_for_element_by_xpath('//div[@role="option"]//span[text()="Horticulturalist"]')
            helper.click_btn(hortiAgriOption)
            time.sleep(1)
            helper.set_zoom(50)
            helper.enter_input("prevEmploymentFields.employmentInfo.previousEmployerName", "Previous Employer Name")

            if (options["fin_analysis_add_income_search_for_prev_emp_address"] == "yes"):
                addressField = helper.wait_for_element_by_xpath('//label[text()="Previous Employer Address"]/..//div//div//div//div//input')
                helper.send_keys(addressField, "350 Hwy 7, Richmond Hill, ON L4B 3N2")
                optionDiv = helper.wait_for_element_by_xpath('//label[text()="Previous Employer Address"]/..//div//div//div//div//div//div//div//div[@data-value="350 Hwy 7, Richmond Hill, ON L4B 3N2"]')
                helper.click_btn(optionDiv)
            else:
                helper.enter_input("prevEmploymentFields.addr.previousEmployerAddressStreetNumber", "9528")
                helper.enter_input("prevEmploymentFields.addr.previousEmployerAddressCity", "Toronto")
                helper.enter_input("prevEmploymentFields.addr.previousEmployerAddressPostalCode", "L9T 2X7")
                helper.enter_input("prevEmploymentFields.addr.previousEmployerAddressStreetName", "25 Hwy")
                helper.enter_input("prevEmploymentFields.addr.previousEmployerAddressProvince", "ON")

            helper.select_today_date_picker('//label[text()="Previous Serving Since"]/..//div//button', 0)
        
        else:
            helper.select_first_at_least_12yrs_ago_date_selector('//label[text()="Serving Since"]/..//div//button', 0)


    elif (options["fin_analysis_add_income_income_type"] == "other income"):
        helper.enter_drop_down("Income Type", 0, 7)
        helper.enter_input("commonFields.incomeTypeOther", "Social Media")
    
    else:
        helper.enter_drop_down("Income Type", 0, 2)
    
    helper.send_backspace_to_input("commonFields.annualIncome")
    helper.enter_input("commonFields.annualIncome", "1000000")
    addIncomeDialogBtn = helper.wait_for_element_by_xpath('//div[@role="dialog"]//div//button[contains(text(), "Add Income")]')
    helper.click_btn(addIncomeDialogBtn)
    helper.set_zoom(100)
    time.sleep(1)
    # WebDriverWait(browser, 10).until_not(EC.visibility_of_element_located((By.NAME, 'commonFields.annualIncome')))
    helper.click_next_btn()

    helper.wait_for_element_by_xpath('//p[text()="Great Job!"]')
    helper.click_next_btn()

def enter_primary_beneficiary_info():
    helper.wait_for_next_btn()
    helper.enter_input("pendingBeneficiary.commonInfo.firstName", "newTest")
    helper.enter_input("pendingBeneficiary.commonInfo.lastName", "newTest")
    if (options["primary_beneficiary_relation_to_annutaint"] == "other option"):
        helper.enter_drop_down("Relation to Annuitant", 0, 26)
        helper.enter_input("pendingBeneficiary.commonInfo.relationToAnnuitantOther", "Other Relation")
    else:
        helper.enter_drop_down("Relation to Annuitant", 0, 0)
    helper.enter_drop_down("Gender", 0, 0)
    if (options["primary_beneficiary_type"] == "revocable"):
        helper.enter_drop_down("Beneficiary Type", 0, 0)
    else:
        helper.enter_drop_down("Beneficiary Type", 0, 1)
    helper.send_backspace_to_input("pendingBeneficiary.commonInfo.sharePercent")
    helper.enter_input("pendingBeneficiary.commonInfo.sharePercent", "100")
    if (options["primary_beneficiary_date_of_birth"] == "first of month at least 24 yrs ago"):
        helper.select_first_at_least_24yrs_ago_date_selector('//label[text()="Date of Birth"]/..//div//button', 0)
    else:
        helper.select_today_date_picker('//label[text()="Date of Birth"]/..//div//button', 0)
        time.sleep(2)
        helper.scroll_down_div_by_amt('//div[contains(@class, "overflow-auto")]', 200)
        if (options["primary_beneficiary_trustee_relation"] == "other option"):
            helper.enter_drop_down("Trustee Relation to Beneficiary", 0, 26)
            helper.enter_input("pendingBeneficiary.trusteeInfo.trusteeRelationToBeneficiaryOther", "Other Relation")
        else:
            helper.enter_drop_down("Trustee Relation to Beneficiary", 0, 0)
        helper.enter_input("pendingBeneficiary.trusteeInfo.trusteeFirstname", "newTest1")
        helper.enter_input("pendingBeneficiary.trusteeInfo.trusteeLastname", "newTest1")
    helper.click_next_btn()
    if (options["primary_beneficiary_type"] == "irrevocable"):
        confirmBtn = helper.wait_for_element_by_xpath('//button[text()="Confirm"]')
        helper.click_btn(confirmBtn)
    time.sleep(2)
    helper.click_next_btn()

def enter_secondary_beneficiary_info():
    helper.wait_for_next_btn()
    if (options["secondary_beneficiary_is_there"] == "yes"):
        helper.set_zoom(50)
        yesOptionBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="true"]')
        helper.click_btn(yesOptionBtn)

        helper.enter_input("pendingBeneficiary.commonInfo.firstName", "sbTest")
        helper.enter_input("pendingBeneficiary.commonInfo.lastName", "sbTest")
        if (options["secondary_beneficiary_relation_to_annutaint"] == "other option"):
            helper.enter_drop_down("Relation to Annuitant", 0, 26)
            helper.enter_input("pendingBeneficiary.commonInfo.relationToAnnuitantOther", "Other Relation")
        else:
            helper.enter_drop_down("Relation to Annuitant", 0, 0)
        helper.enter_drop_down("Gender", 0, 0)
        if (options["secondary_beneficiary_type"] == "revocable"):
            helper.enter_drop_down("Beneficiary Type", 0, 0)
        else:
            helper.enter_drop_down("Beneficiary Type", 0, 1)
        helper.send_backspace_to_input("pendingBeneficiary.commonInfo.sharePercent")
        helper.enter_input("pendingBeneficiary.commonInfo.sharePercent", "100")
        if (options["secondary_beneficiary_date_of_birth"] == "first of month at least 24 yrs ago"):
            helper.select_first_at_least_24yrs_ago_date_selector('//label[text()="Date of Birth"]/..//div//button', 0)
        else:
            helper.select_today_date_picker('//label[text()="Date of Birth"]/..//div//button', 0)
            time.sleep(2)
            if (options["secondary_beneficiary_trustee_relation"] == "other option"):
                helper.enter_drop_down("Trustee Relation to Beneficiary", 0, 26)
                helper.enter_input("pendingBeneficiary.trusteeInfo.trusteeRelationToBeneficiaryOther", "Other Relation")
            else:
                helper.enter_drop_down("Trustee Relation to Beneficiary", 0, 0)
            helper.enter_input("pendingBeneficiary.trusteeInfo.trusteeFirstname", "newTest1")
            helper.enter_input("pendingBeneficiary.trusteeInfo.trusteeLastname", "newTest1")
        helper.click_next_btn()
        if (options["secondary_beneficiary_type"] == "irrevocable"):
            confirmBtn = helper.wait_for_element_by_xpath('//button[text()="Confirm"]')
            helper.click_btn(confirmBtn)
        helper.set_zoom(100)
        time.sleep(2)
        helper.wait_for_next_btn()
    helper.click_next_btn()

def enter_successor_annuitant_info():
    helper.wait_for_next_btn()
    if (options["successor_annuitant_is_there"] == "yes"):
        yesOptionBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="item1"]')
        helper.click_btn(yesOptionBtn)
        helper.enter_input("successorAnnuitant.firstName", "saTest")
        helper.enter_input("successorAnnuitant.lastName", "saTest")
        helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
        homePhoneField = helper.wait_for_element_by_xpath('//label[text()="Home Phone"]/..//div//div//input[@type="tel"]')
        homePhoneField.send_keys("2222222222")
        helper.enter_drop_down("Language Preference", 0, 0)
        helper.select_today_date_picker('//label[text()="Date of Birth"]/..//div//button', 0)
        helper.enter_drop_down("Gender", 0, 0)
        helper.enter_input("successorAnnuitant.SIN", "782766182")
        helper.enter_drop_down("Relation to Annuitant", 0, 0)
    helper.click_next_btn()

def enter_successor_owner_info():
    helper.wait_for_next_btn()
    if (options["successor_owner_is_there"] == "yes"):
        yesOptionBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="item1"]')
        helper.click_btn(yesOptionBtn)
        helper.enter_input("successorOwner.firstName", "soTest")
        helper.enter_input("successorOwner.lastName", "soTest")
        helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-y-auto")]')
        homePhoneField = helper.wait_for_element_by_xpath('//label[text()="Home Phone"]/..//div//div//input[@type="tel"]')
        homePhoneField.send_keys("2222222222")
        helper.enter_drop_down("Language Preference", 0, 0)
        helper.select_today_date_picker('//label[text()="Date of Birth"]/..//div//button', 0)
        helper.enter_drop_down("Gender", 0, 0)
        helper.enter_input("successorOwner.SIN", "702495714")
        helper.enter_drop_down("Relation to Owner", 0, 0)
    helper.click_next_btn()

def enter_investor_profile_info():
    helper.wait_for_next_btn()
    if (options["investor_profile_score"] == "lower than 200"):
        helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-auto")]')
        helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-auto")]')
        fourthAOption = helper.wait_for_element_by_xpath('//label[contains(text(), "A. To generate income for today")]/..//button')
        helper.click_btn(fourthAOption)
        helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-auto")]')
        fifthAOption = helper.wait_for_element_by_xpath('//label[contains(text(), "A. To ensure that my portfolio remains secure")]/..//button')
        helper.click_btn(fifthAOption)
        helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-auto")]')
        sixthCOption = helper.wait_for_element_by_xpath('//label[contains(text(), "C. Between 4 and 5 years")]/..//button')
        helper.click_btn(sixthCOption)
        helper.no_proceed_app()
    if (options["personal_info_if_co_applicant"] == "yes"):
        helper.switch_to_co_applicant_section()
        if (options["investor_profile_co_score"] == "lower than 200"):
            helper.scroll_up_div_by_amt('//div[contains(@class, "overflow-auto")]', 2000)
            helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-auto")]')
            helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-auto")]')
            fourthAOption = helper.wait_for_element_by_xpath('//label[contains(text(), "E. To provide for my dependants")]/..//button')
            helper.click_btn(fourthAOption)
            helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-auto")]')
            fifthAOption = helper.wait_for_element_by_xpath('//label[contains(text(), "A. To ensure that my portfolio remains secure")]/..//button')
            helper.click_btn(fifthAOption)
            helper.scroll_down_div_by_pg_down('//div[contains(@class, "overflow-auto")]')
            sixthCOption = helper.wait_for_element_by_xpath('//label[contains(text(), "C. Between 4 and 5 years")]/..//button')
            helper.click_btn(sixthCOption)
            helper.no_proceed_app()
    helper.click_next_btn()

def enter_credit_report_info():
    helper.wait_for_next_btn()
    if (options["credit_report_score_at_least_700"] == "yes"):
        yesOptionBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="yes"]')
        helper.click_btn(yesOptionBtn)
        helper.upload_file_to_input(0)
    else:
        noOptionBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="no"]')
        helper.click_btn(noOptionBtn)
        helper.no_proceed_app()
    if (options["personal_info_if_co_applicant"] == "yes"):
        helper.switch_to_co_applicant_section()
        if (options["credit_report_co_score_at_least_700"] == "yes"):
            yesOptionBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="yes"]')
            helper.click_btn(yesOptionBtn)
            helper.upload_file_to_input(0)
        else:
            noOptionBtn = helper.wait_for_element_by_xpath('//button[@role="radio" and @value="no"]')
            helper.click_btn(noOptionBtn)
            helper.no_proceed_app()
    helper.click_next_btn()

def enter_feedback_info():
    helper.wait_for_next_btn()
    helper.enter_drop_down("How did you hear about us?", 0, 0)
    helper.enter_input("specialInstructions.heardDetail", "Searching around on google")
    helper.click_next_btn()

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
    enter_successor_annuitant_info()
    enter_successor_owner_info()
    enter_investor_profile_info()
    enter_credit_report_info()
    enter_feedback_info()
    time.sleep(10)
    helper.quit_browser()

async def main(options_data: dict[str, str]): # (yaml_file: str)
    global helper, options
    browser = webdriver.Chrome(options=Options().add_argument("--disable-autofill"))
    browser.maximize_window()
    browser.implicitly_wait(10)
    # options = load_application_options(yaml_file)
    options = options_data
    print(options)
    helper = SeleniumHelper(browser)
    # temp
    helper.set_zoom(80)
    send_verification_code()
    # temp
    helper.set_zoom(100)
    message = "@" # await get_verification_mail()
    if len(message) != 0:
       pre_application_steps(message)
       create_application()
    
if __name__ == "__main__":
    asyncio.run(main("new-quick-loan-various-routes-legacy.yaml"))