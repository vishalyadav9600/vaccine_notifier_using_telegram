import requests

import time
import datetime
from datetime import datetime
base_cowin_url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=512&date=10-07-2021"
now=datetime.now()
today_date=now.strftime("%d-%m-%Y")
api_url_telegram="https://api.telegram.org/bot1806972352:AAHto0z4nO12aijcRBammLvDCoABo9stdB0/sendMessage?chat_id=@__groupid__&text="
group_id="Ghaziabad_Sputnik_Alerts"
delhi_districts_ids = [651]
def fetch_data_from_cowin(district_id):
	query_params="?district_id={}&date={}".format(district_id, today_date)
	headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
	final_url=base_cowin_url+query_params
	response=requests.get(final_url, headers=headers)
	extract_availability_data(response)
	#print(response.text)

def fetch_data_for_state(district_ids):
	for district_id in district_ids:
		fetch_data_from_cowin(district_id)
def extract_availability_data(response):
	response_json=response.json()
	for center in response_json["centers"]:
		for session in center["sessions"]:
			if session["available_capacity_dose1"] >= 0 and session["min_age_limit"]==18 and session["vaccine"]=="SPUTNIK V":
				message ="Pincode: {}, Name: {}, Slots: {}, Minimum Age: {}".format(
					center["pincode"], center["name"], 
					session["available_capacity_dose1"],
					session["min_age_limit"])
				send_message_telegram(message)
def send_message_telegram(message):
	final_telegram_url=api_url_telegram.replace("__groupid__", group_id)
	final_telegram_url=final_telegram_url+message
	response=requests.get(final_telegram_url)
	print(response)
if __name__ =="__main__":
	fetch_data_for_state(delhi_districts_ids)