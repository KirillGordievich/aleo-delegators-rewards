BEGIN;

--
--  Create roles (if not exists) and grant owner to current_user
--

DO $$
BEGIN
    CREATE ROLE ${aleo_rewards_owner_role} ROLE current_user;
EXCEPTION
    WHEN duplicate_object THEN NULL;

END
$$;

DO $$
BEGIN
    CREATE ROLE ${aleo_rewards_app_role} ROLE ${aleo_rewards_app_user};
EXCEPTION
    WHEN duplicate_object THEN NULL;

END
$$;
