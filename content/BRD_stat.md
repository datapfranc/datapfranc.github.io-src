Title: BRD summary stats
Date: 2016-6-21 14:47
Tags: dataset
Slug: brd_stats
Author: Martin Ouellet
Status: draft

After a few weeks spent harvesting and integrating book reviews, it is time to share some statistics.  

Over ?? millions reviews were harvested for about 300K books, or 15% of different books listed in Librarything (for simplicity I'll use the term Book instead of Work).  I've started harvesting book sequentially (by id) to later processed them by popularity as a way to get more reviews.  Some Work catalogued in Librarything could not be found in other sites while others had no reviews.

| Statistics | **Librarything** | **Goodreads** | **Babelio** |
|----|----|----|---|
| Book sample size | 300K | -- | -- |
| Book found | -- | 216K | 78K |
| Number of reviews |  4.5M | 43.6M | 4.65M |

Notes:

* I did not contact Amazon to get my spider working, and decided not to harvest their reviews
* a limit of 100 pages of reviews are available from Goodreads website, so popular book may not have all reviews (max available=3030)
* Babelio is dedicated to french literature, and books found and reviews harvested may not reflect its popularity (sample is biased toward english and/or international best seller).


### Reviewers

How many reviewers wrote these 3?M reviews?

| Site source | #Reviewer | Avg #Reviews per reviewer | Avg #Reviews per book |
|----|----|----|---|
| Librarything | 84K | 14.36 | 9.96 |
| Goodreads | 2.486M | 8.26 | 130.21 |
| Babelio | 29K | 14.07 | 9.11 |


It seems reviewers are more productive on Librarything and Babeliom (both actually have similar reviewers behavior).  Howver the number of reviews per Book in Goodreads is larger by a scale factor (10X times)! (these numbers consider all reviews even duplicate one, see next point).


### Most reviewed Books

The top 10 most reviewed book from my sample (combining all sites):

| Book | Nb of reviews |
| ---- | ---- |
| book1 | 43242342 |
| book2 | 43242342 |



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




These numbers are intriguing and encouraged further investigation.  So let's drill-down the analysis a bit further....

Many reviews have duplicates so I tried to distinguish different cases:

Are these duplicates within site or across sites?



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

I used the Python langid module (ref) to detect the language used in review.  To avoid getting unpredictable results it was used for reviews with at least 50 characters.   

Although Librarything classify reviews by language, these were not used for consistency with the other site (and to avoid some issues where language was not set or wrong).
