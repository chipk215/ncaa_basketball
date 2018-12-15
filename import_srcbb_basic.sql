
IF OBJECT_ID('tempdb..#ImportSeason') IS NOT NULL
    DROP TABLE #ImportSeason
	DROP TABLE [SRCBB].[dbo].[team_summaries]

	

CREATE TABLE #ImportSeason(
	Season INT NOT NULL,
	Rk INT NOT NULL,
    School NVARCHAR(40) NOT NULL,
	Games INT NOT NULL,
	Overall_W INT NOT NULL,
	Overall_L INT NOT NULL,
	win_pct FLOAT NOT NULL,
	SRS	FLOAT NOT NULL,
	SOS	FLOAT NOT NULL,
	Conf_W	INT ,
	Conf_L	INT ,
	Home_W	INT NOT NULL,
	Home_L  INT NOT NULL,
	Away_W	INT NOT NULL,
	Away_L	INT NOT NULL,
	Points_Tm	INT NOT NULL,
	Points_Opp 	INT NOT NULL, 
	MP	INT NOT NULL,
	FGM	INT NOT NULL,
	FGA	 INT NOT NULL,
	fg_pct	FLOAT NOT NULL,
	Three_P	 INT NOT NULL,
	Three_PA	INT NOT NULL,
	Three_P_PCT	FLOAT NOT NULL,
	FT	INT NOT NULL,
	FTA	INT NOT NULL,
	ft_pct	FLOAT NOT NULL,
	ORB	INT NOT NULL,
	TRB	INT NOT NULL,
	AST	INT NOT NULL,
	STL	INT NOT NULL,
	BLK	INT NOT NULL,
	TOV	INT NOT NULL,
	PF INT NOT NULL	
)
GO

BULK INSERT #ImportSeason
FROM 'C:\Users\CHIPK\Developer\NCAA Data\import_data\original_downloads\2010_basic.csv'
WITH(
FIELDTERMINATOR = ',',
ROWTERMINATOR = '\n',
FIRSTROW=3
)

GO

-- Drop unwanted columns
ALTER TABLE #ImportSeason
	DROP COLUMN Overall_W, Overall_L, Three_P, Three_PA, Three_P_PCT, Conf_W, Conf_L, Home_W, Home_L, Away_W, Away_L, AST, BLK, PF
GO

-- Add new columns
ALTER TABLE #ImportSeason
	ADD pts_avg  float,
	    opp_pts_avg float,
		poss_avg float,
		off_rebs_avg float,
		def_rebs_avg float,
		to_avg float,
		steal_avg float,
		off_rating float,
		ft_att_avg float
		
GO

-- Remove the NCAA tournament indicator from school name
UPDATE #ImportSeason
	SET School=REPLACE(School,'NCAA', '')
GO

-- compute the average points scored per game
UPDATE #ImportSeason
	SET pts_avg= Points_Tm / Games
GO

-- compute the opponents average points scored per game
UPDATE #ImportSeason
	SET opp_pts_avg= Points_Opp / Games
GO


-- compute the average  free throws attempted  per game
UPDATE #ImportSeason
	SET ft_att_avg = FTA / Games
GO

-- compute the average possessions per game
UPDATE #ImportSeason
	SET poss_avg= (FGA - (ORB/TRB) * 1.07 * (FGA-FGM) + TOV + 0.4 * FTA) / Games
GO

-- compute the average offensive rebounds per game
UPDATE #ImportSeason
	SET off_rebs_avg = ORB / Games
GO


-- compute the average defensive rebounds per game
UPDATE #ImportSeason
	SET def_rebs_avg = (TRB - ORB) / Games
GO

-- compute the average turn overs per game
UPDATE #ImportSeason
	SET to_avg = TOV / Games
GO

-- compute the average steals per game
UPDATE #ImportSeason
	SET steal_avg = STL / Games
GO

-- compute the offensive rating
UPDATE #ImportSeason
	SET off_rating= 100 * pts_avg / poss_avg
GO


-- Drop columns after computations
ALTER TABLE #ImportSeason
	DROP COLUMN Points_TM, Points_Opp, MP, FGM, FGA, FT, FTA, ORB, TRB, STL, TOV
GO

IF (EXISTS (SELECT *
				FROM INFORMATION_SCHEMA.TABLES
				WHERE TABLE_NAME = 'team_summaries'))
	BEGIN
	   INSERT INTO [SRCBB].[dbo].[team_summaries] 
	   SELECT * 
	   FROM #ImportSeason
	END;
ELSE
	BEGIN
		SELECT * INTO  [SRCBB].[dbo].[team_summaries]
		FROM #ImportSeason
	END;

	ALTER TABLE [SRCBB].[dbo].[team_summaries] 
	ADD CONSTRAINT PK_team_summaries PRIMARY KEY CLUSTERED (Season, Rk, School)

GO



-- Process the opponent file
IF OBJECT_ID('tempdb..#ImportOpponent') IS NOT NULL
    DROP TABLE #ImportOpponent

	CREATE TABLE #ImportOpponent(
	Season INT NOT NULL,
	Rk INT NOT NULL,
    School NVARCHAR(40) NOT NULL,
	Games INT NOT NULL,
	Overall_W INT NOT NULL,
	Overall_L INT NOT NULL,
	win_pct FLOAT NOT NULL,
	SRS	FLOAT NOT NULL,
	SOS	FLOAT NOT NULL,
	Conf_W	INT ,
	Conf_L	INT ,
	Home_W	INT NOT NULL,
	Home_L  INT NOT NULL,
	Away_W	INT NOT NULL,
	Away_L	INT NOT NULL,
	Points_Tm	INT NOT NULL,
	Points_Opp 	INT NOT NULL, 
	MP	INT NOT NULL,
	opp_FGM	INT NOT NULL,
	opp_FGA	 INT NOT NULL,
	allow_fg_pct	FLOAT NOT NULL,
	opp_Three_P	 INT NOT NULL,
	opp_Three_PA	INT NOT NULL,
	opp_Three_P_PCT	FLOAT NOT NULL,
	opp_FT	INT NOT NULL,
	opp_FTA	INT NOT NULL,
	opp_ft_pct	FLOAT NOT NULL,
	opp_ORB	INT NOT NULL,
	opp_TRB	INT NOT NULL,
	opp_AST	INT NOT NULL,
	opp_STL	INT NOT NULL,
	opp_BLK	INT NOT NULL,
	opp_TOV	INT NOT NULL,
	opp_PF INT NOT NULL	
)
GO

BULK INSERT #ImportOpponent
FROM 'C:\Users\CHIPK\Developer\NCAA Data\import_data\original_downloads\2010_basic_opp.csv'
WITH(
FIELDTERMINATOR = ',',
ROWTERMINATOR = '\n',
FIRSTROW=3
)

GO


-- Add new columns
ALTER TABLE #ImportOpponent
	ADD allow_off_rebs_avg float,
		allow_def_rebs_avg float,
		allow_ft_att_avg float
				
GO

-- Remove the NCAA tournament indicator from school name
UPDATE #ImportOpponent
	SET School=REPLACE(School,'NCAA', '')
GO

-- compute the average offensive rebounds per game
UPDATE #ImportOpponent
	SET allow_off_rebs_avg = opp_ORB / Games
GO

-- compute the average allowed free throws attempted  per game
UPDATE #ImportOpponent
	SET allow_ft_att_avg = opp_FTA / Games
GO
-- compute the average defensive rebounds per game
UPDATE #ImportOpponent
	SET allow_def_rebs_avg = (opp_TRB - opp_ORB) / Games
GO


-- Drop unwanted columns
ALTER TABLE #ImportOpponent
	DROP COLUMN Overall_W, Overall_L, win_pct, SRS, SOS, Conf_W, Conf_L,Home_W, Home_L, Away_W, Away_L, Points_Tm, Points_Opp, MP, opp_Three_P, 
				opp_Three_PA, opp_Three_P_PCT, opp_AST, opp_BLK, opp_PF, opp_TOV, opp_STL, opp_ft_pct, opp_FGM, opp_FGA, opp_FT, opp_FTA, opp_ORB, opp_TRB
GO


-- Add new columns
ALTER TABLE [SRCBB].[dbo].[team_summaries] 
	ADD allow_fg_pct  float,
	    allow_off_rebs_avg float,
		allow_def_rebs_avg float,
		allow_ft_att_avg float
		
GO


UPDATE [SRCBB].[dbo].[team_summaries] SET 
 allow_fg_pct = o.allow_fg_pct,
 allow_off_rebs_avg = o.allow_off_rebs_avg,
 allow_def_rebs_avg= o.allow_def_rebs_avg,
 allow_ft_att_avg = o.allow_ft_att_avg
 FROM [SRCBB].[dbo].[team_summaries] t, #ImportOpponent o
 WHERE (o.Season = t.Season) AND
			(o.Rk = t.Rk) AND (o.School= t.School)
GO


SELECT *
FROM [SRCBB].[dbo].[team_summaries] 
GO

/* Alternate Update Query  Query 
UPDATE 
     t1
SET 
     t1.allow_fg_pct =       t2.allow_fg_pct,
	 t1.allow_off_rebs_avg = t2.allow_off_rebs_avg,
	 t1.allow_def_rebs_avg= t2.allow_def_rebs_avg,
	 t1.allow_ft_att_avg = t2.allow_ft_att_avg 
FROM 
     [SRCBB].[dbo].[team_summaries] t1 
     INNER JOIN #ImportOpponent t2 
     ON (t1.Season = t2.Season) AND
			(t1.Rk = t2.Rk) AND (t1.School= t2.School);

*/




