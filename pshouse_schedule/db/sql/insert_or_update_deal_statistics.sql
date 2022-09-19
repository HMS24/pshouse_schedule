INSERT INTO deal_statistics (
  city, district, `year`, `month`, build_name, 
  room, count_num, avg_total_price, 
  avg_house_price, avg_house_unit_price
) 
SELECT 
  tmp.city, 
  tmp.district, 
  tmp.`year`, 
  tmp.`month`, 
  tmp.build_name, 
  tmp.room, 
  tmp.count_num, 
  tmp.avg_total_price, 
  tmp.avg_house_price, 
  tmp.avg_house_unit_price 
FROM 
  (
    SELECT 
      d.city, 
      d.district, 
      year(now()) AS `year`, 
      month(d.transaction_date) AS `month`, 
      d.build_name, 
      d.room, 
      count(*) AS count_num, 
      round(
        avg(d.price / 10000), 
        0
      ) AS avg_total_price, 
      round(
        avg(
          (price - parking_sapce_price) / 10000
        ), 
        0
      ) AS avg_house_price, 
      round(
        avg(
          (
            (price - parking_sapce_price) / (
              (
                building_total_area - parking_sapce_total_area
              ) * 0.3025 * 10000
            )
          )
        ), 
        1
      ) AS avg_house_unit_price 
    FROM 
      deals AS d 
    WHERE 
      d.transaction_date >= makedate(
        year(now()), 
        1
      ) 
      AND d.city = '新北市' 
      AND d.district = '淡水區' 
      AND d.object_of_transaction = '房地(土地+建物)+車位' 
      AND d.main_use = '住家用' 
    GROUP BY 
      d.city, 
      d.district, 
      year(now()), 
      month(d.transaction_date), 
      d.build_name, 
      d.room 
    ORDER BY 
      d.build_name, 
      `year`, 
      `month`, 
      d.room
  ) AS tmp 
  ON duplicate KEY UPDATE count_num = tmp.count_num, 
  avg_total_price = tmp.avg_total_price, 
  avg_house_price = tmp.avg_house_price, 
  avg_house_unit_price = tmp.avg_house_unit_price;
