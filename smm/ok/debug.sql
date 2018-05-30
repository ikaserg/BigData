select (select count(*) from social.users_last_state) as users_last_state,
(select count(*) from social.users_login) as users_login,
(select count(*) from social.temp_users_last_state) as temp_users_last_state,
(select count(*) from social.user_list_item) as user_list_item

 select t_s.social_net_id, t_s.user_id, now(), t_s.online_status
   from social.temp_users_last_state t_s
  inner join social.users_last_state s on s.social_net_id = t_s.social_net_id
                                     and s.user_id =  t_s.user_id
                                     and s.online_status <> t_s.online_status

select
(select count(*) from social.temp_users_last_state t_s where t_s.online_status = 1) as temp_1,
(select count(*) from social.temp_users_last_state t_s where t_s.online_status = -1) as temp_m1,
(select count(*) from social.users_last_state t_s where t_s.online_status = 1) as state_1,
(select count(*) from social.users_last_state t_s where t_s.online_status = -1) as state_m1