Title: BRD summary stats
Date: 2016-6-21 14:47
Tags: dataset
Slug: brd_stats
Author: Martin Ouellet
Status: draft

After a few weeks spent harvesting and integrating book reviews, it is time to share some statistics.  

Over 22 millions reviews were harvested on about 300K books, or 15% of different books listed in Librarything (for simplicity, the term Book is used instead of Work).  I've started harvesting book sequentially (by id) to later processed them by popularity as a way to get more reviews.  Some Work catalogued in Librarything could not be found in other sites while others had no reviews.

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

How many reviewers wrote these 22M reviews?

| Site source | #Reviewer | Avg #Reviews per reviewer | Avg #Reviews per book |
|----|----|----|---|
| Librarything | 84K | 14.36 | 9.96 |
| Goodreads | 2.486M | 8.26 | 130.21 |
| Babelio | 29K | 14.07 | 9.11 |


It seems reviewers are more productive on Librarything and Babelio (both actually have very similar reviewers behavior).  However the number of reviews per Book in Goodreads is larger by a factor of 10! (these numbers consider all reviews, even duplicate ones).


### Most reviewed Books

The top 10 most reviewed book from my sample (combining all sites):

| Book | Nb of reviews |
| ---- | ---- |
| The Hunger Games  |  7020 |
| Twilight (The Twilight Saga, Book 1) |  5578 |
| The Book Thief |  5155 |
| Catching Fire |  5127 |
| Harry Potter and the Sorcerer's Stone (Book 1) |  5082 |
| The Girl With The Dragon Tattoo |  5027 |
| Mockingjay |  5024 |
| The Help |  4954 |
| Divergent |  4873 |
| The Guernsey Literary and Potato Peel Pie Society |  4858 |
| Harry Potter and the Deathly Hallows |  4668 |
| The Da Vinci Code |  4616 |
| The Road |  4575 |
| Pride and Prejudice |  4545 |
| Gone Girl |  4436 |
| The Giver |  4384 |
| The Kite Runner |  4307 |
| The Curious Incident of the Dog in the Night-Time  |  4291 |
| 1984  |  4253 |
| Water for Elephants: A Novel |  4230 |



### Average appreciation and correlation

Whose site's reviewers give more favorable critic?  To answer that we need to compare average rating at <u>book</u> level.

For simplicity, let's define the metric _score_ as being the average rating for a book on a given site (after rating was standardized on a 10 points scale).  This following gives the average and standard deviation for _score_<sub>lt</sub> (Librarything), _score_<sub>gr</sub> (Goodreads) and _score_<sub>ba</sub> (Babelio):

| Site | Avg | Std dev |
| :---- | :----: | :----:|
| _score_<sub>lt</sub> | 7.496  | 1.639 |  
| _score_<sub>gr</sub> | 7.508  | 1.880 |
| _score_<sub>ba</sub> | 6.987  | 2.386 |

Reviewers from both Goodreads and Librarything are very similar in this respect, whereas reviewers from Babelio are more harsh... However, before concluding to another French's reputation, let's note that the confidence level of this average is lower for Babelio (based on a smaller number of reviews) and also confirmed by its higher standard deviation.  

Are reviewer's between different site in agreement with each other?  This can be answered by calculating correlation coefficient between score variables:

| Site          | Librarything | Goodreads | Babelio |
| :-----------  | :----------: | :--------:| :------:|
| Librarything  | 1            | +0.377    |   +0.145 |
| Goodreads     | --           | 1         |   +0.18 |
| Babelio       | --           |  --       |   1     |

Yes all scores are positively correlated but not by much.  It seems reviewers give on average similar rating, but only agree moderately on which books are good or bad.  This is especially true between Babelio and the other sites, where cultural differences seems to be at play.    


### Duplicated Reviews

That one was more surprising! Using the following simple rules, over 581K reviews were found to duplicates!
   - Only comparing reviews from same Work (logical)
   - Comparing reviews with text of at least 100 characters long (ignoring similar short reviews)
   - Comparing reviews with text of similar size (&#177; +/- 8%, however this may reduce plagiarism detection where only a subset was copied)
   - Flag reviews as duplicates when their **trigram** similarity index is above 0.7?  (although this may seem small, most similar reviews had index larger than 0.9?)  

| Metric  | Value |
| Total nb of dupes | 581K<sup>*</sup> |
| Avg dupes per Book | 2.89 |
| Ratio (avg dupes/avg nb of reviews) per book | 2.6% |

<sup>* </sup> here same reviews found twice count for 2 duplicates)

These numbers are intriguing and encouraged further investigation.  So let's drill-down the analysis a bit further....

Are these duplicates within site or across sites?

| Site          | Librarything | Goodreads | Babelio |
| :-----------  | :----------: | :--------:| :------:|
| Librarything  | 17K          | 215K      |   0.7K |
| Goodreads     | --           | 60K        |   4K  |
| Babelio       | --           |  --       |   2K    |


Can we distinguish different cases:


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

What about the languages used for reviewing?  Let's look at the distribution graph of languages.

I used the Python langid module (ref) to detect the language used in review.  To avoid getting unpredictable results it was used for reviews with at least 50 characters.   

Although Librarything classify reviews by language, these were not used for consistency with the other site and to avoid some issues where language was not set or wrong.  
