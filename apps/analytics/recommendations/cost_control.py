SQL_SCRIPT = """SELECT
        entity_id,
        CAST(DATE_FORMAT(date_of_business,"%Y-%m-%d") AS DATE) as date,
        sum(data_value) as revenue,
        DAY(date_of_business) as featDay,
        WEEK(date_of_business) as featWeek,
        MONTH(date_of_business) as featMonth,
        YEAR(date_of_business) as featYear
    FROM `cc_costcontrol_data` as CoCo
    WHERE type_id = 2 and 
            entity_id = %s
    GROUP BY
        entity_id,
        DAY(date_of_business),
        DAYOFWEEK(date_of_business),
        WEEK(date_of_business),
        MONTH(date_of_business),
        YEAR(date_of_business)
    ORDER BY date_of_business"""
