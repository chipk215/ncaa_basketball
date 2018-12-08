/*
 The Apriori CTE computes the running summary statistics for the teams prior to the start of the game.

 The 'enter' part of the column name indicates the statistic corresponds to the value at the start of the game, not the
 usual post game statistic.

 The 'enter' stats are used to train the classification models.

 Stats without 'enter' in the name correspond to stats collected during the game.
*/
;WITH Apriori
AS
(
	SELECT scheduled_date
	   ,game_id
	   ,home_team
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
	   ,opp_field_goals_made
	   ,opp_field_goals_att
	   ,opp_offensive_rebounds
	   ,opp_defensive_rebounds
	   ,opp_free_throws_att
	   ,opp_turnovers
	   ,CAST(AVG(1.0*points_game) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_enter_pts_avg

	   ,CAST(AVG(1.0*opp_points_game) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_enter_allow_pts_avg

	   ,AVG(field_goals_att -  ((offensive_rebounds/(offensive_rebounds + defensive_rebounds)) *(field_goals_att - field_goals_made) *1.07) + 
			turnovers + (0.4 * free_throws_att)) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prn_enter_possesion_avg 

	   ,CAST(SUM(field_goals_made) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)  AS float) / 
			CAST(SUM(field_goals_att) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS float) AS prn_enter_fg_pct

	   ,CAST(SUM(opp_field_goals_made) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)  AS float) / 
			CAST(SUM(opp_field_goals_att) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS float) AS prn_enter_allow_fg_pct

	   ,CAST(AVG(1.0*offensive_rebounds) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_enter_off_rebs_avg

	   ,CAST(AVG(1.0*opp_offensive_rebounds) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_enter_allow_off_rebs_avg

	   ,CAST(AVG(1.0*defensive_rebounds) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_enter_def_rebs_avg

	   ,CAST(AVG(1.0*opp_defensive_rebounds) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_enter_allow_def_rebs_avg

	   ,CAST(AVG(1.0*free_throws_att) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_enter_ft_att_avg

	   ,CAST(AVG(1.0*opp_free_throws_att) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS DECIMAL(8,2)) AS prn_enter_allow_ft_att_avg

	   ,CAST(SUM(free_throws_made) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)  AS float) / 
			CAST(SUM(free_throws_att) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1  PRECEDING) AS float) AS prn_enter_ft_pct

	   ,CAST(AVG(1.0*turnovers) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1  PRECEDING) AS DECIMAL(8,2)) AS prn_enter_turnover_avg

	    ,CAST(AVG(1.0*opp_turnovers) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1  PRECEDING) AS DECIMAL(8,2)) AS prn_enter_take_away_avg

	   ,CAST(AVG(1.0*win) OVER(PARTITION BY market ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND 1  PRECEDING) AS DECIMAL(8,2)) AS prn_enter_win_pct

	FROM dbo.d1_2015_with_duplicates	
), 
M1 AS(
SELECT rows.*
FROM (
   (SELECT *, RN=ROW_NUMBER() OVER(PARTITION BY game_id ORDER BY game_id)
	FROM Apriori)
   ) AS rows
   WHERE RN=2
)

SELECT a.scheduled_date
	,a.game_id
	,a.home_team
	,a.market
	,a.opp_market
    ,a.points_game
	,a.win                            AS game_result
	,a.opp_points_game
	,a.prn_enter_pts_avg
	,a.prn_enter_allow_pts_avg
	,a.prn_enter_possesion_avg 
	,a.prn_enter_fg_pct
	,a.prn_enter_allow_fg_pct
	,a.prn_enter_off_rebs_avg
	,a.prn_enter_allow_off_rebs_avg
	,a.prn_enter_def_rebs_avg
	,a.prn_enter_ft_att_avg
	,a.prn_enter_allow_ft_att_avg
	,a.prn_enter_ft_pct
	,a.prn_enter_turnover_avg
	,a.prn_enter_take_away_avg
	,a.prn_enter_win_pct
	,M1.prn_enter_pts_avg            AS opp_enter_pts_avg
	,M1.prn_enter_allow_pts_avg      AS opp_enter_allow_pts_avg
	,M1.prn_enter_possesion_avg      AS opp_enter_possesion_avg
	,M1.prn_enter_fg_pct             AS opp_enter_fg_pct
	,M1.prn_enter_allow_fg_pct       AS opp_enter_allow_fg_pct
	,M1.prn_enter_off_rebs_avg       AS opp_enter_off_rebs_avg
	,M1.prn_enter_allow_off_rebs_avg AS opp_enter_allow_off_rebs_avg
	,M1.prn_enter_def_rebs_avg       AS opp_enter_def_rebs_avg
	,M1.prn_enter_ft_att_avg         AS opp_enter_ft_att_avg
	,M1.prn_enter_allow_ft_att_avg   AS opp_enter_allow_ft_att_avg
	,M1.prn_enter_ft_pct             AS opp_enter_ft_pct
	,M1.prn_enter_turnover_avg       AS opp_enter_turnover_avg
	,M1.prn_enter_take_away_avg       AS opp_enter_take_away_avg
	,M1.prn_enter_win_pct            AS opp_enter_win_pct
FROM Apriori AS a
INNER JOIN M1 ON a.game_id = M1.game_id AND a.market = M1.opp_market
ORDER BY a.scheduled_date, a.market

