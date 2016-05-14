Title: How to do data integration, BRD example (part2)
Date: 2016-4-01 11:15
Tags: BRD, data integration, dataset
Slug: BRD_DI_part2
Author: Martin Ouellet
Status: draft
Series: BRD-DI
Series_index: 2



## Physical Data model

For the physical data model, better let the code speaks for itself (although SQL is not well suited for self-documented code, most DB engines support explicit comment).

We can see there are things that  (ex. work_site_mapping), or source data idiosynchracies (work_sameas), etc..  We can observe that a lot more tables exist than our logical model.  That is done purposely to easily accommodate future extension.

### Staging layer

Staging layer is the first layer where data is landing once extracted from sources. It is raw (no transformation), volatile and designed for fast loading (bulk) as to limit impact on system sources. This is also a good place to save logistics/auditing aspect of loads.

```sql
------------------------------------------ Staging layer -----------------------------------------------
--------------------------------------------------------------------------------------------------------
-- Goal: - Layer where raw data is bulk loaded from source used by integration ELT steps
--		   - Data is volatile (truncated before each new load)
--       - No transformation or rules are applied on data (taken as-is from source)
--------------------------------------------------------------------------------------------------------
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
comment on column staging.review.work_refid is 'Unique identifier of book (piece of work as ref to lt)';
comment on column staging.review.dup_refid is 'Duplicate id associated to a "master" work_refid (duplicates exist in lt)';
comment on column staging.review.work_uid is 'Work id used by other site; to map with lt''s work_refid during harvest';
comment on column staging.review.parsed_review_date is 'Parsed date from raw string';
comment on column staging.review.likes is 'Nb of users liking the review (concept such as likes, green flag)';

create table staging.thingisbn (
    work_refid bigint,
    isbn_ori text,
    isbn13 char(13),
    isbn10 char(10),
    loading_dts timestamp
);
comment on table staging.thingisbn is 'Data from thingISBN.xml to refresh reference work/isbn data (No PK, as duplicates of <work_id,isbn> exist in source)'

create table staging.work_info (
    work_refid bigint unique,
    dup_refid bigint,
    title text,
    original_lang text,
    ori_lang_code char(3),
    authors text,
    authors_code text,
    mds_code text,
    mds_code_corr text,
    mds_text text,
    lc_subjects text,
    popularity text,
    other_lang_title text,
    load_audit_id int,
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table staging.work_info is 'Staging for reference data harvested from work';

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
```

### Integration --Raw Layer

Integration/raw layer is where we ... well integrate data! Ok besides this pleonasm, the important concept is to identify common business entities conformed across sources and having some common identifiers. Let's see what we got:

```sql
select * from all;

```

### Integration --Business Layer

Integration/business layer is start adding, relating, transforming raw data according to our business rules that can be complex to do only on the presentation layer. For our specific case here, we'll have:

```sql
select * from all;

```
