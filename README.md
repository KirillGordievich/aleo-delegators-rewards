# aleo-delegators-rewards
Service to calculate Aleo rewards for delegators

## DATABASE Requirements

- postgresql ^10
- liquibase

## DATABASE Setup

```shell
-- dbname: aleo_rewards

CREATE DATABASE aleo_rewards OWNER aleo_rewards_liquibase_user;

// ignore these lines if you want to use your own users to work with the database
CREATE USER aleo_rewards_liquibase_user WITH PASSWORD '****';
CREATE USER aleo_rewards_app_user WITH PASSWORD '****';
```

## DATABASE Configs
```shell
$ cp liquibase.properties.sample liquibase.properties

// and edit liquibase.properties (fill actual credentials)
```

```shell
// to init
$ liquibase update

// rollback
$ liquibase rollback v1.0.0
```

## App Requirements

- python3
- python3 libs:
    - psycopg2
    - json

## App Setup
```shell
// open src\configs\db.py and fill actual credentials
```

## Aleo Network Syncer run
```shell
python src/index.py
```