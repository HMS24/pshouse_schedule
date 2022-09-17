# pshouse schedule
pre-sale house schedule

## 描述

關於**預售屋實價登錄**的 EtLT 實作，定期於每月 1, 11, 21 日上內政部網站下載預售屋實價登錄，自動化檢查資料是否已更新至資料庫。

首先擷取到資料後先上傳 AWS S3 備份，其次利用 `pandas` package 做資料的前處理，再存進 ＭySql 資料庫落地應用。最後儲存明顯有問題的幾筆實價登錄並由人工校正。運作方式以 container 的方式部署到 AWS EC2 上執行。另外流程結束後確認資料是否有被下載及存進資料庫，若無則 1 小時候再做一次。

**限制 1: 目前僅抓新北市的預售屋實價登錄，歷史資料包含 2021 第 2 季至 20220911(本期最新)。**
    
## 如何使用

### 前置作業

要部署到遠端機器，假設目標機器 OS 為 `Ubuntu 20.04`:
1. 安裝 `docker` and `docker compose`
2. 新增資料夾 `mkdir ~/pshs` (`./deploy/publish.sh` 有寫入資料夾的名稱 )
3. 設置環境變數 `cd ~/pshs && vi .env`
4. 環境變數
    - `TOKEN`

### 本地部署
    
設置環境變數

    $ cp .env.example .env

建立映像檔並部署。預設映像檔名稱及版本: `local/pshs:latest`

    $ ./run.sh --target local

查看 log

    $ docker logs -f pshs
    
    2022-09-01 00:50:17 [INFO] Adding job tentatively -- it will be properly scheduled when the scheduler starts
    2022-09-01 00:50:17 [INFO] Added job "crawl_deals" to job store "default"
    2022-09-01 00:50:17 [INFO] Scheduler started

### 遠端部署

建立映像檔上傳 docker hub 並部署，預設映像檔名稱:`$DOCKER_USER/$IMAGE:$TAG`

    $ ./run.sh --target $REMOTE_MACHINE \
               --ssh-pem $REMOTE_MACHINE_PEM_PATH \
               --docker-user $DOCKER_USER \
               --docker-pass $DOCKER_PASSWORD_PATH \
               --image $IMAGE \
               --tag $TAG \
               --init $INIT_DATABASE

Parameters
- `REMOTE_MACHINE`: 遠端機器 (user@hostname)
- `REMOTE_MACHINE_PEM_PATH`: pem 檔案位置 ("$HOME/***.pem")
- `DOCKER_USER`: docker 使用者
- `DOCKER_PASSWORD_PATH` docker 密碼檔案位置 ("$HOME/***")
- `IMAGE`(optional): 映像檔名稱
- `TAG`(optional) 映像檔 tag
- `INIT_DATABASE`(optional) 重置 database (0|1) 1 會 truncate table，再插入歷史資料。預設 0

## 架構

```shell
.
├── build
│   ├── build.sh
│   ├── test.sh                 # run container to test
│   ├── push.sh
│   ├── Dockerfile
├── deploy               
│   ├── deploy.sh           
│   ├── publish.sh              # 遠端啟動的 script
├── pshouse_schedule
│   ├── db
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── stores.py
│   ├── jobs.py                 # 定義 scheule 的 job 及 event handlers
│   ├── processes.py            # 流程處理的 functions
│   ├── fetch.py           
│   ├── parse.py
│   ├── load.py
│   ├── storage.py
│   ├── schemas.py             # validate 及 type conversion
│   ├── utils.py
│   ├── config.py
│   ├── exceptions.py
├── tests                       # 測試                 
├── results                     # 存抓下來的 csv 檔
├── .env                    
├── app.py                      # 程式入口
├── boot.sh                     # run container 的 entrypoint script
├── compose.yml
└── run.sh                      # 執行 build and deploy 的 script
```

### modules 說明：

- `boot.sh`: container entrypoint script。未來如要確保 container 的啟動順序，會增加像是 wait for db 的 script，而不用再重新 build image。
- `app.py`: start schedule and keeps the main thread alived
- `jobs.py`: 定義 job 執行的方式(cron or interval) 及調用的 process。另外包含 `APScheduler` 預設的事件處理 functions
- `processes.py`: 主要的流程處理。
- `fetch.py`: 擷取資料的 functions。
- `parse.py`: 資料擷取後的處理，轉換中英欄位、移除英文標題列、轉換至西元日期、填補各欄空值及新增 `city` 欄位。
- `load.py`: 存進 MySql 資料庫，會 import db 資料夾裡的 store 來操作 db。
- `storage.py`: 用 `cloudstorage` 實作的 storage 介面，可以根據 `.env` 的 `STORAGE_TYPE` 選擇上傳本地或雲端(S3)
- `schemas.py`: 存入 database 前將欄位資料轉型並做基本的 validate。
- `db`
    - `database.py`: 有實作 session 的 context manager，統一管理 session 的 rollback 及 close。
    - `models.py`:  database table 的抽象層。
    - `stores.py`: 操作 database 的邏輯層。因為需求簡單，所以直接在這個 module 操作 model 而非用 __init__ 的方式傳進去。
- `build`
    - `build.sh`: 指定特定 platform (linux/amd64)，與要部署的遠端機器 OS 一致。
    - `test.sh`:  run container 並且安裝 pytest 跑測試
    - `push.sh`: 登入 docker 推至 hub
- `deploy`
    - `deploy.sh`: compose.yml, .auth 及 publish.sh 傳至遠端機器準備部署
    - `publish.sh`: 部署 script

### 流程圖

<p align="center">
<img src="./assets/all.jpg" alt="all" width="1680"/>
</p>

### 流程說明

- scheduler 新增 crawl cronjob
- 每月 1, 11, 21 早上 10:00 觸發該 job，以 9/21 為例
- 查看內政部**上期**的資料有無更新至 9/11
    - 有
        - 開始 fetch
        - 將 fetched 的內容上傳至 S3 備份
        - parse data:
            - 沒問題的 records 則插入 database
            - 有問題的則轉換至中文欄位(人工校對比較方便)，存成 json 上傳 S3
    - 沒有 return
- `APScheduler` 發送 JOB EXECUTED 事件
- 監聽器判斷是否為 crawl cronjob
    - 是 呼叫 handler
        - scheduler 新增 check crawl 的 cronjob
    - 否 exit
- 立即觸發 check crawl cronjob
    - 判斷剛抓到的檔案日期是否為 9/21
        - 是則 continue
        - 否則 raise exception
    - 判斷插入 database 的最後一筆 created_at 是否為當日(代表資料存進 db)
        - 是則 continue
        - 否則 raise exception
- 若上一步沒有 raise some exception，則 9/21 的資料已抓到
- 若有 raise exception，`APScheduler` 發送 JOB ERROR 事件
- 監聽器判斷是否為 check crawl 的 cronjob，以及上述的 exception type
    - 是則呼叫 handler
        - scheduler 新增 1 小時之後的 crawl cronjob
    - 否 exit

<!-- - Scheduler:

<p align="center">
<img src="./assets/scheduler.jpeg" alt="scheduler" width="300"/>
</p>

- Crawl process:

<p align="center">
<img src="./assets/crawl_job.jpeg" alt="crawl" width="300"/>
</p>

- Check process:

<p align="center">
<img src="./assets/check_job.jpeg" alt="check" width="300"/>
</p>

- Job executed listener

<p align="center">
<img src="./assets/job_executed_listener.jpeg" alt="executed_listener" width="300"/>
</p>

- Job error listener

<p align="center">
<img src="./assets/job_error_listener.jpeg" alt="error_listener" width="300"/>
</p> -->

## 未來想要

- 新增統計表。
    找出新北市淡水區一年內新開的預售案，統計各案 1、3 及 6 個月其 10 坪以下、20 坪、30 坪及 40 坪以上的平均單價及總價。
    這一段想寫 raw SQL statement 執行，直接 transform data。
    未來當其他縣市資料也加進來時因為資料很多，可以考慮直接從 S3 copy 進 Redshift(data warehouse)，那時候單純 sql 查詢的效率會比較高。而且若寫在 python 這邊處理，可能資料量太大，記憶體 load 不進來(自己猜測)
    
    1. 接在 check process 之後，當確認沒問題則開始這一段 transform process
    2. models 新增 deal_statistics table
    3. ```sql
            INSERT INTO deal_statistics
            SELECT * FROM deals
            WHERE ...
            GROUP BY ...
        ```
    4. 新增 check deal_statistics process(是否有必要？)

- 不正確的紀錄，經人工校正再 insert into database。
- 定期 mysql dump，目前可以直接抹掉整張 table，但未來如果 web application 可以開放 api 從前端 update 不正確的資訊，就需要定期備份。

## 雜記

### 關於 Database

原本是與 pshouse project 一起開發，後來覺得 code 太雜拆分 2 個專案分別開發。 schedule 關注排程是否有被正確的執行，以及資料是否完整的存入資料庫。

而 pshouse 是由 flask 框架開發的 web application，關注的是最終使用者的需求。呈現單頁實價登錄以客製化我自己的需求😃。
另外還能快速搜尋關鍵字及排序。

因此，目前兩邊的 database 是共用的。並由 web 那邊做 migrate。缺點就是必須維護兩邊的 model 層。schedule 僅去擷取並插入資料而已。
另外如果這邊也用一個 database 存資料，再由 web 那邊打 API 進來拿...會大幅增加開發成本。

最後 database 的建置是以 container 的方式啟動，並寫在 web 的 `compose.yml` 裡，然後 mount volume(db_data) 在 host 上，會造成一些不便。因為我將 app 跟 db 放在同一個 container bridge 的 networks 之中，當要部署 schedule 時得確保 web 那邊的 database 先 run 起來，而 schedule 這邊才能去 link db...有點繞。

解決方式是把 database 服務拆出來，最簡單就是使用 AWS rds 的服務。

### 關於 Schedule

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

### 關於測試