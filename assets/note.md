# 一些筆記及想法

## 關於 Database

原本是與 [pshouse](https://github.com/HMS24/pshouse) project 一起開發，後來覺得 code 太雜拆分 2 個專案分別開發。 schedule 關注排程是否有被正確的執行，以及資料是否完整的存入資料庫。

而 [pshouse](https://github.com/HMS24/pshouse) 是由 `Flask` 框架開發的 web application，關注的是最終使用者的需求。呈現單頁實價登錄以客製化我自己的需求😃。另外還能快速搜尋關鍵字及排序。

因此，目前兩邊的 database 是共用的。並由 web 那邊做 migrate。缺點就是必須維護兩邊的 model 層。schedule 僅去擷取並插入資料而已。
另外如果這邊也用一個 database 存資料，再由 web 那邊打 API 進來拿...會大幅增加開發成本。

最後 database 的建置是以 container 的方式啟動，並寫在 web 的 `compose.yml` 裡，然後 mount volume(db_data) 在 host 上，會造成一些不便。因為我將 app 跟 db 放在同一個 container bridge 的 networks 之中，當要部署 schedule 時得確保 web 那邊的 database 先 run 起來，而 schedule 這邊才能去 link db...有點繞。

解決方式是把 database 服務拆出來，最簡單就是使用 AWS rds 的服務。

## 關於 Schedule

schedule 方面

1. Crontab
2. APscheduler
3. Airflow
4. AWS Lambda 設定 event 及 rate

`1` 目前需求為一個 cronjob，不過這個專案之後想做的排程 cronjob 不算少，因此管理上不方便。

`2` 僅用 python 就能解決，相對 `1` 符合未來 cronjob 的擴充，但目前版本僅有 default 的 event，且無法控制何時 emit event 及 custom event type，得找其他 package 輔助，顯然有點美中不足。

`3` 架設 airflow server 以 configuration as code 建造 ETL。看了一下有蠻多功能，可以 task 重跑也可以將 task 組合成不一樣的 ETL 流程，感覺是項利器。

`4` 以 cloud 的方式相對不熟。

先選 `2` 的方式開發。

## 關於 test
- `test_fetch.py` mock 掉 requests 及檢查更新的 function，測試 fetch 邏輯。
- `test_parse.py` 測試資料整理的邏輯。
- `test_save.py` mock 掉 storage class 測試 save 功能，檔案是否存在。
- `test_process.py` mock 掉 各種操作，主要驗證流程以及錯誤處理。

另外關於 `load.py` 的測試，需要 mock 掉 database 以作隔離，不過尚未實作。

## 關於 modules

### modules 邏輯順序：

<p align="center">
<img src="./module_order.jpeg" alt="scheduler" width="1080"/>
</p>

### modules 說明：

- `boot.sh`: 未來如要保證 container 的啟動順序，需增加 wait for db 的 script，可以不用再 build image，以節省時間。
- `app.py`: start schedule and keeps the main thread alived.
- `jobs.py`: 定義 cronjob 及所調用的 process。包含 `APScheduler` 預設的事件處理 handlers
- `processes.py`: 主要的流程處理 functions。
- `fetch.py`: 擷取資料的 functions。
- `parse.py`: 資料擷取後的處理會轉換中英欄位、移除英文標題列、日期轉換至西元日期、填補各欄空值及新增 `city` 欄位。
- `load.py`: 資料插入 MySql 資料庫。
- `storage.py`: 用 `cloudstorage` 實作的 storage 介面，可以根據 `.env` 的 `STORAGE_TYPE` 選擇上傳本地或雲端(S3)
- `schemas.py`: 存入 database 前將欄位資料轉型並做基本的 validate。
- db
    - `database.py`: 有實作 session 的 context manager，以便統一管理 session 的 rollback 及 close。
    - `models.py`:  database table 的抽象層。
    - `stores.py`: 操作 database 的邏輯層。因為需求簡單，所以直接在這個 module 操作 model 而非用 __init__ 的方式傳進去。
- build
    - `build.sh`: 指定特定 platform (linux/amd64)，與要部署的遠端機器 OS 一致。
    - `test.sh`:  run container 並且安裝 pytest 跑測試
    - `push.sh`: 登入 docker 推至 hub
- deploy
    - `deploy.sh`: 將 compose.yml, .auth 及 publish.sh 傳至遠端機器準備部署
    - `publish.sh`: 部署 script

## 關於流程

### 流程圖

<p align="center">
<img src="./all.jpg" alt="all" width="1680"/>
</p>

### 流程說明

- scheduler 新增 crawl cronjob
- 每月 1, 11, 21 早上 10:00 觸發該 job。
- 以 9/21 為例，查看內政部上期的資料有無更新至 9/11
    - 有
        - fetch 9/21 資料
        - 將 fetched 的內容備份至 S3
        - parse content:
            - 沒問題的 records 插入 database
            - 有問題的則轉回中文欄位(人工校對比較方便)，存成 json 備份至 S3
    - 沒有，return
- `APScheduler` 發送 JOB EXECUTED 事件
- listener 判斷是否為 crawl cronjob
    - 是，呼叫 handler
        - scheduler 新增 check crawl 的 job
    - 否，exit
- scheduler 立即執行 check crawl job
    - 判斷剛才抓到的檔案日期是否為 9/21
        - 是， continue
        - 否， raise exception
    - 判斷插入 database 的最後一筆 created_at 是否為當日(代表資料存進 database)
        - 是， continue
        - 否， raise exception
- 若上一步沒有 raise some exception，則 9/21 的資料已抓到
- 若有 raise exception，`APScheduler` 發送 JOB ERROR 事件
- listener 判斷是否為 check crawl 的 job 及符合的 exception type
    - 是，呼叫 handler
        - scheduler 新增 1 小時之後的 crawl cronjob
    - 否，exit

## 關於 TODO

- [ ] 用 raw SQL statement 新增統計表。
    找出新北市淡水區一年內新開預售案，並統計各案 1、3 及 6 個月期間，其 10 坪以下、20 坪、30 坪及 40 坪以上各別的平均單價及總價。
    這一段想用 raw SQL statement 執行，直接 transform data。未來當其他縣市資料也加進來時因為資料很多，可以考慮直接從 S3 copy 進 Redshift(data warehouse)，那時候單純 sql 查詢的效率會比較高。而且若寫在 python 這邊處理，可能資料量太大，記憶體 load 不進來(自己猜測)
    
    steps:
    1. 接在 check process 之後，當確認沒問題則開始這一段 transform process
    2. models 新增 deal_statistics table
    3. ```sql
            INSERT INTO deal_statistics
            SELECT * FROM deals
            WHERE ...
            GROUP BY ...
        ```
    4. 新增 check deal_statistics process(是否有必要？)

- [ ] 不正確的紀錄，經人工校正再 insert into database。
- [ ] 定期 mysql dump，目前可以直接抹掉整張 table，但未來如果 web application 可以開放 api 從前端 update 不正確的資訊，就需要定期備份。
- [ ] transform_to_deal_statistics，沒有 truncate table
- [ ] deal_statistics 的 avg_house_unit_price type int 改 float

## 關於 pattern

state machine...
