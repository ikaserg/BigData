drop table social.threads;
create table social.threads(
    social_net_id integer,
    user_id integer,
    contact_user_id integer
);
create index ind_threads_user_key on social.threads(social_net_id, user_id, contact_user_id);
create index ind_threads_user_id on social.threads(user_id);
create index ind_threads_contact_user_id on social.threads(contact_user_id);

drop table social.messages;
create table social.messages(
    thread_id bigint,
    social_net_id integer,
    from_user_id bigint,
    to_user_id bigint,
    message_date timestamp,
    message text,
    message_meta bytea
);

create index ind_messages_thread_id on social.messages(thread_id);
create index ind_messages_social_net_id on social.messages(social_net_id);
create index ind_messages_from_user_id on social.messages(from_user_id);
create index ind_messages_to_user_id on social.messages(to_user_id);
create index ind_messages_message_date on social.messages(message_date);
