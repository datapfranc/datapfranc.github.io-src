Title: BRD summary stats
Date: 2016-6-21 14:47
Tags: dataset
Slug: brd_stats
Author: Martin Ouellet
Status: draft

After a few weeks spent harvesting and integrating book reviews, it is time to share some statistics.  

Over ?? millions reviews were harvested for about 150K books, or 15% of different books listed in Librarything (for simplicity I'll use the term Book instead of Work).  I've started harvesting book sequentially (by id) to later processed them by popularity as a way to get more reviews.  Some Work  catalogued in Librarything could not be found in other sites while many other had no reviews.

| Statistics | **Librarything** | **Goodreads** | **Babelio** |
|----|----|----|---|
| Book sample size | 32 | -- | -- |
| Book found | -- | 23 | 30 |
| Book without review | 32 | 23 | 30 |
| Number of reviews |  4.5M | 43.6M | 4.65M |

Notes:

* I did not contact Amazon to get my spider working, and decided not to harvest their reviews
* a limit of 100 pages of reviews are available from Goodreads website, so popular book may not have all reviews (max available=3030)
* Babelio is dedicated to french literature, and reviews harvested may not reflect its popularity (book sample is biased toward english and/or international best seller).


### Reviewers

How many reviewers wrote these 3?M reviews?

| Site source | #Reviewer | Avg #Reviews per reviewer | Avg #Reviews per book |
|----|----|----|---|
| Librarything | 323K | 43 | 30 |
| Goodreads | 325K | 54 | 30 |
| Babelio | 32K | 87 | 30 |


It seems reviewers are more productive on site x and less on site y. These stats will need further analysis considering the important number of reviews duplicates found (see next point).

<!--
select site_id, count(distinct user_id) as "Nb of reviewer"
      , count(1) / count(distinct user_id) as "Avg nb of reviews per reviewer"
      , count(1) / count(distinct work_refid) as "Avg nb of reviews per book"
from integration.review
group by 1;
-->

### Most reviewed Books

The top 10 most reviewed book from my sample dataset combining the three sites:

| Book | Total Nb of reviews |
| ---- | ---- |
| book1 | 43242342 |
| book2 | 43242342 |


<!--
select concat(w.title, ' (id=', w.work_refid, ')'), count(1)
from integration.review r
join work_info w on w.work_refid = r.work_refid
group by 1
order by 2 desc
limit 20;
-->

### Average appreciation and correlation

Whose site's reviewers give more favorable critic?  To answer that we need to compare average rating at <u>book</u> level between site.

For simplicity, let's define the metric _score_ as the average rating given on a book per site (where rating was standardized on a 10 points scale).  This following gives the average and standard deviation for _score_<sub>lt</sub> (Librarything), _score_<sub>gr</sub> (Goodreads) and _score_<sub>ba</sub> (Babelio):

| Site | Avg | Std dev |
| :---- | :----: | :----:|
| _score_<sub>lt</sub> | 8.3  | 2.3 |  
| _score_<sub>gr</sub> | 7.4  | 2.5 |
| _score_<sub>ba</sub> | 5.3  | 1.2 |

We see reviewer from Goodreads are slightly less harsh than LT by an average of 0.3 (rating was) ? whereas reviewer from GR are the least.....
However, Lt's reviewer tend to be more alike given the smaller standard deviation...        

Are reviewer's between different site in agreement with each other?  This can be answered by calculating correlation coefficient of our score variables by sites:

| Site          | Librarything | Goodreads | Babelio |
| :-----------  | :----------: | :--------:| :------:|
| Librarything  | 1            | +0.3      |   +0.4  |
| Goodreads     | --           | 1         |   - 0.4 |
| Babelio       | --           |  --       |   1     |


<!--
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
-->


### Duplicated Reviews

That one was more surprising!  Using these simple rules to identify duplicate reviews:
   - Only comparing reviews from same Work (logical)
   - Comparing reviews with text of at least 100 characters long (avoid similar short reviews)
   - Comparing reviews with text of similar size (&#177; +/- 8%, however this may reduce plagiarism detection)
   - Flag reviews as duplicates when their **trigram** similarity is above 0.7?  (although this may seem small, most similar reviews have index larger than 0.9?)  

| Site source | Total nb of dupes | Avg dupes per Book | Ratio avg dupes per book over avg nb per book |
|----|----|----|---|----|
| Librarything | 32 | same | 30 | 300 |
| Goodreads | 32 | same | 30 | 300 |
| Babelio | 32 | same | 30 | 300 |



<!--
with per_wid as (
 select
       r.work_refid
       , sum(case when dupes.id IS NOT NULL then 1 else 0 end) as Nb_dupes
       , count(1) as Nb_reviews
 from integration.review r
 left join (select review_id as id from integration.review_similarto
            union
            select other_review_id as id from integration.review_similarto) as dupes on (r.id = dupes.id)
 group by 1
 --for perf only.. TO BE REMOVED
 limit 200)
select
     sum(Nb_dupes) as "Total dupes"
     , sum(Nb_reviews) as "Total reviews"
     , avg(Nb_dupes) as "Avg dupes"
     , avg(Nb_dupes) / avg(Nb_reviews) as "Ratio avg dupes over avg nb reviews"
from per_wid;
-->



These numbers are intriguing and encouraged further investigation.  So let's drill-down the analysis a bit further....

Many reviews have duplicates so I tried to distinguish different cases:

Are these duplicates within site or across sites?



<!--
--here it's just the distinct dupes (the same 2 reviews only be counted once)
select sum(case when r.site_id = 1 and o.site_id = 1 then 1 else 0 end) as "Total within Lt"
     , sum(case when r.site_id = 2 and o.site_id = 2 then 1 else 0 end) as "Total within Gr"
     , sum(case when r.site_id = 4 and o.site_id = 4 then 1 else 0 end) as "Total within Ba"
     , sum(case when r.site_id = 1 and o.site_id = 2 then 1
                when r.site_id = 2 and o.site_id = 1 then 1 else 0 end) as "Total between Lt and Gr"
     , sum(case when r.site_id = 1 and o.site_id = 4 then 1
                when r.site_id = 4 and o.site_id = 1 then 1 else 0 end) as "Total between Lt and Ba"
     , sum(case when r.site_id = 2 and o.site_id = 4 then 1
                when r.site_id = 4 and o.site_id = 2 then 1 else 0 end) as "Total between Gr and Ba"
from integration.review_similarto s
join integration.review r on (s.review_id = r.id)
join integration.review o on (s.other_review_id = o.id);
-->


Duplicates assessment:

————————Site Goodreads —————————————
-Exact duplicates (sim=1): same day, same username, same site: 9120, 9119
—Near duplicates (sim=1):  same day, similar username (salcarla vs salsabrarian), same site (2):  review-ids: 4135, 4130
-Exact sim=1, same username, diff date : 15366, 8636
-same as above but two different date: 4514, 4511
-same as above but more different date: 6785 and 5542

- Duplicate with slight text var (sim=0.91): diff username, dif date, one review has prefix: ‘EDITORIAL REVIEW’: 13250,9843
- What seems to be a case of plagiarism: 13773, 13368
- Same user with some habit of duplicating: ‘Mark Valentine’ with redid (17988,16742) and (15366, 8636)
- Some write the same (in foreign lang) with its usersname in arabic and in english (30861, 28679)
- Some other may be pure coincidental: the one giving citation only (32895, 25544)
- Could it be that people simply copy reviews to get more: see 1002184-sara/6808758-shirley (revid 35315 and 32345), where sara has much more, could it be all copies .. check out username with many copies!!


563106-mark-sellers / 672130-emily




### International Reviews

What about the languages used?  Let's look at the distribution chart of languages used.

I used the Python lang_detect module (ref) to detect the language used in review.  To avoid getting unpredictable results it was used for reviews with at least 50 characters.   

Although Librarything classify reviews by language, these were not used for consistency with the other site (and to avoid some issues where language was not set or wrong).

<!--
select lang_code, count(1)
from integration.review
where lang_code not in ('--','')
group by 1
limit 20;
-->
