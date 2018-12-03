SELECT game_id,scheduled_date, home_team, market, opp_market, win, 
        points_game, opp_points_game,
        field_goals_pct, 
        offensive_rebounds, 
        free_throws_att,
        free_throws_pct,
        turnovers      
FROM [NCAA_Basketball].[dbo].[d1_2015]
WHERE ( (market = 'Oakland') OR (opp_market = 'Oakland')) AND (scheduled_date < '2016-01-02' )