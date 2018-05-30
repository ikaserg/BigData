insert into social.user_relations(
    social_net_id,
    user_id,
    rel_user_id,
    group_id,
    relation_date,
    relation_type_id,
    int_param1,
    int_param2,
    inner_id,
    int_param3,
    int_param4)
    select t.social_net_id,
    t.user_id,
    t.rel_user_id,
    t.group_id,
    t.relation_date,
    t.relation_type_id,
    t.int_param1,
    t.int_param2,
    nextval('user_relations_inner_id_seq'),
    t.int_param3,
    t.int_param4
  from social.user_relations_1 t
 where t.relation_type_id in (3, 4)
 and not exists (select 1
                   from social.user_relations r
                  where r.social_net_id = t.social_net_id
                    and r.user_id = t.user_id
                    and r.rel_user_id = t.rel_user_id );


select t.date_to, t.date_next
  from(
    select coalesce((select min(t_n.date_from)
              from etl.etl_log t_n
             where t_n.source_id = t.source_id
               and t_n.source_key = t.source_key
               and t_n.date_from >= t.date_to), now()) as date_next,
            t.*
      from etl.etl_log t
     where t.source_id = 1 and t.source_key = '79155989207'
) t
 where DATE_PART('day', t.date_next - t.date_to) > 1
 group by t.date_next, t.date_to
 order by t.date_to


order by t.log_date desc


update etl.etl_log
set source_id = 1,
    source_key = substring(file_name, '_([0-9]+)__[0-9]+__[0-9]+.$'),
    date_from = to_timestamp(substring(file_name, '__([0-9]+)__[0-9]+.$'), 'DDMMYYYY'),
    date_to = to_timestamp(substring(file_name, '__([0-9]+).$'), 'DDMMYYYY')
where file_name like '/home/etl/mts%';
commit;


GRANT ALL ON ALL TABLES IN SCHEMA schedule TO etl;
commit;

select coalesce((select min(t_n.date_from)
          from etl.etl_log t_n
         where t_n.source_id = t.source_id
           and t_n.source_key = t.source_key
           and t_n.date_from >= t.date_to), now()) as date_next,
        t.date_from, t.date_to,
        t.*
  from etl.etl_log t
 where t.source_id = 1 and t.source_key = '79155989207'
 order by t.date_to desc


select t.date_to, t.date_next
  from(
    select coalesce((select min(t_n.date_from)
              from etl.etl_log t_n
             where t_n.source_id = t.source_id
               and t_n.source_key = t.source_key
               and t_n.date_from >= t.date_to), now()) as date_next,
            t.*
      from etl.etl_log t
     where t.source_id = 1
       and t.source_key = '79155989207'
      ) t
 where t.date_next::date - t.date_to::date > 1
 group by t.date_next, t.date_to
 order by t.date_to


