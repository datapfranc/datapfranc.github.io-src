Title: How to do data integration, the BRD example
Date: 2016-4-01 11:15
Tags: data integration, dataset, BRD
Slug: BRD-data-integration_part1


Author: Martin Ouellet

### Data Integration: one of the main BI functions

BI environment architecture is often done along the way as an after-thought. Business is pressuring technical teams on delivery, so they quickly jump designing star schema or dimensional models (the **presentation layer**), and neglect the **integration layer**.  End result : no separation of concerns exist as we're trying to integrate AND present the data all at once!

Integration and Presentation are two critical functions of BI and must be decoupled into separate layers (at least logically) reflecting their independent goals and specifications. This post is not concerned on architecture principles (see [link](http://martin-ouellet.blogspot.ch/2013/08/bi-ideal-platform.html)) but is meant to illustrate, through a simple example, how integration is done.

### Book Reviews: an example of data integration

Let's say I want to report on book reviews/rating done by users of these cool social media sites [librarything](https://librarything.com), [goodreads](https://goodreads.com) or [babelio](http:babelio). Note: I really enjoy spending time (procrastinating) on these book review sites, so my first dataset choice was deliberate knowing how important personal interest is to stay motivated).

So how should we proceed?

First, we need proper data model for both reference data (book title, authors, isbn...) and review data (rating, text).  There are other important decisions like etl/pipeline design, data quality, ..but I'll stick to data modeling here. Data modeling is done by 1) identity important business entity (ex. Author, Work, Isbn..), 2) define common entity used for integration along with candidate keys, 3) identify links/relationship between them, 4) identify descriptive attribute, .  


[Model Image]({filename}/images/blog/BRD_model.jpeg)

Let's discuss a few aspect.  First, integration is done through common Entity, i.e. Book.  Book is a generic term and we can't afford to be loose especially related to "granularity" of entity.  Amazon records reviews at book edition level, but probably more appropriate to record them at **Work** level ([concept](https://www.librarything.com/concepts)).

Next is defining natural-key for Work allowing the integration of reviews (done on same Work entity) across sits.  For that, we could choose Work's Title/Author as a composite key and face issues like spelling differences and other titles translated in different languages. A much better alternative is to use ISBN which is meant to uniquely identify editions of same work. And it turns out Lt generously produces an export called [thingISBN.xml](http://www.librarything.com/wiki/index.php/LibraryThing_APIs) available for non-commercial use.  This gives a list ISBN's belonging to Lt's Work entity (yet another by-product of work done collaboratively through social media).

So Reviews from any site can be harvested by looking up its ISBN(s) and linked together through the Lt's Work-id key lookup. This implies Lt becoming the master data source for Work.

Another decision is about **User**, could we integrate them across sites? The easiest is to consider all users across sites as different and unique. However, this does not reflect reality as many will post their reviews in multiple sites for increased visibility (ref to discussion thread about that).

Users are not easily merged across Sites directly from source data. This requires more complex business logic to be implemented (ex. of rules: users with 2 or more highly similar reviews are considered same user). Complex transformation rules do not belong to Integration layer but more to the Presentation layer.  We can still record as-is using site/username as unique key, and deal with this grouping later (and leave it for future post).


### Physical Data model

For additional description, let's leave the code speaks for itself (). It is self-documented and should be meaningful to anyone with minimal exposure to relational DB. We can see there are things that concern the logistics aspect of loads (ex. work_site_mapping), or source data idiosynchracies (work_sameas), etc..  We can observe that a lot more tables exist than our logical model.  That is done purposely to easily accommodate future extension.

```sql

------------------------------------------ Staging layer -----------------------------------------------
--------------------------------------------------------------------------------------------------------
-- Goal:   - Layer where raw data is bulk loaded from source used by integration ELT steps
--		   - Data is volatile (truncated before each new load)
--
--------------------------------------------------------------------------------------------------------
create table staging.load_audit (
    id serial primary key,
    batch_job text,
    step_name text,
    step_no int,
    status text,
    run_dts timestamp,
    elapse_sec int,
    rows_impacted int,
    output text
);

comment on table staging.load_audit is 'Metadata to report on running batch_job/steps';
comment on column staging.load_audit.status is 'Status of step';
comment on column staging.load_audit.run_dts is 'Timestamp when step run (useful for things like limiting harvest period)';
comment on column staging.load_audit.output is 'Output produced by a step like error msg when failure or additional info';


create or replace view staging.handy_load_audit as
    select id, batch_job, step_name, status, run_dts, rows_impacted
    from staging.load_audit order by 1;

create table staging.thingisbn (
    work_refid bigint,
    isbn_ori text,
    isbn13 char(13),
    isbn10 char(10),
    loading_dts timestamp
);

--comment on table staging.thingisbn is 'Data from thingISBN.xml to refresh reference work/isbn data (duplicates for couple (work_id,isbn) exist in source)';
create table staging.review (
    id bigserial primary key,
    site_logical_name text not null,
    username text,
    user_uid text,
    rating text,
    review text,
    review_date text,
    review_lang char(3),
    likes text,
    work_refid bigint not null,
    dup_refid bigint,
    work_uid text,
    title text,
    authors text,
    tags_t text,
    tags_n text,
    tags_lang varchar(3),
    parsed_review_date date,
    parsed_rating text,
    parsed_likes int,
    parsed_dislikes int,
    loading_dts timestamp,
    load_audit_id int,
    foreign key (load_audit_id) references staging.load_audit(id)
);

comment on table staging.review is 'Review and/or Rating harvested from site';
comment on column staging.review.work_refid is 'Unique identifier of the book as a piece of work (ref to lt)';
comment on column staging.review.dup_refid is 'Duplicate id associated to a unique "master" work_refid (duplicates exist in lt)';
comment on column staging.review.work_uid is 'Work id used in other site; to map with lt''s work_refid during harvest';
comment on column staging.review.parsed_review_date is 'The parse date from raw string';
comment on column staging.review.likes is 'Nb of users liking the review (concept likes, green flag)';
```

### Wrap-up

We slightly cover an important aspect of BI projects: Data integration. Doing so, it seems not much was discussed concerning Report and Presentation aspects (although in real life we'd look at these to determine data content needed). My point is that Reporting should only influence data content aspect and not modeling aspect of the integration layer.

Presentation layer is also more influenced by tools and technology, and many legacy designs (star schema modeling, aggregation, materialized view, etc.) may no longer play such important roles when it comes to MPP Cloud databases implementations and Tools.  More on that later.

Martin
