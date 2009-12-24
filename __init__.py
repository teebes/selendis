"""
If upgrading from previous versions, you may need to run (in order of upgrades, so most recent is last):

alter table world_equipment add column "slot" varchar(40);

alter table anima_player add column "eq_head_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_player add column "eq_chest_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_player add column "eq_arms_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_player add column "eq_legs_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_player add column "eq_feet_id" integer REFERENCES "world_iteminstance" ("id");

alter table anima_mob add column "eq_head_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_mob add column "eq_chest_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_mob add column "eq_arms_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_mob add column "eq_legs_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_mob add column "eq_feet_id" integer REFERENCES "world_iteminstance" ("id");

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