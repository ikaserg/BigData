select count(*)
  from social.users t
 where (t.first_name is not null
   and t.last_name is not null)
    or t.is_deleted is not null

delete
  from social.users t
  where (select count(*)
           from social.users t_i
          where t_i.user_id = t.user_id
            and t_i.social_net_id = t.social_net_id
        ) > 1




select count(*)
  from (select t.rel_user_id
          from social.user_relations t
         where t.relation_type_id in (1,4)
         group by t.rel_user_id) t

select t.*
  from social.users t
 where t.last_name is null
 limit 10

select u.user_id
  from social.users u
 where u.url_profile is null

select count(*)
  from social.users t
 inner join social.user_relations r on r.social_net_id = t.social_net_id
                                   and r.rel_user_id = t.user_id
 where t.city like '%Рязань%'
   and r.relation_type_id = 1;

select count(*)
  from social.users t
 inner join social.user_relations r on r.social_net_id = t.social_net_id
                                   and r.rel_user_id = t.user_id
 where t.city not like '%Рязань%'
   and r.relation_type_id = 1;

update social.users t
   set is_deleted = 1
 where t.first_name is null and t.last_name is null

delete from social.topic_schedule;
delete from social.topic_schedule_img;

select t.*
  from social.topic_schedule t

select t.*
  from social.topic_schedule_img t


