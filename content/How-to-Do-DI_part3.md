Title: How to do data integration, BRD example (part3)
Date: 2016-5-24 9:07
Tags: BRD, data integration
Slug: BRD_DI_part3
Author: Martin Ouellet
Status: draft
Series: BRD-DI
Series_index: 3

## Business Layer

As said in previous post, in this layer we start adding and complementing our ^raw data with useful elements needed by our Presentation/Delivery layer. Here we can start fixing data issues, grouping and associating similar entities, applying business rules, etc.


Data issues :
handling Work-id found inside thingISBN.xml but corresponding to duplicates of other id (merged to the same Work). These are discovered during harvesting, as LT website re-directs request made to thee duplicates ids to the "master" work.  

Other data processing is linking very similar reviews together so they can be reported as duplicates and/or used to identify same user (to be discussed in separate post).

```sql
-----------------------------------------------------------------------------------------------
-------------------------------------- Business layer -----------------------------------------
--          - 2) Business sub-layer: apply transformation to help preparing for presentation layer
--                 ex.) de-duplication (same_as for work, user, review, etc...)
--                 ex.) any sort of standardization/harmonization...
------------------------------------------------------------------------------------------------

create table integration.work_sameas (
    work_refid bigint,
    master_refid bigint,
    create_dts timestamp,
    load_audit_id int,
    primary key (work_refid),
    foreign key (work_refid) references integration.work(refid),
    foreign key (master_refid) references integration.work(refid),
    foreign key (load_audit_id) references staging.load_audit(id)
);
comment on table integration.work_sameas is 'Different work_refid may exist in lt for same "master" Work';
comment on column integration.work_sameas.master_refid is 'The "master" work that work_refid refers to';


-- .. recursive hierarchical relations
create table integration.mds_parent (
    code text,
    parent_code text,
    create_dts timestamp,
    load_audit_id int,
    primary key (code, parent_code),
    foreign key (code) references integration.mds(code),
    foreign key (parent_code) references integration.mds(code),
    foreign key (load_audit_id) references staging.load_audit(id)
);

create table integration.review_similarto (
    rev_id bigint,
    other_rev_id bigint,
    similar_index float,
    check (other_rev_id < rev_id),
    primary key(rev_id, other_rev_id),
    foreign key(rev_id) references integration.review(id),
    foreign key(other_rev_id) references integration.review(id),
    create_dts timestamp,
    load_audit_id int,
    foreign key (load_audit_id) references staging.load_audit(id)
);

--could be convenient for downstream to store all pair-wise of similar review ??
comment on table integration.review_similarto is 'To track down reviews with similarity';
comment on column integration.review_similarto.rev_id is 'Review-id constraint that it is larger than other_rev_id (avoid dup pairwise comparison)'
comment on column integration.review_similarto.other_rev_id is 'The other similar review-id';

create table integration.user_sameas (
    user_id uuid not null,
    same_user_id uuid not null,
    valid_from timestamp not null,
    valid_to timestamp,
    create_dts timestamp,
    update_dts timestamp,
    load_audit_id int,
    primary key (user_id, same_user_id, valid_from),
    foreign key (user_id) references integration.user(id) on delete cascade,
    foreign key (same_user_id) references integration.user(id) on delete cascade,
    foreign key (load_audit_id) references staging.load_audit(id)
);

comment on table integration.user_sameas as 'Store "same-as" user across sites spotted when multiple reviews have very similar text (exact rules TBD)';
comment on column integration.user_sameas.user_id as 'All user_id in diff sites recognized as same user';
comment on column integration.user_sameas.same_user_id as 'Flag to identify same user_id (taken arbitrarily)';
```


## Linking reviews

There is no direct way from our source data to link/merge same user from different sites.  One (indirect) way, could be to use review raw text and measure their similarity index against each other. We could have received a business rules similar to :  *Flag user from different sites as being the same use whenever more than, say 3 review have similarity close to*.

talk about which distance/algo to use

### Similarity calculation

present the code sql used ...

```sql
select * from dummy
```


### Result Example
