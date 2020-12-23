[![Build Status](https://travis-ci.com/gbourniq/lambda-restapi.svg?branch=main)](https://travis-ci.com/gbourniq/lambda-restapi)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
![Pylint](.github/sam-application.svg)
![Coverage](.github/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/gbourniq/hello-lambda/blob/master/LICENSE)

## Overview
This project contains a base files and make commands to quickly develop and deploy serverless RESTful APIs running on FastAPI and deployed on AWS Lambda. An AWS API Gateway is used to make the function reachable via HTTP/S and for additional security at the API Gateway level.

Infrastructure, application code and package dependencies are managed by the AWS Serverless Application Framework, and a CI/CD build configuration pipeline is defined in the `.travis.yaml` file.


## Contents

- [Prerequisites](#Prerequisites)
- [Virtual environment and git-hooks setup](#virtual-environment-and-git-hooks-setup)
- [Build python dependencies as a Lambda layer](#build-python-dependencies-as-a-lambda-layer)
- [Local development and testing](#local-development-and-testing)
- [API Gateway and Lambda deployment to AWS](#api-gateway-and-lambda-deployment-to-aws)
- [Secure the API Gateway endpoint](#secure-the-api-gateway-endpoint)
- [Production endpoint with a Custom Domain Name](#production-endpoint-with-a-custom-domain-name)
- [CI/CD](#cicd)

## Prerequisites
- Configure the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) with your AWS credentials.
- Install [Docker](https://hub.docker.com/search/?type=edition&offering=community)
- Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) 
- Install [Poetry](https://github.com/sdispater/poetry)
- Install [Make](https://www.gnu.org/software/make/)
- Create an [AWS S3 Bucket](https://aws.amazon.com/s3/) to store application code and dependencies artifacts

## Virtual environment and git-hooks setup

To make things easy, you can create the conda environment and install the dependencies by running:
```bash
make env
conda activate lambda-restapi
```
> Note: the environment can then be updated using the `make env-udpate` command when poetry packages are modified.

A [pre-commit](https://pypi.org/project/pre-commit/) package is used to manage git-hooks. The hooks are defined in `.pre-commit-config.yaml`, and will automatically format the code with `autoflake`, `isort` and `black`, and run code analysis and testing with `pylint` and `pytest`, on each commit. To set them up, run:
```bash
make pre-commit
```

Make sure to run `source .env` to avoid import errors

## Build python dependencies as a Lambda layer 

Application code dependencies must be located at `./bin/python`, which will be used by the SAM Framework to build a Lambda layer. To package dependencies into `./bin/python`, run:
```bash
make build
```
> Lambda application code dependencies are managed by [Lambda layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html#configuration-layers-manage), which helps reduce the size of uploaded archives and make it faster to deploy your application code.

## Local development and testing

1. Set main environment variables in the following files:
- `Makefile`: for the S3 bucket name, and application name
- `sam-application/.env`: for any FastAPI and Lambda configurations

2. Run the FastAPI server to test endpoints locally
```bash
make start-fastapi-server
```

3. Run tests against the FastAPI Test Client
```bash
make test
```
> To view the unit-tests coverage report, run `make open-cov-report`

4. Run tests against the mock API Gateway, which forwards HTTP requests to the Lambda function
Start the local (mock) API Gateway with
```bash
make start-api # To run
```
> Note the above command will create a local HTTP server hosting all of your functions. When accessed (via browser, cli etc), it will launch a Docker container locally  to invoke the Lambda function

In a separate terminal, run tests against the mock HTTP server with
```bash
make test-local-api
```

## API Gateway and Lambda deployment to AWS

1. Upload application code and dependencies artifacts to AWS S3
```bash
make package
```

2. Deploy the serverless infrastructure (Lambda and API Gateway) and application code + dependencies

```bash
make deploy
```
> Note the above 2 commands can be run subsequently with a convenient `make update` command. If the package dependencies are updated, please make sure to run `make build` first.

3. Utilities commands:
- `make get-dev-endpoint`: Retrieve the API Gateway Endpoint URL & the API Key (if configured).
- `make get-logs`: Tail Lambda logs from CloudWatch Logs into the terminal.
- `make stack-delete`: To delete the deployed stack resources: API Gateway and Lambda function


## Secure the API Gateway endpoint

The API Gateway integration allows for the Lambda function to be reachable via HTTP/S. To view the endpoint URL, run `make get-dev-endpoint`. This public endpoint is not secured by default, which means anyone can access it and potentially occur unwanted costs. 

To secure the endpoint, the API Gateway `dev` deployment stage needs to be associated with an `API Key` and `API Usage Plan`, from within the API Gateway online portal. Then please take note of the API Key name and update the `API_KEY_NAME` variable in the `Makefile`.

You can ensure the API is now secured, by running
```bash
make check-api-is-secured
```

## Production endpoint with a Custom Domain Name

1. Follow the steps in [Setting up a regional custom domain name in API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-regional-api-custom-domain-create.html)
2. In the API Gateway portal, the desired API version to new API deployment stage, eg. called `prod`
3. Navigate to the Custom Domain API Mappings section and map the `prod` stage to a desired path (eg. `api`) to be able to access the API via `https://<custom-domain-name/api/` instead of the default API Gateway Endpoint `https://<ApiGtwId>.execute-api.eu-west-2.amazonaws.com/prod/`
5. In the API Gateway settings, disabled the default API Gateway Endpoint so that Lambda can only be reached by the production / custom domain name.

## CI/CD

The `.travis.yml` build configuration file defines the following CI/CD pipeline:

* Continuous Integration
```
make env                          <-- Create conda environment and install dependencies
conda activate lambda-restapi     <-- Activate conda environment
make test                         <-- Run unit-tests against the built-in FastAPI Testing server
```

* Continuous Deployment
```
make build                        <-- Build Python dependencies as a Lambda layer
make start-api &                  <-- Start a local mock API Gateway server as a background process
make test-local-api               <-- Run unit-tests against the mock API Gateway server
make package                      <-- Upload application code and Lambda layer to S3
make deploy                       <-- Deploy/Update the Cloudformation stack: API Gateway and Lambda
make check-api-is-secured         <-- Ensure the API Gateway endpoint is secured with an API Key
make check-healthcheck-endpoint   <-- Ping the healthcheck endpoint with the API Key
```

Note that the following secret environment variables must be set in the Travis Repository settings, so that the Travis server can deploy and update AWS resources.
```bash
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION
```

#### Additional resource to your application
The application template `sam-template.yaml` uses AWS Serverless Application Model (AWS SAM) to define [serverless application resources](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-resources-and-properties.html) such as Lambda, API Gateway, DynamoDB, etc.

AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) to extend the template.










