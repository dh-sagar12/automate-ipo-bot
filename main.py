

import json
from  Meroshare import Meroshare
import logging
import datetime
import requests
import notification


if __name__ == "__main__":

    # setting for logging 
    today = datetime.datetime.today().date()
    logging.basicConfig(filename=f"{today}.log", 
					format='%(asctime)s %(message)s', 
					filemode='a+') 
    logger=logging.getLogger() 
    logger.setLevel(logging.DEBUG) 



    try:
        logger.info("\nReading Configurations: Appsetting.json") 
        with open("appsetting.json") as config:
            configuration =  json.loads(config.read()).get('credentials')
            logger.info(f"Configurations Found: {len(configuration)}") 

    except FileNotFoundError:
        logger.error(f"FileNotFoundError: appsetting.json is not available in root directory") 
        


    if configuration is not None and len(configuration) >  0:
        
        for item in configuration:
            logger.info(f"Initializing MeroShare Instance For Username {item.get('username')} With Full Demat {item.get('demat')}")             

            meroshare_instance = Meroshare(clientId=item.get('clientId'), username=item.get('username'), password=item.get('password'))

            auth_token  =   meroshare_instance.authorize()

            if auth_token:
                meroshare_instance.get_bank_detial()
                meroshare_instance.set_apply_kitta_and_crn_related_data(boid= item.get('username'), appliedKitta=item.get('appliedKitta'), crnNumber= item.get('crnNumber'), transactionPIN=item.get('transactionPIN'), demat=item.get('demat'))
                available_ipos  =  meroshare_instance.get_available_ipo()
                
                if len(available_ipos) > 0 :
                    for ipo in available_ipos:
                        logger.info(f"IPO Applying For {ipo.get('companyName')}({ipo.get('scrip')})")

                        apply = meroshare_instance.apply_for_ipo(companyShareId =  ipo.get('companyShareId'))
                        if apply:
                            message_body =  f"Greeting!! IPO App Sent For BOID: {meroshare_instance.boid}, SCRIP: {ipo.get('scrip')}"
                            notification.SendNotificationMessage(cell_number=item.get('notificationNumber'), msg_body=message_body)
                        else:
                            message_body =  f"Greeting!! IPO App Failed For: {meroshare_instance.boid}, SCRIP: {ipo.get('scrip')}"
                            notification.SendNotificationMessage(cell_number=item.get('notificationNumber'), msg_body=message_body)
                else:
                    logger.info('No Script Available Right Now!!!')

    else:        
        logger.info('There Might Me a Configuration File Mistake Right Now!!!')

