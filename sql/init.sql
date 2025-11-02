-- Custom Types
CREATE TYPE public.entity_type_options AS ENUM
    ('Slow Growth Fast Bust', 'Volatile', 'Fluctuating Decline', 'Fluctuating Rise');
-- Tables
CREATE TABLE IF NOT EXISTS public.entities (
    entity_code       	char(5) CONSTRAINT firstkey PRIMARY KEY,
    entity_type       	entity_type_options NOT NULL,
	first_constant 		numeric NOT NULL,
    second_constant 	numeric NOT NULL,
    third_constant 		numeric NOT NULL
);

CREATE TABLE IF NOT EXISTS public.entity_values (
    entity_code 	 	char(5) NOT NULL,
    entity_count 	    integer NOT NULL,
	entity_value 	 	numeric NOT NULL,
	PRIMARY KEY (entity_code, entity_count)
);

CREATE TABLE IF NOT EXISTS public.users (
    user_name           varchar(10) NOT NULL UNIQUE,
    password            text NOT NULL,
    email               text NOT NULL UNIQUE,
    PRIMARY KEY (user_name)
);

CREATE TABLE IF NOT EXISTS public.user_entities (
    user_name           varchar(10) NOT NULL,
    entity_code         char(5) NOT NULL,
    PRIMARY KEY (user_name, entity_code)
);

CREATE TABLE IF NOT EXISTS public.user_encryption_key (
    encryption_key      char(44) NOT NULL,
    PRIMARY KEY (encryption_key)
);
-- Data loading
INSERT INTO user_encryption_key VALUES ('pWuWW4uT4JiO1UNofsY67XepmGsLaQ7AUkvsqZGbcZs=');
-- Functions
CREATE OR REPLACE FUNCTION public.add_entity(entity_code 	 char(5), 
											 entity_type 	 entity_type_options, 
											 first_constant  numeric, 
											 second_constant numeric, 
											 third_constant  numeric) 
	RETURNS boolean AS
	$$
		BEGIN
			INSERT INTO entities 
			VALUES (entity_code, entity_type, first_constant, second_constant, third_constant);
			RETURN TRUE;
		EXCEPTION WHEN others THEN
			RETURN FALSE;
		END;
	$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION public.add_entity_value(entity_code 		char(5),
												   entity_count     integer,
												   entity_value		numeric)
	RETURNS boolean AS
	$$
		BEGIN
			INSERT INTO entity_values
			VALUES (entity_code, entity_count, entity_value);
			RETURN TRUE;
		EXCEPTION WHEN others THEN
			RETURN FALSE;
		END;
	$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION public.get_existing_entities()
	RETURNS SETOF char(5) AS 
	$$
		BEGIN
			RETURN QUERY SELECT entity_code 
				   FROM public.entities;
		EXCEPTION WHEN others THEN
			RETURN;
		END;
	$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION public.get_entity_details(code char(5))
	RETURNS SETOF entities AS
	$$ 
		BEGIN
			RETURN QUERY SELECT entity_code, 
								entity_type, 
								first_constant, 
								second_constant, 
								third_constant
				   FROM public.entities WHERE entity_code = code;
		EXCEPTION WHEN others THEN
			RETURN;
		END;
	$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION public.get_values(code char(5), code_count integer)
	RETURNS SETOF entity_values AS
	$$
		BEGIN
			RETURN QUERY SELECT entity_code,
								entity_count,
								entity_value
				   FROM public.entity_values WHERE entity_code=code AND entity_count >= code_count;
		EXCEPTION WHEN others THEN
			RETURN;
		END;
	$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION public.add_user(user_name varchar(10), password text, email text)
    RETURNS boolean AS
	$$
		BEGIN
			INSERT INTO users
			VALUES (user_name, password, email);
			RETURN TRUE;
		EXCEPTION WHEN others THEN
			RETURN FALSE;
		END;
	$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION public.get_user(provided_user_name varchar(10))
    RETURNS SETOF users AS
    $$
        BEGIN
            RETURN QUERY SELECT user_name,
                                password,
                                email
                   FROM public.users WHERE user_name = provided_user_name;
        EXCEPTION WHEN others THEN
			RETURN;
		END;
	$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION public.get_entities_assigned_to_user(provided_user_name varchar(10))
    RETURNS SETOF user_entities AS
    $$
        BEGIN
            RETURN QUERY SELECT user_name,
                                entity_code
                   FROM public.user_entities WHERE user_name = provided_user_name;
        EXCEPTION WHEN others THEN
			RETURN;
		END;
	$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION public.connect_user_entity(user_name varchar(10), entity_code char(5))
    RETURNS boolean AS
    $$
        BEGIN
            INSERT INTO user_entities
            VALUES (user_name, entity_code);
            RETURN TRUE;
        EXCEPTION WHEN others THEN
			RETURN FALSE;
		END;
	$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION public.get_encryption_key()
    RETURNS char(44) AS
    $$
        SELECT encryption_key
        FROM public.user_encryption_key;
	$$ LANGUAGE 'sql';
-- Permissions	
CREATE ROLE data_seeder LOGIN PASSWORD 'data';
CREATE ROLE api LOGIN PASSWORD 'data';
GRANT ALL ON public.entities TO data_seeder, api;
GRANT ALL ON public.entity_values TO data_seeder, api;
GRANT ALL ON public.users TO api;
GRANT ALL ON public.user_entities TO api;
GRANT ALL ON public.user_encryption_key TO api;
GRANT EXECUTE ON FUNCTION public.get_existing_entities() TO data_seeder, api;
GRANT EXECUTE ON FUNCTION public.get_entity_details(character) TO data_seeder, api;
GRANT EXECUTE ON FUNCTION public.add_entity(character, entity_type_options, numeric, numeric, numeric) 
	TO data_seeder;
GRANT EXECUTE ON FUNCTION public.add_entity_value(character, integer, numeric) TO data_seeder;
GRANT EXECUTE ON FUNCTION public.get_values(character, integer) TO data_seeder, api;
GRANT EXECUTE ON FUNCTION public.add_user(varchar(10), text, text) TO api;
GRANT EXECUTE ON FUNCTION public.get_user(varchar(10)) TO api;
GRANT EXECUTE ON FUNCTION public.get_entities_assigned_to_user(varchar(10)) TO api;
GRANT EXECUTE ON FUNCTION public.connect_user_entity(varchar(10), char(5)) TO api;
GRANT EXECUTE ON FUNCTION public.get_encryption_key() TO api;