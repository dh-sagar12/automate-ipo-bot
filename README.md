# Automate Ipo Bot
This is the Bot  Written in Python to Automatically Apply for the IPO Offering in Meroshare with the help of Meroshare's internal APIs. It also Send you notifications in SMS after you complete the process.


## How to Use:

First of all, Create an **appsetting.json** file in the base Directory where the credential related to Meroshare is Present The format will Look like this 

    {
	    "credentials": [
		    {
		    "clientId": 190,
		    "username: "<your_user_name>", 
        "password": "<your_password>", 
        "demat": "<your_demat>", 
        "appliedKitta": "<applied_kitta>",
        "crnNumber": "<Your CRN>",
        "transactionPIN": "<YOur Pin>",
        "notificationNumber": "<YOur Number>"
		    }
		   ]
	}

You Can have Multiple Credential as a List and After that run the main.py file for the Process. 
Messaging API configurations are confidential and they are kept in the .env file 
.env in Base Directory Consists of the Following Credentials:
	

    BASEURL=<Meroshare Api Base Directory>
    TWILIO_ACCOUNT_SID=Can get after login in Twilio
    TWILIO_AUTH_TOKEN=Can get after login in Twilio
    TWILIO_SENDER_PHONE_NUMBER=Can get after login in Twilio

Thank you for using:
For more enquiry please contact to me in:
Twitter(Link In Bio)