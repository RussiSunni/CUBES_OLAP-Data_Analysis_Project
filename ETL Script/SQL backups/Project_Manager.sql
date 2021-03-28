CREATE VIEW Project_Manager AS
SELECT pm.name, project_difference.name as project, project_difference.difference as difference, project_difference.is_active, project_difference.project_id as project_id
FROM
(SELECT p.name, (SUM(t.hours) - p.budget) AS difference, t.project_id as project_id, p.is_active
FROM Fact_Time_Entries as t
JOIN Dim_Projects as p ON t.project_id = p.id 
GROUP BY p.name, t.project_id, p.budget, p.is_active) as project_difference
JOIN 
(SELECT DISTINCT u.last_name as name, t.project_id as project_id
FROM Dim_Users as u 
JOIN Fact_Time_Entries as t ON t.user_id = u.id
JOIN Dim_Project_User_Assignments as pua ON t.user_assignment_id = pua.id
WHERE pua.is_project_manager = 1
) as pm
ON pm.project_id = project_difference.project_id

