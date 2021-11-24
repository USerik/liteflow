class Tables:
    workflows_table_name = "workflows"
    subscriptions_table_name = "subscriptions"
    events_table_name = "events"

    workflows_table = f""" CREATE TABLE if not exists {workflows_table_name} (
        id INTEGER PRIMARY KEY,
        workflow_definition_id text,
        version text,
        description text,
        next_execution text,
        status text,
        data text,
        create_time text,
        complete_time text,
        execution_pointers text
        ) """

    subscriptions_table = f""" CREATE TABLE if not exists {subscriptions_table_name} (
        id INTEGER PRIMARY KEY,
        event_name text,
        event_key text,
        step_id text,
        workflow_id text,
        subscribe_as_of text
        ) """

    events_table = f""" CREATE TABLE if not exists {events_table_name} (
        id INTEGER PRIMARY KEY,
        event_name text,
        event_key text,
        event_data text,
        event_time text,
        is_processed text
        ) """
