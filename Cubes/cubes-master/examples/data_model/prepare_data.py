# -*- coding: utf-8 -*-
# Data preparation for the hello_world example
from __future__ import print_function

from sqlalchemy import create_engine
from cubes.tutorial.sql import create_table_from_csv

# 1. Prepare SQL data in memory

# for CSVs ---
engine = create_engine('sqlite:///data.sqlite')



# - CSVs (Google Cloud SQL) ------------------------------

# FACT_TABLE1 = "csv.Week_10_to_16_Feb_2020"

# create_table_from_csv(engine,
#                       "csvs/projects_by_week.csv",
#                       table_name=FACT_TABLE1,
#                       fields=[
#                           ("client", "string"),
#                           ("project", "string"),
#                           ("project_code", "string"),
#                           ("task", "string"),
#                           ("day", "integer"),
#                           ("amount", "integer"),
#                           ("last_name", "string")
#                       ],
#                       create_id=True
#                       )

# print("file data.sqlite created")

# FACT_TABLE2 = "csv.Year_2020"

# create_table_from_csv(engine,
#                       "csvs/projects_by_year.csv",
#                       table_name=FACT_TABLE2,
#                       fields=[
#                           ("client", "string"),
#                           ("project", "string"),
#                           ("project_code", "string"),
#                           ("task", "string"),
#                           ("day", "integer"),
#                           ("amount", "integer"),
#                           ("last_name", "string")
#                       ],
#                       create_id=True
#                       )

# print("done. files data.sqlite created")

FACT_TABLE3 = "csv.Active_Projects"

create_table_from_csv(engine,
                      "csvs/active_projects.csv",
                      table_name=FACT_TABLE3,
                      fields=[
                          ("client", "string"),
                          ("project", "string"),
                          ("project_code", "string"),
                          ("task", "string"),
                          ("start_date", "integer"),
                          ("end_date", "integer"),
                          ("total_hours", "integer"),
                          ("billable_hours", "integer"),
                          ("budget", "integer"),
                          ("budget_spent", "integer"),
                          ("budget_remaining", "integer")

                      ],
                      create_id=True
                      )

print("file data.sqlite created")

# FACT_TABLE4 = "csv.Archived_Projects"

# create_table_from_csv(engine,
#                       "csvs/archived_projects.csv",
#                       table_name=FACT_TABLE4,
#                       fields=[
#                           ("client", "string"),
#                           ("project", "string"),
#                           ("project_code", "string"),
#                           ("task", "string"),
#                           ("start_date", "integer"),
#                           ("end_date", "integer"),
#                           ("total_hours", "integer"),
#                           ("billable_hours", "integer"),
#                           ("budget", "integer"),
#                           ("budget_spent", "integer"),
#                           ("budget_remaining", "integer")

#                       ],
#                       create_id=True
#                       )

# print("file data.sqlite created")


# FACT_TABLE5 = "csv.Goal"

# create_table_from_csv(engine,
#                       "csvs/goal2.csv",
#                       table_name=FACT_TABLE5,
#                       fields=[
#                           ("day", "integer"),
#                           ("client", "string"),
#                           ("contract", "string"),
#                           ("project", "string"),
#                           ("project_code", "string"),
#                           ("task", "string"),
#                           ("project_manager", "string"),
#                           ("start_date", "integer"),
#                           ("end_date", "integer"),
#                           ("last_name", "string"),
#                           ("amount", "integer")
#                       ],
#                       create_id=True
#                       )

# print("file data.sqlite created")


