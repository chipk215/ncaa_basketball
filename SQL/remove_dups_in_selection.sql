SELECT rows.game_id, rows.scheduled_date, market
FROM (
   (SELECT *, RN=ROW_NUMBER() OVER(PARTITION BY game_id ORDER BY game_id)
	FROM [NCAA_Basketball].[dbo].[d1_2015_with_duplicates])
   ) AS rows
--WHERE RN >1
ORDER BY market



SELECT rows.market, rows.opp_market,  rows.game_id
FROM (
   (SELECT *, RN=ROW_NUMBER() OVER(PARTITION BY game_id ORDER BY game_id)
	FROM [NCAA_Basketball].[dbo].[d1_2015_with_duplicates])
   ) AS rows
WHERE RN =1
ORDER BY rows.market



SELECT rows.market, rows.opp_market, rows.game_id
FROM (
   (SELECT *, RN=ROW_NUMBER() OVER(PARTITION BY game_id ORDER BY game_id)
	FROM [NCAA_Basketball].[dbo].[d1_2015_with_duplicates])
   ) AS rows
WHERE RN =2
ORDER BY rows.market