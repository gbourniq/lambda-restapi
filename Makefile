# Set shell
SHELL=/bin/bash -e -o pipefail

### Environment variables ###
CONDA_ENV_NAME=lambda-restapi
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate
S3_BUCKET_NAME=gbournique-s3-sam-builds
# Deployed resources
VERSION=$(shell poetry version | awk '{print $$NF}')
APP_NAME=lambda-restapi-stack
STACK_NAME=${APP_NAME}-v$$(echo ${VERSION} | tr . -)
STACK_TAGS="name=\"${APP_NAME}\" version=\"${VERSION}\""
# API Key & Usage Plan (Optional)
API_KEY_NAME=MyApiKey


### Environment and pre-commit hooks ###
.PHONY: env env-update pre-commit
env:
	@ ${INFO} "Creating ${CONDA_ENV_NAME} conda environment and poetry dependencies"
	@ conda env create -f environment.yml -n $(CONDA_ENV_NAME)
	@ ($(CONDA_ACTIVATE) $(CONDA_ENV_NAME); poetry install)
	@ ${SUCCESS} "${CONDA_ENV_NAME} conda environment has been created and dependencies installed with Poetry."
	@ ${MESSAGE} "Please activate the environment with: conda activate ${CONDA_ENV_NAME}"

env-update:
	@ ${INFO} "Updating ${CONDA_ENV_NAME} conda environment and poetry dependencies"
	@ conda env update -f environment.yml -n $(CONDA_ENV_NAME)
	@ ($(CONDA_ACTIVATE) $(CONDA_ENV_NAME); poetry update)
	@ ${SUCCESS} "${CONDA_ENV_NAME} conda environment and poetry dependencies have been updated!"
 
pre-commit:
	@ pre-commit install -t pre-commit -t commit-msg
	@ ${SUCCESS} "pre-commit set up"


### Build dependencies ###
.PHONY: build
build:
	@ rm -rf bin && mkdir -p bin/lambda-layer/python
	@ poetry export -f requirements.txt --output bin/lambda-layer/requirements.txt
	@ docker run --rm \
		-v $$(pwd):/foo \
		-w /foo \
		lambci/lambda:build-python3.8 \
		pip install -r bin/lambda-layer/requirements.txt --target bin/lambda-layer/python
	${SUCCESS} "Built dependencies into bin/lambda-layer/python"


### Testing ###
.PHONY: unit-tests get-cov-report start-fastapi-server start-api test-api-local

unit-tests:
	@ ${INFO} "Running unit tests..."
	@ pytest .
	@ ${INFO} "Run 'make open-cov-report' to view coverage details"

open-cov-report:
	@ open htmlcov/index.html

# For testing during development
start-fastapi-server:
	@ uvicorn lambda_restapi.main:app --host 0.0.0.0 --port 8080 --reload

# For integrations tests as part of CD pipeline
start-api:
	@ ${INFO} "Running local API to test incoming API Gateway Proxy events"
	@ sam local start-api --template-file integration_tests/local-api.yaml

test-api-local:
	@ python integration_tests/run_api_tests.py --server http://127.0.0.1:3000/api/


### Deployment ###
.PHONY: package deploy update get-dev-endpoint test-api-dev get-logs
package:
	@ sam package \
		--template-file sam-application/sam-template.yaml \
		--output-template-file bin/packaged.yaml \
		--s3-bucket ${S3_BUCKET_NAME}
	@ ${SUCCESS} "Final SAM template generated at bin/packaged.yaml"
	@ ${SUCCESS} "Uploaded artifacts to s3://${S3_BUCKET_NAME}"

deploy:
	@ sam deploy \
		--template-file bin/packaged.yaml \
		--capabilities CAPABILITY_IAM \
		--stack-name ${STACK_NAME} \
		--tags ${STACK_TAGS} \
		--no-fail-on-empty-changeset
	@ ${SUCCESS} "Deployed Lambda application as a Cloudformation stack: ${STACK_NAME}"

update: package deploy

get-dev-endpoint:
	@ ${INFO} "API Gateway endpoint"
	@ $(call get_dev_endpoint)
	@ ${INFO} "API Key value"
	@ $(call get_api_key_value)

test-api-dev:
	@ python integration_tests/run_api_tests.py --server "$$($(call get_dev_endpoint))" --api-key "$$($(call get_api_key_value))"

get-logs:
	@ ${INFO} "Tailing logs for the FastApiFunction Lambda function from stack '${STACK_NAME}'"
	@ sam logs -n FastApiFunction --stack-name ${STACK_NAME} --tail


### Clean up ###
.PHONY: stack-delete
stack-delete:
	@ aws cloudformation delete-stack --stack-name ${STACK_NAME}
	@ ${INFO} "Deleting all resources within the ${STACK_NAME} CloudFormation stack..."


### Helpers ###
define get_dev_endpoint
aws cloudformation describe-stacks \
	--stack-name ${STACK_NAME} \
	--query 'Stacks[].Outputs[?OutputKey==`FastApiGateway`].OutputValue' \
	--output text
endef

define get_api_key_value
aws apigateway get-api-keys \
	--include-value \
	--name-query ${API_KEY_NAME} | jq '.["items"][0]["value"]' | tr -d \"
endef


### Helpers ###
RED := "\e[1;31m"
YELLOW := "\e[1;33m"
GREEN := "\033[32m"
NC := "\e[0m"
INFO := @bash -c 'printf ${YELLOW}; echo "[INFO] $$1"; printf ${NC}' MESSAGE
MESSAGE := @bash -c 'printf ${NC}; echo "$$1"; printf ${NC}' MESSAGE
SUCCESS := @bash -c 'printf ${GREEN}; echo "[SUCCESS] $$1"; printf ${NC}' MESSAGE
WARNING := @bash -c 'printf ${RED}; echo "[WARNING] $$1"; printf ${NC}' MESSAGEs