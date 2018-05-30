insert into schedule.source_names(source_id, source_name)
    values(1, 'Детализация МТС');

insert into schedule.act_periods(act_period_id, act_period_name)
    values(1, 'Год');
insert into schedule.act_periods(act_period_id, act_period_name)
    values(2, 'Квартал');
insert into schedule.act_periods(act_period_id, act_period_name)
    values(3, 'Месяц');
insert into schedule.act_periods(act_period_id, act_period_name)
    values(4, 'Декада');
insert into schedule.act_periods(act_period_id, act_period_name)
    values(5, 'Неделя');
insert into schedule.act_periods(act_period_id, act_period_name)
    values(5, 'День');
insert into schedule.act_periods(act_period_id, act_period_name)
    values(5, 'Час');

delete from schedule.schedule_bot_action;

insert into schedule.schedule_bot_action(act_period, date_mask, time_mask, bot_class_name, bot_params)
    values(5, null, null, 'MtsReport', '{"login": "(915) 598-92-07",
     "password": "6wiqNt", "email": "mts@ikaserg.ru", "source_key": "79155989207"}');
insert into schedule.schedule_bot_action(act_period, date_mask, time_mask, bot_class_name, bot_params)
    values(5, null, null, 'MtsReport', '{"login": "(915) 598-91-87",
     "password": "v5zpgG", "email": "mts@ikaserg.ru", "source_key": "79155989187"}');
