#Arif Cengic June 25, 2020 for Systecon
import csv
import numpy as np
import datetime as dt
from collections import namedtuple
from matplotlib import pyplot as plt 
import os.path
import sys

print (f' SKIPING histogram graphs')
print (f' Run python homework1.py plot - TO DISPAY HISTOGRAM GRAPHS')

ITEM = 0
SYSTEM = 1
DATE = 2
REPAIR_TIME = 3
DATE_FORMAT = "%d-%m-%Y"
FLOAT_FORMAT = "{0:0.2f}"
FILE_NAME = "maintenance_data.csv"
ANSWER_SEPARATOR = "\n*****************************************************\n"
ITEM_SEPARATOR =   "=======================================================\n"
SYSTEM_SEPARATOR = "      -------------------------------------------------"
# Named Touple (Class) to store rows
Entry = namedtuple('Entry', 'item system date repair_time')

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
		print(f"      {it}-{s} Total {len(dates)}")
		print(f"      {it}-{s} Date Min:{min_dt}  Max:{max_dt}")

		times = [x.repair_time for x in system_data]
		print(f"      {it}-{s} Repair Min:{min(times)}  Max:{max(times)}")
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
	item_data = list( filter(lambda x: x.item == it, maint_data))
	for s in systems:
		system_data = list( filter(lambda x: x.system == s, item_data))
		dates = [x.date for x in system_data]
		ts = max(dates) - min(dates)
		hours = ts.days * 24
		# fail_per_hour Number too small to display
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

print()
print()
print (f'INFO Run python homework1.py plot - TO DISPAY HISTOGRAM GRAPHS')
	

def alt_faster_one_pass_solution_w_dicts():
	# This soultion will pass through data once
	# and calculate all values min-max etc per Item,Syste, Item-System
	# It doesn't use numpy and should be more efficient
	# but code would be more complicated
	
	MIN = 0
	MAX = 1
	DateRepair = namedtuple('DateRepair', 'date repair_time')
	# Dict w all data Item-System-Entry
	item_systems = {}
	# Dict of item - min and max date  
	item_date_mm = {}
	# Dict of item - min and max repair
	item_repair_mm = {}
	with open('maintenance_data.csv') as f:
		csv_reader = csv.reader(f)
		for i, r in enumerate(csv_reader):
			if i == 0:
				print(f"Headers {r}")
			else:
				row = Entry(r[ITEM], 
							r[SYSTEM], 
							dt.datetime.strptime(r[DATE],"%m/%d/%Y"),
							float(r[REPAIR_TIME]))
				maint_data.append(row)
				if row.item not in item_systems:
					item_systems[row.item] = {}
				if row.system not in item_systems[row.item].values():
					item_systems[row.item][row.system] = []
				
				if row.item not in item_date_mm:
					item_date_mm[row.item] = [row.date, row.date]
				if row.item not in item_repair_mm:
					item_repair_mm[row.item] = [row.repair_time, row.repair_time]
				item_systems[row.item][row.system].append(DateRepair(row.date, row.repair_time))
				
				#Keep runuing score of min & max for date and repair_time
				item_date_mm[row.item][MIN] = min((row.date, item_date_mm[row.item][MIN]))
				item_date_mm[row.item][MAX] = max((row.date, item_date_mm[row.item][MAX]))

				item_repair_mm[row.item][MIN] = min((row.repair_time, item_repair_mm[row.item][MIN]))
				item_repair_mm[row.item][MAX] = max((row.repair_time, item_repair_mm[row.item][MAX]))
#End of File Read
	
	

	

	
