SELECT market, season, team_id
	,CAST(AVG(1.0*points_game)       AS DECIMAL(8,3)) AS points_avg
	,CAST(AVG(1.0*opp_points_game)   AS DECIMAL(8,3)) AS opp_pts_avg

	,AVG(field_goals_att -  ((offensive_rebounds/(offensive_rebounds + defensive_rebounds)) *(field_goals_att - field_goals_made) *1.07) + 
			turnovers + (0.4 * free_throws_att)) AS possesion_avg 

	,CAST(SUM(field_goals_made)  AS DECIMAL(8,3)) / SUM(field_goals_att)  AS fg_pct

	, CAST(SUM(opp_field_goals_made)  AS DECIMAL(8,3)) / SUM(opp_field_goals_att)  AS allow_fg_pct

	,CAST(AVG(1.0*offensive_rebounds)  AS DECIMAL(8,3)) AS off_rebs_avg

	,CAST(AVG(1.0*opp_offensive_rebounds) AS DECIMAL(8,3)) AS allow_off_rebs_avg

	,CAST(AVG(1.0*defensive_rebounds)  AS DECIMAL(8,3)) AS def_rebs_avg

	,CAST(AVG(1.0*opp_defensive_rebounds) AS DECIMAL(8,3)) AS allow_def_rebs_avg

	,CAST(AVG(1.0*free_throws_att)  AS DECIMAL(8,3)) AS ft_att_avg

	,CAST(AVG(1.0*opp_free_throws_att) AS DECIMAL(8,3)) AS allow_ft_att_avg

	,CAST(SUM(free_throws_made)   AS DECIMAL(8,3)) / SUM(free_throws_att) AS ft_pct

	,CAST(AVG(1.0*turnovers) AS DECIMAL(8,3)) AS turnover_avg

	,CAST(AVG(1.0*opp_turnovers)AS DECIMAL(8,3)) AS take_away_avg

	,CAST(AVG(1.0*win)  AS DECIMAL(8,3)) AS win_pct

	,100*AVG(1.0*points_game)/ (AVG(field_goals_att -  ((offensive_rebounds/(offensive_rebounds + defensive_rebounds)) *(field_goals_att - field_goals_made) *1.07) + 
			turnovers + (0.4 * free_throws_att))) AS off_rating
FROM dbo.d1_2015_with_duplicates
WHERE division_alias='D1' AND opp_division_alias='D1'
GROUP BY market,season, team_id 
ORDER BY off_rating DESC