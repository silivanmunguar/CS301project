-- Add data to Event table

insert into Events(eid, title, descrip, time, location, sid) VALUES (1, 'Party at Gac', 'Come join our party', '2022-06-18 10:34:09', 'Gac', 1);
insert into Events(eid, title, descrip, time, location, sid) VALUES (2, 'Party at Sig', 'Come join our party', '2022-06-18 10:34:09', 'Sig', 2);
insert into Events(eid, title, descrip, time, location, sid) VALUES (3, 'Party at Coho', 'Come join our party', '2022-06-18 10:34:09', 'Coho', 3);
insert into Events(eid, title, descrip, time, location, sid) VALUES (4, 'Party at Jewett', 'Come join our party', '2022-06-18 10:34:09', 'Jewett', 4);
insert into Events(eid, title, descrip, time, location, sid) VALUES (5, 'Party at Anderson', 'Come join our party', '2022-06-18 10:34:09', 'Anderson', 5);
insert into Events(eid, title, descrip, time, location, sid) VALUES (6, 'Party at Stanton', 'Come join our party', '2022-06-18 10:34:09', 'Stanton', 6);

-- Query to select all event data
SELECT * FROM Events;