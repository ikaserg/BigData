select t.*
from social.user_relations t
where t.rel_user_id = 158475116392

select count(*)
from (
select t.rel_user_id
from social.user_relations t
group by t.rel_user_id
) a