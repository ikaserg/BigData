insert into data.social_net values(1, 'Facebook', 'https://www.facebook.com/');
insert into data.social_net values(2, 'Вконтакте', 'https://vk.com/');
insert into data.social_net values(3, 'Одноклассники', 'https://ok.ru/');

delete from social.users;
insert into social.users values(3, 574248559595, 'Наталья Гринина Адвокат');
insert into social.users values(3, 575918147556, 'Юридическая Консультация Карпухин');

delete from social.users_auth;
insert into social.users_auth values(3, 574248559595, 'tkn1UI4z0QIiVWlVELixiRAqYne564oqLcs5OrwUKq0RgvHEnpxUhoChw4fQIv4EF3sc9',
  '3348a373acb5ecaead2b861b41fee11f', '89106455257', '5Y5HmwNgj6lUfYY');
insert into social.users_auth values(3, 575918147556, '',
  '', '89106442900', '1978lawyer');

insert into schedule.scheduled_action values(3, 574248559595, 'friends.online');

insert into social.user_lists values(1, 'Регистраци входа-выхода', 'Пользователи для которых собирается информация о входе выходе');

delete from social.time_slot;
insert into social.time_slot values(1, time '06:30');
insert into social.time_slot values(2, time '10:30');
insert into social.time_slot values(3, time '17:20');
insert into social.time_slot values(4, time '18:25');
insert into social.time_slot values(5, time '19:10');

insert into social.theme_types values(1, 'Промо', 'Промо записи');
insert into social.theme_types values(2, 'Новости', 'Новостные записи');
insert into social.theme_types values(3, 'Юмор', 'Юмористические записи');

insert into social.topic_themes values(1, 1, 'Юристы', '');
insert into social.topic_themes values(2, 1, 'Недвижимость', '');
insert into social.topic_themes values(3, 1, 'Семейное право', '');
insert into social.topic_themes values(4, 1, 'Уголовное право', '');
insert into social.topic_themes values(5, 1, 'Защита прав потребителя', '');
insert into social.topic_themes values(6, 1, 'Банкротсво физических лиц', '');
insert into social.topic_themes values(7, 1, 'Риэлтор', '');
insert into social.topic_themes values(8, 1, 'Наследство', '');

insert into social.topic_texts values(1, 2, 'НУЖНО ОФОРМИТЬ ДОМ, ЗЕМЛЮ ИЛИ ПРОБЛЕМЫ С СОСЕДЯМИ?', 'Опытные адвокаты помогут вам! Татьяна Морозкина 8 915 598-91-87 и Наталья Гринина 8 915 598-92-07 звоните или пишите в сообщениях.');
insert into social.topic_texts values(2, 2, 'НУЖНО ОФОРМИТЬ ЗЕМЛЮ?', 'Опытные адвокаты помогут вам! Татьяна Морозкина 8 915 598-91-87 и Наталья Гринина 8 915 598-92-07 звоните или пишите в сообщениях.');

insert into social.topic_texts values(3, 3, 'ДЕЛИТЕ ИМУЩЕСТВО?', 'Консультация по разводу и разделу имущества от опытных адвокатов Татьяна Морозкина 8 915 598-91-87 и Наталья Гринина 8 915 598-92-07 звоните или пишите в сообщениях.');
insert into social.topic_texts values(4, 3, 'ПРЕДСТОИТ РАЗВОД?', 'Консультация по разводу и разделу имущества от опытных адвокатов Татьяна Морозкина 8 915 598-91-87 и Наталья Гринина 8 915 598-92-07 звоните или пишите в сообщениях.');

insert into social.topic_texts values(5, 4, 'ВЫ ИЛИ ВАШ РОДСТВЕННИК ПОПАЛ В БЕДУ?','Нужна помощь в УГОЛОВНОМ деле? Вам помогут опытные адвокаты Наталья Гринина 8 915 598-92-07 и Татьяна Морозкина. тел 8 915 598-91-87 или пишите в сообщениях.');
insert into social.topic_texts values(6, 1, 'СКОРО СУД?', ' Грамотные адвокаты решат ваши проблемы Татьяна Морозкина 8 915 598-91-87 и Наталья Гринина 8 915 598-92-07 звоните или пишите в сообщениях. urzn.ru grinina.net');
insert into social.topic_texts values(7, 5, 'ОБМАНУЛИ В МАГАЗИНЕ ИЛИ ПРОДАЛИ НЕКАЧЕСТВЕННЫЙ ТОВАР?', 'Опытные юристы помогут грамотно решить ваши проблемы. Адвокат Наталья Гринина 8 915 598-92-07 и Татьяна Морозкина 8 915 598-91-87 звоните или пишите в сообщениях.');

insert into social.topic_texts values(8, 6, 'УСТАЛИ ОТ КРЕДИТОВ?', 'Выход есть - законное списание долгов через суд. Опытный адвокат решит ваши проблемы с кредитами. ЗВОНИТЕ 8 915 598-92-07, 8 915 598-91-87.');

insert into social.topic_texts values(9, 7, 'НУЖНО ПРОДАТЬ, КУПИТЬ ИЛИ ПОДАРИТЬ КВАРТИРУ?', 'Опытные юристы помогут вам правильно и безопасно оформить и провести сделки с недвижимостью. Звоните Наталья Гринина 8 915 598-92-07, Татьяна Морозкина 8 915 598-91-87.');

insert into social.topic_texts values(10, 8, 'ПРОБЛЕМЫ С НАСЛЕДСТВОМ?', 'Вам помогут опытные адвокаты Наталья Гринина 8 915 598-92-07 и Татьяна Морозкина. тел 8 915 598-91-87 или пишите в сообщениях.');


insert into social.bot_messages(bot_message_id, message_type_id, message)
  values (1, 1, 'Здравствуйте, я адвокат коллегии адвокатов № 2 Гринина Наталья. Для друзей в одноклассниках я даю бесплатные консультации. Если вам или вашим друзьям потребуется совет юриста, вы сможете обратиться ко мне.');
insert into social.bot_messages(bot_message_id, message_type_id, message)
  values (2, 1, 'Здравствуйте, я работаю в коллегии адвокатов № 2. Если вам нужна юридическая помощь напишите мне.');

insert into social.bot_message_sets(bot_message_set_id, name)
  values (1, 'Приглашения в друзья адвокат');

insert into social.bot_message_set_items(bot_message_set_id, bot_message_id, message_prob)
  values(1, 1, 0.5);
insert into social.bot_message_set_items(bot_message_set_id, bot_message_id, message_prob)
  values(1, 2, 0.5);

update social.bot_message_set_items
   set message_prob = 0.75
 where bot_message_set_id = 1
   and bot_message_id = 1;

update social.bot_message_set_items
   set message_prob = 0.25
 where bot_message_set_id = 1
   and bot_message_id = 2;


insert into social.bot_messages(bot_message_id, message_type_id, message)
  values (3, 2, 'Здравствуйте, я юрист Карпухин Андрей Николаевич. Для друзей в одноклассниках я даю бесплатные консультации. Если вам или вашим друзьям потребуется совет юриста, вы сможете обратиться ко мне.');
insert into social.bot_messages(bot_message_id, message_type_id, message)
  values (4, 2, 'Здравствуйте, я работаю юристом. Если вам нужна юридическая помощь напишите мне.');

insert into social.bot_message_sets(bot_message_set_id, name)
  values (2, 'Приглашения в друзья бро');

insert into social.bot_message_set_items(bot_message_set_id, bot_message_id, message_prob)
  values(2, 3, 0.5);
insert into social.bot_message_set_items(bot_message_set_id, bot_message_id, message_prob)
  values(2, 4, 0.5);
