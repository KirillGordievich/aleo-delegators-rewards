# aleo-delegators-rewards
Service to calculate Aleo rewards for delegators

## DATABASE Requirements

- postgresql ^10
- liquibase

## DATABASE Configs
```shell
$ cp liquibase.properties.sample liquibase.properties

// and edit liquibase.properties (fill actual credentials)
```

## DATABASE Setup

```shell
-- dbname: aleo_rewards

CREATE USER aleo_rewards_liquibase_user WITH PASSWORD '****';
CREATE USER aleo_rewards_app_user WITH PASSWORD '****';
CREATE DATABASE aleo_rewards OWNER aleo_rewards_liquibase_user;

```

```shell
$ liquibase update

// rollback
$ liquibase rollback v1.0.0
