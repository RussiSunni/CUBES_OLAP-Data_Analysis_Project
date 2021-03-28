CREATE VIEW Client_Contract_Project_PM_Time AS
SELECT DISTINCT p.name as project, pd.difference, p.budget, p.starts_on, p.is_active, c.name as client, p.contract_number, p.contract2_number, pm.project_manager, d.db_date, d.year, d.quarter, d.month, d.month_name, d.week, d.day, d.day_name
FROM Fact_Time_Entries as t
JOIN Dim_Projects as p ON t.project_id = p.id
JOIN
(SELECT p.name, (SUM(t.hours) - p.budget) AS difference, t.project_id as project_id, p.is_active
FROM Fact_Time_Entries as t
JOIN Dim_Projects as p ON t.project_id = p.id 
GROUP BY p.name, t.project_id, p.budget, p.is_active) as pd ON pd.project_id = p.id
JOIN Dim_Clients AS c ON t.client_id = c.id
JOIN 
(SELECT DISTINCT CONCAT(u.first_name, ' ',  u.last_name) as project_manager, t.project_id as project_id
FROM Dim_Users as u 
JOIN Fact_Time_Entries as t ON t.user_id = u.id
JOIN Dim_Project_User_Assignments as pua ON t.user_assignment_id = pua.id
WHERE pua.is_project_manager = 1
) as pm ON pm.project_id = p.id
LEFT JOIN Dim_Dates as d ON p.starts_on = d.db_date