/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [Season] as season
      ,[School]
	  , m.kaggle_id as team_id
      ,[Games]
      ,[SRS]
      ,[SOS]
      ,[win_pct]
      ,[pts_avg]
      ,[opp_pts_avg]
      ,[fg_pct]
      ,[allow_fg_pct]
      ,[ft_pct]
      ,[allow_ft_att_avg]
      ,[poss_avg]
      ,[off_rebs_avg]
      ,[allow_off_rebs_avg]
      ,[def_rebs_avg]
      ,[allow_def_rebs_avg]
      ,[to_avg]
      ,[steal_avg]
      ,[off_rating]
      ,[ft_att_avg]
  FROM [SRCBB].[dbo].[team_summaries] as t
  LEFT JOIN [SRCBB].[dbo].[sr_school_to_kaggle_id] as m ON t.School= m.sr_school;



