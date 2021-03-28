# -*- coding: utf-8 -*-
# Data preparation for the hello_world example
from __future__ import print_function

from sqlalchemy import create_engine
from cubes.tutorial.sql import create_table_from_csv

# 1. Prepare SQL data in memory

print("preparing data...")

engine = create_engine('sqlite:////home/JonathanDyason/cubes/examples/hello_world/data.sqlite')


FACT_TABLE1 = "Week_10_to_16_Feb_2020"

create_table_from_csv(engine,
                      "csvs/projects_by_week.csv",
                      table_name=FACT_TABLE1,
                      fields=[
                          ("client", "string"),
                          ("project", "string"),
                          ("project_code", "string"),
                          ("task", "string"),
                          ("day", "integer"),
                          ("amount", "integer"),
                          ("last_name", "string")
                      ],
                      create_id=True
                      )

print("file data.sqlite created")


FACT_TABLE2 = "Year_2020"

create_table_from_csv(engine,
                      "csvs/projects_by_year.csv",
                      table_name=FACT_TABLE2,
                      fields=[
                          ("client", "string"),
                          ("project", "string"),
                          ("project_code", "string"),
                          ("task", "string"),
                          ("day", "integer"),
                          ("amount", "integer"),
                          ("last_name", "string")
                      ],
                      create_id=True
                      )

print("done. files data.sqlite created")


FACT_TABLE3 = "Active_Projects"

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


FACT_TABLE4 = "Archived_Projects"

create_table_from_csv(engine,
                      "csvs/archived_projects.csv",
                      table_name=FACT_TABLE4,
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