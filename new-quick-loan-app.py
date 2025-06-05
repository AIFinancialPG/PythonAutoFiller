import streamlit as st
import asyncio
from newQuickLoanScript import main

st.title("New Quick-Loan Application")

# Personal Info Section
st.header("Personal Info")
personal_info_pref_name = st.text_input("Preferred Name")
personal_info_country_of_birth = st.selectbox("Country of Birth", ["us", "canada"])
if personal_info_country_of_birth != "canada":
    personal_info_resi_since = st.selectbox("Residing Since", ["first of month", "today"])
personal_info_citizenship = st.selectbox("Citizenship", ["us", "canada"])
personal_info_if_co_applicant = st.selectbox("Is there a co-applicant?", ["yes", "no"])
if personal_info_if_co_applicant == "yes":
    personal_info_co_pref_name = st.text_input("Co-applicant Preferred Name")
    personal_info_co_country_of_birth = st.selectbox("Co-applicant Country of Birth", ["us", "canada"])
    if personal_info_co_country_of_birth != "canada":
        personal_info_co_resi_since = st.selectbox("Co-applicant Residing Since", ["first of month", "today"])
    personal_info_co_citizenship = st.selectbox("Co-applicant Citizenship", ["us", "canada"])

# Contact Info Section
st.header("Contact Info")
contact_info_search_for_cur_address = st.selectbox("Search for current address?", ["yes", "no"])
if contact_info_search_for_cur_address == "no":
    contact_info_cur_province = st.selectbox("Current Province", ["valid", "invalid"])
    if contact_info_cur_province == "invalid":
        st.error("Cannot proceed with invalid province.")
contact_info_cur_living_since = st.selectbox("Living since", ["first of month", "today", "first of month at least 12 yrs ago"])
if contact_info_cur_living_since != "first of month at least 12 yrs ago":
    contact_info_search_for_prev_address = st.selectbox("Search for previous address?", ["yes", "no"])
    if contact_info_search_for_prev_address == "no":
        contact_info_prev_province = st.selectbox("Previous Province", ["valid", "invalid"])
        if contact_info_prev_province == "invalid":
            st.error("Cannot proceed with invalid previous province.")
    contact_info_prev_living_since = st.selectbox("Previous Living Since", ["first of month", "today"])
if personal_info_if_co_applicant == "yes":
    contact_info_co_applicant_same_address = st.selectbox("Co-applicant same address?", ["yes", "no"])
    if contact_info_co_applicant_same_address == "no":
        contact_info_co_search_for_cur_address = st.selectbox("Co-applicant search for current address?", ["yes", "no"])
        if contact_info_co_search_for_cur_address == "no":
            contact_info_co_cur_province = st.selectbox("Co-applicant Current Province", ["valid", "invalid"])
            if contact_info_co_cur_province == "invalid":
                st.error("Cannot proceed with invalid co-applicant province.")
        contact_info_co_cur_living_since = st.selectbox("Co-applicant Living since", ["first of month", "today", "first of month at least 12 yrs ago"])
        if contact_info_co_cur_living_since != "first of month at least 12 yrs ago":
            contact_info_co_search_for_prev_address = st.selectbox("Co-applicant search for previous address?", ["yes", "no"])
            if contact_info_co_search_for_prev_address == "no":
                contact_info_co_prev_province = st.selectbox("Co-applicant Previous Province", ["valid", "invalid"])
                if contact_info_co_prev_province == "invalid":
                    st.error("Cannot proceed with invalid co-applicant previous province.")
            contact_info_co_prev_living_since = st.selectbox("Co-applicant Previous Living Since", ["first of month", "today"])

# ID Info Section
st.header("ID Info")
id_info_id1_type = st.selectbox("ID 1 Type", ["citizenship card", "other"])
id_info_id1_issue_date = st.selectbox("ID 1 Issue Date", ["first of month", "today"])
if id_info_id1_type == "other":
    id_info_id1_expiry_date = st.selectbox("ID 1 Expiry Date", ["today"])
id_info_id2_type_options = ["other"] if id_info_id1_type == "citizenship card" else ["citizenship card", "other"]
id_info_id2_type = st.selectbox("ID 2 Type", id_info_id2_type_options)
id_info_id2_issue_date = st.selectbox("ID 2 Issue Date", ["first of month", "today"])
if id_info_id1_type == "other":
    id_info_id2_expiry_date = st.selectbox("ID 2 Expiry Date", ["today"])
id_info_in_person_verify = st.selectbox("In-person verification?", ["yes", "no"])
if id_info_in_person_verify == "no":
    id_info_id_verify_doc_type = st.selectbox("Verification Document Type", ["other option", "other"])
    id_info_id_verify_doc_date = st.selectbox("Verification Document Date", ["first of month", "today"])
if personal_info_if_co_applicant == "yes":
    id_info_co_id1_type = st.selectbox("Co-applicant ID 1 Type", ["citizenship card", "other"])
    id_info_co_id1_issue_date = st.selectbox("Co-applicant ID 1 Issue Date", ["first of month", "today"])
    if id_info_co_id1_type == "other":
        id_info_co_id1_expiry_date = st.selectbox("Co-applicant ID 1 Expiry Date", ["today"])
    id_info_co_id2_type_options = ["other"] if id_info_co_id1_type == "citizenship card" else ["citizenship card", "other"]
    id_info_co_id2_type = st.selectbox("Co-applicant ID 2 Type", id_info_co_id2_type_options)
    id_info_co_id2_issue_date = st.selectbox("Co-applicant ID 2 Issue Date", ["first of month", "today"])
    if id_info_co_id1_type == "other":
        id_info_co_id2_expiry_date = st.selectbox("Co-applicant ID 2 Expiry Date", ["today"])
    id_info_co_in_person_verify = st.selectbox("Co-applicant in-person verification?", ["yes", "no"])
    if id_info_co_in_person_verify == "no":
        id_info_co_id_verify_doc_type = st.selectbox("Co-applicant Verification Document Type", ["other option", "other"])
        id_info_co_id_verify_doc_date = st.selectbox("Co-applicant Verification Document Date", ["first of month", "today"])

# Tax Status Info Section
st.header("Tax Status Info")
tax_status_info_tax_resi_of_canada = st.selectbox("Tax resident of Canada?", ["yes", "no"])
if tax_status_info_tax_resi_of_canada == "no":
    st.error("Cannot proceed if not a tax resident of Canada.")
tax_status_info_us_resi = st.selectbox("US resident?", ["yes", "no"])
if tax_status_info_us_resi == "yes":
    tax_status_info_tin_from_us = st.selectbox("TIN from US?", ["yes", "no"])
    if tax_status_info_tin_from_us == "no":
        tax_status_info_reason_for_no_tin = st.selectbox("Reason for no US TIN", ["apply", "other"])
tax_status_info_other_region = st.selectbox("Resident of other region?", ["yes", "no"])
if tax_status_info_other_region == "yes":
    tax_status_info_tin_from_other = st.selectbox("TIN from other region?", ["yes", "no"])
    if tax_status_info_tin_from_other == "no":
        tax_status_info_reason_for_no_other_tin = st.selectbox("Reason for no other TIN", ["apply", "other"])
if personal_info_if_co_applicant == "yes":
    tax_status_info_co_tax_resi_of_canada = st.selectbox("Co-applicant tax resident of Canada?", ["yes", "no"])
    if tax_status_info_co_tax_resi_of_canada == "no":
        st.error("Cannot proceed if co-applicant is not a tax resident of Canada.")
    tax_status_info_co_us_resi = st.selectbox("Co-applicant US resident?", ["yes", "no"])
    if tax_status_info_co_us_resi == "yes":
        tax_status_info_co_tin_from_us = st.selectbox("Co-applicant TIN from US?", ["yes", "no"])
        if tax_status_info_co_tin_from_us == "no":
            tax_status_info_co_reason_for_no_tin = st.selectbox("Co-applicant reason for no US TIN", ["apply", "other"])
    tax_status_info_co_other_region = st.selectbox("Co-applicant resident of other region?", ["yes", "no"])
    if tax_status_info_co_other_region == "yes":
        tax_status_info_co_tin_from_other = st.selectbox("Co-applicant TIN from other region?", ["yes", "no"])
        if tax_status_info_co_tin_from_other == "no":
            tax_status_info_co_reason_for_no_other_tin = st.selectbox("Co-applicant reason for no other TIN", ["apply", "other"])

# Employment Info Section
st.header("Employment Info")
emp_info_status = st.selectbox("Employment Status", ["employed", "other"])
if emp_info_status != "employed":
    st.error("Cannot proceed if not employed.")
if personal_info_if_co_applicant == "yes":
    emp_info_co_status = st.selectbox("Co-applicant Employment Status", ["employed", "other"])
    if emp_info_co_status != "employed":
        st.error("Cannot proceed if co-applicant is not employed.")

# Source of Contribution Section
st.header("Source of Contribution")
source_of_contri_info_new_loan = st.selectbox("New loan?", ["yes", "no"])

# Contribution Option Section
st.header("Contribution Option")
contri_option_requires_more_than_one_sign = st.selectbox("Requires more than one signature?", ["yes", "no"])

# Policy Guarantee Level Section
st.header("Policy Guarantee Level")
policy_guarantee_level = st.selectbox("Policy Guarantee Level", ["75/75", "75/100", "100/100"])

# Residential Status Section
st.header("Residential Status")
resi_status_info_main_applicant_resi = st.selectbox("Main Applicant Residential Status", ["own home", "rented home", "live with parents", "others"])
if personal_info_if_co_applicant == "yes":
    resi_status_info_co_applicant_resi_options = {
        "own home": ["own home", "others"],
        "rented home": ["rented home"],
        "live with parents": ["live with parents"],
        "others": ["own home", "others"]
    }.get(resi_status_info_main_applicant_resi, ["own home", "rented home", "live with parents", "others"])
    resi_status_info_co_applicant_resi = st.selectbox("Co-applicant Residential Status", resi_status_info_co_applicant_resi_options)
if resi_status_info_main_applicant_resi == "own home" or (personal_info_if_co_applicant == "yes" and resi_status_info_co_applicant_resi == "own home"):
    owner_options = ["both"] if resi_status_info_main_applicant_resi == "own home" and resi_status_info_co_applicant_resi == "own home" else (
        ["applicant", "both"] if resi_status_info_main_applicant_resi == "own home" else ["co applicant", "both"])
    resi_status_info_owner_of_home = st.selectbox("Owner of Home", owner_options)
    resi_status_info_is_mortgage = st.selectbox("Is there a mortgage?", ["yes", "no"])
    resi_status_info_is_maintenance_fee = st.selectbox("Is there a maintenance fee?", ["yes", "no"])

# Canadian Real-Estate Question Section
st.header("Canadian Real-Estate Question")
cad_real_estate_is_canadian_resi = st.selectbox("Canadian resident?", ["yes", "no"])
if cad_real_estate_is_canadian_resi == "yes":
    if personal_info_if_co_applicant == "yes":
        cad_real_estate_owner_of_home = st.selectbox("Owner of Canadian Home", ["applicant", "co applicant", "both"])
    else:
        cad_real_estate_owner_of_home = st.selectbox("Owner of Canadian Home", ["applicant"])
    cad_real_estate_is_mortgage = st.selectbox("Is there a mortgage on Canadian property?", ["yes", "no"])
    cad_real_estate_is_maintenance_fee = st.selectbox("Is there a maintenance fee on Canadian property?", ["yes", "no"])

# Financial Analysis Section
st.header("Financial Analysis")
fin_analysis_add_lib_owner_options = ["applicant"] if personal_info_if_co_applicant == "no" else ["applicant", "co applicant", "both"]
fin_analysis_add_lib_owner = st.selectbox("Liability Owner", fin_analysis_add_lib_owner_options)
fin_analysis_add_lib_liability_type = st.selectbox("Liability Type", ["mortgage", "rent", "other debts", "other"])
if fin_analysis_add_lib_liability_type == "mortgage":
    fin_analysis_add_lib_no_mortgage = st.selectbox("No mortgage?", ["yes", "no"])
    fin_analysis_add_lib_no_mortgage_maintain_fee = st.selectbox("No mortgage maintenance fee?", ["yes", "no"])
fin_analysis_add_asset_owner = st.selectbox("Asset Owner", fin_analysis_add_lib_owner_options)
fin_analysis_add_asset_asset_type = st.selectbox("Asset Type", ["real estate", "other assets", "other"])
fin_analysis_add_income_owner = st.selectbox("Income Owner", fin_analysis_add_lib_owner_options)
fin_analysis_add_income_income_type = st.selectbox("Income Type", ["employment", "other income", "other"])
if fin_analysis_add_income_income_type == "employment":
    fin_analysis_add_income_search_for_cur_emp_address = st.selectbox("Search for current employment address?", ["yes", "no"])
    fin_analysis_add_income_cur_serving_since = st.selectbox("Serving since", ["today", "first of month at least 12 yrs ago"])
    if fin_analysis_add_income_cur_serving_since == "today":
        fin_analysis_add_income_search_for_prev_emp_address = st.selectbox("Search for previous employment address?", ["yes", "no"])

# Primary Beneficiary Info Section
st.header("Primary Beneficiary Info")
primary_beneficiary_type = st.selectbox("Primary Beneficiary Type", ["revocable", "irrevocable"])
primary_beneficiary_date_of_birth = st.selectbox("Primary Beneficiary Date of Birth", ["today", "first of month at least 24 yrs ago"])
primary_beneficiary_relation_to_annutaint = st.selectbox("Relation to Annuitant", ["other option", "other"])
primary_beneficiary_trustee_relation = st.selectbox("Trustee Relation", ["other option", "other"])

# Secondary Beneficiary Info Section
st.header("Secondary Beneficiary Info")
secondary_beneficiary_is_there = st.selectbox("Is there a secondary beneficiary?", ["yes", "no"])
if secondary_beneficiary_is_there == "yes":
    secondary_beneficiary_type = st.selectbox("Secondary Beneficiary Type", ["revocable", "irrevocable"])
    secondary_beneficiary_date_of_birth = st.selectbox("Secondary Beneficiary Date of Birth", ["today", "first of month at least 24 yrs ago"])
secondary_beneficiary_relation_to_annutaint = st.selectbox("Secondary Relation to Annuitant", ["other option", "other"])
secondary_beneficiary_trustee_relation = st.selectbox("Secondary Trustee Relation", ["other option", "other"])

# Successor Annuitant Info Section
st.header("Successor Annuitant Info")
successor_annuitant_is_there = st.selectbox("Is there a successor annuitant?", ["yes", "no"])

# Successor Owner Info Section
st.header("Successor Owner Info")
successor_owner_is_there = st.selectbox("Is there a successor owner?", ["yes", "no"])

# Investor Profile Info Section
st.header("Investor Profile Info")
investor_profile_score = st.selectbox("Investor Profile Score", ["lower than 200", "equal or more than 200"])
if investor_profile_score == "lower than 200":
    st.error("Cannot proceed if investor profile score is lower than 200.")
if personal_info_if_co_applicant == "yes":
    investor_profile_co_score = st.selectbox("Co-applicant Investor Profile Score", ["lower than 200", "equal or more than 200"])
    if investor_profile_co_score == "lower than 200":
        st.error("Cannot proceed if co-applicant investor profile score is lower than 200.")

# Credit Report Info Section
st.header("Credit Report Info")
credit_report_score_at_least_700 = st.selectbox("Credit score at least 700?", ["yes", "no"])
if credit_report_score_at_least_700 == "no":
    st.error("Cannot proceed if credit score is not at least 700.")
if personal_info_if_co_applicant == "yes":
    credit_report_co_score_at_least_700 = st.selectbox("Co-applicant credit score at least 700?", ["yes", "no"])
    if credit_report_co_score_at_least_700 == "no":
        st.error("Cannot proceed if co-applicant credit score is not at least 700.")

# Submit and Generate YAML
if st.button("Submit"):
    data = {}
    data["personal_info_pref_name"] = personal_info_pref_name
    data["personal_info_country_of_birth"] = personal_info_country_of_birth
    if personal_info_country_of_birth != "canada":
        data["personal_info_resi_since"] = personal_info_resi_since
    data["personal_info_citizenship"] = personal_info_citizenship
    data["personal_info_if_co_applicant"] = personal_info_if_co_applicant
    if personal_info_if_co_applicant == "yes":
        data["personal_info_co_pref_name"] = personal_info_co_pref_name
        data["personal_info_co_country_of_birth"] = personal_info_co_country_of_birth
        if personal_info_co_country_of_birth != "canada":
            data["personal_info_co_resi_since"] = personal_info_co_resi_since
        data["personal_info_co_citizenship"] = personal_info_co_citizenship

    data["contact_info_search_for_cur_address"] = contact_info_search_for_cur_address
    if contact_info_search_for_cur_address == "no":
        data["contact_info_cur_province"] = contact_info_cur_province
    data["contact_info_cur_living_since"] = contact_info_cur_living_since
    if contact_info_cur_living_since != "first of month at least 12 yrs ago":
        data["contact_info_search_for_prev_address"] = contact_info_search_for_prev_address
        if contact_info_search_for_prev_address == "no":
            data["contact_info_prev_province"] = contact_info_prev_province
        data["contact_info_prev_living_since"] = contact_info_prev_living_since
    if personal_info_if_co_applicant == "yes":
        data["contact_info_co_applicant_same_address"] = contact_info_co_applicant_same_address
        if contact_info_co_applicant_same_address == "no":
            data["contact_info_co_search_for_cur_address"] = contact_info_co_search_for_cur_address
            if contact_info_co_search_for_cur_address == "no":
                data["contact_info_co_cur_province"] = contact_info_co_cur_province
            data["contact_comments_info_co_cur_living_since"] = contact_info_co_cur_living_since
            if contact_info_co_cur_living_since != "first of month at least 12 yrs ago":
                data["contact_info_co_search_for_prev_address"] = contact_info_co_search_for_prev_address
                if contact_info_co_search_for_prev_address == "no":
                    data["contact_info_co_prev_province"] = contact_info_co_prev_province
                data["contact_info_co_prev_living_since"] = contact_info_co_prev_living_since

    data["id_info_id1_type"] = id_info_id1_type
    data["id_info_id1_issue_date"] = id_info_id1_issue_date
    if id_info_id1_type == "other":
        data["id_info_id1_expiry_date"] = id_info_id1_expiry_date
    data["id_info_id2_type"] = id_info_id2_type
    data["id_info_id2_issue_date"] = id_info_id2_issue_date
    if id_info_id1_type == "other":
        data["id_info_id2_expiry_date"] = id_info_id2_expiry_date
    data["id_info_in_person_verify"] = id_info_in_person_verify
    if id_info_in_person_verify == "no":
        data["id_info_id_verify_doc_type"] = id_info_id_verify_doc_type
        data["id_info_id_verify_doc_date"] = id_info_id_verify_doc_date
    if personal_info_if_co_applicant == "yes":
        data["id_info_co_id1_type"] = id_info_co_id1_type
        data["id_info_co_id1_issue_date"] = id_info_co_id1_issue_date
        if id_info_co_id1_type == "other":
            data["id_info_co_id1_expiry_date"] = id_info_co_id1_expiry_date
        data["id_info_co_id2_type"] = id_info_co_id2_type
        data["id_info_co_id2_issue_date"] = id_info_co_id2_issue_date
        if id_info_co_id1_type == "other":
            data["id_info_co_id2_expiry_date"] = id_info_co_id2_expiry_date
        data["id_info_co_in_person_verify"] = id_info_co_in_person_verify
        if id_info_co_in_person_verify == "no":
            data["id_info_co_id_verify_doc_type"] = id_info_co_id_verify_doc_type
            data["id_info_co_id_verify_doc_date"] = id_info_co_id_verify_doc_date

    data["tax_status_info_tax_resi_of_canada"] = tax_status_info_tax_resi_of_canada
    data["tax_status_info_us_resi"] = tax_status_info_us_resi
    if tax_status_info_us_resi == "yes":
        data["tax_status_info_tin_from_us"] = tax_status_info_tin_from_us
        if tax_status_info_tin_from_us == "no":
            data["tax_status_info_reason_for_no_tin"] = tax_status_info_reason_for_no_tin
    data["tax_status_info_other_region"] = tax_status_info_other_region
    if tax_status_info_other_region == "yes":
        data["tax_status_info_tin_from_other"] = tax_status_info_tin_from_other
        if tax_status_info_tin_from_other == "no":
            data["tax_status_info_reason_for_no_other_tin"] = tax_status_info_reason_for_no_other_tin
    if personal_info_if_co_applicant == "yes":
        data["tax_status_info_co_tax_resi_of_canada"] = tax_status_info_co_tax_resi_of_canada
        data["tax_status_info_co_us_resi"] = tax_status_info_co_us_resi
        if tax_status_info_co_us_resi == "yes":
            data["tax_status_info_co_tin_from_us"] = tax_status_info_co_tin_from_us
            if tax_status_info_co_tin_from_us == "no":
                data["tax_status_info_co_reason_for_no_tin"] = tax_status_info_co_reason_for_no_tin
        data["tax_status_info_co_other_region"] = tax_status_info_co_other_region
        if tax_status_info_co_other_region == "yes":
            data["tax_status_info_co_tin_from_other"] = tax_status_info_co_tin_from_other
            if tax_status_info_co_tin_from_other == "no":
                data["tax_status_info_co_reason_for_no_other_tin"] = tax_status_info_co_reason_for_no_other_tin

    data["emp_info_status"] = emp_info_status
    if personal_info_if_co_applicant == "yes":
        data["emp_info_co_status"] = emp_info_co_status

    data["source_of_contri_info_new_loan"] = source_of_contri_info_new_loan
    data["contri_option_requires_more_than_one_sign"] = contri_option_requires_more_than_one_sign
    data["policy_guarantee_level"] = policy_guarantee_level

    data["resi_status_info_main_applicant_resi"] = resi_status_info_main_applicant_resi
    if personal_info_if_co_applicant == "yes":
        data["resi_status_info_co_applicant_resi"] = resi_status_info_co_applicant_resi
    if resi_status_info_main_applicant_resi == "own home" or (personal_info_if_co_applicant == "yes" and resi_status_info_co_applicant_resi == "own home"):
        data["resi_status_info_owner_of_home"] = resi_status_info_owner_of_home
        data["resi_status_info_is_mortgage"] = resi_status_info_is_mortgage
        data["resi_status_info_is_maintenance_fee"] = resi_status_info_is_maintenance_fee

    data["cad_real_estate_is_canadian_resi"] = cad_real_estate_is_canadian_resi
    if cad_real_estate_is_canadian_resi == "yes":
        data["cad_real_estate_owner_of_home"] = cad_real_estate_owner_of_home
        data["cad_real_estate_is_mortgage"] = cad_real_estate_is_mortgage
        data["cad_real_estate_is_maintenance_fee"] = cad_real_estate_is_maintenance_fee

    data["fin_analysis_add_lib_owner"] = fin_analysis_add_lib_owner
    data["fin_analysis_add_lib_liability_type"] = fin_analysis_add_lib_liability_type
    if fin_analysis_add_lib_liability_type == "mortgage":
        data["fin_analysis_add_lib_no_mortgage"] = fin_analysis_add_lib_no_mortgage
        data["fin_analysis_add_lib_no_mortgage_maintain_fee"] = fin_analysis_add_lib_no_mortgage_maintain_fee
    data["fin_analysis_add_asset_owner"] = fin_analysis_add_asset_owner
    data["fin_analysis_add_asset_asset_type"] = fin_analysis_add_asset_asset_type
    data["fin_analysis_add_income_owner"] = fin_analysis_add_income_owner
    data["fin_analysis_add_income_income_type"] = fin_analysis_add_income_income_type
    if fin_analysis_add_income_income_type == "employment":
        data["fin_analysis_add_income_search_for_cur_emp_address"] = fin_analysis_add_income_search_for_cur_emp_address
        data["fin_analysis_add_income_cur_serving_since"] = fin_analysis_add_income_cur_serving_since
        if fin_analysis_add_income_cur_serving_since == "today":
            data["fin_analysis_add_income_search_for_prev_emp_address"] = fin_analysis_add_income_search_for_prev_emp_address

    data["primary_beneficiary_type"] = primary_beneficiary_type
    data["primary_beneficiary_date_of_birth"] = primary_beneficiary_date_of_birth
    data["primary_beneficiary_relation_to_annutaint"] = primary_beneficiary_relation_to_annutaint
    data["primary_beneficiary_trustee_relation"] = primary_beneficiary_trustee_relation

    data["secondary_beneficiary_is_there"] = secondary_beneficiary_is_there
    if secondary_beneficiary_is_there == "yes":
        data["secondary_beneficiary_type"] = secondary_beneficiary_type
        data["secondary_beneficiary_date_of_birth"] = secondary_beneficiary_date_of_birth
    data["secondary_beneficiary_relation_to_annutaint"] = secondary_beneficiary_relation_to_annutaint
    data["secondary_beneficiary_trustee_relation"] = secondary_beneficiary_trustee_relation

    data["successor_annuitant_is_there"] = successor_annuitant_is_there
    data["successor_owner_is_there"] = successor_owner_is_there

    data["investor_profile_score"] = investor_profile_score
    if personal_info_if_co_applicant == "yes":
        data["investor_profile_co_score"] = investor_profile_co_score

    data["credit_report_score_at_least_700"] = credit_report_score_at_least_700
    if personal_info_if_co_applicant == "yes":
        data["credit_report_co_score_at_least_700"] = credit_report_co_score_at_least_700

    asyncio.run(main(data))

    # yaml_content = yaml.dump(data, default_flow_style=False)
    # st.download_button("Download YAML", yaml_content, "application.yaml", "text/yaml")
