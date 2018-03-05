select count(*) from Frequency where docid='10398_txt_earn';
select * from Frequency order by term

select count(*) from (select term from Frequency where docid='10398_txt_earn' and `count` = 1);

--c
select * from (select term from ( select term from Frequency where docid='10398_txt_earn' and `count` = 1  UNION  select term from Frequency where docid='925_txt_trade' and `count` = 1));

--d
select count(docid) from (select docid from Frequency WHERE term = 'law' or term like 'legal' GROUP BY docid);


-- e
select docid, sum(count) as c from Frequency GROUP BY docid HAVING c >= 300;


--f
select docid from Frequency where term  = 'transactions' INTERSECT select docid from Frequency where term = 'world'

-- g
select value from (SELECT a.row_num, b.col_num, SUM(a.value*b.value) as value
FROM a, b
WHERE a.col_num = b.row_num
GROUP BY a.row_num, b.col_num)

where row_num = 2 AND col_num = 3;


create view crude as select * from Frequency where docid='10080_txt_crude';
create view earn as select * from Frequency where docid='17035_txt_earn';


select crude.docid, earn.docid, crude.term, SUM(crude.count * earn.count)
from crude, earn
where crude.term = earn.term
group by crude.docid, earn.docid;


CREATE VIEW New_Frequency as SELECT * FROM frequency
UNION
SELECT 'q' as docid, 'washington' as term, 1 as count
UNION
SELECT 'q' as docid, 'taxes' as term, 1 as count
UNION
SELECT 'q' as docid, 'treasury' as term, 1 as count;


select * from New_Frequency where docid='q';


SELECT
  Bdocid,
  sum(f) as sum_f
FROM (
  SELECT
    A.docid,
    B.docid as Bdocid,
    B.term,
    SUM(A.count * B.count) AS f
  FROM New_Frequency AS A, New_Frequency AS B
  WHERE A.term = B.term
        AND A.docid = 'q'
        AND A.docid != B.docid
  GROUP BY a.docid, B.docid)

GROUP BY Bdocid
ORDER BY sum_f DESC
