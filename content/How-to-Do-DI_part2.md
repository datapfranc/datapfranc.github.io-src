Title: How to do data integration, BRD example (part2)
Date: 2016-5-21 11:15
Tags: BRD, data integration
Slug: BRD_DI_part2
Author: Martin Ouellet
Series: BRD-DI
Series_index: 2


## Physical Data model

This post presents the physical data model. Looking back at the [logical model]({filename}How-to-Do-DI.md), we'll see it contains a lot more tables than entities defined. Relational databases are less flexible than schema-less NoSQL environments and highly normalized model is one technique to mitigate rigidity through extension. We accommodate changes by adding new structures as we discover new attributes and relationship relevant to our evolving needs. Interested reader can check methods like [Data Vault](https://en.wikipedia.org/wiki/Data_Vault_Modeling) or [Anchor Modeling](http://www.anchormodeling.com/?page_id=2).

To explain the detail of physical data model, better let the code speaks for itself.  Although SQL is not well suited for self-documented code, most DB engines support explicit comment in DDL.

### Staging sub-layer

This is where data is landing once extracted from source. It is raw, volatile (truncated before new load) and designed for speed (bulk loading) to limit impact on system sources. This is also a good place to manage logistics/auditing aspect of loads.

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

### Integration (raw) Layer

Integration is where we ... integrate data! Behind this pleonasm, integration from multi-source is only possible with common business entities conforming through same identifiers. We've discussed this previously with the choice of ISBN to be used as "anchor" point across source.

We can see all dedicated tables like `user_info` or `work_info` (normalized) that store user or work attributes.  This will allow us to add stuff later on or decide to track historical changes without affecting existing structure.   

```sql
---------------------------------- Integration layer -------------------------------------------
------------------------------------------------------------------------------------------------
-- Raw -layer: untransformed data from source without applying business rules
------------------------------------------------------------------------------------------------
create table integration.site (
    id int primary key,
    logical_name text unique,
    status text,
    create_dts timestamp not null
);
comment on table integration.site is 'Website of book reviews';
comment on column integration.site.logical_name is 'Name used as business key independent of evolving domain/url';
comment on column integration.site.status is 'Flag used to get status for sites';

create table integration.site_identifier (
    site_id int not null,
    hostname text not null,
    full_url text,
    valid_from timestamp not null,
    valid_to timestamp,
    create_dts timestamp,
    update_dts timestamp,
    primary key (site_id, valid_from),
    foreign key (site_id) references integration.site(id) on delete cascade
);
comment on table integration.site_identifier is 'Natural key, hostname, is decoupled from site_id to accommodate change in time';
comment on column integration.site_identifier.hostname is 'Hostname such as www.amazon.fr, www.amazon.com, www.thelibrary.fr';

create table integration.language (
    code char(3) primary key,
    code3 char(3) unique,
    code3_term char(3) unique,
    code2 char(2) unique,
    english_name text,
    english_iso_name text,
    french_name text,
    french_iso_name text,
    create_dts timestamp
);
comment on table integration.language is 'Language immutable reference';
comment on column integration.language.code is 'Primary key using MARC code (same as ISO 639-2 alpha-3 bibliographic code)';
comment on column integration.language.code3 is 'The ISO 639-2 alpha-3 bibliographic code (originally sourced from MARC code)';
comment on column integration.language.code3_term is 'The ISO 639-2 alpha-3 terminology code';
comment on column integration.language.code2 is 'The ISO 639-1 alpha-2 code (subset of alpha-3)';

create table integration.work (
    refid bigint primary key,
    last_harvest_dts timestamp,
    last_seen_date date,
    create_dts timestamp,
    load_audit_id int,
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table integration.work is 'Book as a single piece of work irrespective of translations, editions and title sourced from lt (taken as refernece master data)';
comment on column integration.work.refid is 'Work identifer created, curated and managed by lt';
comment on column integration.work.last_seen_date is 'Last time this work was seen during a thingisbn bulkload';

create table integration.work_info (
    work_refid bigint primary key,
    title text,
    original_lang char(3),
    popularity int,
    mds_code text,
    mds_code_ori text,
    lc_subjects text,
    create_dts timestamp,
    update_dts timestamp,
    load_audit_id int,
    foreign key (work_refid) references integration.work(refid),
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table integration.work_info is 'Attribute data related to a Work (unhistorized Satellite-type, could add history if need be)';
comment on column integration.work_info.mds_code is 'mds code without dot and truncated to align with mds_text, same as integration.mds(code)';
comment on column integration.work_info.mds_code_ori is 'The mds original code as found from lt';

create table integration.isbn (
    ean bigint primary key,
    isbn13 char(13) not null,
    isbn10 char(10),
    last_seen_date date,
    create_dts timestamp,
    load_audit_id int,
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table integration.isbn is 'ISBNs associated to Work sourced from lt (used to relate reviews between site)';
comment on column integration.isbn.ean is 'Ean used as primary-key is simply the numerical representation of isbn13';

create table integration.isbn_info (
    ean bigint primary key,
    book_title text,
    lang_code char(3),
    source_site_id int,
    create_dts timestamp,
    update_dts timestamp,
    load_audit_id int,
    foreign key (ean) references integration.isbn(ean),
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table integration.isbn_info is 'Attribute data related to ISBN (un-historized Satellite-type, could add history if need be)';

create table integration.work_isbn (
    ean bigint primary key,
    work_refid bigint,
    last_seen_date date,
    deletion_date date,
    create_dts timestamp,
    load_audit_id int,
    foreign key(ean) references integration.isbn(ean),
    foreign key(work_refid) references integration.work(refid),
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table integration.work_isbn is 'Association of work and ISBN (sourced from lt)';
comment on column integration.work_isbn.ean is 'The ISBN13 code in numerical, defined as PK so one ean only associated to 1 work';

create table integration.author (
    id uuid primary key,
    code text unique,
    create_dts timestamp,
    load_audit_id int,
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table integration.author is 'Author sourced from lt';
comment on column integration.author.id is 'Identifier derived from MD5 hashing of code';
comment on column integration.author.code is 'Unique and disambiguation code given by lt: /author/lnamefname-x';

create table integration.author_info (
    author_id uuid primary key,
    name text,
    legal_name text,
    gender char(1),
    nationality text,
    birth_year smallint,
    create_dts timestamp,
    update_dts timestamp,
    load_audit_id int,
    foreign key (author_id) references integration.author(id),
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table integration.author_info is 'Author info sourced from lt';

create table integration.work_author (
    work_refid bigint,
    author_id uuid,
    create_dts timestamp,
    load_audit_id int,
    primary key (work_refid, author_id),
    foreign key (work_refid) references integration.work(refid),
    foreign key (author_id) references integration.author(id),
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table integration.work_author is 'Association between Work and its author(s), sourced from lt';

create table integration.work_title (
    work_refid bigint,
    lang_code char(3),
    lang_text text,
    title text,
    create_dts timestamp,
    load_audit_id int,
    primary key (work_refid, lang_text),
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table integration.work_title is 'Title of work in different language edition';
comment on column integration.work_title.lang_text is 'Language is used as PK and preserve so we spot missing language ref';

create table integration.user (
    id uuid primary key,
    user_uid text,
    site_id int,
    username text,
    last_seen_date date,
    create_dts timestamp,
    load_audit_id int,
    unique (user_uid, site_id),
    foreign key (site_id) references integration.site(id) on delete cascade,
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table integration.user is 'User having contributed in some way to a site (submitted rating, review, list own''s book, etc..)';
comment on column integration.user.id is 'Primary-key generated by MD5 hashing of concat(user_uid, site_logical_name)';
comment on column integration.user.user_uid is 'Site system-generated id to identify the user if present,(more stable than username), otherwise same as username)';
comment on column integration.user.username is 'Username or pseudo associated to the user';

create table integration.review(
    id bigserial primary key,
    work_refid bigint not null,
    user_id uuid not null,
    site_id int not null,
    rating text,
    parsed_rating int,
    likes text,
    parsed_likes int,
    review text,
    review_date date,
    review_lang char(3),
    create_dts timestamp,
    load_audit_id int,
    foreign key (work_refid) references integration.work(refid),
    foreign key (user_id) references integration.user(id),
    foreign key (site_id) references integration.site(id),
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table integration.review is 'Review and/or rating done for a Work in a specific language by a user, with no PK since most sites do not restrict users from reviewing same book multiple times';
comment on column integration.review.user_id is 'User identifier derived from MD5 hashing of username, site (ref. integration.derive_userid)';

-- skipping a few other tables...
```

Work_site_mapping table plays an important role in integration. We collect reviews associated to Work from multiple sites, but each have their own work identifier (`work_uid`). After finding these `work_uid` through a look-up of ISBN values, we store them and provide mapping with the Librarything's reference (`work_refid`). We also use this table to keep track of when reviews were last harvested for this site's Work.

`Work_refid` is thus essential to our integration as many other elements (see above `work`, `reviews`..) are tied to Work using this reference identifier.

```sql
create table integration.work_site_mapping(
    work_refid bigint not null,
    work_uid text not null,
    site_id int not null,
    last_harvest_dts timestamp not null,
    title text,
    book_lang text,
    authors text,
    create_dts timestamp,
    load_audit_id int,
    primary key(work_refid, work_uid, site_id),
    foreign key(work_refid) references integration.work(refid),
    foreign key(site_id) references integration.site(id),
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table integration.work_site_mapping is 'Map between work ref_id in lt and work_uid (id used by other site)';
comment on column integration.work_site_mapping.work_refid is 'Reference work id used in lt';
comment on column integration.work_site_mapping.work_uid is 'Id used in other site.  Value of -1 means no work found. Values -2 mans more than one id associated to same refid and not wish to tie them to the refid until reviews are found (e.g. asin for AZ) ';
comment on column integration.work_site_mapping.last_harvest_dts is 'Last time work was harvested';
comment on column integration.work_site_mapping.title is 'Book title, author, lang are for QA purposes (mapping between sites done through isbn(s) lookup)';
```

### Consolidation --Business Layer

Next, we'll discuss another (sub)layer called Business.  Here terminology and practice vary much (we may have sub-layer like Business, Semantic, or simply adding components to Presentation layer .), but the important features is that we need to enrich, correct, transform raw data according to our business rules.  And these may be too complex to implement downstream on one shot. From our specific example, in this layer we we'll fix data issues and start creating added-value components useful for Presentation layer.

Let's postpone this on a future post.
