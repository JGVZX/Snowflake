Snowflake/dbt/airflow pipeline project.
- Data extraction and loading to Snowflake using our local, containerised environment.
- Tested, version controlled and documented data tranformation using dbt connection to snowflake.
- Orchestration of the whole pipeline using airflow.

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:

- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [dbt community](http://community.getbdt.com/) to learn from other analytics engineers
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

## Specifics of this project:

- Download dataset from Kaggle: https://www.kaggle.com/datasets/joebeachcapital/startups
- Snowflake set-up:
  - 'RAW' database with schema 'STARTUPS' containing satge and file format for loading the staged data.
  - 'STARTUPS' database which is used for the transformed data.
  - DBT_ROLE used for the dbt project - this will require relevent permissions the read the raw data.
  - AIRFLOW_ROLE used for airflow connections - this will require relevent permissions to the startups schema in the raw database, to load files to the stage, and copy data from the stage into tables.
- DBT set-up:
  - Create account with Snowflake connection. Use database STARTUPS and set a schema (e.g. dbt_schema) (this is where dbt will write the transformed data to). Use role DBT_ROLE.
  - In dbt we stage our data with minor transformations, test the staged data, and we then transform into an intermediate, normalised model with tested key constraints and relationships. From there, we could add more transformations to get the data into dimensional models and datamarts etc. Find more on the file structure here: <https://docs.getdbt.com/guides/best-practices/how-we-structure/1-guide-overview>
  - See this course: <https://courses.getdbt.com/courses/fundamentals>
  - Also, these docs on packages: <https://docs.getdbt.com/docs/build/packages> (we use the db-utils packages once for testing uniqueness across multiple columns)
- Airflow set-up:
  - See [this repo](https://github.com/jonathangosling/Rightmove_Analysis) for some more indepth stuff setting up airflow.
  - Here we just use the base airflow image in our docker-compose, with the additional container and volume set-ups for the scheduler and database.
  - Our DAG contains all necessary tasks to:
    - Download files (Here we are downloading the data from Kaggle, will need the kaggle API installed)
    - Load the files to our stage in Snowflake (using a PythonOperator containing a Snowflake Connection object obtained using the SnowflakeHook function)
    - Copy the data from the stage into the table using the file_format stored in snowflake. This uses the SnowflakeOperator and the locally stored sql script.
    - Trigger the dbt job (using DbtCloudRunJobOperator) and check the job (DbtCloudJobRunSensor, DbtCloudGetJobRunArtifactOperator).
    - Two connections are required to be set up (this can be done in the UI under the Admin tab):
      - SNOW_FLAKE_CONN_ID: schema - startups; account - snowflake account (find this in the admin tab in snowflake and change to the format: xxxxxxx.region.cloud); database - raw; role - airflow_role
      - DBT_CONN_ID: account id - your account id (if you go into your job in dbt the account id is the first 6 digit number in the url. fyi the second is the project id and the last is the job id - needed in the DbtCloudRunJobOperator); api token - generate one in your dbt account by going to 'account settings' - 'service tokens'.
  - Run `docker-compose up` from the airflow directory to kick off the airflow containers.

