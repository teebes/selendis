"""
If upgrading from previous versions, you may need to run (in order of upgrades, so most recent is last):

sqlite> alter table anima_mob add column "experience" integer;
sqlite> alter table anima_player add column "experience" integer;
sqlite> update anima_mob set experience = 1;
sqlite> update anima_player set experience = 1;

sqlite> drop table world_weapon;
sqlite> drop table world_equipment;
sqlite> drop table world_misc;
sqlite> drop table world_sustenance;

sqlite> alter table anima_player add column "main_hand_id" integer REFERENCES "world_iteminstance" ("id");
sqlite> alter table anima_mob add column "main_hand_id" integer REFERENCES "world_iteminstance" ("id");

sqlite> alter table anima_player add column     "target_type_id" integer REFERENCES "django_content_type" ("id");
sqlite> alter table anima_mob add column     "target_type_id" integer REFERENCES "django_content_type" ("id");
sqlite> alter table anima_player add column "target_id" integer unsigned;
sqlite> alter table anima_mob add column "target_id" integer unsigned;

sqlite> alter table anima_mob add column "static" bool;
"""