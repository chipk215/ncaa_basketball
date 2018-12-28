SELECT [t].[school_ncaa]
FROM [NCAA_Basketball].[dbo].[D1_teams] as t
Group By t.school_ncaa
ORDER BY t.school_ncaa


SELECT School   
  FROM [SRCBB].[dbo].[team_summaries]
  Group BY School
  ORDER BY School


--- matches
SELECT [t].[school_ncaa], t.id, s.school as sr_school
FROM [NCAA_Basketball].[dbo].[D1_teams] as t
INNER JOIN  [SRCBB].[dbo].[team_summaries] s ON t.school_ncaa = s.school
GROUP BY t.school_ncaa , t.id, s.school




--- identify unmatched teams
SELECT[t].[school_ncaa], t.id, s.school as sr_school
FROM [NCAA_Basketball].[dbo].[D1_teams] as t
    FULL JOIN[SRCBB].[dbo].[team_summaries] s ON (t.school_ncaa = s.school)
WHERE t.school_ncaa IS NULL OR s.school IS NULL
GROUP BY t.school_ncaa ,t.id, s.school