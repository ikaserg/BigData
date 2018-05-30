select date_trunc('day', t.relation_date) t_day


select coalesce(t.int_param5, 0),
       sum(case when t.confirm_date is null then 0 else 1 end),
       count(t.*),
       cast(sum(case when t.confirm_date is null then 0 else 1 end) as FLOAT)/cast(count(t.*) as FLOAT) rate
  from social.friend_requests t
 where t.relation_date > date '2016-11-29'
   and t.user_id = 574248559595
 group by coalesce(t.int_param5, 0)

select coalesce(t.int_param5, 0),
       sum(case when t.confirm_date is null then 0 else 1 end),
       count(t.*),
       cast(sum(case when t.confirm_date is null then 0 else 1 end) as FLOAT)/cast(count(t.*) as FLOAT) rate
  from social.friend_requests t
 where t.relation_date > date '2016-11-29'
   and t.user_id = 575918147556
 group by coalesce(t.int_param5, 0)


select coalesce(t.int_param3, 0) as cls,
       sum(case when t.confirm_date is null then 1 else 0 end),
       count(t.*),
       cast(sum(case when t.confirm_date is null then 0 else 1 end) as FLOAT)/cast(count(t.*) as FLOAT) rate
  from social.friend_requests t
 where t.relation_date > date '2016-05-01'
 group by coalesce(t.int_param3, 0)

select coalesce(t.int_param4, 0) as vote,
       sum(case when t.confirm_date is null then 1 else 0 end),
       count(t.*),
       cast(sum(case when t.confirm_date is null then 0 else 1 end) as FLOAT)/cast(count(t.*) as FLOAT) rate
  from social.friend_requests t
 where t.relation_date > date '2016-05-01'
 group by coalesce(t.int_param4, 0)

select coalesce(t.int_param3, 0) as cls, coalesce(t.int_param4, 0) as vote,
       sum(case when t.confirm_date is null then 1 else 0 end),
       count(t.*),
       cast(sum(case when t.confirm_date is null then 0 else 1 end) as FLOAT)/cast(count(t.*) as FLOAT) rate
  from social.friend_requests t
 where t.relation_date > date '2016-05-01'
 group by coalesce(t.int_param3, 0), coalesce(t.int_param4, 0)
 having count(t.*) > 10




select sum(case when t.int_param5 > 0 then 1 else 0 end),
       count(t.*),
       cast(sum(case when t.int_param5 > 0 then 1 else 0 end) as FLOAT)/cast(count(t.*) as FLOAT) rate
  from social.friend_requests t
 where t.relation_date > date '2016-11-30'


select sum(case when t.confirm_date is null then 1 else 0 end),
       count(t.*),
       cast(sum(case when t.confirm_date is null then 0 else 1 end) as FLOAT)/cast(count(t.*) as FLOAT) rate
  from social.friend_requests t
 where t.relation_date > date '2016-11-01'


select min(t.relation_date)
  from social.friend_requests t
 where t.relation_date > date '2016-11-30'
 t.int_param5 is not null
