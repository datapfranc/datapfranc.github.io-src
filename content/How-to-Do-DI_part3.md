Title: How to do data integration, BRD example (part3)
Date: 2016-6-2 9:07
Tags: BRD, data integration
Slug: BRD_DI_part3
Author: Martin Ouellet
Series: BRD-DI
Series_index: 3

## Business Layer

This layer contains derived data needed by Presentation/Delivery layer. We can build components like associations, groupings or hierarchies defined by Business Rules, and also do data cleansing to fix issues found in our *raw data*.  

### Building new association: Similar Reviews

Let's say we're required to find similar reviews written on Work. This could be useful for:

* Identify duplication issues
* Identify users duplicating reviews within or across sites
* Identify spam where reviews are written to bias opinion
* Find plagiarism among reviewers

How do we do that?  Data processing on unstructured text is more efficiently done with NoSQL engines with massively parallel processing capability (MPP).  These engines leverage a "divide and conquer" strategy by distributing reviews among different cluster nodes. This is a good illustration of complementary usage/collaboration between modern NoSQL engine and more traditional RDBMS-based approach.   

However for this demonstration, neither data volume/rate nor latency constraint impose the use of such MPP-based engines.  We can directly proceed within PostgreSQL by leveraging text comparison functions like trigram (see module [pg_trgm](https://www.postgresql.org/docs/current/static/pgtrgm.html)).


> [N-gram](https://en.wikipedia.org/wiki/N-gram) is a way to represent documents as set of sequential items (could b words, letters...).  Trigram is the 3-item version of the generic n-gram and for letters will results to a 26^3 dimensional space.  It's shownmonstrated that two documents with similar n-gram vector-representation are likely to be similar, and consequently this technique has many applications in [NLP](https://en.wikipedia.org/wiki/N-gram#Applications_and_consideration) (e.g. identifying lexically similar documents, detecting plagiarism, ..).  

Here's an example of two reviews done on the book _A People's History of the United States_ :

|User-uid|Review text|
|:----|:----|
|21587504-zeus-polak| *This should be required reading for every American.* |
|14259285-samantha|  *every american should be required to read this book.* |

The similarity index between the two is 0.732143. This correctly reflects the fact that both convey the same meaning (robust in relation to ordering of words). However, to avoid catching too many of these small variations of words permutation we'll filter out too short reviews (see below).

#### Database implementation

Let's define a working table `rev_similarto_process` that will store all needed review-to-review pair combinations:

```sql
create table integration.rev_similarto_process (
    work_refid bigint not null,
    review_id bigint not null,
    text_length int not null,
    review_lang char(3),
    other_review_id bigint,
    similarity float,
    date_processed timestamp,
    create_dts timestamp,
    load_audit_id int,
    primary key (work_refid, review_id),
    check (other_review_id < review_id)
);

comment on table integration.rev_similarto_process is 'Use to help manage the similar processing reviews (keep all reviews processed or being processed';
comment on column integration.rev_similarto_process.review_id is 'The review being compared for similarity';
comment on column integration.rev_similarto_process.other_review_id is 'The other review found to be similar to review (min id if more than one found, or NULL if none is found)';
comment on column integration.rev_similarto_process.similarity is 'Similarity index between the two reviews using tri-gram (pg_trgm)';
comment on column integration.rev_similarto_process.date_processed is 'Flag indicating when review comparison was processed (NULL when not yet processed)';
```

Out of the mXm possible pairs of reviews (assuming there are m reviews for the Work), we can ignore the same review pair where review is compared to itself.  We can also avoid comparing twice same pair, so only need distinct pair or combination (binomial coefficients m choose 2). Using the source `rev_similarto_process`, this would translate into SQL as:

```sql
select rev.work_refid,
        ,rev.review_id as id, r.review, r.site_id
        ,other.review_id as other_id, o.review as other_review, o.site_id as other_site_id
        ,similarity(r.review, o.review)
from integration.rev_similarto_process rev
join integration.review r on (rev.review_id = r.id)
join integration.rev_similarto_process other on
          (rev.work_refid = other.work_refid
          and rev.review_lang = other.review_lang
          and rev.review_id > other.review_id
          and rev.text_length between other.text_length - round(other.text_length * %(len_delta)s) and
                                      other.text_length + round(other.text_length * %(len_delta)s))
join integration.review o on (other.review_id = o.id)
where
  rev.date_processed IS NULL
  and rev.text_length >= %(len_min)s
  and other.text_length >= %(len_min)s
```

Joining reviews on `work_refid` produces a mXm cross-product which is reduced by the clause `and rev.review_id > other.review_id`.  We further reduce pairs by keeping reviews of same language (`rev.review_lang = other.review_lang`), with similar number of characters (`rev.text_length between other.text_length - round(other.text_length * %(len_delta)s)` `and  other.text_length + round(other.text_length * %(len_delta)s))`) and finally with a minimum number of characters  (`rev.text_length >= %(len_min)s`) (useless to compare "Very Good" and "Excellent!" type of reviews).

We calculate similarity of each pairs and can populate the end-result table using a threshold on similarity:

```sql
create table integration.review_similarto (
    review_id bigint,
    other_review_id bigint,
    similarity float,
    check (other_review_id < review_id),
    primary key(review_id, other_review_id),
    foreign key(review_id) references integration.review(id),
    foreign key(other_review_id) references integration.review(id),
    create_dts timestamp,
    load_audit_id int,
    foreign key (load_audit_id) references staging.load_audit(id)
);

comment on table integration.review_similarto is 'Track down reviews having some similarity with others (min threshold on the trigram calculation)';
comment on column integration.review_similarto.review_id is 'Review-id  (under constraint: larger than other_rev_id to avoid dup pairwise comparison)';
comment on column integration.review_similarto.other_review_id is 'The other similar review-id (take minimum id, if more than one).  If r1, r4, r7 are all similar, then: (r4,r1), (r7,r1)';
-- Not recursively go back to minimum: If r1 is same as r4 only, and r7 same as r4 --> rows: (r4,r1) and (r7,r4) although the three are probably all similar
```

In presentation layer, this derivation can be used to filter out similar reviews for statistical-based Report or it can be used explicitly to report on these duplicates.

The results so far are interesting...I'll write a dedicate post on these results once harvesting of all sub-set of Reviews is completed.


### Other derived components

From similar Reviews derivation, we could try to identify same users across sites. There is no direct way to identify these from our source data.  A possible (indirect) way could be to use reviews similarity. Let's say we have a business rules like :  *Flag user from different sites as being the same whenever more than x reviews are highly similar*. This would be straightforward to implement using the derivations above.

```sql
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
```

### Data cleansing

Also relevant here is to fix data issues... One example is related to Work-id loaded from thingISBN.xml export. There are ids that correspond to duplicates of other id (probably later merged to the same Work). These are discovered during harvesting, when Librarything host re-directs request using such duplicate id to a page corresponding to its "master" id. This is stored using the `work_sameas` table:

```sql
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
```
