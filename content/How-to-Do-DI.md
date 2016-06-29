Title: How to do data integration, BRD example
Date: 2016-4-01 11:15
Tags: BRD, data integration
Slug: brd_di_part1
Author: Martin Ouellet
Series: BRD-DI
Series_index: 1

### Data Integration: one of the main BI functions

BI environment architecture is often left as an after-thought. Business is pressuring technical teams for delivery, so they quickly jump into designing star schema or dimensional models (the **Presentation Layer**), and neglect the **Integration Layer**.  End result: no separation of concerns will exist between the integration AND presentation aspects.

Integration and Presentation are critical functions that must be decoupled into separate layers (at least logically) reflecting their independent goals and specifications. Integration is concerned with capturing raw and untransformed data originating from sources, while Presentation applies transformation and business rules to derive information from raw data and optimize its structure for data access. Data in Presentation layer should always be derived from Integration (*regenerated* on-demand), whereas data in Integration exists by itself (fact-based) as recorded by source system (cannot be regenerated independently from source).

This post illustrates through a simple example, how data integration is done. For more on BI architecture principles, you can check out [this](http://essay.utwente.nl/65553/1/Spruijt_MA_School%20of%20Management%20and%20Governance.pdf), or my personal view on [that](http://martin-ouellet.blogspot.ch/2013/08/bi-ideal-platform.html)).

### Book Reviews: an example of data integration

Let's say I want to report on book reviews/rating done by users of these cool social media sites [librarything](https://librarything.com), [goodreads](https://goodreads.com) or [babelio](http:babelio).  *Note: I enjoy spending time (procrastinating) on these book review sites, so the choice of Book reviews as a first dataset is one of personal interest... key to stay motivated!*

So how should we proceed?

We need proper data model for both reference data (book title, authors, isbn...) and review data (rating, text).  There are other important decisions like ETL/pipeline design, data quality, ..but let's focus on how data  modeling is done:

1. identity important business entities (i.e. our core business concept like Author, Work, Tag, Review Isbn..)
2. define core entities potentially used for integration (with natural-key, like Book's title/author)
3. identify links/relationship between them
4. identify descriptive attributes for both entity and relationship

<img src='/images/blog/BRD_model.jpg' width='65%' alt='Logical Data model'/>

### Reviews integration

First we can integration and link reviews through the 'Book' they refer to. For that we need to work with a clear and well specified Book concept.  Amazon records reviews at Book edition level, but it is probably more appropriate to record them at **Work** level. [Work](https://www.librarything.com/concepts)) is irrespective of translations, editions and title.  So this is a good choice to consolidate reviews from different languages, culture and small variations of edition.. all pertaining to the same Book.   

Next step is to decide on which Work's natural-key to use for integrating reviews across sites. We could choose Work's Title/Author as a composite key but this will result in issues like spelling differences, titles translation, small variation in different editions.. An alternative would be to use [ISBN](http://www.isbn.org/faqs_general_questions) to uniquely identify each editions and use a mapping between these ISBN's and the unique Work.  Fortunately, Librarything produces an export called [thingISBN.xml](http://www.librarything.com/wiki/index.php/LibraryThing_APIs) that is available for non-commercial use and does exactly that!  This export list ISBN's along with their assignation to same Work entity (yet another social media by-product or collaboration done by the mass).

So Reviews from any site are harvested by first finding its identifier through a look-up the ISBNs. This implies using Librarything Work identifier as the <u>master</u> data source for Work.


### Users integration

Another integration decision is about **User**. Could we integrate and merge same user across sites?  hmm...the easiest is surely to consider all users across sites as different. However, this does not seem to reflect [reality](http://www.goodreads.com/topic/show/1545181-will-goodreads-reviews-be-on-amazon) and many users post their reviews in multiple sites for increased visibility.

But users most likely have different username/pseudo so these are not easily merged from raw data. We need more complex business logic and transformation to be implemented (ex. of rules: users with 2 or more highly similar reviews are considered same user). Remember: transformation rules do not belong to Integration layer but more toward Presentation layer.  So let's postpone this transformation (and leave it for future post..) and simply record users as-is from site/username .


###Wrap-up

Data Integration layer is critical to BI/Analytic projects. Along the path to Knowledge, every derived data depends on the layer capturing raw fact-based data!

Presentation aspects (aka Delivery, Reporting, etc.) should not influence design decisions and modeling aspect of Data Integration layer, but only its data content.

Presentation layer is also more influenced by tools and technology, and many legacy designs (star schema modeling, aggregation, materialized view, etc.) may no longer play such important roles when it comes to MPP Cloud databases implementations and Tools.  I'll explore these issues down the road when we implement the front-end interface connecting to BRD.

In next part of this series, we'll look at Physical data model and see some of the implementation choices made.
