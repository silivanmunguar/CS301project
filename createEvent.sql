-- Add data to Event table

insert into Events(eid, title, descrip, time, location) VALUES (1, 'Party at Gac', 'Come join our party', '2022-06-18 10:34:09', 'Gac');
insert into Events(eid, title, descrip, time, location) VALUES (2, 'Party at Sig', 'Come join our party', '2022-06-18 10:34:09', 'Sig');
insert into Events(eid, title, descrip, time, location) VALUES (3, 'Party at Coho', 'Come join our party', '2022-06-18 10:34:09', 'Coho');
insert into Events(eid, title, descrip, time, location) VALUES (4, 'Party at Jewett', 'Come join our party', '2022-06-18 10:34:09', 'Jewett');
insert into Events(eid, title, descrip, time, location) VALUES (5, 'Party at Anderson', 'Come join our party', '2022-06-18 10:34:09', 'Anderson');
insert into Events(eid, title, descrip, time, location) VALUES (6, 'Party at Stanton', 'Come join our party', '2022-06-18 10:34:09', 'Stanton');

-- Query to select all event data
SELECT * FROM Events;