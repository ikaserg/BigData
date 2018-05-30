select (t.date_to::date - 1)::date as date_to, t.date_next
  from( 
    select coalesce((select min(t_n.date_from)
              from etl.etl_log t_n 
             where t_n.source_id = t.source_id 
               and t_n.source_key = t.source_key 
               and t_n.date_from >= t.date_to), now()::date - 1) as date_next, 
            t.* 
      from etl.etl_log t 
     where t.source_id = 1
       and t.source_key = '79155989207'
       and t.date_from > '2016-05-03 0:0'
      ) t 
 where 1 = 1
   and t.date_next::date - t.date_to::date > 0
 group by t.date_next, t.date_to 
 order by t.date_to;

select (t.date_to::date - 1)::date as date_to, t.date_next, t.date_next::date - t.date_to::date
  from(
    select coalesce((select min(t_n.date_from)
                       from etl.etl_log t_n
                      where t_n.source_id = t.source_id
                        and t_n.source_key = t.source_key
                        and t_n.date_to > t.date_to), (now()::date)) as date_next,
           t.date_to
      from etl.etl_log t
     where t.source_id = 1
       and t.source_key = '79155989207'
       and t.date_from > '2016-05-03 0:0'
     group by t.source_id,  t.source_key, t.date_to
      ) t
 where t.date_next::date - t.date_to::date > 0
 group by t.date_next, t.date_to
 order by t.date_to


select coalesce((select min(t_n.date_from)
                   from etl.etl_log t_n
                  where t_n.source_id = t.source_id
                    and t_n.source_key = t.source_key
                    and t_n.date_from >= t.date_to), now()::date) as date_next,
        t.*
  from etl.etl_log t
 where t.source_id = 1
   and t.source_key = '79155989207'
   and t.date_from > '2016-05-03 0:0'


select t.*
  from etl.etl_log t
 where t.source_id = 1
   and t.source_key = '79155989207'
 order by t.date_from desc

 select length(error_msg) as l, t.*
 from social.bot_log t
 where t.bot_log_id = 120

 update social.user_relations
set int_param5 = int_param5 - 1
where rel_user_id = 486060669227
  and relation_type_id = 4

select t.bot_day, sum(error) as err, count(error) as total, sum(error)::float/count(error) as rate
  from(
    select date_trunc('day', b_l.log_date) as bot_day,
           b_l.bot_log_id,
           case when sum(case when b_l.status = -1 then 1 else null end ) > 0 then 1
             else 0
           end as error
      from bot_log b_l
     group by date_trunc('day', b_l.log_date), b_l.bot_log_id
    ) t
group by t.bot_day


select t.relation_type_id, count(t.rel_user_id)
from social.user_relations t
group by t.relation_type_id

select count(*)
from(
select t.rel_user_id
from social.user_relations t
group by t.rel_user_id
) u

select count(*)
from(
select t.rel_user_id
  from social.user_relations t
 group by t.rel_user_id
) u


