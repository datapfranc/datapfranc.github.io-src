Title: How to do data integration, BRD example (part3)
Date: 2016-5-24 9:07
Tags: BRD, data integration
Slug: BRD_DI_part3
Author: Martin Ouellet
Status: draft
Series: BRD-DI
Series_index: 3

## Business Layer

As introduced in previously, this layer should contain derived data needed by our Presentation/Delivery layer. We can build stuff like associations, groups or hierarchies defined by Business Rules, or also do cleansing to fix data issues found in our *raw data*.  This post looks at two examples of that.

### Building new association: Similar Reviews

Let's say we're required to find similar reviews written on Work. This could be useful for:

* Identify data duplication issues
* Identify users duplicating reviews within the same site or (most likely) across sites
* Identify spam or ?? where reviews are done to bias opinion
* Find plagiarism among the reviewers community

How do we do that?  Data processing done on unstructured text can be done efficiently by NoSQL engines with massively parallel processing capability (MPP).  These engines would leverage a "divide and conquer" strategy by distributing reviews among different cluster nodes while  making sure reviews of same work land on same node (locality ??).  (transform the review text into ?? and easily find N-gram ... . ex. Spark using etc.. related to my course)


> N-gram is a way to represent documents as set useful to identify similarity between them (trigram version based on 3-letters, will results to a 26^3 dimensional space).  It is shown that two documents with similar vector-representation are likely to be similar, and as such many applications are using this technique (e.g. identifying lexically similar documents, detecting plagiarism, ..).  

Using BRD'review data, we spotted these two reviews (from book XX) as being similar (similarity=??):

User-uid  |  Review-date  |  Review text  
----------|---------------|---------------
rrrr | feb-25-2016 | bla biehfpo uèoj èoiu èpoi öij àlkjè o ¨pojkj èpo èop jénékih èoij
uuu | feb-26-2016 | bla biehfpo uèoj èoiu èpoi öij àlkjè o ¨pojkj èpo èop jénékih èoij



This is a good illustration of complementary usage/collaboration between modern NoSQL engine and more traditional RDBMS-based approach.   

However for this demonstration, neither the data volume/rate nor the latency constraint impose the use of MPP-based engines.  We can directly proceed within PostgreSQL by leveraging text comparison functions like tri-gram (see pg_trgm package).

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

Out of the mXm possible pairs of reviews (assuming there are m reviews for the Work), we don't need to compare each review with
itself, neither compare twice each same pair.  We only need distinct pair, i.e. binomial m choose 2 combinations.  Using the source `rev_similarto_process`, this would translate into SQL as:

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

Joining review only through `work_refid` this produces a mXm cross-product which is reduced through the clause `and rev.review_id > other.review_id`.  We further reduce pairs by making sure reviews are in same language (`rev.review_lang = other.review_lang`), have similar number of characters (`rev.text_length between other.text_length - round(other.text_length * %(len_delta)s) and  other.text_length + round(other.text_length * %(len_delta)s))`) and finally have a minimum number of characters  (`rev.text_length >= %(len_min)s`) (probably useless to compare "Very Good" and "Excellent!" type of reviews).

Once we calculate similarity of each resulting pairs of reviews, then we can populate the end-result table using a threshold on similarity:

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

comment on table integration.review_similarto is 'Track down reviews having some similarity with others (min threshold on the tri-gram calculation)';
comment on column integration.review_similarto.review_id is 'Review-id  (under constraint: larger than other_rev_id to avoid dup pairwise comparison)';
comment on column integration.review_similarto.other_review_id is 'The other similar review-id (take minimum id, if more than one).  If r1, r4, r7 are all similar, then: (r4,r1), (r7,r1)';
-- Not recursively go back to minimum: If r1 is same as r4 only, and r7 same as r4 --> rows: (r4,r1) and (r7,r4) although the three are probably all similar
```

Some example of results we have with the similarity tri-gram calculation:

--same meaning but different ordering of words!

--similar but not quite the same (looks like plagiarism?)


--exact duplication  

I'll write a dedicate post on these results once processing is completed on the sub-set of Reviews harvested.




### Other derived components

Based on the same Reviews derivation, we could also try to find out same users across sites. There is no direct way from our source data to link/merge same user from different sites.  So the indirect way could be to use reviews similarity. Let's say we have a business rules similar to :  *Flag user from different sites as being the same whenever more than x (say 3) reviews are highly similar*. This would be straightforward to implement using the derivations above.


TODO: re-travailler...
We also fix data issues and store in this layer.. An example, is the handling of Work-id found inside thingISBN.xml.  These may correspond to duplicates of other id (merged to the same Work). These are discovered during harvesting, as LT website re-directs request made to thee duplicates ids to the "master" work.  

Other data processing is linking very similar reviews together so they can be reported as duplicates and/or used to identify same user (to be discussed in separate post).


Here's the illustration of these (and others) in code:

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
