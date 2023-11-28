BEGIN;

--
--  Create schemas
--

CREATE SCHEMA aleo_rewards AUTHORIZATION ${aleo_rewards_owner_role};

--
--  Grant usage on schema aleo_rewards
--

GRANT USAGE ON SCHEMA aleo_rewards TO ${aleo_rewards_app_role};
