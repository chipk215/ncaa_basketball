SELECT scheduled_date, market, opp_market, win, points_game, opp_points_game
FROM [NCAA_Basketball].[dbo].[D1_Sample_Games_2015]
WHERE (season = 2015) AND
    (market = 'Virginia Tech')
ORDER BY scheduled_date
