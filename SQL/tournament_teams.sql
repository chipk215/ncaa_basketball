SELECT [ts].[Season]
      ,[ts].[TeamID]
	  ,CAST(SUBSTRING([ts].[Seed],2,2) AS int) AS Seed
	  ,[teams].id
FROM [NCAA_Basketball].[dbo].[NCAATourneySeeds] as ts
LEFT JOIN [NCAA_Basketball].[dbo].[D1_teams] as teams
ON ts.TeamID = teams.kaggle_team_id
WHERE [ts].Season IN (2014, 2015, 2016, 2017, 2018)
ORDER BY [ts].Season