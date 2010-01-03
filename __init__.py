"""

Things that should be there by 0.2:
- level mechanism, with thresholds & extra health and all
- room remembering time of entry / exit (create a new 'tracking' app?)
- abs, dodge, parry and magic resist on armor as well as on anima
- very clean user mechanisms
- stats and combat system done

If upgrading from previous versions, you may need to run
(in order of upgrades, so most recent is last).

This is only being provided as development reference. None of these queries
should actually be run in a production system ; they don't even set up the
correct constraints.

---

alter table world_iteminstance add column "name" varchar(40);

alter table anima_player add column "next_level" integer;
alter table anima_mob add column "next_level" integer;

alter table world_weapon add column "hit_first" varchar(20);
alter table world_weapon add column "hit_third" varchar(20);

update anima_player set strength = 10;
update anima_player set agility = 10;
update anima_player set constitution = 10;
update anima_mob set strength = 10;
update anima_mob set agility = 10;
update anima_mob set constitution = 10;

alter table anima_player add column "strength" integer;
alter table anima_player add column "agility" integer;
alter table anima_player add column "constitution" integer;
alter table anima_mob add column "strength" integer;
alter table anima_mob add column "agility" integer;
alter table anima_mob add column "constitution" integer;

alter table world_iteminstance add column "modified" datetime;

update world_room set zone_id=1;
insert into world_zone (id, name) values (1, 'Capital');
alter table world_room add column "zone_id" integer REFERENCES "world_zone" ("id");

alter table anima_player add column "hands_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_mob add column "hands_id" integer REFERENCES "world_iteminstance" ("id");

alter table anima_player add column "description" text;
alter table anima_mob add column "description" text;
alter table anima_mob add column "template" bool;

alter table world_weapon add column "slot" varchar(40);
update world_weapon set slot = 'main_hand';

alter table anima_player add column "head_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_player add column "chest_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_player add column "arms_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_player add column "legs_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_player add column "feet_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_mob add column "head_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_mob add column "chest_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_mob add column "arms_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_mob add column "legs_id" integer REFERENCES "world_iteminstance" ("id");
alter table anima_mob add column "feet_id" integer REFERENCES "world_iteminstance" ("id");


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