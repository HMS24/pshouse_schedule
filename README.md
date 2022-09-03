# presale

## use
...

## todo
- s3
    - add .env and from config load env, default local
- 資料沒更新 > retry
    - investigate apschedule background retry
- 重複 > examine
    - before insert, select last record and compare to current last recod
    - or store last run first record id, compare to current first row
        - if not, update last run first id
- data model > static