# ATDBquery: modules to query ATDB for survey status (ARTS or imaging)
# V.A. Moss 16/01/2019 (vmoss.astro@gmail.com)

__author__ = "V.A. Moss"
__date__ = "$16-jan-2019 17:00:00$"
__version__ = "0.1"

import os
import sys
import requests
import json

###################################################################
# Query the ATDB database

def query_database(obs_mode,failures,transient):

	# Define the list of valid statuses:
	valid_statuses = "ingesting,valid,completed,completing,archived,removed,on%20hold,removed%20(manual)"

	# Define the URL for query
	if failures:
		url = 'http://atdb.astron.nl/atdb/observations/?observing_mode__icontains=%s' % (obs_mode)
	elif transient:
		url = 'http://atdb.astron.nl/atdb/observations/?observing_mode__icontains=imaging&my_status__in=ingesting,valid,completing' 
	else:
		url = 'http://atdb.astron.nl/atdb/observations/?my_status__in=%s&observing_mode__icontains=%s' % (valid_statuses,obs_mode)

	# First, determine how many results there are
	# Do the query
	try: 
		response = requests.get(url)
		response.raise_for_status() # This uses the requests library to determine if the URL response is bad or not
	except Exception as e:
		print(e)
		sys.exit()	

	# Can only do 100 per page
	result_num = json.loads(response.text)['count']
	print('Total number of results found in ATDB for %s: %s' % (obs_mode.upper(),result_num))
	
	# Deal with the edge effect 
	if result_num % 100 != 0:
		pagenum = result_num // 100 + 1
	else:
		pagenum = result_num // 100		

	# Define the observation dictionary
	# Get only the field_name,field_ra,field_dec,status
	obs_list = []

	for page in range(1,pagenum+1):

		# Add page to URL
		#url = url + '&page=%s' % (page)

		# Do the query
		try: 
			response = requests.get(url, params=dict(page=page))
			response.raise_for_status() # This uses the requests library to determine if the URL response is bad or not
		except Exception as e:
			print(e)
			sys.exit()

		# Parse the data
		try: 
			metadata = response.json()['results']
		except:
			print(response.text)
			continue

		# Return all information
		for i in range(0,len(metadata)):
			obs_list.append(metadata[i])

		# # Loop
		# for i in range(0,len(metadata)):
		# 	obs = metadata[i]
		# 	name = obs['field_name']
		# 	tid = obs['taskID']
		# 	ra = obs['field_ra']
		# 	dec = obs['field_dec']
		# 	status = obs['my_status']

		# 	obs_dict[tid] = {'field_name':name, 'field_ra':ra, 'field_dec':dec, 'status':status}

	return obs_list