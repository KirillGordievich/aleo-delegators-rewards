BEGIN;

--
--  Revoke grants on schema
--

REVOKE USAGE ON SCHEMA aleo_rewards FROM ${aleo_rewards_app_role};

--
--  Drop schemas
--

DROP SCHEMA IF EXISTS aleo_rewards;
