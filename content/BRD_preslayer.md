Title: Draft Example
Date: 2016-6-22 13:35
Tags: dataset
Slug: draft
Author: Martin Ouellet
Status: draft

### Presentation layer

The Presentation layer has the important role to respond to user needs for reporting, data analytics and other visualization or dashboarding applications. This layer's goal is to optimize read-access in the most flexible way as we can hardly predict all type of ad-hoc queries later triggered from these applications.

In this post I'll define the physical data model to be used with a [Redshift](http://amazon.com/redshift) DWH Cloud platform.  This platform implementation choice is important and influence considerably our physical data model.

### Redshift

Redshift is "bla bla bla".  

TODO: put the image Redshift under images/blog.


Redshift's features such as Distribution type, Column-oriented storage and compression scheme all play an important role.  I've gathered more details on a separate [post](http://martin.ouellet.blogspot.ch/rrrr)) for those interested.




### Physical Data model

Our integration layer was highly normalized for greater flexibility, and this will penalize Redshift data access performance critical to our Presentation layer.  So one change is to denormalize tables such as merging descriptive tables (ex. user_..) and association ones (ex. review_similarto, work_title, ..) into their parent entity.  Also, Redshift support of [data type](http://amazon.com/rdsdatatype) is more limited than Postgres, so for example all `UUID` and `TEXT` type will need to be changed.  Note that UUID are useful for data integration load as jobs can be parallelized with no dependency on surrogate keys lookup based on natural key, but much less useful to our Presentation layer.  

The `TEXT` type are converted to `VARCHAR` using data input to determine its size, while `UUID` are replaced by `BIGINT`.  
For each table, we must also determine its Distribution type (using some assumption on expected frequent query join) and its Sort key, as well as the compression scheme of all attributes.


#### Review

`REVIEW` table is, by far, our biggest table and needs to be distributed optimally.  The `book_id` is the best candidate for this as to colocate reviews with their associated `BOOK` (frequently joined together).  However, another good candidate would be `reviewer_id` but this can only be determined much later after real utilization.  The advantage of our layered-approach is that we can re-build the Presentation-layer at will following any changes of requirement or optimization sourcing from the Integration-layer where our data is safely kept!


We decide to sort rows based on review's date to optimize time-series chart.

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


### Other tables


Languages, Site, Date, Tag ...
