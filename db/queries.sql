-- Most recent conversion history.
SELECT c.conversion_id, i.filename, c.operation, c.mae, c.rmse,
       c.status, c.created_at
FROM conversions AS c
JOIN images AS i ON i.image_id = c.image_id
ORDER BY c.conversion_id DESC
LIMIT 20;

-- Count records in each required table.
SELECT 'images' AS table_name, COUNT(*) AS record_count FROM images
UNION ALL
SELECT 'colour_spaces', COUNT(*) FROM colour_spaces
UNION ALL
SELECT 'conversions', COUNT(*) FROM conversions;

-- Failed batch jobs for review.
SELECT c.conversion_id, i.filename, c.status, c.created_at
FROM conversions AS c
JOIN images AS i ON i.image_id = c.image_id
WHERE c.status = 'failed'
ORDER BY c.conversion_id DESC;
-- Conversion counts grouped by status.
SELECT status, COUNT(*) AS conversion_count FROM conversions GROUP BY status;