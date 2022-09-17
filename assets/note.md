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