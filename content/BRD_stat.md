Title: BRD summary stats
Date: 2016-6-28 14:47
Tags: BRD, dataset
Slug: brd_basicstat
Author: Martin Ouellet


After a few weeks spent harvesting and integrating a sample of book reviews, it is time to share some statistics.  

Over **22 millions** reviews have been harvested on about 300K books (I use the term Book here instead of Work).  I've started harvesting book sequentially (by id) and later processed them by popularity as a way to get more reviews.  Some Book catalogued in Librarything could not be found in other sites while others had no reviews.


| Statistics | **Librarything** | **Goodreads** | **Babelio** |
|----|----|----|---|
| Book sample size | 300K | -- | -- |
| Book found | -- | 216K | 78K |
| Number of reviews |  1.2M | 20.5M | 415K |

Notes on Amazon [ref]I did not contact Amazon to get my spider working (their sites are not robot friendly since many try to get financial advantages from their data), and decided not to harvest their reviews[/ref], Goodreads [ref]Goodreads has a limit of 100 pages of reviews available on website, so popular book may not have all reviews (max available=3030)[/ref] and Babelio [ref]Babelio is dedicated to french literature, and books found and reviews harvested may not reflect its popularity (sample is biased toward english and/or international best seller)[/ref]


## Reviewers

How many reviewers wrote these 22M reviews?

| Site source | #Reviewer | Avg #Reviews per reviewer | Avg #Reviews per book |
|----|----|----|---|
| Librarything | 84K | 14.36 | 9.96 |
| Goodreads | 2,486K | 8.26 | 130.21 |
| Babelio | 29K | 14.07 | 9.11 |


It seems reviewers are more productive on Librarything and Babelio (both actually have very similar reviewers behavior), however the number of reviews per Book in Goodreads is larger by a factor of 10 (due to its much larger user base).


## Most reviewed Books

The top 10 most reviewed books from this sample are:

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


## Appreciation differences and correlation

Whose site reviewers give more favorable critic?  To answer that we need to compare average rating at <u>book</u> level.

For simplicity, let's define the metric **_score_** as being the average rating for a book on a given site (after rating was standardized on a 10 points scale).  The following table gives the average and standard deviation of **_score_<sub>lt</sub>** (Librarything), **_score_<sub>gr</sub>** (Goodreads) and **_score_<sub>ba</sub>** (Babelio) calculated over all books:

| Site | Avg | Std dev |
| :---- | :---- | :---- |
| _score_<sub>lt</sub> | 7.496  | 1.639 |  
| _score_<sub>gr</sub> | 7.508  | 1.880 |
| _score_<sub>ba</sub> | 6.987  | 2.386 |

Reviewers from both Goodreads and Librarything are very similar in this respect, whereas reviewers from Babelio are more harsh...before drawing conclusion, let's note that the confidence level of Babelio's average is lower (based on a smaller number of reviews as shown by its higher standard deviation).  

Also, there is not much variation in user's rating, with standard deviation less than 2 on a 10 point scale, it seems most people give similar rating.

Are reviewer's between different site in agreement with each other?  This can be answered by calculating correlation coefficient between the score variables:

| Site          | Librarything | Goodreads | Babelio |
| :-----------  | ----- | ----- | ----- |
| Librarything  | 1            | +0.377    |   +0.145 |
| Goodreads     | --           | 1         |   +0.18 |
| Babelio       | --           |  --       |   1     |

Yes all scores are positively correlated but not by much.  It seems reviewers give on average similar rating, but only agree moderately on which books are good or bad.  This is especially obvious between Babelio and other sites, where cultural differences seem to be at play.     


## Duplicated Reviews

Over **581K** reviews were identified as very similar!  These were found using the following simple rules:

   - Only comparing reviews from same Work (logical)
   - Comparing reviews with text of at least 100 characters long (ignoring similar short reviews)
   - Comparing reviews with text of similar size (&#177;8%)
   - Flag reviews as duplicates when their **trigram** [similarity index]({filename}How-to-Do-DI_part3.md) is above 0.7 (although this may seem small, most similar reviews had index larger than 0.9)

| Metric  | Value |
| ---- | ---- |
| Total nb of duplicates<sup>*</sup> | 581K |
| Avg nb of reviews per Book | 110.1 |
| Avg nb of duplicates per Book | 2.89 |
| Ratio avg duplicates/avg reviews | 2.6% |

<sup>* </sup> When 2 reviews are considered similar, nb of duplicates count is 2.

These numbers are important and encourage further investigation.  So let's drill-down the analysis a bit further...

#### Are these duplicates within or across sites?

| Site          | Librarything | Goodreads | Babelio |
| :-----------  | ----- | -----| -----|
| Librarything  | 17K          | 215K      |   0.7K |
| Goodreads     | --           | 60K        |   4K  |
| Babelio       | --           |  --       |   2K    |

(Note: 2 reviews considered similar are counted as only one duplicate here).

It seems like a large proportion are originating from users copying their reviews between Librarything and Goodreads.

Let's look at some examples to distinguish various cases:

#### Case: Identical duplicates

| Site | Username | Published Date | Review |
| :-----------  | :---------- | :--------| :------|
| Goodreads  | Dead John Williams | 2015-05-31 |  *His evocation of the city is so overwhelming and powerful that you can feel that you know this place. It is seedy, run down and dangerous. It stinks, it is decrepit and corrupt and yet it is...* |
| Goodreads  | Dead John Williams | 2015-05-31 | *His evocation of the city is so overwhelming and powerful that you can feel that you know this place. It is seedy, run down and dangerous. It stinks, it is decrepit and corrupt and yet it is...* |

These cases are probably technical errors. (review_id: 9120, 9119)

#### Case: Different username

| Site | Username | Published Date | Review |
| :-----------  | :---------- | :--------| :------|
| Goodreads  | Salcarla | 2016-02-03 | *In the new world order that is the United States Federated Economic Bloc, Hack Nike is a hapless merchandising officer who accepts an assignment from VP John Nike to kill 10 people who've purchased the hot new Mercury...* |
| Goodreads  | Salsabrarian | 2016-02-03 | *In the new world order that is the United States Federated Economic Bloc, Hack Nike is a hapless merchandising officer who accepts an assignment from VP John Nike to kill 10 people who've purchased the hot new Mercury...* |

These cases are users with either many identities or issues with their change of identity (review_id: 4135, 4130)

#### Case: Different published date

| Site | Username | Published Date | Review |
| :-----------  | :---------- | :--------| :------|
| Goodreads  | Mark Valentine | 2016-03-06 | *Much of the standard Harry Potter staples have been included, but I was disappointed by several things:...* |
| Goodreads  | Mark Valentine | 2016-01-17 | *Much of the standard Harry Potter staples have been included, but I was disappointed by several things:...* |
| Goodreads  | Mark Valentine |  2016-03-13 | *I have read this now about four or five times and it never ceases to impress me. This time I sensed that the brutality of his experiences came from an iron commitment to tell the truth. He lived his life with complete focus on achieving first, freedom,...* |
| Goodreads  | Mark Valentine | 2016-01-17 | *I have read this now about four or five times and it never ceases to impress me. This time I sensed that the brutality of his experiences came from an iron commitment to tell the truth. He lived his life with complete focus on achieving first, freedom,...* |

These cases of same review on different date could be due to technical issues or user re-entering reviews (review_id: 15366, 8636 & 17988,16742)


#### Case: Different published date & username

| Site | Username | Published Date | Review |
| :-----------  | :---------- | :--------| :------|
| Goodreads  | Gary Duncan | 2016-01-24 | *Couldn't get into this as hard as I tried. Possibly with more perseverance I might've stuck it out, but plot got too confusing.* |
| Goodreads  | Gary | 2013-11-07 | *Couldn't get into this as hard as I tried. Possibly with more perseverance I might've stuck it out, but plot got too confusing.* |
| Goodreads  | K.H. Vaughan | 2012-11-21 | *A well-written and compelling account of helicopter operations in Vietnam and the personal price paid by the men who flew them. There are many eye-witness combat accounts, but what made this one stand out for me was the way in which...* |
| Goodreads  | Ken | 2016-01-22 | *A well-written and compelling account of helicopter operations in Vietnam and the personal price paid by the men who flew them. There are many eye-witness combat accounts, but what made this one stand out for me was the way in which...* |


These cases are probably users with many identities (review_id: 4514,4511 and 6785,5542 and 30861,28679) (did not print these last two in arabic which somehow messes up with markdown editing)


#### Case: Slight variation of text and different username & date

| Site | Username | Published Date | Review |
| :-----------  | :---------- | :--------| :------|
| Goodreads  | Bettie☯ | 2014-05-08 | *The man known as Cheradenine Zakalwe was one of Special Circumstances' foremost agents, changing the destiny of planets to suit the Culture through intrigue, dirty tricks or military action. The woman...* |
| Goodreads  | Dave | 2013-01-08 | *EDITORIAL REVIEW: The man known as Cheradenine Zakalwe was one of Special Circumstances' foremost agents, changing the destiny of planets to suit the Culture through intrigue, dirty tricks or military action. The woman...* |
| Goodreads  | Jimmy | 2012-05-29 | *Caucasia is one of the better books that I've read. It was a very touching story that just made me want to read more. It taught me the impacts that can be made by being together with people of different race and color. It also showed me what a simple little girl would feel if she was judged and if her family was judged too. In fact, I noticed how it was actually the reality in life, no matter how harsh the journey in one's life was, only a few people will be concerned of it...* |
| Goodreads  | Charlene | 2012-04-05 | *Caucasia is one of the nicest book I've read. It was truly a touching work of art. It taught me the impacts that can be made by being biased with people of different race and color. It showed me what a simple little girl would feel if she was judged and if her family was judged. In fact, I noticed how it was actually the reality in life, no matter how harsh the journey in one's life was, only a few people will be concerned of it...* |

Here the first two have similarity index = 0.91, due to the 'EDITORIAL REVIEW:' added to one of the review.  The second example could well be case of plagiarism with similarity index = 0.7804. (review_id: 13250,9843 and 13773, 13368)


#### Case: Quotation

| Site | Username | Published Date | Review |
| :-----------  | :---------- | :--------| :------|
| Goodreads  | Roddy Williams | 2013-08-25 | *'The metropolis of New Crobuzon sprawls at the centre of the world. Humans and mutants and arcane races brood in the gloom beneath its chimneys,...'* |
| Goodreads  | Feistytiger | 2012-05-09 | *The metropolis of New Crobuzon sprawls at the centre of its own bewildering world. Humans and mutants and arcane races throng the gloom beneath its chimneys,,..* |

Example like these are taken from a back cover of a book (this one was from a China Miéville's book), so most probably coincidental. (review_id: 32895, 25554)


#### Case Summary stats

In summary, it seems the bulk of duplicates originate from people copying their reviews across sites (a large number also due to technical issues) :

| Case/Site     | # of occurence |
| :-----------  | :----------: |
| Case 1 (same date, username & site) | 47.3K |
| Case 2 (same date & site, diff username) | 2.7K |
| Case 3 (same username & date, diff date) | 7.9K |
| Case 4 (same username & site, diff site) | 2.6K |
| Case 5 (same username, diff date & site) | 5.2K |
| Case 6 (same date, diff username & site) | 47.7K |
| Case 7 (diff site, date & username) | 164.9K |
