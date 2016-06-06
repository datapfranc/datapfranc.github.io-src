Title: Draft Example
Date: 2016-5-21 11:15
Tags: dataset
Slug: draft
Author: Martin Ouellet
Status: draft

### BRD's summary stats

Ok after a few weeks spent harvesting and integrating book reviews, it is time to share some statistics.  

Overall, reviews were harvested for about 150K books, i.e. 15% of all books found in Librarything (for simplicity I'll use the term Book instead of Work here).  I've started harvesting book sequentially (ordered by work-id), and later ordered them by popularity in order to have more reviews. Some Work could not be found in other sites while many had no reviews.

| Statistics | **Librarything** | **Goodreads** | **Babelio** |
|----|----|----|---|
| Total book sample size | 32 | n.a. | n.a. |
| Book found | n.a. | 23 | 30 |
| Book without review | 32 | same | 30 | 300 |
| Total reviews |  

*Note on Amazon: did not know how to contact them to get my spider working, so decided not to harvest reviews from them*
*Note on Goodreads: a limit of 100 pages of reviews are available from Web, so popular book may not be complete (max available=3030)*
*Note on Babelio: dedicated to french literature, number of reviews harvested may not reflect their overall reviews number*

### Reviewers

How many reviewers wrote these 3?M reviews?

```sql
select site_id, count(distinct user_id) as "Nb of reviewer", count(1) / count(distinct user_id) as "Avg per reviewer",
       count(1) / count(distinct work_refid) as "Avg per book"
from integration.review
group by 1;
```


It seems reviewers are more productive on site x and less on site y. These stats will need further analysis considering the important number of reviews duplicates found (see next point).

| Site source | Nb of Reviewer | Nb of Work found | Nb of Work without Reviews | Nb of reviews |
|----|----|----|---|----|
| Librarything | 32 | same | 30 | 300 |
| Goodreads | 32 | same | 30 | 300 |
| Babelio | 32 | same | 30 | 300 |


### Most reviewed Books

The top 10 most reviewed book from my sample are:

| Book | Total Nb of reviews |
| ---- | ---- |
| book1 | 43242342 |
| book2 | 43242342 |


```sql
select concat(w.title, ' (id=', w.work_refid, ')'), count(1)
from integration.review r
join work_info w on w.work_refid = r.work_refid
group by 1
order by 2 desc
limit 20;
```



### Duplicated Reviews

That one was surprising!  Using following rules, I discover there are many duplicate reviews.
   - Only compare reviews belonging to same Work (logically)
   - Only compare reviews with text of at least 100 characters long (avoid the similar short reviews)
   - Only compare reviews with text of comparable size (however this reduces plagiarism detection)
   - Flag reviews as duplicates when their trigram similarity is above ??  

| Site source | Total nb of dupes | Avg dupes per Book | Ratio avg dupes per book over avg nb per book |
|----|----|----|---|----|
| Librarything | 32 | same | 30 | 300 |
| Goodreads | 32 | same | 30 | 300 |
| Babelio | 32 | same | 30 | 300 |


These number are intriguing and encouraged further investigation.  So I drill-down the analysis to get more details....


```sql
select sum(case when s.id IS NOT NULL 1 else 0 end) as "Total dupes"
      , sum(case when s.id IS NOT NULL 1 else 0 end) / count(distinct work_refid) as "Avg #ofdupes per book"
      ,
      avg(over  partition by ) / count(distinct work_refid) as "Ratio nb diff vs sim"
      ,

from integration.review r
left join (select review_id as id from integration.review_similarto
           union
           select other_review_id as id from integration.review_similarto) as s on (r.id = s.id)

```


Many reviews have duplicates so I tried to distinguish different cases:
