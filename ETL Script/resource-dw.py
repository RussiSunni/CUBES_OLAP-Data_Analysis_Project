import os
import json
import urllib.request
import mysql.connector
from mysql.connector import Error
import datetime
import requests
import csv


# set up connection to target database --------------------

# Cloud SQL db

# mydb = mysql.connector.connect(
#   host="***",
#   user="***",
#   passwd="***",
#   database="***"
# )

# db_Info = mydb.get_server_info()
# print("Connected to MySQL Server version ", db_Info)


# local db - home

mydb = mysql.connector.connect(
  host="***",
  user="***",
  passwd="***",
  database="***"
)

# local db - work

# mydb = mysql.connector.connect(
#   host="***",
#   user="***",
#   passwd="***",
#   database="***"
# )


mycursor = mydb.cursor()


# import dates from CSV

csv_data = csv.reader(open('C:\Users\Jonathan\Desktop\Cubes\cubes-master\examples\hello_world\Update data\date.csv'))
for row in csv_data:

    mycursor.execute('INSERT IGNORE INTO dim_date(id, db_date, year, month, day, quarter, week, day_name, month_name, holiday_flag, weekend_flag, event)'
          'VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")',
          row)
# close the connection to the database.
mycursor.close()
print("Done")


# Harvest authorization ------------------------------

headers = {
    "User-Agent": "***",
    "Authorization": "***",
    "Harvest-Account-ID": "***"
}

# to print in Python console ---------------------
print(json.dumps(jsonResponse["time_entries"], sort_keys=True, indent=4))


# populate date table from json file

file = os.path.abspath('/home/JonathanDyason/data') + "/date.json"
json_data = open(file).read()
json_obj = json.loads(json_data)

# do validation and checks before insert


def validate_string(val):
   if val != None:
        if type(val) is int:
            # for x in val:
            #   print(x)
            return str(val).encode('utf-8')
        else:
            return val


# parse json data to SQL insert
for i, item in enumerate(json_obj):
    id = validate_string(item.get("id", None))
    db_date = validate_string(item.get("db_date", None))
    year = validate_string(item.get("year", None))
    month = validate_string(item.get("month", None))
    day = validate_string(item.get("day", None))
    quarter = validate_string(item.get("quarter", None))
    week = validate_string(item.get("week", None))
    day_name = validate_string(item.get("day_name", None))
    month_name = validate_string(item.get("month_name", None))
    holiday_flag = validate_string(item.get("holiday_flag", None))
    weekend_flag = validate_string(item.get("weekend_flag", None))
    event = validate_string(item.get("event", None))

    mycursor.execute("INSERT INTO dim_date (id, db_date, year, month, day, quarter, week, day_name, month_name, holiday_flag, weekend_flag, event) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                     (id, db_date, year, month, day, quarter, week, day_name, month_name, holiday_flag, weekend_flag, event))

mydb.commit()
mydb.close()


# populate Time Entries fact table--------------------------------------


url_address = "https://api.harvestapp.com/v2/time_entries"

# find out total number of pages

r = requests.get(url=url_address, headers=headers).json()
total_pages = int(r['total_pages'])
print(total_pages)
all_time_entries = []

# loop through all pages and return JSON object
for page in range(1, total_pages):
    url = "https://api.harvestapp.com/v2/time_entries?page="+str(page)
    # response = requests.get(url=url, headers=headers).json()
    # all_time_entries.append(response)
    page += 1

    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request, timeout=5)
    responseBody = response.read().decode("utf-8")
    jsonResponse = json.loads(responseBody)

    for i in jsonResponse["time_entries"]:

        sql = "INSERT IGNORE INTO Fact_Time_Entries (id, date_id, hours, user_id, client_id, project_id, task_id, user_assignment_id, billable, billable_hours, non_billable_hours) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # determine filed 'billable_hours'
        if(i["billable"]):
          billable_hours = i["hours"]
          non_billable_hours = 0
        else:
          billable_hours = 0
          non_billable_hours = i["hours"]

        val = (i["id"], int(((i["spent_date"]).replace('-', ''))), i["hours"], i["user"]["id"], i["client"]["id"],
               i["project"]["id"], i["task"]["id"], i["user_assignment"]["id"], i["billable"], billable_hours, non_billable_hours)

        print(val)

        mycursor.execute(sql, val)
        mydb.commit()


# populate Users dimension table ---------------------------------------------------

# only doing one page at a time ----!

# find out total number of pages
url_address = "https://api.harvestapp.com/v2/users"

r = requests.get(url=url_address, headers=headers).json()
total_pages = int(r['total_pages'])
all_users_entries = []

# loop through all pages and return JSON object
for page in range(1, total_pages):
     url = "https://api.harvestapp.com/v2/users?page=2"
     page = 2
     request = urllib.request.Request(url=url, headers=headers)
     response = urllib.request.urlopen(request, timeout=5)
     responseBody = response.read().decode("utf-8")
     jsonResponse = json.loads(responseBody)

     for i in jsonResponse["users"]:

       url = "https://api.harvestapp.com/v2/users/" + \
           str(i["id"]) + "/project_assignments?page=1"

      page = 1
      request2 = urllib.request.Request(url=url, headers=headers)
      response2 = urllib.request.urlopen(request2, timeout=5)
      responseBody2 = response2.read().decode("utf-8")
      jsonResponse2 = json.loads(responseBody2)
      projects = 0
      for j in jsonResponse2["project_assignments"]:
        projects = projects + 1

      sql = "INSERT IGNORE INTO dim_user (id, first_name, last_name, weekly_capacity, is_employee, full_name, is_active, num_projects) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

      if (i["is_contractor"] == 1):
        is_employee = 0
      elif (i["is_contractor"] == 0):
        is_employee = 1

      val = (i["id"], i["first_name"], i["last_name"], i["weekly_capacity"], is_employee, i["first_name"] + ' ' + i["last_name"], i['is_active'], projects)
      print(val)

      mycursor.execute(sql, val)
      mydb.commit()






# populate Clients dimension table ---------------------------------------------------

# find out total number of pages
url_address = "https://api.harvestapp.com/v2/clients"

r = requests.get(url=url_address, headers=headers).json()
total_pages = int(r['total_pages'])
all_clients_entries = []


# loop through all pages and return JSON object
 for page in range(1, total_pages):
    url = "https://api.harvestapp.com/v2/clients?page="+str(page)

    page += 1

    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request, timeout=5)
    responseBody = response.read().decode("utf-8")
    jsonResponse = json.loads(responseBody)

    for i in jsonResponse["clients"]:

        sql = "INSERT IGNORE INTO dim_client (id, name) VALUES (%s, %s)"
        val = (i["id"], i["name"])
        print(val)

        mycursor.execute(sql, val)
        mydb.commit()




# populate Projects table ---------------------------------------------------

# find out total number of pages
url_address = "https://api.harvestapp.com/v2/projects"

r = requests.get(url=url_address, headers=headers).json()
total_pages = int(r['total_pages'])
all_projects_entries = []


# loop through all pages and return JSON object
for page in range(1, total_pages):
    url = "https://api.harvestapp.com/v2/projects?page="+str(page)

    page += 1

    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request, timeout=5)
    responseBody = response.read().decode("utf-8")
    jsonResponse = json.loads(responseBody)

    for i in jsonResponse["projects"]:

        sqlQuery = "SELECT sum(hours) FROM Fact_Time_Entries where project_id ="+ str(i["id"])
        mycursor.execute(sqlQuery)
        totalHoursPerProjectArray = mycursor.fetchone()
        totalHoursPerProject = totalHoursPerProjectArray[0]

        sqlQuery2 = "SELECT sum(billable_hours) FROM Fact_Time_Entries where project_id ="+ str(i["id"])
        mycursor.execute(sqlQuery2)
        totalBillableHoursPerProjectArray = mycursor.fetchone()
        totalBillableHoursPerProject = totalBillableHoursPerProjectArray[0]

        sql = "INSERT IGNORE INTO dim_project (id, name, is_active, budget, starts_on, ends_on, total_hours, total_billable_hours) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (i["id"], i["name"], i["is_active"], i["budget"], i["starts_on"], i["ends_on"], totalHoursPerProject, totalBillableHoursPerProject)

        print(val)

        mycursor.execute(sql, val)
        mydb.commit()



# populate Tasks dimension table ---------------------------------------------------

# looping through pages not working

# find out total number of pages
url_address = "https://api.harvestapp.com/v2/tasks"
r = requests.get(url=url_address, headers=headers).json()
total_pages = int(r['total_pages'])
all_tasks_entries = []

loop through all pages and return JSON object
for page in range(1, total_pages):
    url = "https://api.harvestapp.com/v2/tasks?page="+str(page)

    page += 1

    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request, timeout=5)
    responseBody = response.read().decode("utf-8")
    jsonResponse = json.loads(responseBody)

    print(json.dumps(jsonResponse["tasks"], sort_keys=True, indent=4))

    for i in jsonResponse["tasks"]:

        sql = "INSERT INTO dim_task (id, name) VALUES (%s, %s)"
        val = (i["id"], i["name"])

        print(val)

        mycursor.execute(sql, val)
        mydb.commit()



# populate Roles dimension table ---------------------------------------------------

# find out total number of pages
url_address = "https://api.harvestapp.com/v2/roles"

r = requests.get(url=url_address, headers=headers).json()
total_pages = int(r['total_pages'])
all_user_assignments_entries = []
print(total_pages)

# loop through all pages and return JSON object
for page in range(1, total_pages):

url = "https://api.harvestapp.com/v2/roles?page=1"

page = 1
request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request, timeout=5)
responseBody = response.read().decode("utf-8")
jsonResponse = json.loads(responseBody)


for i in jsonResponse["roles"]:
  sql = "INSERT IGNORE INTO dim_role (id, name, num_users) VALUES (%s, %s, %s)"
  k = 0

# check if the users are active
  for j in i["user_ids"]:
    url = "https://api.harvestapp.com/v2/users/" + str(j)
    page = 1
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request, timeout=5)
    responseBody = response.read().decode("utf-8")
    jsonResponse = json.loads(responseBody)

    if (jsonResponse["is_active"] == True):
      k = k + 1
      print (k)

  val = (i["id"], i["name"], k)
  print(val)

  mycursor.execute(sql, val)
  mydb.commit()


# populate bridge Role/User table ---------------------------------------------------

# find out total number of pages
url_address = "https://api.harvestapp.com/v2/roles"

r = requests.get(url=url_address, headers=headers).json()
total_pages = int(r['total_pages'])
all_user_assignments_entries = []

# loop through all pages and return JSON object
for page in range(1, total_pages):

url = "https://api.harvestapp.com/v2/roles?page=1"

page = 1
request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request, timeout=5)
responseBody = response.read().decode("utf-8")
jsonResponse = json.loads(responseBody)

for i in jsonResponse["roles"]:
  for j in i["user_ids"]:
    sql = "INSERT IGNORE INTO bridge_role_user (role_id, user_id) VALUES (%s, %s)"
    val = (i["id"], j)
    print(val)

    mycursor.execute(sql, val)
    mydb.commit()


# Project User Assignments--------------------------------
# find out total number of pages
url_address = "https://api.harvestapp.com/v2/user_assignments"

r = requests.get(url=url_address, headers=headers).json()
total_pages = int(r['total_pages'])
all_user_assignments_entries = []


# loop through all pages and return JSON object
for page in range(1, total_pages):

  url = "https://api.harvestapp.com/v2/user_assignments?page="+str(page)

# page = 1
  request = urllib.request.Request(url=url, headers=headers)
  response = urllib.request.urlopen(request, timeout=5)
  responseBody = response.read().decode("utf-8")
  jsonResponse = json.loads(responseBody)

  for i in jsonResponse["user_assignments"]:
    # print(json.dumps(jsonResponse["user_assignments"], sort_keys=True, indent=4))

    sql = "INSERT IGNORE INTO dim_project_user_assignment (id, project_id, project_name, user_id, user_name, is_active, is_project_manager) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (i["id"], i["project"]["id"], i["project"]["name"], i["user"]["id"], i["user"]["name"], i["is_active"], i["is_project_manager"])
    print(val)

    mycursor.execute(sql, val)
    mydb.commit()



# populate Project Manager table ---------------------------------------------------

# find out total number of pages
url_address = "https://api.harvestapp.com/v2/users"

r = requests.get(url=url_address, headers=headers).json()
total_pages = int(r['total_pages'])
all_user_assignments_entries = []


# loop through all pages and return JSON object
for page in range(1, total_pages):

  url = "https://api.harvestapp.com/v2/users?page=1"

  page = 1
  request = urllib.request.Request(url=url, headers=headers)
  response = urllib.request.urlopen(request, timeout=5)
  responseBody = response.read().decode("utf-8")
  jsonResponse = json.loads(responseBody)

  for i in jsonResponse["users"]:

    if (i["is_project_manager"]):

      sql = "INSERT INTO dim_project_manager (full_name, id) VALUES (%s, %s)"

      val = ( i["first_name"] + ' ' + i["last_name"], i["id"])

      print(val)

      mycursor.execute(sql, val)
      mydb.commit()




# populate Project Manager / Project Bridge table ---------------------------------------------------

# find out total number of pages
url_address = "https://api.harvestapp.com/v2/user_assignments"

r = requests.get(url=url_address, headers=headers).json()
total_pages = int(r['total_pages'])
all_user_assignments_entries = []


# loop through all pages and return JSON object
for page in range(1, total_pages):

  url = "https://api.harvestapp.com/v2/user_assignments?page="+str(page)

  page += 1
  request = urllib.request.Request(url=url, headers=headers)
  response = urllib.request.urlopen(request, timeout=5)
  responseBody = response.read().decode("utf-8")
  jsonResponse = json.loads(responseBody)

  for i in jsonResponse["user_assignments"]:
    if (i["is_project_manager"]):

      sql = "INSERT INTO bridge_project_manager_project (project_manager_id, project_id) VALUES (%s, %s)"

      val = (i["user"]["id"], i["project"]["id"])

      print(val)

      mycursor.execute(sql, val)
      mydb.commit()




mydb.close()
