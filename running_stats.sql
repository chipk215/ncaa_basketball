SELECT scheduled_date
	   ,game_id
	   ,market
	   ,opp_market
       ,points_game
	   ,field_goals_made
	   ,field_goals_att
	   ,free_throws_made
	   ,free_throws_att
	   ,offensive_rebounds
	   ,defensive_rebounds
	   ,turnovers
	   ,win
	   ,opp_points_game
	   ,opp_offensive_rebounds
	   ,opp_defensive_rebounds
	   ,opp_free_throws_att
	--   ,field_goals_att -  ((offensive_rebounds/(offensive_rebounds + defensive_rebounds)) *(field_goals_att - field_goals_made) *1.07) + turnovers + (0.4 * free_throws_att) AS poss
	   ,CAST(AVG(1.0*points_game) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING) AS DECIMAL(8,2)) AS prn_pts_avg
	   ,CAST(AVG(1.0*opp_points_game) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING) AS DECIMAL(8,2)) AS opp_pts_avg
	   ,AVG(field_goals_att -  ((offensive_rebounds/(offensive_rebounds + defensive_rebounds)) *(field_goals_att - field_goals_made) *1.07) + 
			turnovers + (0.4 * free_throws_att)) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING) AS prn_possesion_avg 
	   ,CAST(SUM(field_goals_made) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING)  AS float) / 
			CAST(SUM(field_goals_att) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING) AS float) AS prn_fg_pct
	   ,CAST(AVG(1.0*offensive_rebounds) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING) AS DECIMAL(8,2)) AS prn_off_rebs_avg
	   ,CAST(AVG(1.0*opp_offensive_rebounds) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING) AS DECIMAL(8,2)) AS opp_off_rebs_avg
	   ,CAST(AVG(1.0*defensive_rebounds) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING) AS DECIMAL(8,2)) AS prn_def_rebs_avg
	   ,CAST(AVG(1.0*opp_defensive_rebounds) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING) AS DECIMAL(8,2)) AS opp_def_rebs_avg
	   ,CAST(AVG(1.0*free_throws_att) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING) AS DECIMAL(8,2)) AS prn_ft_att_avg
	   ,CAST(AVG(1.0*opp_free_throws_att) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING) AS DECIMAL(8,2)) AS opp_ft_att_avg
	   ,CAST(SUM(free_throws_made) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING)  AS float) / 
			CAST(SUM(free_throws_att) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING) AS float) AS prn_ft_pct
	   ,CAST(AVG(1.0*turnovers) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING) AS DECIMAL(8,2)) AS prn_turnover_avg
	   ,CAST(AVG(1.0*win) OVER(PARTITION BY market ORDER BY scheduled_date ROWS UNBOUNDED PRECEDING) AS DECIMAL(8,2)) AS prn_win_pct
FROM dbo.d1_2015_with_duplicates
ORDER BY scheduled_date,game_id



-- Compute apriori statistics entering the game (stats cover games up to the start of the game)
SELECT scheduled_date
	   ,game_id
	   ,market
	   ,opp_market
       ,points_game
	   ,field_goals_made
	   ,field_goals_att
	   ,free_throws_made
	   ,free_throws_att
	   ,offensive_rebounds
	   ,defensive_rebounds
	   ,turnovers
	   ,win
	   ,opp_points_game
	   ,opp_offensive_rebounds
	   ,opp_defensive_rebounds
	   ,opp_free_throws_att
	   ,opp_turnovers
	--   ,field_goals_att -  ((offensive_rebounds/(offensive_rebounds + defensive_rebounds)) *(field_goals_att - field_goals_made) *1.07) + turnovers + (0.4 * free_throws_att) AS poss
	   ,CAST(AVG(1.0*points_game) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_enter_pts_avg

	   ,CAST(AVG(1.0*opp_points_game) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_allow_enter_pts_avg

	   ,AVG(field_goals_att -  ((offensive_rebounds/(offensive_rebounds + defensive_rebounds)) *(field_goals_att - field_goals_made) *1.07) + 
			turnovers + (0.4 * free_throws_att)) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prn_enter_possesion_avg 

	   ,CAST(SUM(field_goals_made) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)  AS float) / 
			CAST(SUM(field_goals_att) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS float) AS prn_enter_fg_pct

	   ,CAST(AVG(1.0*offensive_rebounds) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_enter_off_rebs_avg

	   ,CAST(AVG(1.0*opp_offensive_rebounds) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_allow_enter_off_rebs_avg

	   ,CAST(AVG(1.0*defensive_rebounds) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_enter_def_rebs_avg

	   ,CAST(AVG(1.0*opp_defensive_rebounds) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_allow_enter_def_rebs_avg

	   ,CAST(AVG(1.0*free_throws_att) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_enter_ft_att_avg

	   ,CAST(AVG(1.0*opp_free_throws_att) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_allow_enter_ft_att_avg

	   ,CAST(SUM(free_throws_made) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)  AS float) / 
			CAST(SUM(free_throws_att) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1  PRECEDING) AS float) AS prn_enter_ft_pct

	   ,CAST(AVG(1.0*turnovers) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1  PRECEDING) AS DECIMAL(8,2)) AS prn_enter_turnover_avg

	    ,CAST(AVG(1.0*opp_turnovers) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1  PRECEDING) AS DECIMAL(8,2)) AS prn_enter_takeaway_avg

	   ,CAST(AVG(1.0*win) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1  PRECEDING) AS DECIMAL(8,2)) AS prn_enter_win_pct

FROM dbo.d1_2015_with_duplicates
ORDER BY market