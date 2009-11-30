"""
Run on prod:

sqlite> drop table world_weapon;
sqlite> drop table world_equipment;
sqlite> drop table world_misc;
sqlite> drop table world_sustenance;

sqlite> alter table anima_player add column "main_hand_id" integer REFERENCES "world_iteminstance" ("id");
sqlite> alter table anima_mob add column "main_hand_id" integer REFERENCES "world_iteminstance" ("id");

   
"""