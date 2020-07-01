#Arif Cengic June 25, 2020 for Systecon
import csv
import numpy as np
import datetime as dt
from collections import namedtuple
from matplotlib import pyplot as plt 
import os.path
import sys

# print (f' SKIPING histogram graphs')
# print (f' Run python {__file__} plot - TO DISPAY HISTOGRAM GRAPHS')

ITEM = 0
SYSTEM = 1
DATE = 2
REPAIR_TIME = 3
DATE_FORMAT = "%d-%m-%Y"
FLOAT_FORMAT = "{0:0.2f}"
FILE_NAME = "maintenance_data.csv"
# FILE_NAME = "toto.csv"

ANSWER_SEPARATOR = "\n*****************************************************\n"
ITEM_SEPARATOR =   "\n======================================================="
SYSTEM_SEPARATOR = "      -------------------------------------------------"
# Named Touple (Class) to store rows
Entry = namedtuple('Entry', 'item system date repair_time')


def process_maintenance_data():
	# All entries as list
	maint_data = [] 

	if not os.path.exists(FILE_NAME):
		print(f"Can not find file {FILE_NAME}. Make sure it is in application folder/directory")
		exit()

	with open(FILE_NAME) as f:

		for i, r in enumerate(csv.reader(f)):
			if i == 0:
				# Headers in first row
				# print(f"Headers {r}")
				pass
			else:
				row = Entry(r[ITEM], 
							r[SYSTEM], 
							dt.datetime.strptime(r[DATE],"%m/%d/%Y"),
							float(r[REPAIR_TIME]))
				maint_data.append(row)
	# End of File Read
		
	# We will get required data using maint_data list and NUMPY 
	print(ANSWER_SEPARATOR)
	print("1. number of observations, and minimum and maximum values \n")
	print(f"Total records {len(maint_data)} ")

	items = np.unique(np.array([[x.item for x in maint_data]]))
	print(f"Total Items {len(items)} ")

	dates = [x.date for x in maint_data]
	min_dt = min(dates).strftime(DATE_FORMAT)
	max_dt = max(dates).strftime(DATE_FORMAT)
	print(f"Date Min:{min_dt}  Max:{max_dt}")

	times = [x.repair_time for x in maint_data]
	print(f"Repair time Min:{min(times)}  Max:{max(times)}")
	print(ITEM_SEPARATOR)
	for it in items:
		item_data = list( filter(lambda x: x.item == it, maint_data))
		
		dates = [x.date for x in item_data]
		print(" ")
		print(f"Item {it} Total Records {len(dates)}")
		min_dt = min(dates).strftime(DATE_FORMAT)
		max_dt = max(dates).strftime(DATE_FORMAT)
		print(f"Date Min:{min_dt}  Max:{max_dt}")

		times = [x.repair_time for x in item_data]
		print(f"Repair Min:{min(times)}  Max:{max(times)}")

		systems = np.unique(np.array([[x.system for x in item_data]]))
		print(f"Total Systems {len(systems)} ")
		print(ITEM_SEPARATOR)

		for s in systems:
			system_data = list( filter(lambda x: x.system == s, item_data))
			dates = [x.date for x in system_data]
			min_dt = min(dates).strftime(DATE_FORMAT)
			max_dt = max(dates).strftime(DATE_FORMAT)
			print(f"      {s} Total {len(dates)}")
			print(f"      {s} Date Min:{min_dt}  Max:{max_dt}")

			times = [x.repair_time for x in system_data]
			print(f"      {s} Repair Min:{min(times)}  Max:{max(times)}")
			print(SYSTEM_SEPARATOR)

	print(ANSWER_SEPARATOR)
	print("2. Calculate the mean repair time for each item. \n")
	for it in items:
		item_data = list( filter(lambda x: x.item == it, maint_data))
		repairs = [x.repair_time for x in item_data]
		mean_repair_time = FLOAT_FORMAT.format(np.mean(repairs))
		print(f"Item {it} Mean Repair Time {mean_repair_time}")
		
	
	print(ANSWER_SEPARATOR)
	print("3. Calculate the failures per hour for each item and system combination.")
	print("4. Generate time between failures for each item and system ??? Combination ???.\n ")
	for it in items:
		item_data = list(filter(lambda x: x.item == it, maint_data))
		for s in systems:
			system_data = list(filter(lambda x: x.system == s, item_data))
			dates = [x.date for x in system_data]
			ts = max(dates) - min(dates)
			hours = ts.days * 24
			# fail_per_hour number too small to display 
			# hours = hours/96 
			fail_per_hour = FLOAT_FORMAT.format(len(dates)/hours)
			print(f"      {it}-{s} Failure Per Hour {fail_per_hour}")
			
			dates.sort()
			interarrival = []
			for i in range(1,len(dates)):
				time_span = dates[i] - dates[i-1]
				interarrival.append(time_span.days)
			
			avg_interarrival = FLOAT_FORMAT.format(np.average(interarrival))
			print(f"      {it}-{s} Interarrival Avg {avg_interarrival}")
			print(SYSTEM_SEPARATOR)

	print(ANSWER_SEPARATOR)
	print("5. Create a histogram of the interarrival times for a single item \n")
	for it in items:
		item_data = list( filter(lambda x: x.item == it, maint_data))
		dates = [x.date for x in item_data]
		
		interarrival = []
		dates.sort()
		for i in range(1,len(dates)):
			time_span = dates[i] - dates[i-1]
			interarrival.append(time_span.days)
		print(f"Histogram Item {it} Total Repairs {len(dates)}")

		if (len(sys.argv) > 1):
			plt.hist(interarrival, 10)
			plt.xlabel('Repairs')
			plt.ylabel('Time Between Repairs - Days')
			plt.title(f"Histogram Item {it} Total Repairs {len(dates)}")
			plt.show()

		
def update_info(info, dr):
	info.min_date = min(dr.date, info.min_date)
	info.max_date = max(dr.date, info.max_date)
	info.min_time = min(dr.time, info.min_time)
	info.max_time = max(dr.time, info.max_time)
	info.count += 1

def alt_faster_one_pass_solution_w_dicts():
	# This soultion will pass through data once
	# and calculate all values min-max etc per Item,Syste, Item-System
	# It doesn't use numpy and should be more efficient
	# but code would be more complicated

	MIN = 0
	MAX = 1
	DateRepair = namedtuple('DateRepair', 'date time')
	# Info = namedtuple('Info', 'min_date max_date min_time max_time count')
	class Info:
		def __init__(self, min_date, max_date, min_time, max_time, count):
			self.min_date = min_date
			self.max_date = max_date
			self.min_time = min_time
			self.max_time = max_time
			self.count = count
	
	# Dict Item - system_repair string - {}
	item_systems = {}
	# Dict  string - []
	system_repair = {}

	total_info = None
	item_info = {}
	item_system_info = {}

	with open('maintenance_data.csv') as f:
		csv_reader = csv.reader(f)
		for i, r in enumerate(csv_reader):
			if i == 0:
				print(f"Headers {r}")
			else:
				item, system = r[ITEM], r[SYSTEM]
				date, repair_time = r[DATE], r[REPAIR_TIME]
				
				dr = DateRepair(dt.datetime.strptime(date,"%m/%d/%Y"),
								float(repair_time))

				if item not in item_systems:
					item_systems[item] = {}

				if system not in item_systems[item]:
					item_systems[item][system] = []
				
				item_systems[item][system].append(dr)

				#Keep running score of min & max for date and repair_time
				if total_info is None:
					total_info = Info(dr.date, dr.date, dr.time, dr.time, 1)
				else:
					update_info(total_info, dr)

				if item not in item_info:
					item_info[item] =  Info(dr.date, dr.date, dr.time, dr.time, 1)
				else:
					update_info(item_info[item], dr)
				
				if item not in item_system_info:
					item_system_info[item] = {} # dict for system-info
				
				if  system not in item_system_info[item]:
					item_system_info[item][system] = Info(dr.date, dr.date, dr.time, dr.time, 1)
				else:
					update_info(item_system_info[item][system], dr)
					
				
#End of File Read
	print(ANSWER_SEPARATOR)
	print("1. number of observations, and minimum and maximum values \n")
	print(f"Total records {total_info.count} ")
	min_dt = total_info.min_date.strftime(DATE_FORMAT)
	max_dt = total_info.max_date.strftime(DATE_FORMAT)
	print(f"Date   Min:{min_dt}  Max:{max_dt}")
	print(f"Repair Min:{total_info.min_time}  Max:{total_info.max_time}")

	print(ITEM_SEPARATOR)
	for it, info in item_info.items():
		
		print(f"Item {it} Total Records {info.count}")
		min_dt = info.min_date.strftime(DATE_FORMAT)
		max_dt = info.max_date.strftime(DATE_FORMAT)
		print(f"Date   Min:{min_dt}  Max:{max_dt}")
		print(f"Repair Min:{info.min_time}  Max:{info.max_time}")

		print(f"Total Systems {len(item_system_info[it])} ")
		print(ITEM_SEPARATOR)

		for s, info in item_system_info[it].items():
			print(f"      {s} Total {info.count}")
			print(f"      {s} Date   Min:{info.min_date}  Max:{info.max_date}")
			print(f"      {s} Repair Min:{info.min_time}  Max:{info.max_time}")
			print(SYSTEM_SEPARATOR)
	
	print(ANSWER_SEPARATOR)
	print("2. Calculate the mean repair time for each item. \n")
	
	for it, systems in item_systems.items():
		repairs = []
		for s, arr in systems.items():
			repair_times = [x.time for x in arr]
			repairs.extend(repair_times) 

		mean_repair_time = FLOAT_FORMAT.format(np.mean(repairs))
		print(f"Item {it} Mean Repair Time {mean_repair_time}")

	print(ANSWER_SEPARATOR)
	print("3. Calculate the failures per hour for each item and system combination.")
	print("4. Generate time between failures for each item and system ??? Combination ???.\n ")
	for it, systems in item_systems.items():
		for s, arr in systems.items():
			ts = item_system_info[it][s].max_date - item_system_info[it][s].min_date
			hours = ts.days * 24
			# fail_per_hour number too small to display 
			# hours = hours/96 
			fail_per_hour = FLOAT_FORMAT.format(len(arr)/hours)
			print(f"      {it}-{s} Failure Per Hour {fail_per_hour}")
			
			dates = [x.date for x in arr]
			dates.sort()
			interarrival = []
			for i in range(1,len(dates)):
				time_span = dates[i] - dates[i-1]
				interarrival.append(time_span.days)
			
			avg_interarrival = FLOAT_FORMAT.format(np.average(interarrival))
			print(f"      {it}-{s} Interarrival Avg {avg_interarrival}")
			print(SYSTEM_SEPARATOR)
	
	print("5. Create a histogram of the interarrival times for a single item \n")
	for it, systems in item_systems.items():
		item_repairs = [] 
		for s, arr in systems.items():
			item_repairs.extend(arr)
			
		dates = [x.date for x in item_repairs]
		dates.sort()
		interarrival = []
		for i in range(1,len(dates)):
			time_span = dates[i] - dates[i-1]
			interarrival.append(time_span.days)

		print(f"Histogram Item {it} Total Repairs {len(dates)}")

if __name__ == "__main__":
	
	a = dt.datetime.now()
	alt_faster_one_pass_solution_w_dicts()
	b = dt.datetime.now()
	print()
	print(f" First  {b-a}")

	a1 = dt.datetime.now()
	process_maintenance_data()
	b1 = dt.datetime.now()
	print()
	print(f" Second {b1-a1}")
	
	print (f'INFO Run python  {__file__} plot - TO DISPAY HISTOGRAM GRAPHS')
