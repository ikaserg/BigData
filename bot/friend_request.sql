 SELECT u.relation_date,
    u.relation_type_id,
    u.rel_user_id,
    u.group_id,
    u.inner_id,
    u.int_param1,
    u.int_param2,
    u.int_param3,
    u.int_param4,
    u.int_param5,
    u.social_net_id,
    u.user_id,
    a.relation_date AS confirm_date
   FROM user_relations_date u
     LEFT JOIN ( SELECT r_i.user_id,
            r_i.social_net_id,
            r_i.rel_user_id,
            max(r_i.relation_date) AS relation_date
           FROM user_relations_date r_i
          WHERE r_i.relation_type_id = 1
          GROUP BY r_i.user_id, r_i.social_net_id, r_i.rel_user_id) a ON a.user_id = u.user_id AND a.social_net_id = u.social_net_id AND a.rel_user_id = u.rel_user_id AND a.relation_date > u.relation_date
  WHERE u.relation_type_id = 4;