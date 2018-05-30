--Социальные сети--
drop table data.social_net;
create table data.social_net(
    social_net_id integer PRIMARY KEY,
    name varchar(100),
    base_url varchar(100)
);

--Пользователи социальных сетей--
drop table social.users;
create table social.users(
    social_net_id integer,
    user_id bigint,
    name varchar(250),
    first_name varchar(250),
    last_name varchar(250),
    gender integer,
    birthday timestamp,
    birth_day integer,
    birth_month integer,
    city  varchar(250),
    country varchar(250),
    current_status text,
    current_status_id bigint,
    current_status_date timestamp,
    url_profile varchar(250),
    allows_anonym_access integer,
    registered_date timestamp,
    premium integer,
    create_date timestamp,
    update_date timestamp,
    is_deleted integer
);

drop table data.users_auth;
create table data.users_auth(
    social_net_id integer,
    user_id bigint,
    token varchar(100),
    session_secret varchar(100),
    user_login varchar(100),
    user_password varchar(255)
);

---------------------------------------------------------------------------------
drop table schedule.scheduled_action;
create table schedule.scheduled_action(
    social_net_id integer,
    user_id bigint,
    action_type varchar(100)
);

---------------------------------------------------------------------------------
drop table stat.friends_online_stat;
create table stat.friends_online_stat(
    social_net_id integer,
    user_id bigint,
    stat_time timestamp with time zone,
    online_count integer,
    total_coun integer
);

create index ind_friends_online_stat_user_key on stat.friends_online_stat(social_net_id, user_id);
create index ind_friends_online_stat_stat_time on stat.friends_online_stat(stat_time);
create index ind_friends_online_stat_day on stat.friends_online_stat(date_trunc('day'::text, stat_time  AT TINE ZONE 'UTC'));
create index ind_friends_online_stat_m15 on stat.friends_online_stat(floor(date_part('minute'::text, stat_time) / 15::double precision));

---------------------------------------------------------------------------------
drop table data.calendar;
create table data.calendar(
    day_date timestamp,
    -- day types 0 -work day 1 - day off 2 - holiday
    day_type integer
);

create index ind_friends_online_stat_day_date on data.calendar(day_date);
create index ind_friends_online_stat_day_type on data.calendar(day_type);

---------------------------------------------------------------------------------
drop table social.user_relations;
create table social.user_relations(
    social_net_id integer,
    user_id bigint,
    rel_user_id bigint,
    group_id bigint,
    relation_date timestamp,
    relation_type_id integer,
    int_param1 bigint,
    int_param2 bigint,
    innner_id bigint,
    int_param3 bigint,
    int_param4 bigint,
    int_param5 bigint
);

create index ind_user_relations_user_key on data.user_relations(social_net_id, user_id);
create index ind_user_relations_rel_user_key on data.user_relations(social_net_id, rel_user_id);
create index ind_user_relations_relation_date on data.user_relations(relation_date);
create index ind_user_relations_group_key on data.user_relations(social_net_id, group_id);

---------------------------------------------------------------------------------
--  Списки пользователей
---------------------------------------------------------------------------------
drop table social.user_lists;
create table social.user_lists(
    user_lists_id integer  PRIMARY KEY,
    list_name varchar(100),
    note text
);

create index ind_user_lists_key on social.user_lists(user_lists_id);

---------------------------------------------------------------------------------
--  Элементы списков пользователей
---------------------------------------------------------------------------------
drop table social.user_list_item;
create table social.user_list_item(
    user_list_id integer,
    social_net_id integer,
    user_id bigint,
    add_date timestamp
);

create index ind_user_lists_user_list_id on social.user_list_item(user_list_id);
create index ind_user_lists_user_key on social.user_list_item(social_net_id, user_id);
create index ind_user_lists_add_date on social.user_list_item(add_date);


drop table social.temp_user_list_item;
create table social.temp_user_list_item(
    user_list_id integer,
    social_net_id integer,
    user_id bigint,
    add_date timestamp
);

create index ind_temp_user_lists_user_list_id on social.temp_user_list_item(user_list_id);
create index ind_temp_user_lists_user_key on social.temp_user_list_item(social_net_id, user_id);
create index ind_temp_user_lists_add_date on social.temp_user_list_item(add_date);


---------------------------------------------------------------------------------
--  История входов - выходов
---------------------------------------------------------------------------------
drop table social.users_login;
create table social.users_login(
    social_net_id integer,
    user_id bigint,
    login_date timestamp,
    -- 1 - стал онлайн -1 - стал не в сети
    online_status integer
);

create index ind_users_login_user_key on social.users_login(social_net_id, user_id);
create index ind_users_login_user_id on social.users_login(user_id);
create index ind_users_login_login_date on social.users_login(login_date);

drop table social.users_last_state;
create table social.users_last_state(
    social_net_id integer,
    user_id bigint,
    state_date timestamp,
    -- 1 - в сети -1 - не в сети
    online_status integer
);

create index ind_users_last_state_user_key on social.users_last_state(social_net_id, user_id);
create index ind_users_last_state_user_id on social.users_last_state(user_id);
create index ind_users_last_state_ыефеу_date on social.users_last_state(state_date);

drop table social.temp_users_last_state;
create table social.temp_users_last_state(
    social_net_id integer,
    user_id bigint,
    state_date timestamp,
    -- 1 - в сети -1 - не в сети
    online_status integer
);

create index ind_temp_users_last_state_user_key on social.temp_users_last_state(social_net_id, user_id);
create index ind_temp_users_last_state_user_id on social.temp_users_last_state(user_id);
create index ind_temp_users_last_state_ыефеу_date on social.temp_users_last_state(state_date);

select (select count(*) from social.users_last_state) as users_last_state,
(select count(*) from social.users_login) as users_login,
(select count(*) from social.temp_users_last_state) as temp_users_last_state,
(select count(*) from social.user_list_item) as user_list_item


drop table social.theme_types;
create table social.theme_types(
    type_id integer,
    type_name varchar(100),
    type_note text
);
create index ind_theme_types_type_id on social.theme_types(type_id);


drop table social.topic_themes;
create table c(
    theme_id integer,
    type_id integer,
    theme_name varchar(100),
    theme_note text
);
create index ind_topic_themes_theme_id on social.topic_themes(theme_id);
create index ind_topic_themes_type_id on social.topic_themes(type_id);


drop table social.topic_texts;
create table social.topic_texts(
    topic_text_id integer,
    theme_id integer,
    topic_caption varchar(150),
    topic_text text
);

create index ind_topic_texts_topic_text_id on social.topic_texts(topic_text_id);
create index ind_topic_texts_theme_id on social.topic_texts(theme_id);


drop table social.topic_images;
create table social.topic_images(
    topic_image_id integer,
    theme_id integer,
    img bytea
);

create index ind_topic_images_topic_image_id on social.topic_images(topic_image_id);
create index ind_topic_images_theme_id on social.topic_images(theme_id);

commit;


drop table social.time_slot;
create table social.time_slot(
    slot_id integer,
    time_value time
);


drop table social.topic_schedule;
create table social.topic_schedule(
    schedule_id integer,
    topic_text_id integer,
    user_id bigint,
    group_id bigint,
    slot_id integer,
    schedule_date timestamp,
    is_posted integer,
    posted_topic_id bigint
);

create index ind_topic_schedule_schedule_id on social.topic_schedule(schedule_id);
create index ind_topic_schedule_topic_text_id on social.topic_schedule(topic_text_id);
create index ind_topic_schedule_slot_id on social.topic_schedule(slot_id);
create index ind_topic_schedule_posted_topic_id on social.topic_schedule(posted_topic_id);

drop sequence social.seq_topic_schedule;
create sequence social.seq_topic_schedule start 1;
commit;

drop table social.topic_schedule_img;
create table social.topic_schedule_img(
    schedule_id integer,
    ord integer,
    topic_image_id integer
);

create index ind_topic_schedule_img_schedule_id on social.topic_schedule_img(schedule_id);
create index ind_topic_schedule_img_topic_image_id on social.topic_schedule_img(topic_image_id);
commit;

---------------------------------------------------------------------------------
--  История работ роботов
---------------------------------------------------------------------------------

drop table social.bot_log;
create table social.bot_log(
    bot_log_id integer,
    bot_id integer,
    log_date timestamp,
    action_id integer,
    status integer,
    note text,
    error_msg text
);

create index ind_bot_log_bot_log_id on social.bot_log(bot_log_id);
create index ind_bot_log_bot_id on social.bot_log(bot_id);
create index ind_bot_log_log_date on social.bot_log(log_date);
create index ind_bot_log_action_id on social.bot_log(action_id);
create index ind_bot_log_status on social.bot_log(status);

drop sequence social.bot_log_bot_log_id;
create sequence social.bot_log_bot_log_id start 1;


drop table social.bot_messages;
create table social.bot_messages(
    bot_message_id integer,
    message_type_id integer,
    message text
);

create index ind_bot_messages_bot_message_id on social.bot_messages(bot_message_id);

drop table social.bot_message_sets;
create table social.bot_message_sets(
    bot_message_set_id integer,
    name varchar(100)
);

create index ind_bot_message_sets_bot_message_set_id on social.bot_message_sets(bot_message_set_id);

drop table social.bot_message_set_items;
create table social.bot_message_set_items(
    bot_message_set_id integer,
    bot_message_id integer,
    message_prob real
);

create index ind_bot_message_set_items_bot_message_set_id on social.bot_message_set_items(bot_message_set_id);
create index ind_bot_message_set_items_bot_message_id on social.bot_message_set_items(bot_message_id);

commit;
