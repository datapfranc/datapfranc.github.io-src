Title: Draft Example
Date: 2016-6-22 13:35
Tags: dataset
Slug: brd_pl_intro
Author: Martin Ouellet
Status: draft

### Presentation layer

The Presentation layer's role is to respond to all user needs for reporting, data analytics and other front-end applications like visualization or dashboard. Its goal is thus to optimize read-access (as opposed to write-access) in the most flexible way as it is impossible to predict all data access pattern from users interacting with these applications.

In this post I'll define the physical data model to be used with a [Redshift](http://amazon.com/redshift) DWH Cloud platform.  This platform implementation choice is important and influences considerably our physical data model.

### Redshift

Redshift is a Massively parallel processing (MPP) Cloud-based database suited for BI and analytics needs running on top of commodity hardware based architectures available from AWS.  Among its features, we can highlight Columnar storage, high compression data, execution of query compiled code.  More info available [here](http://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html) and I've also gathered details on a separate [post](http://martin-ouellet.blogspot.co.at/2016/07/redshift-cloud-based-data-warehousing.html) covering key aspects influencing data modeling.

### Physical Data model

BRD integration layer is highly normalized for flexibility, but this can penalize Redshift data access performance so important to Presentation layer.  So a first change is to denormalize tables such as merging descriptive tables (ex. user_..) and association ones (ex. review_similarto, work_title, ..) into their parent entity.  Also, Redshift support of [data type](http://amazon.com/rdsdatatype) is more limited than Postgres, so for example all `UUID` and `TEXT` type will need to be changed.  Note that UUID are useful for data integration load as jobs can be parallelized with no dependency on surrogate keys lookup based on natural key, but much less useful to our Presentation layer.  

The `TEXT` type are converted to `VARCHAR` using data input to determine its size, while `UUID` are replaced by `BIGINT`.  
For each table, we must also determine its Distribution type (using some assumption on expected frequent query join) and its Sort key, as well as the compression scheme of all attributes.


#### Review

`REVIEW` table is, by far, our biggest table and needs to be distributed optimally.  Its distribution key should correspond to one FK that often gets used for joining another large table.  Two logical candidates are `book_id` for table `WORK` or `reviewer_id` for table `REVIEWER`.  At this point, it is quite difficult to know whether our analysis of reviews will be against users demographic or book information (or both), so without real usage trend we'll have to decide arbitrarily... and that's ok:  one advantage of the layered-architecture is that we can always re-build Presentation-layer following any changes of optimization goals (Integration-layer safely keeps our data)!

Let's assume `book_id` is the best candidate for this, and hence co-locate reviews with their associated books data.  

As for the sorting, we'll sort rows based on their review's date as a way to optimize time-series report.

The compression chosen by Redshift was ....

```sql
-- Table DDL using 'id' as DISTRIBUTION-KEY and 'date_id' as SORT-KEY
-- the encoding scheme
create table presentation.review (
    -- dimensions links
    id bigint primary key,
    id_similarto bigint,
    book_id int not null,
    reviewer_id int not null,
    site_id smallint not null,
    date_id smallint not null, --smart-key
    -- facts
    rating smallint,
    nb_likes int,
    lang_code char(3),
    review varchar(30000),  --based on max found
    foreign key (book_id) references presentation.book(id),
    foreign key (reviewer_id) references presentation.reviewer(id),
    foreign key (site_id) references presentation.site(id),
    foreign key (date_id) references presentation.dim_date(id),
)
diststyle KEY distkey (book_id)
sortkey(date_id)
;

-- Use COPY command to let Redshift determine the best compression encoding scheme

-- After data loaded, check out compression encoding chosen  


```


#### Book

`BOOK` table holds informational data on Book reviewed.  For reason just explained we chose `id` as its distribution key. We also decided to de-normalize completely the titles used in the most popular language edition.  This will allow sending search query by title to all cluster nodes which will greatly improve performance.    

We decide to sort rows based on ???.     

The compression chosen by Redshift was ....

```sql
-- Table DDL using 'id' as DISTRIBUTION-KEY and ?? as SORT-KEY
-- the encoding scheme
create table presentation.book (
    id int primary key,
    title_ori text,
    ori_lang_code char(3),
    mds_code varchar(30),
    --calculate pop based on nb_of_reviews loaded
    --pivot 10th most popular lang
    english_title varchar(500),
    french_title varchar(500),
    german_title varchar(500),
    dutch_title varchar(500),
    spanish_title varchar(500),
    italian_title varchar(500),
    japenese_title varchar(500),
    swedish_title varchar(500),
    finish_title varchar(500),
    portuguese_title varchar(500)
);

diststyle KEY distkey (book_id)
sortkey(??)
;

-- Use COPY command to let Redshift determine the best compression encoding scheme

-- After data loaded, check out compression encoding chosen  


```



#### Reviewer

`REVIEWER` table holds informational data on users having reviewed one or more books.  ....

We decide to sort rows based on ???.     

The compression chosen by Redshift was ....

```sql
-- Table DDL using '??' as DISTRIBUTION-KEY and `??` as SORT-KEY


diststyle KEY distkey (book_id)
sortkey(??)
;

-- Use COPY command to let Redshift determine the best compression encoding scheme

-- After data loaded, check out compression encoding chosen  

```


### Complete Data Model

Ok without going over the details of all tables, let's just show a diagram of the full Presentation Data model:






Next step will be to populate it through Redshift load command and connect some kind of Client access tool for doing analytics.
