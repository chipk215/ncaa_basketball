/****** Script for SelectTopNRows command from SSMS  ******/

SELECT * 
FROM [NCAA_Basketball].[dbo].[d1_2015]
WHERE game_id = 'f2f34755-942b-4fa1-9dc9-234234d25f2b';



SELECT *
FROM [NCAA_Basketball].[dbo].[d1_2015]
WHERE (market = 'St. Francis (PA)' OR opp_market = 'St. Francis (PA)') AND (scheduled_date < '2015-11-22')



SELECT *
FROM [NCAA_Basketball].[dbo].[d1_2015]
WHERE (market = 'St. Francis (PA)' ) AND (scheduled_date < '2016-03-01')



SELECT *
FROM [NCAA_Basketball].[dbo].[d1_2015]
WHERE (opp_market = 'St. Francis (PA)' ) AND (scheduled_date < '2016-03-01')



SELECT COUNT(*)
FROM [NCAA_Basketball].[dbo].[d1_2015]
WHERE (home_team = 'true') AND (win = 'true')

SELECT COUNT(*)
FROM [NCAA_Basketball].[dbo].[d1_2015]
WHERE (home_team = 'true') AND (win = 'false')



SELECT *
FROM [NCAA_Basketball].[dbo].[d1_2015]
WHERE (market = 'Butler' OR opp_market = 'Butler') AND (scheduled_date < '2015-11-19')




SELECT sum(x1.points_game)
FROM
(
   SELECT points_game
   FROM [NCAA_Basketball].[dbo].[d1_2015]
   WHERE (market = 'Oakland' ) AND (scheduled_date < '2016-01-02')
)x1



SELECT sum(x1.opp_points_game)
FROM
(
   SELECT opp_points_game
   FROM [NCAA_Basketball].[dbo].[d1_2015]
   WHERE (opp_market = 'Oakland' ) AND (scheduled_date < '2016-01-02')
)x1





SELECT market, COUNT(*)
FROM [NCAA_Basketball].[dbo].[d1_2015]
GROUP BY market
ORDER BY market


SELECT opp_market, COUNT(*)
FROM [NCAA_Basketball].[dbo].[d1_2015]
GROUP BY opp_market
ORDER BY opp_market



SELECT market
FROM [NCAA_Basketball].[dbo].[d1_2015]
GROUP BY market
ORDER BY market

