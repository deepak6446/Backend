# Running test cases 
test:
	pytest tests
# Create production build
build-prod: rmdir build pipdep

build-prod-azure: rmdir build pipdep-azure

# Build on local without reinstalling dependency to speed up build
build-local: build

# Build on local with installing dependency (use when requirements.txt changes)
build-dep-local: rmdir build pipdep

build-dep-local-azure: rmdir build pipdep-azure

# Remove dist folders
rmdir: 
	rm -rf ./dist && mkdir ./dist

build:
	# dist contains all files required to be zipped for spark
	cp ./src/main.py ./dist
	cp ./config.json ./dist
	rm -rf dist/jobs.zip
	rm -rf dist/shared.zip
	rm -rf dist/schema.zip
	cd src; zip -r ../dist/jobs.zip jobs
	cd src; zip -r ../dist/shared.zip shared
	cd src; zip -r ../dist/schema.zip schema

pipdep:
	# install any third party libs using docker so that it stays platform independent
	# To develop faster on local copy dist/libs.zip and comment docker command.
	# docker run --rm -v ${PWD}:/foo -w /foo lambci/lambda:build-python3.7 
	pip install -r requirements.txt -t ./dist/libs
	cd ./dist/libs && zip -rm -D ../libs.zip . && cd ../ && rm -rf libs

pipdep-azure:
	# install any third party libs using docker so that it stays platform independent
	# To develop faster on local copy dist/libs.zip and comment docker command.
	# docker run --rm -v ${PWD}:/foo -w /foo lambci/lambda:build-python3.7 
	/opt/conda/envs/py35new/bin/pip install -r requirements_azure.txt -t ./dist/libs
	cd ./dist/libs && zip -rm -D ../libs.zip . && cd ../ && rm -rf libs

run: 
	spark-submit --conf spark.default.parallelism=120 --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 --py-files dist/jobs.zip,dist/shared.zip,dist/libs.zip,dist/schema.zip --files config.json dist/main.py --job cdn api ui images assets graphql launch_api launch_deployer launch_manager launch_server automations_api automations_engine cma_branches data_dog_cost --start_date "2021-03-27" --end_date "2021-03-27"

pylint-azure:
	# Install packages in env
	# Install package to check if all code package exist in requirements.txt
	 ( \
       /opt/conda/envs/py35new/bin/pip install -r requirements_azure.txt; \
	   pylint ./src/*/*.py ./src/main.py; \
    )
pylint:
	# Install packages in env
	# Install package to check if all code package exist in requirements.txt
	 ( \
       source env/bin/activate; \
       python3 -m pip install -r requirements.txt; \
	   pylint ./src/*/*.py ./src/main.py; \
    )