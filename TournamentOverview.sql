/****** Script for SelectTopNRows command from SSMS  ******/

  SELECT season, COUNT(*) AS [Number Games]
  FROM [NCAA_Basketball].[dbo].[tournament_results]
  GROUP BY season
  ORDER BY season
