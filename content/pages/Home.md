Date: 2016-04-21 12:43
Author: Martin Ouellet
Title: What is it?
save_as: index.html
URL:
status: hidden


The *DataPlatform Franchising* project is dedicated to applying the concept of **Franchising** to Data Asset. To paraphrase Wikipedia's definition of franchising:

> For the data franchisor, the franchise is an alternative to building <s>chained stores</s> **data stores** to distribute <s>goods</s> **data assets** that avoids the investment and liability of a <s>chained stores</s> **data store**. The franchisor's success depends on the success of the franchisee.

This site is used to document my experimentation and adventures while trying to implement this concept.

## Premise

This project is speculating that DataPlateform**[^footnote]** which give access to cleansed dataset integrating multiple 3rd-party source will become prevalent to many analytical projects. This is considering:

1. __Data Preparation__
This is a costly and <u>mandatory</u> step when integrating multi-source data... best left to dedicated and specialized team
2. __Cloud-based cost model__
With its zero initial investment and pay-per-usage policy, Cloud-based SaaS's is a very attractive solution
3. __Cloud computing scalability__
Linear and "infinite" scalability is needed to open analytical capability to a much larger audience
4. __Data asset integration__
A single source dataset has very limited use/value by itself... the famous saying "The whole is greater than the sum of its parts”
5. __A bit of idealism!__
Our dense, interconnected and interdependent world strive for more collaboration... sharing dataset should prevail over competitive argument!

Refer to [context]({filename}2-Context.md) for more details.


## DataPlatform offering

The project is dedicated to create DataPlatform holding interesting dataset. It is dedicated to taking on all Data Preparation work in place of Data Providers as well as visualisation/dashboarding work to offer BI analytics as a self-service to non-expert.

It is the place to find LIVE, CLEANSED, STRUCTURED, MODELED, CONSISTENT and INTEGRATED multi-source dataset accessible in the Cloud! There are many [large datasets](https://www.quora.com/Where-can-I-find-large-datasets-open-to-the-public) available like [BigQuery dataset](https://www.reddit.com/r/bigquer/wiki/datasets), or [AWS dataset](http://aws.amazon.com/datasets/), but these are raw data derived from a single source.

This project is about providing [**r​ich data**](http://www.techradar.com/news/world-of-tech/why-big-data-is-crude-oil-while-rich-data-is-refined-and-the-ultimate-in-bi-1289628) and not only big data!

[^footnote]: DataPlatform is a generic term avoiding to debate on BI platform architectures.  Call it data warehouse, datamart, olap cube, star schema, datahub, data lake,.. the main focus is on <u>access</u> not physical design.

## Benefit

### Data provider

Anyone interested in capitalizing on its valuable data asset, but put off by the idea and cost associated with data preparation, hosting service, operation and maintenance.  

*DPF* takes care of the technical, tedious and specialized tasks involved in implementing and hosting DataPlatform service using a shared-revenue model.

Benefits foreseen are:

* Easily capitalize on your data assets without investing on development and infrastructure
* Enrich your data asset’s value through integration/mashup with other source
* Publish dataset with restricted license to secure collaboration or discover new partnership leads
* Enhance your own analytics by integrating external data  

### Data consumer

Data consumer will benefit from:

* Accessing cleansed and integrated dataset with no initial cost
* Accessing sophisticated analytical techniques through pre-built visualisation/dashboard tools developed on top of the DataPlatform
* Reuse your BI tool investment by connecting them through standard API access
* Pay only for what you consume

### Technology vendor

On the front-end side, visualisation and dashboarding analytical tools like [QlikView](qlick.com), [Tableau](tableau.com) and [Looker](looker.com) could showcase their capabilities by connecting to Cloud-based DataPlatform through standard API and language (JDBC, ODBC, Python DB-API, and SQL).

On the back-end side, a Cloud-based solution providers like [RedShift](https://aws.amazon.com/redshift/) from Amazon, Azure [SQL Data Warehouse](https://azure.microsoft.com/en-us/services/sql-data-warehouse/) from Microsoft and [Elastic Data Warehouse](http://www.snowflake.net/product/) from Snowflake could be interested in scalability testing with large public-access.
