from dotenv import load_dotenv
import os
import requests
import json
import logging

load_dotenv()


base_url = os.environ['BASEURL']
logger = logging.getLogger()

applicable_issue_payload = {
    "filterFieldParams": [
        {
            "key": "companyIssue.companyISIN.script",
            "alias": "Scrip"
        },
        {
            "key": "companyIssue.companyISIN.company.name",
            "alias": "Company Name"
        },
        {
            "key": "companyIssue.assignedToClient.name",
            "value": "",
            "alias": "Issue Manager"
        }
    ],
    "page": 1,
    "size": 100,
    "searchRoleViewConstants": "VIEW_APPLICABLE_SHARE",
    "filterDateParams": [
        {
            "key": "minIssueOpenDate",
            "condition": "",
            "alias": "",
            "value": ""
        },
        {
            "key": "maxIssueCloseDate",
            "condition": "",
            "alias": "",
            "value": ""
        }
    ]
}


class Meroshare():

    def __init__(self, clientId, username, password):
        self.clientId = clientId
        self.username = username
        self.password = password
        self.auth_token = None
        self.demat = None
        self.boid = None
        self.accountNumber = None
        self.customerId = None
        self.accountBranchId = None
        self.appliedKitta = None
        self.companyShareId = None
        self.bankId = None

    def set_auth_toke(self, token):
        self.auth_token = token

    def set_apply_kitta_and_crn_related_data(self, appliedKitta, crnNumber, transactionPIN, demat, boid):
        self.appliedKitta = appliedKitta
        self.crnNumber = crnNumber
        self.transactionPIN = transactionPIN
        self.demat = demat
        self.boid = boid

    def authorize(self):
        payload = {
            'username': self.__dict__.get('username'),
            'clientId': self.__dict__.get('clientId'),
            'password': self.__dict__.get('password'),
        }

        try:
            logger.info("Attempting MeroShare Authorization...")
            response = requests.post(
                f'{base_url}/auth/', json=payload)
            print(response.status_code)

        except Exception as e:

            # logging
            logger.error(
                f'Error : {e} WHILE :Attempting MeroShare Authorization')

        if response.headers.get('Authorization') is not None:

            # logging
            logger.info(
                f"Authorization successful : Generated Token :")

            # setter method for auth token
            self.set_auth_toke(response.headers.get('Authorization'))

            return True
        else:
            # logging
            logger.error('Authorization Failed Unable to generate token!!!!')
            return False

    def get_bank_detial(self):
        try:
            logger.info("Attempting Getting Bank Details")
            response = requests.get(f'{base_url}/bank/', headers={
                'Authorization': self.auth_token
            })
            data = response.json()
            self.bankId = data[0]['id']

            bank_detail_response = requests.get(f'{base_url}/bank/{self.bankId}', headers={
                'Authorization': self.auth_token
            })
            bank_data = bank_detail_response.json()
            logger.info("Bank Details Retrived ....")

            self.accountNumber = bank_data['accountNumber']
            self.customerId = bank_data['id']
            self.accountBranchId = bank_data['accountBranchId']

        except Exception as e:
            # logging
            logger.error(
                f'Error : {e} WHILE : Attempting Getting Bank Details...')

    def get_available_ipo(self):
        try:
            logger.info("Getting Available IPOs List....")
            response = requests.post(
                f'{base_url}/companyShare/applicableIssue/', json=applicable_issue_payload, headers={
                    'Authorization': self.auth_token
                })

            response_data = list(filter(lambda x: x.get('shareTypeName') == 'IPO' and x.get(
                'shareGroupName') == 'Ordinary Shares' and x.get('action') is None,  response.json().get('object')))
            logger.info(
                f"Available IPOs Retrived : Count {len(response_data)}...")
            return response_data

        except Exception as e:
            logger.error(f'Error : {e} WHILE : Getting Available IPOs List')
            return None

    def apply_for_ipo(self, companyShareId):
        self.companyShareId = companyShareId
        print(self.__dict__)
        request_data = {
            "demat": self.__dict__.get('demat'),
            "boid":self.__dict__.get('boid'),
            "accountNumber": self.__dict__.get('accountNumber'),
            "customerId": self.__dict__.get('customerId'),
            "accountBranchId": self.__dict__.get('accountBranchId'),
            "appliedKitta": self.__dict__.get('appliedKitta'),
            "crnNumber": self.__dict__.get('crnNumber'),
            "transactionPIN": self.__dict__.get('transactionPIN'), 
            "companyShareId": self.__dict__.get('companyShareId'),
            "bankId": self.__dict__.get('bankId')
        }
        print(request_data)
        logger.info(f"Payload Ready for DEMAT: {self.__dict__.get('demat')}. COMPANY: {self.__dict__.get('companyShareId')} ")
        
        try:
            logger.info(f"Applying for IPO: COMPANY ID: {request_data.get('companyShareId')} ...")
            # response = requests.post(
            #     f'{base_url}/applicantForm/share/apply/', json=request_data, headers={
            #         'Authorization': self.auth_token
            #     })
            # if response.status_code == 200:
            #     logger.info(f'IPO  Application Submiited successfuly with Status code 200 For Bank Verification...')
            #     return True
            # else:
            #     logger.info(f'IPO  Application Failed with Status Code: {response.status_code}')
            #     return False

            return True
            

        except Exception as e:
            # logging
            logger.error(
                f'Error : {e} WHILE :Applying For IPO...')
            return False


    def __str__(self) -> str:
        self.username
