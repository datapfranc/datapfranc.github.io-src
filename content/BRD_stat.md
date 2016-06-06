Title: Draft Example
Date: 2016-5-21 11:15
Tags: dataset
Slug: draft
Author: Martin Ouellet
Status: draft

### BRD's summary stats

Ok after a few weeks spent harvesting and integrating book reviews, I'd like to share some statistics.  

Overall, I did manage to harvest reviews for a sample of about 15?% of all work in Librarything, i.e. 1xxK books (for simplicity I'll use the term Book instead of Work here).  I've started harvesting book sequentially (order by by work-id), and then ordered them by popularity to have more reviews. Some Work could not be found in other sites and some had no reviews.


| Statistics | **Librarything** | **Goodreads** | **Babelio** |
|----|----|----|---|
| Total book sample size | 32 | n.a. | n.a. |
| Book found | n.a. | 23 | 30 |
| Book without review | 32 | same | 30 | 300 |
| Total reviews |  

*Note on Amazon: did not contact them to get my spider working, so decided not to harvest reviews from amazon (interested to see how many copy of reviews between Amazon and Goodreads)*
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
   - Flag reviews as similar when their trigram similarity is above ??  

| Site source | Total nb of similar | Ratio nb diff vs similar |  | Nb of reviews |
|----|----|----|---|----|
| Librarything | 32 | same | 30 | 300 |
| Goodreads | 32 | same | 30 | 300 |
| Babelio | 32 | same | 30 | 300 |


These number are intriguing and encouraged further investigation.  So I drill-down the analysis to get more details....







Many reviews have duplicates so I tried to distinguish different cases:
