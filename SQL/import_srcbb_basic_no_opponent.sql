

IF (EXISTS (SELECT *
					FROM INFORMATION_SCHEMA.TABLES
					WHERE TABLE_SCHEMA = 'dbo'
					AND TABLE_NAME = 'team_summaries'))
	BEGIN
		PRINT N'team_summaries table exists.'
	END
ELSE
	BEGIN
		PRINT N'team_summaries table does not exist. Creating table...'
		CREATE TABLE [SRCBB].[dbo].[team_summaries] (
			Season					INT NOT NULL,
			School					NVARCHAR(40) NOT NULL,
			Games					INT NOT NULL,
			SRS						FLOAT ,
			SOS						FLOAT ,
			win_pct					FLOAT NOT NULL,
			pts_avg					FLOAT,
			opp_pts_avg				FLOAT,
			fg_pct					FLOAT,
			allow_fg_pct			FLOAT,
			ft_pct					FLOAT, 
			allow_ft_att_avg		FLOAT,
			poss_avg				FLOAT,
			off_rebs_avg			FLOAT,
			allow_off_rebs_avg		FLOAT,
			def_rebs_avg			FLOAT,
			allow_def_rebs_avg		FLOAT,
			to_avg					FLOAT,
			steal_avg				FLOAT,
			off_rating				FLOAT,
			ft_att_avg				FLOAT,

			PRIMARY KEY (Season, School)	
		)
	END
GO


-- Drop the temporary table used to import the season's team data
IF OBJECT_ID('tempdb..#ImportSeason') IS NOT NULL
    DROP TABLE #ImportSeason
	

CREATE TABLE #ImportSeason(
	Season INT NOT NULL,
	Rk INT,
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
	MP	INT,
	FGM	INT NOT NULL,
	FGA	 INT NOT NULL,
	fg_pct	FLOAT NOT NULL,
	Three_P	 INT NOT NULL,
	Three_PA	INT NOT NULL,
	Three_P_PCT	FLOAT NOT NULL,
	FT	INT NOT NULL,
	FTA	INT NOT NULL,
	ft_pct	FLOAT NOT NULL,
	ORB	INT,
	TRB	INT NOT NULL,
	AST	INT NOT NULL,
	STL	INT NOT NULL,
	BLK	INT NOT NULL,
	TOV	INT NOT NULL,
	PF INT NOT NULL
)
GO

BULK INSERT #ImportSeason
FROM 'C:\Users\CHIPK\Developer\NCAA Data\import_data\SRCBB_basic_2018.csv'
WITH(
FIELDTERMINATOR = ',',
ROWTERMINATOR = '\n',
FIRSTROW=3
)

GO



-- Remove the NCAA tournament indicator from school name
INSERT INTO [team_summaries] (Season, 
							  School,
							  Games,
							  SRS,
							  SOS,
							  win_pct,
							  pts_avg,
							  opp_pts_avg,
							  fg_pct,
							  ft_pct,
							  poss_avg,
							  off_rebs_avg,
							  def_rebs_avg,
							  to_avg,
							  steal_avg,
							  ft_att_avg
							  )
    SELECT  Season, 
			REPLACE(School,'NCAA', ''),
			Games,
			SRS,
			SOS,
			win_pct,
			Points_Tm / Games,
			opp_pts_avg= Points_Opp / Games,
			fg_pct,
			ft_pct,
			(FGA - (ORB/TRB) * 1.07 * (FGA-FGM) + TOV + 0.4 * FTA) / Games,
			ORB / Games,
			(TRB - ORB) / Games,
			TOV / Games,
			STL / Games,
			FTA / Games

    FROM [#ImportSeason]; 
GO

-- compute the offensive rating
UPDATE [team_summaries]
	SET off_rating= 100 * pts_avg / poss_avg
GO



DELETE FROM [SRCBB].[dbo].[team_summaries] WHERE (School = 'Centenary (LA)') 

SELECT *
FROM [SRCBB].[dbo].[team_summaries] 
GO





