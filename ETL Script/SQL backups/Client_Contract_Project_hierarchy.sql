CREATE VIEW Client_Contract_Project_hierarchy AS
SELECT c.name as client, co.name as contract, p.name as project, p.id as project_id, pm.name as 'project manager', p.is_active, p.starts_on, (SUM(hours) -  p.budget) as difference
FROM Fact_Time_Entries as t JOIN Dim_Projects as p
ON t.project_id = p.id
JOIN Dim_Clients as c ON t.client_id = c.id
JOIN 
(SELECT DISTINCT u.last_name as name, t.project_id as project_id
FROM Dim_Users as u 
JOIN Fact_Time_Entries as t ON t.user_id = u.id
JOIN Dim_Project_User_Assignments as pua ON t.user_assignment_id = pua.id
WHERE pua.is_project_manager = 1
) as pm
ON t.project_id = pm.project_id
JOIN Dim_Tasks as ta ON t.task_id = ta.id
LEFT OUTER JOIN Dim_Contracts as co ON t.contract_id = co.id
group by c.name, co.name, p.name, p.id, pm.name, p.starts_on, p.budget, p.is_active

