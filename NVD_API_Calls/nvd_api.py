"""
I was told in an interview that part of my job would be to make an API call, grab newly published CVEs,
and somehow find a way to calculate a CVSS score using a CVSS calculator

Fortunately, toolswatch on GitHub made a wonderful cvss calculator. I have written code that makes an API call to NVD
(NIST's National Vulnerability Database). This code will then write the returned json in pretty format, and
write an Excel sheet that has the original relevant data.

It will then use toolswatch's code to calculate it, then write a new Excel sheet with the newly calculated scores

Big shoutout to toolswatch and their code: https://github.com/toolswatch/pycvss3

Dependencies: openpyxl, art

Seido Karasaki(yakitategohan on github)
v1 04/22/2023
"""

from requests import get
from datetime import datetime, timedelta
from openpyxl import Workbook
from os import mkdir
from art import tprint
from toolswatch_code.pycvss3 import CVSS3
from toolswatch_code import *
import json


def cve_list_today():
    # Yesterday's date using datetime
    date_today = datetime.today()
    date_yesterday = str((date_today - timedelta(days=1)).strftime('%Y-%m-%d'))
    beginning_of_yesterday = f'{date_yesterday}T00:00:00.000'
    end_of_yesterday = f'{date_yesterday}T23:59:59.999'

    # API key from NVD
    api_key = ''

    # Submit URL, include date and times in url
    cve_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0/?' \
              f'pubStartDate={beginning_of_yesterday}&pubEndDate={end_of_yesterday}'
    submit_headers = {
        'x-apiKey': api_key
    }
    submit_response = get(cve_url, headers=submit_headers)
    return submit_response


def separate_cves(response):
    # Make sure API call was valid
    if str(response.status_code) == '200':

        # Separate json list by vulnerabilities. Meat of the response
        cve_list = response.json()['vulnerabilities']

        # Yesterday's date again
        date_today = datetime.today()
        date_yesterday = str((date_today - timedelta(days=1)).strftime('%Y-%m-%d'))

        # Tell user how many vulnerabilities were written yesterday
        print(f'There are a total of {response.json()["totalResults"]} CVEs from {date_yesterday}')

        # Write raw json format to file
        try:
            mkdir(f"{date_yesterday}")
        except FileExistsError:
            print('Directory already exists.')

        file_name = f"./{date_yesterday}/{date_yesterday}.txt"
        with open(file_name, "w") as f:
            parsed = json.loads(response.text)
            f.write(json.dumps(parsed, indent=4))
            f.close()
        return cve_list

    else:
        print('Invalid response from API call')


def cve_to_exel(response):
    # Yesterday's date again
    date_today = datetime.today()
    date_yesterday = str((date_today - timedelta(days=1)).strftime('%Y-%m-%d'))

    # Make exel file with yesterday's name as file name
    workbook = Workbook()
    sheet = workbook.active

    # Column values
    sheet['A1'] = 'Number'
    sheet['B1'] = 'ID'
    sheet['C1'] = 'Description'
    sheet['D1'] = 'CVSS Vector String'
    sheet['E1'] = 'Attack Vector'
    sheet['F1'] = 'Attack Complexity'
    sheet['G1'] = 'Privileges Required'
    sheet['H1'] = 'User Interaction'
    sheet['I1'] = 'Scope'
    sheet['J1'] = 'Confidentiality Impact'
    sheet['K1'] = 'Integrity Impact'
    sheet['L1'] = 'Availability Impact'
    sheet['M1'] = 'Base Score'
    sheet['N1'] = 'Base Severity'
    sheet['O1'] = 'Exploitability Score'
    sheet['P1'] = 'Impact Score'
    sheet['Q1'] = 'CWE'

    # Write CVE values. See raw json file in folder for references!
    index_of_cve_json = 0
    excel_cve_number = 1
    skip_metrics = False

    for num in range(2, int(response.json()["totalResults"] + 2)):

        # CVSS Metric versions may vary. Temporary way to grab the first one
        try:
            cvss_val = list(response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'].keys())[0]
        except IndexError:
            skip_metrics = True
        sheet[f'A{num}'] = excel_cve_number
        sheet[f'B{num}'] = \
            response.json()['vulnerabilities'][index_of_cve_json]['cve']['id']
        sheet[f'C{num}'] = \
            response.json()['vulnerabilities'][index_of_cve_json]['cve']['descriptions'][0]['value']
        if not skip_metrics:
            sheet[f'D{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'][cvss_val][0]['cvssData'][
                    'vectorString']
            sheet[f'E{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'][cvss_val][0]['cvssData'][
                    'attackVector']
            sheet[f'F{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'][cvss_val][0]['cvssData'][
                    'attackComplexity']
            sheet[f'G{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'][cvss_val][0]['cvssData'][
                    'privilegesRequired']
            sheet[f'H{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'][cvss_val][0]['cvssData'][
                    'userInteraction']
            sheet[f'I{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'][cvss_val][0]['cvssData'][
                    'scope']
            sheet[f'J{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'][cvss_val][0]['cvssData'][
                    'confidentialityImpact']
            sheet[f'K{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'][cvss_val][0]['cvssData'][
                    'integrityImpact']
            sheet[f'L{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'][cvss_val][0]['cvssData'][
                    'availabilityImpact']
            sheet[f'M{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'][cvss_val][0]['cvssData'][
                    'baseScore']
            sheet[f'N{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'][cvss_val][0]['cvssData'][
                    'baseSeverity']
            sheet[f'O{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'][cvss_val][0][
                    'exploitabilityScore']
            sheet[f'P{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'][cvss_val][0][
                    'impactScore']

        # Weaknesses may not exist
        try:
            sheet[f'Q{num}'] = \
                response.json()['vulnerabilities'][index_of_cve_json]['cve']['weaknesses'][0]["description"][0][
                    'value']
        except KeyError:
            pass
        index_of_cve_json += 1
        excel_cve_number += 1
        skip_metrics = False
    try:
        workbook.save(f"{date_yesterday}/{date_yesterday}.xlsx")
    except PermissionError:
        print('Excel file has already been written')


def calculate_our_cves(response):
    # Yesterday's date again
    date_today = datetime.today()
    date_yesterday = str((date_today - timedelta(days=1)).strftime('%Y-%m-%d'))

    # Make exel file with yesterday's name as file name
    workbook = Workbook()
    sheet = workbook.active

    # Column values
    sheet['A1'] = 'Number'
    sheet['B1'] = 'ID'
    sheet['C1'] = 'Description'
    sheet['D1'] = 'CVSS Vector String'
    sheet['E1'] = 'Exploit Code Maturity (E)'
    sheet['F1'] = 'Remediation Level (RL)'
    sheet['G1'] = 'Report Confidence (RC)'
    sheet['H1'] = 'Attack Vector (MAV)'
    sheet['I1'] = 'Attack Complexity (MAC)'
    sheet['J1'] = 'Privileges Required (MPR)'
    sheet['K1'] = 'User Interaction (MUI)'
    sheet['L1'] = 'Scope (MS)'
    sheet['M1'] = 'Confidentiality Impact (MC)'
    sheet['N1'] = 'Integrity Impact (MI)'
    sheet['O1'] = 'Availability Impact (MA)'
    sheet['P1'] = 'Confidentiality Requirement (CR)'
    sheet['Q1'] = 'Integrity Requirement (IR)'
    sheet['R1'] = 'Availability Requirement (AR)'
    sheet['S1'] = 'Recalculated Vector'
    sheet['T1'] = 'CVSS Base Score'
    sheet['U1'] = 'CVSS Temporal Score'
    sheet['V1'] = 'CVSS Environmental Score'

    # Write CVE values. See raw json file in folder for references!
    index_of_cve_json = 0
    excel_cve_number = 1

    for num in range(2, int(response.json()["totalResults"] + 2)):

        # CVSS Metric versions may vary. Temporary way to grab the first one
        # Check is to give user opportunity to redo CVSS calculator if they need to
        check = True
        try:
            while check:
                cvss_val = list(response.json()['vulnerabilities'][index_of_cve_json]['cve']['metrics'].keys())[0]
                print(f"\nThis is CVE {response.json()['vulnerabilities'][index_of_cve_json]['cve']['id']}. "
                      f"The description is the following:\n"
                      f"{response.json()['vulnerabilities'][index_of_cve_json]['cve']['descriptions'][0]['value']}")
                sheet[f'A{num}'] = excel_cve_number
                sheet[f'B{num}'] = \
                    response.json()['vulnerabilities'][index_of_cve_json]['cve']['id']
                sheet[f'C{num}'] = \
                    response.json()['vulnerabilities'][index_of_cve_json]['cve']['descriptions'][0]['value']

                # Store vector string for future use
                original_vector_string = response.json()['vulnerabilities'][index_of_cve_json][
                    'cve']['metrics'][cvss_val][0]['cvssData']['vectorString']
                sheet[f'D{num}'] = original_vector_string

                # Now take user inputs for CVE calculations. Temporal Score Metrics
                # Exploit Code Maturity
                print('TEMPORAL SCORE METRICS')
                exploit_code_maturity = input(
                    '\nEnter Exploit Code Maturity (E).\n'
                    'X:Not Defined, U:Unproven that exploit exists, P:Proof of Concept Code, F:Functional '
                    'exploit exists, H: High\n').upper()
                while exploit_code_maturity not in 'XUPFH':
                    exploit_code_maturity = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, U:Unproven that exploit exists, P:Proof of Concept Code, F:Functional '
                        'exploit exists, H: High\n').upper()
                sheet[f'E{num}'] = exploit_code_maturity

                # Remediation Level
                remediation_level = input(
                    '\nEnter Remediation Level (RL).\n'
                    'X:Not Defined, O:Official Fix, T:Temporary Fix, W:Workaround, '
                    'U: Unavailable\n').upper()
                while remediation_level not in 'XOTWU':
                    remediation_level = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, O:Official Fix, T:Temporary Fix, W:Workaround, '
                        'U: Unavailable\n').upper()
                sheet[f'F{num}'] = remediation_level

                # Report Confidence
                report_confidence = input(
                    '\nEnter Report Confidence (RC).\n'
                    'X:Not Defined, U:Unknown, R:Reasonable, C:Confirmed\n').upper()
                while report_confidence not in 'XURC':
                    report_confidence = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, U:Unknown, R:Reasonable, C:Confirmed\n').upper()
                sheet[f'G{num}'] = report_confidence

                # Environmental Score Metrics
                # Exploitability Metrics:
                # Attack Vector
                print('ENVIRONMENTAL SCORE METRICS')
                print('-EXPLOITABILITY METRICS-')
                attack_vector = input(
                    '\nEnter Attack Vector (MAV).\n'
                    'X:Not Defined, N:Network, A:Adjacent Network, L:Local, P:Physical\n').upper()
                while attack_vector not in 'XNALP':
                    attack_vector = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, N:Network, A:Adjacent Network, L:Local, P:Physical\n').upper()
                sheet[f'H{num}'] = attack_vector

                # Attack Complexity
                attack_complexity = input(
                    '\nEnter Attack Complexity (MAC).\n'
                    'X:Not Defined, L:Low, H:High\n').upper()
                while attack_complexity not in 'XLH':
                    attack_complexity = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, L:Low, H:High\n').upper()
                sheet[f'I{num}'] = attack_complexity

                # Privileges Required
                privileges_required = input(
                    '\nEnter Privileges Required (MPR).\n'
                    'X:Not Defined, N:None, L:Low, H:High\n').upper()
                while privileges_required not in 'XNLH':
                    privileges_required = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, N:None, L:Low, H:High\n').upper()
                sheet[f'J{num}'] = privileges_required

                # User Interaction
                user_interaction = input(
                    '\nEnter User Interaction (MUI).\n'
                    'X:Not Defined, N:None, R:Required\n').upper()
                while user_interaction not in 'XNR':
                    user_interaction = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, N:None, R:Required\n').upper()
                sheet[f'K{num}'] = user_interaction

                # Scope
                scope = input(
                    '\nEnter Scope (MS).\n'
                    'X:Not Defined, U:Unchanged, C:Changed\n').upper()
                while scope not in 'XUC':
                    scope = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, U:Unchanged, C:Changed\n').upper()
                sheet[f'L{num}'] = scope

                # IMPACT METRICS
                print('-IMPACT METRICS-')

                # Confidentiality Impact
                confidentiality_impact = input(
                    '\nEnter Confidentiality Impact (MC).\n'
                    'X:Not Defined, N:None, L:Low, H:High\n').upper()
                while confidentiality_impact not in 'XNLH':
                    confidentiality_impact = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, N:None, L:Low, H:High\n').upper()

                sheet[f'M{num}'] = confidentiality_impact

                # Integrity Impact
                integrity_impact = input(
                    '\nEnter Integrity Impact (MI).\n'
                    'X:Not Defined, N:None, L:Low, H:High\n').upper()
                while integrity_impact not in 'XNLH':
                    integrity_impact = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, N:None, L:Low, H:High\n').upper()
                sheet[f'N{num}'] = integrity_impact

                # Availability Impact
                availability_impact = input(
                    '\nEnter Availability Impact (MC).\n'
                    'X:Not Defined, N:None, L:Low, H:High\n').upper()
                while availability_impact not in 'XNLH':
                    availability_impact = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, N:None, L:Low, H:High\n').upper()
                sheet[f'O{num}'] = availability_impact

                # IMPACT SUBSCORE MODIFIERS
                print('-IMPACT SUBSCORE MODIFIERS-')

                # Confidentiality Requirement
                confidentiality_requirement = input(
                    '\nEnter Confidentiality Requirement (CR).\n'
                    'X:Not Defined, L:Low, M:Medium, H:High\n').upper()
                while confidentiality_requirement not in 'XLMH':
                    confidentiality_requirement = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, L:Low, M:Medium, H:High\n').upper()
                sheet[f'P{num}'] = confidentiality_requirement

                # Integrity Requirement
                integrity_requirement = input(
                    '\nEnter Integrity Requirement (IR).\n'
                    'X:Not Defined, L:Low, M:Medium, H:High\n').upper()
                while integrity_requirement not in 'XLMH':
                    integrity_requirement = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, L:Low, M:Medium, H:High\n').upper()
                sheet[f'Q{num}'] = integrity_requirement

                # Availability Requierment
                availability_requirement = input(
                    '\nEnter Availability Requirement (AR).\n'
                    'X:Not Defined, L:Low, M:Medium, H:High\n').upper()
                while availability_requirement not in 'XLMH':
                    availability_requirement = input(
                        '\nPlease enter valid code.\n'
                        'X:Not Defined, L:Low, M:Medium, H:High\n').upper()
                sheet[f'R{num}'] = availability_requirement

                print('Your ')
                index_of_cve_json += 1
                excel_cve_number += 1

                # Total recalculated vector
                recalculated_vector = f'{original_vector_string}/' \
                                      f'E:{exploit_code_maturity}/RL:{remediation_level}/RC:{report_confidence}/' \
                                      f'CR:{confidentiality_requirement}/IR:{integrity_requirement}/' \
                                      f'AR:{availability_requirement}/MAV:{attack_vector}/MAC:{attack_complexity}/' \
                                      f'MPR:{privileges_required}/MUI:{user_interaction}/MS:{scope}/' \
                                      f'MC:{confidentiality_impact}/MI:{integrity_impact}/MA:{availability_impact}'
                cvss3 = CVSS3(recalculated_vector)
                (cvss_base_score, cvss_base_risk) = cvss3.cvss_base_score()
                (cvss_temporal_score, cvss_temporal_risk) = cvss3.cvss_temporal_score()
                (cvss_environmental_score, cvss_environmental_risk) = cvss3.cvss_environmental_score()
                print("CVSS v3 vector:", recalculated_vector)
                print("\tCVSS v3 Base Score:", cvss_base_score)
                print("\tCVSS v3 Temporal Score:", cvss_temporal_score)
                print("\tCVSS 3 Environmental Score:", cvss_environmental_score)
                check_user_input = input('Does this sound correct? (y/n): ')
                if check_user_input[0].lower() == 'y':
                    check = False
                    sheet[f'S{num}'] = recalculated_vector
                    sheet[f'T{num}'] = cvss_base_score
                    sheet[f'U{num}'] = cvss_temporal_score
                    sheet[f'V{num}'] = cvss_environmental_score
                else:
                    check = True

        # Unlike original excel, will skip if no metrics
        except IndexError:
            pass
    try:
        # Write Key
        sheet[f'A{num + 5}'] = 'A:Adjacent Network\n' \
                               'C:Confirmed or C:Changed\n' \
                               'F:Functional exploit exists\n' \
                               'H:High\n' \
                               'L:Local or L:Low\n' \
                               'M:Medium\n' \
                               'N:Network or N:None\n' \
                               'O:Official Fix\n' \
                               'P:Proof of Concept Code or P:Physical\n' \
                               'R:Reasonable or R:Required\n' \
                               'T:Temporary Fix\n' \
                               'U:Unproven that exploit exists or U:Unavailable or U:Unchanged\n' \
                               'W:Workaround\n' \
                               'X:Not Defined\n'

        workbook.save(f"{date_yesterday}/{date_yesterday}_calculated_scores.xlsx")
    except PermissionError:
        print('Excel file has already been written')


if __name__ == '__main__':
    tprint('CVSS    CALCULATOR')
    print('\n\n********WRITTEN BY SEIDO KARASAKI********\n\n')
    print('\n\n********CVSS CALCULATOR CODE BY TOOLSWATCH********\n\n')
    cve_list_from_today = cve_list_today()
    print('[+]\tWriting raw json file in pretty format...')
    separate_cves(cve_list_from_today)
    print('\n[+]\tWriting API response to excel...')
    cve_to_exel(cve_list_from_today)
    print('Done...')
    print('\n[+]\tPlease Calculate CVSS Scores...')
    calculate_our_cves(cve_list_from_today)
