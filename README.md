Contents
=========
 * [Features](#features)
 * [Usage](#usage)
   * [Run](#run)
   * [Parameters](#parameters)
 * [Architecture](#architecture)
   * [Flow](#flow)
   * [Diagrams](#diagrams)
 * [Support](#support)
 
   
 
 
 
Features
--------
 
- Provides unit test and regression test solutions.
- Can take input data from sql statements, sql scripts or even from the local file system using snowsql cli.
- Provides a cumulative test reports of total number test cases and success.
- Accepts different types of test configuration files like - json, yaml etc.
- Supports variety of resources like - filesystem, git and s3.
- Can be extended in future. 


Usage
-----

We will see how to use the framework in action. But before that there are some prerequisities.

Pre-requisites:-
 - Make sure the snowsql CLI program is installed. (this is needed to ingest data from local system into the snowflake warehouse).
 - python 3.6+ is recommended.
 - the dependencies needs to be installed . (PyYAML, boto3, pycryptodome, snowflake-connector-python)
   to install a dependency you can use >pip install module_name

### Run
python runner.py execute-one fs xunit /Users/deepak/PycharmProjects/rfk-sql-test-framework/test/files/running_config_be_step1_inventory_shoulbe.json

### Parameters

|  attribute|type  |required |                description 					                                      |              example |
|-----------|------|---------|-----------------------------------------------------------------------|----------------------|
| name 		|string  |mandatory | name of the configuration | test_inventory_step1 |
|author |string|optional | author of the config | ABC |
|date | string | optional | date | 20180723 |
|sql_path |string | mandatory | path where all the test files, scripts will be searched when executing the conf file | /user/abc/tests |
|script_path | string | mandatory | actual sql script to run | ../be/workflow_step1_inventory_triggers_hourly.sql
| before_once | array| mandatory| it can be a an array of sql statements or keys or scripts, executed only once for the entire configuration file| ["INSERT INTO TABLE1..","$INSERT2"]
| before_each| do | do | same as before_once, only things is it is executed for each test case | do|
| before_test | do | do | executed before each test. put all the test case specific queries here | do |
|asserts | array of objects | mandatory | | |
|sql | string | mandatory | can be a sql statement. query to compute the actual and expected query diff | |
|expected | array | mandatory | array of sql statements to load the data into the expected tables | |


Architecture
------------

### Flow
 1. The "Runner" acts as  the bootstrap of the framework. It scans the command line arguments like - python runner.py execute-one fs xunit /Users/deepak/PycharmProjects/rfk-sql-test-framework/test/files/running_config_be_step1_inventory_shoulbe.json
 2. The first step is from the it resolves where to check the configuration file
 3. Then once the path is resolved then based on the file extension the engine calls the "ParserFactory" and creates a Parser.
 	so, if the configuration file is test_x.json then the engine will call the Parserfactory and creates JsonParser object.
 	if the configuration file name is test_*.yaml then the engine will call the YamlParser and parse.
 4.After the configuration object 

### Diagrams

![alt text](docs/test_framework_seq_diagram.png "seq diagram")
![class_diagram](docs/test_framework_class_diagram-Page-2.jpg)
 
 Support
 -------
 - For enhancements/issues please raise a jira ticket.
 - For support email us at - dataplatform@reflektion.com or slack us


