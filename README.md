# pre-sale house schedule

實價登錄 ETL job

每月 1、11 及 21 號從內政部擷取電子檔，並檢查 job 是否完成，若無則過 1 小時再重新執行。</br>
以 `APScheduler` 排程。首先擷取資料並上傳 AWS S3 備份。其次利用 `Pandas` 做轉換及過濾處理，最後新增資料到 ＭySQL。
    
## 如何使用
    
設置環境變數

    $ cp .env.example .env

建立並部署

    $ ./run.sh --target local

    預設映像檔名稱及版本: `local/pshs:latest`

## 架構

```shell
.
├── build
│   ├── build.sh
│   ├── test.sh                 # 啟動一個 container 跑測試
│   ├── push.sh
│   └── Dockerfile
├── deploy               
│   ├── deploy.sh           
│   └── publish.sh              # 在遠端機器部署的 script
├── pshouse_schedule
│   ├── db
│   │   ├── database.py
│   │   ├── models.py
│   │   └── stores.py
│   ├── jobs.py                 # 定義 job 及 event handlers
│   ├── processes.py            # ETL jobs
│   ├── fetch.py           
│   ├── parse.py
│   ├── load.py
│   ├── storage.py
│   ├── schemas.py              # validate 及 type conversion
│   ├── utils.py
│   ├── config.py
│   └── exceptions.py
├── tests                                       
├── results
├── .env                    
├── app.py                      # 程式入口
├── boot.sh                     # container entrypoint script
├── compose.yml
└── run.sh                      # 執行 build and deploy 的 script
```

## 其他
[筆記](https://github.com/HMS24/pshouse_schedule/blob/master/assets/note.md)