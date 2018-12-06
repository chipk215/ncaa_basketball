SELECT rows.game_id, rows.scheduled_date
FROM (
   (SELECT *, RN=ROW_NUMBER() OVER(PARTITION BY game_id ORDER BY game_id)
	FROM [NCAA_Basketball].[dbo].[d1_2015_with_duplicates])
   ) AS rows
WHERE RN >1