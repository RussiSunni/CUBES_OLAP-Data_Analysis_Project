# -*- coding: utf-8 -*-
# Data preparation for the hello_world example
from __future__ import print_function

from sqlalchemy import create_engine
from cubes.tutorial.sql import create_table_from_csv

# 1. Prepare SQL data in memory

FACT_TABLE1 = "Week 10 – 16 Feb 2020"

print("preparing data...")

engine = create_engine('sqlite:///data.sqlite')

# create_table_from_csv(engine,
#                       "projects_by_week.csv",
#                       table_name=FACT_TABLE1,
#                       fields=[
#                             ("category", "string"),
#                             ("category_label", "string"),
#                             ("subcategory", "string"),
#                             ("subcategory_label", "string"),
#                             ("line_item", "string"),
#                             ("year", "integer"),
#                             ("amount", "integer"),
#                              ("lastname", "string")
#                             ],
#                       create_id=True
#                   )

# print("first file data.sqlite created")

# FACT_TABLE2 = "Year 2020"

# create_table_from_csv(engine,
#                       "projects_by_year.csv",
#                       table_name=FACT_TABLE2,
#                       fields=[
#                             ("category", "string"),
#                             ("category_label", "string"),
#                             ("subcategory", "string"),
#                             ("subcategory_label", "string"),
#                             ("line_item", "string"),
#                             ("year", "integer"),
#                             ("amount", "integer"),
#                              ("lastname", "string")
#                             ],
#                       create_id=True
#                   )

# print("done. files data.sqlite created")

# FACT_TABLE3 = "Active Projects"

# create_table_from_csv(engine,
#                       "active_projects.csv",
#                       table_name=FACT_TABLE3,
#                       fields=[
#                           ("category", "string"),
#                           ("category_label", "string"),
#                           ("subcategory", "string"),
#                           ("subcategory_label", "string"),
#                           ("line_item", "string"),
#                           ("startdate", "integer"),
#                           ("enddate", "integer"),
#                           ("totalhours", "integer"),
#                           ("billablehours", "integer"),
#                           ("budget", "integer"),
#                           ("budgetspent", "integer"),
#                           ("budgetremaining", "integer")

#                       ],
#                       create_id=True
#                       )

# print("file data.sqlite created")


# FACT_TABLE4 = "Archived Projects"

# create_table_from_csv(engine,
#                       "archived_projects.csv",
#                       table_name=FACT_TABLE4,
#                       fields=[
#                           ("category", "string"),
#                           ("category_label", "string"),
#                           ("subcategory", "string"),
#                           ("subcategory_label", "string"),
#                           ("line_item", "string"),
#                           ("startdate", "integer"),
#                           ("enddate", "integer"),
#                           ("totalhours", "integer"),
#                           ("billablehours", "integer"),
#                           ("budget", "integer"),
#                           ("budgetspent", "integer"),
#                           ("budgetremaining", "integer")

#                       ],
#                       create_id=True
#                       )

# print("file data.sqlite created")


FACT_TABLE5 = "Goal"

create_table_from_csv(engine,
                      "goal.csv",
                      table_name=FACT_TABLE5,
                      fields=[
                          ("date", "integer"),
                          ("client", "string"),
                          ("contract", "string"),
                          ("project", "string"),
                          ("task", "string"),
                          ("project_manager", "string"),
                          ("start_date", "integer"),
                          ("end_date", "integer"),
                          ("total_hours", "integer"),
                          ("billable_hours", "integer"),
                          ("budget", "integer"),
                          ("budget_spent", "integer"),
                          ("budget_remaining", "integer"),
                          ("hours", "integer"),
                          ("billable", "string"),
                          ("name", "string"),
                          ("roles", "string")
                      ],
                      create_id=True
                      )

print("file data.sqlite created")
