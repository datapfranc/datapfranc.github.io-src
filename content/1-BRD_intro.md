Title: Book Reviews Dataset
Date: 2016-4-01 11:15
Tags: BRD, dataset
Category: BRD
Slug: brd-intro
Author: Martin Ouellet

### Preamble

This introduction post is written as a [recit d'anticipation](https://fr.wikipedia.org/wiki/Anticipation_(fiction)) hopefully predicting the outcome of the first *DataPlatform Franchising* experimentation!

Follow-up update at [BRD]({category}BRD).

### BRD: the first DataPlatform Franchising

**BRD** or **Book Review Dataset** is a [rich dataset](http://www.techradar.com/news/world-of-tech/why-big-data-is-crude-oil-while-rich-data-is-refined-and-the-ultimate-in-bi-1289628) gathering millions of book reviews/ratings along with book reference data. Its goals is focusing on "understanding book" in contrast to "understanding reader".  Information related to reviewers/users are anonymized (to be discussed) with only demographics info available (gender, country, age, etc..).

BRD showcase end-to-end BI and data integration expertise applied to produce a high-quality dataset collected from social media sites.

BRD is relevant for many analytical needs from applications such as recommending system, data mining and machine learning and online analytical processing (OLAP), etc.  It is useful for anyone looking to gain insights on:

* Book explicit and implicit relationships
* Book reader's social-demographics
* Review text mining to identify fake reviews, sock-puppet, griefer and troll reviewer
* Book sentiment and opinion analyst and evolution
* Book recommendation engine and collaborative filtering
* Book ratings evolution timeline and analysis
* Book and author characteristics in relation to their number of reviews
* Book reviews text analysis by applying sophisticated NLP and text mining techniques
* Book preference variation across cultural and language differences
* etc.

It provides ready-­to-­be­-consumed data :

* Book **t​itle**​ (original and translated)
* Book **a​uthor**
* Book r​eference ​data (**ISBN**, library of congress subjects, MDS, ..)
* Social **d​emographic​** of readers (reviewers)
* Review standardized **r​ating**
* Review **t​ext** (clean, dedupe, formatting and tag stripping, ..)
* **Tag** ​given to books

It contains over ? millions reviews collected from well known sites (feel free to contact us if you’re running a review’s book site):

1. Librarything.com
2. Goodreads.com
3. Amazon.com
4. International Amazon (br, ca, fr, de, in, it, jp, mx, nl, es, uk and au)
5. Babelio.fr
6. CritiquesLibres.fr

With BRD, you can start doing analytics on millions of book reviews with no initial investment and get only charged for what you consume!

### Benefits for website owner

First off, BRD has a pay­-per-­use cost policy applicable to all registered users. A percentage of benefit generated is shared with site’s owner pro­-rata (i.e. using number of reviews).

BRD focus is not about understanding users/readers behavior and profile, so it only needs site user’s unique id for integration purposes (data deduplication and demographics roll­up). BRD will neither expose it to its registered users (except for user coming from one of the participating sites).

Besides monetizing your data asset, you can also enhance your own analytical capability by extending your database with many more millions of reviews.

If you choose to participate to BRD, you can also take advantage of BRD data integrity checks and obtain special reports on:

* Data anomalies
* Plagiarism reviews check on same work
* Duplicate reviews and reviewers across sites
* Fake reviews or spam
* Other on-demand analysis

### BRD Data Integration

BRD collects and integrates heterogeneous and mutli-­source dataset into its Cloud­-based solution. All reviews are reported at Work and language level. Work is the main integration point that consolidate reviews assigned to all Books regardless of their editions/translations (whether print, digital or other form). Refer to LT’s Work concept definition.

### BRD Data Cleansing

BRD applies procedure to cleanse, conform and validate data:

1. Review Data is deduped
    * Spot reader making same reviews within/across sites
2. Data Error correction
    * Review with data issues can be flagged/corrected
    * Reviews too small or considered non meaningful can be filter out
3. Data harmonization
    * Rating are normalized to a 10 point scale to account for full stars only or half­-star
    * Tag can be aggregated across site and report as-­is or reformat to merge similar Tag (case insensitive and singular form)

### BRD status

Currently, a small percentage of reviews available from listed sites are integrated (roughly 10% of Work held by Librarything).  It should be sufficient to validate the Cloud DW design choice and experiment on some realistic analytic/visualization applications.

I'll soon contact the site owners for their feedback/interest and also discuss about future interest. Although the data is publicly available, it does not give me legal right to harvest full content of any site.  Among other things, you need to respect site licensing, limit your hitting rate, and consider a lot more issues that I can deal with (ref. the jurisprudence is far from being clear on this aspect).
