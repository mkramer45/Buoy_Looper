import bs4
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen as uReq
import time
import datetime
import pandas as pd
# from datetime import datetime


wave_height_list = ['0.1 ft','0.2 ft','0.3 ft','0.4 ft','0.5 ft','0.6 ft','0.7 ft','0.8 ft','0.9 ft',
						'1.1 ft', '1.2 ft', '1.3 ft', '1.4 ft', '1.5 ft', '1.6 ft', '1.7 ft', '1.8 ft','1.9 ft',
						'2.0 ft','2.3 ft','2.4 ft','2.5 ft','2.6 ft','2.7 ft','2.8 ft','2.9 ft']


wave_interval_list = ['1 sec', '2 sec', '3 sec', '4 sec', '5 sec', '6 sec', '7 sec']


wind_direction_list = ["SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]


def loading_screens():
	# Loading Screens 
	print("\n")
	print("Hacking Weather Sensors...")
	print("\n")
	time.sleep(1)
	print("Retrieving Government Data...")
	print("\n")
	time.sleep(1)
	print("Decrypting Classified Documents...")
	print("\n")
	time.sleep(1)
	print("Initializing Data...")	
	print("\n")
	time.sleep(1)
	print("\n")

	print("-----Current Buoy Data for Boston Harbor:-----")
	time.sleep(1)
	print("\n")


def current_date_time():
	# Current Time 
	#Grab current date/time (24 hr format, includes seconds)
	current_time_AM_PM = datetime.datetime.now()
	#12-hour format
	current_time_sliced = current_time_AM_PM.strftime('%Y/%m/%d %I:%M%p')
	# separating Date from Time (DD/MM/YYY HH/MM)
	date_today = current_time_sliced.split(' ')
	date_ = date_today[0]
	time_ = date_today[1]
	# Removing first letter if it's '0', so it doesn't read as '08:07pm', etc
	if time_[0]=="0":
		time_ = time_[1:]

	print("Date:", date_)
	print("Current Time:", time_)
	print("Location: Boston Harbor")
	time.sleep(1)
	print("\n")



# This function retrieves the wave height
def surf_info_finder():
	#list of URLs to scrape from
	my_url = ['https://www.ndbc.noaa.gov/station_page.php?station=44013']

	for url in my_url:
	#initiating python's ability to parse URL
		uClient = uReq(url)
	# this will offload our content in'to a variable
		page_html = uClient.read()
	# closes our client
		uClient.close()
		page_soup = BeautifulSoup(page_html, "html.parser")
		return page_soup
		

def wave_height_printer():
	wave_height = surf_info_finder().find('td', string='Wave Height (WVHT):').find_next_sibling().get_text().strip()
	# print("Current Wave Height:", wave_height)
	# print(wave_height)
	return wave_height

def wave_interval_printer():
	wave_interval = surf_info_finder().find('td', string='Dominant Wave Period (DPD):').find_next_sibling().get_text().strip()
	# print(wave_interval)
	return wave_interval


def wind_direction_printer():
	wind_direction = surf_info_finder().find('td', string='Wind Direction (WDIR):').find_next_sibling().get_text().strip()
	wind_direction_abbreviated = wind_direction[:2]
	# print("Current Wind Direction:", wind_direction)
	# print(wind_direction_abbreviated)
	return wind_direction_abbreviated



def wind_speed_printer():
	wind_speed = surf_info_finder().find('td', string='Wind Speed (WSPD):').find_next_sibling().get_text().strip()
	# print(wind_speed)
	return wind_speed


def wind_speed_splicer():
	# wind_speed = surf_info_finder().find('td', string='Wind Speed (WSPD):').find_next_sibling().get_text().strip()
	#Wind Speed Splicing
	wind_speed_abbreviated = wind_speed_printer().split('.')
	# print(wind_speed_abbreviated)
	wind_speed_sliced = wind_speed_abbreviated[0]
	wind_speed_abbreviated_int = int(wind_speed_sliced)
	# print(wind_speed_abbreviated_int)
	return wind_speed_abbreviated_int


def air_temp_printer():
	air_temp = surf_info_finder().find('td', string='Air Temperature (ATMP):').find_next_sibling().get_text().strip()
	# print(air_temp)
	return air_temp

def water_temp_printer():
	water_temp = surf_info_finder().find('td', string='Water Temperature (WTMP):').find_next_sibling().get_text().strip()
	# print(water_temp)
	return water_temp


def forecast_logic():
	wave_height_ = wave_height_printer()
	wave_interval_ = wave_interval_printer()
	wind_direction_ = wind_direction_printer()
	air_temp_ = air_temp_printer()
	water_temp_ = water_temp_printer()
	wind_speed_spliced_ = wind_speed_splicer()

	# if wave_height_ not in wave_height_list:
	if wave_height_ not in wave_height_list and wave_interval_ not in wave_interval_list and wind_direction_ in wind_direction_list and wind_speed_spliced_ < 17:
		print("\n")
		print("-----Conclusion-----")
		print("Good Waves Right Now in Boston! Go out & Surf!")
		print("\n")
	else:
		print("\n")
		print("-----Conclusion-----")
		print("\n")
		print("Unfortunately, surf conditions in Boston are not good right now.")
		print("\n")


def tide_finder():
	# Using Pandas to parse through the html table found in the URL containing Tide Data
	tide_table = pd.read_html('https://www.tide-forecast.com/locations/Castle-Island-Boston-Harbor-Massachusetts/tides/latest')[0]

	tide_ = tide_table['Tide'].values

	time_date = tide_table['Time (EDT) & Date'].values

	for (t, i) in zip(tide_, time_date):
		time_date_sliced = i.split('(')
		time_ = time_date_sliced[0]
		date_ = time_date_sliced[1]

		#change the variable name so it makes it clear what we're printing :)
		tide_ = t
		print(tide_ + ':', time_)


def forecast_summary_printer():
	print("-----Wave Info: Boston Harbor-----")
	print("\n")
	print("Current Wave Height:", wave_height_printer())
	print("Current Wave Interval:", wave_interval_printer())
	print("Current Wind Direction:", wind_direction_printer())
	print("Current Air Temperature:", air_temp_printer())
	print("Current Water Temperature:", water_temp_printer())
	print("Current Wind Speed:", wind_speed_splicer())
	print("\n")
	print("-----Tide Info: Boston Harbor-----")
	print("\n")
	tide_finder()



# wave_height_printer()
# wave_interval_printer()
# wind_direction_printer()
# wind_speed_printer()
# air_temp_printer()
# water_temp_printer()
# wind_speed_splicer()
loading_screens()
current_date_time()
forecast_summary_printer()
forecast_logic()
