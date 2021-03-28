CREATE VIEW Date AS
SELECT p.name, (SUM(t.hours) - p.budget) AS difference, t.project_id as project_id, p.is_active, p.starts_on
FROM Fact_Time_Entries as t
JOIN Dim_Projects as p ON t.project_id = p.id 
GROUP BY p.name, t.project_id, p.budget, p.is_active 