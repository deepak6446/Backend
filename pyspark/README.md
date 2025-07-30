## Getting started on local

### Docker

Docker version 20.10.5

- Build docker Image </br>
  `docker image build -t spark-local .`
- Run docker Image </br>
  `docker run --name spark-local -p 8000:8081 -p 18080:18081 -v /Users/deepak.poojari/Desktop/deepak_work/<repo>/:/<repo> -dit spark-local`
- Move into docker Image </br>
  `docker exec -it spark-local /bin/bash`</br>
  run all below commands inside docker
- Master node
  - Start: `/spark-3.0.2-bin-hadoop3.2/sbin/start-master.sh`
  - UI : on local: `http://localhost:8000/ (port may change check logs)`
  - Stop : `/spark-3.0.2-bin-hadoop3.2/sbin/stop-master.sh`
- Spark worker
  - start: `/spark-3.0.2-bin-hadoop3.2/sbin/start-slave.sh spark://1e22f81c753a:7077 (master url from master logs)`
  - stop: `/spark-3.0.2-bin-hadoop3.2/sbin/stop-slave.sh`
- History server </br>
  - start: `/spark-3.0.2-bin-hadoop3.2/sbin/start-history-server.sh`
  - stop : `/spark-3.0.2-bin-hadoop3.2/sbin/stop-history-server.sh`
  - UI: http://localhost:18080/
- Make</br>
  Make file is used to build Pyspark project.</br>
  commands (run under dir: <repo>)
  - `make build-local`: This will just build the changed .py files, runs faster.
  - `make build-dep-local`: Use this when any third party package is changed.
  - `make build-prod`: Used to build package for production.
  - `make run`: run spark job on local or pro
  - `make build-local && time make run 2>&1 | tee ./log.log`
- Pylint
  - python3 -m pip install -r requirements.txt
  - make pylint
- Test your code.</br>
  `make test`

## Running spark in production

- Following packages should be installed with version specified
  - Python 3.8.2
  - Java 11.0.10
  - Spark 3.0.1, hadoop 2.7
  - Download packages</br>
    $SPARK_HOME/bin/spark-shell --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1
  - Docker 20.10.5 for building stage
  - Make
- Running test case
  - make test
- Build package
  - make build-prod
- Submit spark job </br>
  Make job dates or any config changes in config.json</br>
  `spark-submit --py-files dist/jobs.zip,dist/shared.zip,dist/libs.zip,dist/schema.zip --files config.json dist/main.py --job ui --start_date yyyy-mm-dd --end_date yyyy-mm-dd`
  or
  `spark-submit --py-files dist/jobs.zip,dist/shared.zip,dist/libs.zip,dist/schema.zip --files config.json dist/main.py --job ui --start_date yyyy-mm-dd-hh --end_date yyyy-mm-dd-hh`

## Deployment

Follow ReadMe in deployment folder for deployment details

## Deployment of azure functions

Follow Readme in deployment/azure/functions folder for details

## Project Structure

Get new tree structure using: `tree -L 3 --dirsfirst`

<pre>
├── dist
│   ├── libs
│   ├── config.json
│   ├── jobs.zip
│   ├── libs.zip
│   ├── main.py
│   ├── schema.zip
│   └── shared.zip
├── env
│   ├── bin
├── spark-config
│   └── spark-history.conf
├── src
│   ├── jobs
│   │   ├── __init__.py
│   │   └── ui.py
│   ├── schema
│   │   ├── __init__.py
│   │   └── ui.py
│   ├── shared
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── reader.py
│   │   ├── udfs.py
│   │   ├── utils.py
│   │   └── writer.py
│   └── main.py
├── test-data
│   ├── logs
│   │   └── ui.log.gz
│   └── parquet
│       └── ui
├── Makefile
├── README.md
├── config.json
└── requirements.txt
</pre>
