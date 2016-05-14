Title: How to do data integration, BRD example
Date: 2016-5-01 11:15
Tags: BRD, data integration, dataset
Slug: BRD_DI_part1
Author: Martin Ouellet
Status: draft
Series: BRD-DI
Series_index: 1


Author: Martin Ouellet

### Data Integration: one of the main BI functions

BI environment architecture is often done along the way as an after-thought. Business is pressuring technical teams on delivery, so they quickly jump designing star schema or dimensional models (the **presentation layer**), and neglect the **integration layer**.  End result : no separation of concerns exist as we're trying to integrate AND present the data all at once!

Integration and Presentation are two critical functions of BI and must be decoupled into separate layers (at least logically) reflecting their independent goals and specifications. This post is not concerned on architecture principles (see [link](http://martin-ouellet.blogspot.ch/2013/08/bi-ideal-platform.html)) but is meant to illustrate, through a simple example, how integration is done.

### Book Reviews: an example of data integration

Let's say I want to report on book reviews/rating done by users of these cool social media sites [librarything](https://librarything.com), [goodreads](https://goodreads.com) or [babelio](http:babelio).  *Note: I enjoy spending time (procrastinating) on these book review sites, so the choice of Book reviews as my first dataset is one of personal interest... which is key to stay motivated in any personal project!*

So how should we proceed?

First, we need proper data model for both reference data (book title, authors, isbn...) and review data (rating, text).  There are other important decisions like ETL/pipeline design, data quality, ..but I'll stick to data modeling here. Data modeling is done by 1) identity important business entity (ex. Author, Work, Isbn..), 2) define common entity used for integration along with candidate keys, 3) identify links/relationship between them, 4) identify descriptive attribute, .  

<img src='/images/blog/BRD_model.jpg' width='100%' alt='Logical Data model'/>
[Logical Data Model]({filename}/images/blog/BRD_model.jpg)

Let's discuss a few aspect.  First, integration is done through common Entity, i.e. Book.  Book is a generic term and we can't afford to be loose especially related to "granularity" of entity.  Amazon records reviews at book edition level, but probably more appropriate to record them at **Work** level ([concept](https://www.librarything.com/concepts)).

Next is defining natural-key for Work allowing the integration of reviews (done on same Work entity) across sits.  For that, we could choose Work's Title/Author as a composite key and face issues like spelling differences and other titles translated in different languages. A much better alternative is to use ISBN which is meant to uniquely identify editions of same work. And it turns out Lt generously produces an export called [thingISBN.xml](http://www.librarything.com/wiki/index.php/LibraryThing_APIs) available for non-commercial use.  This gives a list ISBN's belonging to Lt's Work entity (yet another by-product of work done collaboratively through social media).

So Reviews from any site can be harvested by looking up its ISBN(s) and linked together through the Lt's Work-id key lookup. This implies Lt becoming the master data source for Work.

Another decision is about **User**, could we integrate them across sites? The easiest is to consider all users across sites as different and unique. However, this does not reflect reality as many will post their reviews in multiple sites for increased visibility (ref to discussion thread about that).

Users are not easily merged across Sites directly from source data. This requires more complex business logic to be implemented (ex. of rules: users with 2 or more highly similar reviews are considered same user). Complex transformation rules do not belong to Integration layer but more to the Presentation layer.  We can still record as-is using site/username as unique key, and deal with this grouping later (and leave it for future post).

In this part 1, we slightly cover an important aspect of BI/Analytic projects: Data integration. It seems not much was discussed concerning Report and Presentation aspects (although in real life we'd look at these to determine data content needed), and that's the main point: Data Presentation/Reporting should only influence data content and not modeling aspect during the modeling of data integration layer.

Presentation layer is also more influenced by tools and technology, and many legacy designs (star schema modeling, aggregation, materialized view, etc.) may no longer play such important roles when it comes to MPP Cloud databases implementations and Tools.  More on that later.

In next part of this series, we'll look at Physical data model and see some of the implementation details.
