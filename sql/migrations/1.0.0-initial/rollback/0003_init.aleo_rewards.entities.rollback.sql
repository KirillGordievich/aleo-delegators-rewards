BEGIN;

--
--  Drop tables
--
DROP TABLE IF EXISTS aleo_rewards.stake_transaction;
DROP TABLE IF EXISTS aleo_rewards.block_height;
DROP TABLE IF EXISTS aleo_rewards.address;

DROP TYPE IF EXISTS aleo_rewards.stake_function;
DROP TYPE IF EXISTS aleo_rewards.address_type;

