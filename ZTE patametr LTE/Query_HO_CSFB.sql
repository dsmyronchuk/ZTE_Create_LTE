SELECT [BSC],[Cell_ID]
,[SAC]
,[LAC]
,[RAC]
,[Site Name]
,[BSIC]
,[BCCH]
,[Azimuth]
,[Target BSC]
,[Target Cell_ID]
,[Target SAC]
,[Target LAC]
,[Target RAC]
,[Target Site Name]
,[Target BSIC]
,[Target BCCH]
,[Target Azimuth]
,[Date_Add]
,[User]
,[Distance]
FROM [rpdb].[dbo].[vExpSiemensNB] as e
WHERE e.Id_Site = (SELECT Top 1 Id_Site FROM dbo.vSiteHistory as s WHERE s.NamePoint= 'KIE CHK SBT')
and [BCCH] < 950 and [Target BCCH] < 950
ORDER BY Cell_ID ASC, Distance ASC