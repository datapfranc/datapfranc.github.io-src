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

### Average appreciation

Whose site's reviewers give more favorable critic?  To answer that we need to compare average rating at <u>book</u> level:  first calculate average rating per book per site then average over their differences.

| Site          | Librarything | Goodreads | Babelio |
| :------------ | :----------: | :--------:| :------:|
| Librarything  | 8.3 (0.4)    | +0.3 (-0.02) |   +0.4 (+0.04) |
| Goodreads     |              |  7.4 (0.4)   |   -0.2 ()      |
| Babelio       |              |           |   8.1 ()    |

We see reviewer from Gd are less harsh than LT by an average of 0.3 (rating was standardized on a 10 points scale) ? whereas reviewer from GR are the least.....

The number in parenthesis gives the standard deviation differences (again at book level). Reviewer from GR tend to be more in aggreement than the reviewers from the other sites...        

```sql
--base table to construct
create table public.res_stats as
(select work_refid
       , avg(case when site_id = 1 then parsed_rating else null end) as avg_rating_lt
       , stddev(case when site_id = 1 then parsed_rating else null end) as std_rating_lt
       , sum(case when site_id = 1 then 1 else 0 end) as ctn_lt
       , avg(case when site_id = 2 then parsed_rating else null end) as avg_rating_gr
       , stddev(case when site_id = 2 then parsed_rating else null end) as std_rating_gr
       , sum(case when site_id = 2 then 1 else 0 end) as ctn_gr
       , avg(case when site_id = 4 then parsed_rating else null end) as avg_rating_ba
       , stddev(case when site_id = 4 then parsed_rating else null end) as std_rating_ba
       , sum(case when site_id = 4 then 1 else 0 end) as ctn_ba       
from integration.review
group by work_refid);

select
   avg(avg_rating_lt) as mean_lt, avg(std_rating_lt) as std_lt
   , avg(avg_rating_gr) as mean_gr, avg(std_rating_gr) as std_gr
   , avg(avg_rating_ba) as mean_ba, avg(std_rating_ba) as std_ba
   , avg(avg_rating_lt-avg_rating_gr) as mean_lt_gr, avg(std_rating_lt-std_rating_gr) as std_lt_gr
   , avg(avg_rating_lt-avg_rating_ba) as mean_lt_ba, avg(std_rating_lt-std_rating_ba) as std_lt_ba
   , avg(avg_rating_gr-avg_rating_ba) as mean_gr_ba, avg(std_rating_gr-std_rating_ba) as std_gr_ba
   , corr(avg_rating_lt, avg_rating_gr) as corr_lt_gr
   , corr(avg_rating_lt, avg_rating_ba) as corr_lt_ba
   , corr(avg_rating_gr, avg_rating_ba) as corr_gr_ba
from public.res_stats
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




### Site Correlation

Are reviewer's between different site in agreement with each other?  This can be answered by calculating correlation coefficient of average rating between different sites:

| Site          | Librarything | Goodreads | Babelio |
| :-----------  | :----------: | :--------:| :------:|
| Librarything  | 1            | +0.3      |   +0.4  |
| Goodreads     | --           | 1         |   - 0.4 |
| Babelio       | --           |  --       |   1     |



### International Reviews

What about the languages used?  Let's look at the distribution chart of languages used.

```sql
select lang_code, count(1)
from integration.review
where lang_code not in ('--','')
group by 1
limit 20;
```

I used the Python lang_detect module (ref) to detect the language used in review.  To avoid getting unpredictable results it was used for reviews with at least 50 characters.   

Although Librarything classify reviews by language, these were not used for consistency with the other site (and to avoid some issues where language was not set or wrong).
