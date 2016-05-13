Title: How to do data integration, the BRD example
Date: 2016-5-01 11:15
Tags: BRD, data integration, dataset
Slug: BRD_DI_part1
Author: Martin Ouellet
Series: BRD-DI
Series_index: 1

### Data Integration: one of the main BI functions

BI environment architecture is often left as an after-thought. Business is pressuring technical teams for delivery, so they quickly jump into designing star schema or dimensional models (the **presentation layer**), and neglect the **integration layer**.  End result: no separation of concerns will exist between the integration AND presentation aspects.

Integration and Presentation are two critical functions of BI and must be decoupled into separate layers (at least logically) reflecting their independent goals and specifications. This post is not about architecture principles (see [link](http://martin-ouellet.blogspot.ch/2013/08/bi-ideal-platform.html)) but is meant to illustrate through a simple example, how data integration is done.

### Book Reviews: an example of data integration

Let's say I want to report on book reviews/rating done by users of these cool social media sites [librarything](https://librarything.com), [goodreads](https://goodreads.com) or [babelio](http:babelio).  *Note: I enjoy spending time (procrastinating) on these book review sites, so the choice of Book reviews as my first dataset is one of personal interest... which is key to stay motivated in any personal project!*

So how should we proceed?

First, we need proper data model for both reference data (book title, authors, isbn...) and review data (rating, text).  There are other important decisions like ETL/pipeline design, data quality, ..but I'll stick to data modeling here. Data modeling is done by:

1. identity important business entities (i.e. our core business concept like Author, Work, Tag, Review Isbn..)
2. define core entities potentially used for integration (and their natural-key, like Book with title/author)
3. identify links/relationship between them
4. identify descriptive attribute to both entity and relationship

<img src='/images/blog/BRD_model.jpeg' width='100%' alt='Logical Data model'/>
[Logical Data Model]({filename}/images/blog/BRD_model.jpeg)

Let's discuss a few aspects.  First, one entity used for integration is obviously 'Book'.  But we cannot integrate based on loosely defined and generic term, so we must precisely define its meaning (grain, identity, ..).  Amazon records reviews at Book edition level, but it is probably more appropriate to record them at **Work** level. Work ([concept](https://www.librarything.com/concepts)) as defined by librarything as a single piece of work irrespective of translations, editions and title.  So this is a good choice to consolidate reviews from different languages, culture and small variations of edition .. all essentially pertaining to the same Book.   

Next is defining natural-key for Work that will allow us to integrate reviews on same Work across sites. For that, we could choose Work's Title/Author as a composite key and face issues like spelling differences, titles translation, small variation in different editions.. An alternative would be to use [ISBN](http://www.isbn.org/faqs_general_questions) to uniquely identify each editions and use a mapping generously produced by librarything called [thingISBN.xml](http://www.librarything.com/wiki/index.php/LibraryThing_APIs) available for non-commercial use.  This gives list ISBN's with their assignation to same Work entity (yet another social media by-product or collaboration done by the mass).

So Reviews from any site are harvested by first finding its identifier through a look-up the ISBNs. This implies using Librarything Work identifier as the master data source for Work.

Another integration decision is about **User**. Could we integrate and recognize same user across sites? The easiest is to consider all users across sites as different and unique. However, this does not seem to reflect [reality](http://www.goodreads.com/topic/show/1545181-will-goodreads-reviews-be-on-amazon) as many post their reviews in multiple sites for increased visibility.

But users across site are probably using a different username/pseudo so not easily merged directly from raw source. This requires more complex business logic to be implemented (ex. of rules: users with 2 or more highly similar reviews are considered same user). And complex transformation rules do not belong to Integration layer but more toward Presentation layer.  We can still record them as-is using site/username as unique key, and deal with this grouping later (in the same time leave it for future post..).

Let's stop here for this first part, which slightly cover an important aspect of BI/Analytic projects: Data integration. It seems not much was discussed concerning Report and Presentation aspects (although in real life we'd look at these to determine data content needed), and that's the main point: Data Presentation/Reporting should only influence data content and not modeling aspect of the data integration layer.

Presentation layer is also more influenced by tools and technology, and many legacy designs (star schema modeling, aggregation, materialized view, etc.) may no longer play such important roles when it comes to MPP Cloud databases implementations and Tools.  I'll explore these issues down the road when it is time to implement the front-end interface connecting to BRD.

In next part of this series, we'll look at Physical data model and see some of the implementation details.
