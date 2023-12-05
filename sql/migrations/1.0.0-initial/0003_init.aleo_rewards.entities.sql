BEGIN;

CREATE TYPE aleo_rewards.stake_function AS ENUM ('bond_public', 'unbond_public', 'claim_unbond_public');
CREATE TYPE aleo_rewards.address_type AS ENUM ('validator', 'delegator');

--
--  Add address info
--

CREATE TABLE IF NOT EXISTS aleo_rewards.address (
  id                          bigint                    PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  address                     text                      NOT NULL,
  created_at                  timestamptz               NOT NULL DEFAULT now(),
  updated_at                  timestamptz               NOT NULL DEFAULT now(),
  type                        aleo_rewards.address_type NOT NULL,

  UNIQUE(address)
);

ALTER TABLE aleo_rewards.address OWNER TO ${aleo_rewards_owner_role};
GRANT ALL PRIVILEGES ON TABLE aleo_rewards.address TO ${aleo_rewards_app_role};

--
--  Add block info
--

CREATE TABLE IF NOT EXISTS aleo_rewards.block_height (
  id                          bigint                  PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  height                      bigint                  NOT NULL CONSTRAINT unique_height UNIQUE,
  updated_at                  timestamptz             NOT NULL DEFAULT now(),

  CONSTRAINT height_non_negative CHECK(height >= 0)
);

CREATE INDEX idx_block_height_desc ON  aleo_rewards.block_height (height DESC);

ALTER TABLE aleo_rewards.block_height OWNER TO ${aleo_rewards_owner_role};
GRANT ALL PRIVILEGES ON TABLE aleo_rewards.block_height TO ${aleo_rewards_app_role};

--
--  Add transaction info table
--

CREATE TABLE IF NOT EXISTS aleo_rewards.stake_transaction (
  id                          bigint                        PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  tx_id                       text                          NOT NULL,
--  validator                   text                          NOT NULL,
--  delegator                   text                          NOT NULL,
--  function                    aleo_rewards.stake_function   NOT NULL,
--  amount                      numeric                       NOT NULL,
  height                      bigint                        NOT NULL,
  round                       bigint                        NOT NULL,
  payload                     jsonb                         NOT NULL,
  created_at                  timestamptz                   NOT NULL DEFAULT now(),
  updated_at                  timestamptz                   NOT NULL DEFAULT now(),

  CONSTRAINT height_is_not_negative CHECK(height> 0)

--  CONSTRAINT validator_is_not_delegator CHECK (validator != delegator),
--  CONSTRAINT amount_is_positive CHECK(amount > 0),

-- TODO: add method to save new validators and delegators to the address table
--  CONSTRAINT fk_validator FOREIGN KEY(validator) REFERENCES aleo_rewards.address(address),
--  CONSTRAINT fk_delegator FOREIGN KEY(delegator) REFERENCES aleo_rewards.address(address)
);

CREATE UNIQUE INDEX idx_uniq_transaction ON aleo_rewards.stake_transaction (tx_id);


ALTER TABLE aleo_rewards.stake_transaction OWNER TO ${aleo_rewards_owner_role};
GRANT ALL PRIVILEGES ON TABLE aleo_rewards.stake_transaction TO ${aleo_rewards_app_role};