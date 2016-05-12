Date: 2016-04-21 12:43
Author: Martin Ouellet
title: Context

### Presentation

This project capitalizes on 1) my experience acquired during 15 years doing BI projects in the industry, combined with 2) the maturity level recently reached by Data Warehousing/Analytical Cloud providers.

DW in the cloud, in contrast to on­-premise, is tailored for organizations not willing (or no longer) to run expensive, risky and over-­budget DW platforms on­-premise.  It mitigates risk and lower expenses by offering p​ay-per­use ​cost model common to cloud computing and SaaS.

But I believe it will also lead to the emergence of **DataPlatform Franchising**, a logical step for Cloud computing and Analytics.


### Cloud Computing

In recent years, ​cloud computing​ has increased both in scope and popularity to reach nearly ubiquity. It started off with simple needs like storage space and infra (IaaS), subsequently evolved into more advanced offers like computing resource with OS (letting user run their own software as in **​PaaS**)​ and has finally moved up the abstraction ladder with complete solution and service stacks offered (ex offering full CRM suite as **​SaaS**​).

In the realm of ​Business Intelligence​ and Data Warehousing, this trend did not pick up so rapidly (political and security worries) but things are quickly catching up with recent offering like [RedShift](https://aws.amazon.com/redshift/) from Amazon, Azure [SQL Data Warehouse](https://azure.microsoft.com/en-us/services/sql-data-warehouse/) from Microsoft and [Elastic Data Warehouse](http://www.snowflake.net/product/) from Snowflake. I believe this will grow a lot more, the simplest and quickest reason: cost! Doing Business Intelligence and data warehousing projects with on­-premise platform is an expensive adventure!


### Data Deluge

We have apparently entered a data-centric era where decision taking will be data-driven! Meanwhile, in recent years we have seen the emergence of new source of data originating from social media, connected device, Internet of Thing, machine-generated log, etc.  This phenomenon qualified as [​data deluge](http://www.economist.com/node/15579717) has not only created its own buzzwords (​Big Data​, ​NoSQL​, ​Data Science​ and ​Predictive Analytics​..), but clearly been disruptive in terms of data type (semi­structured and unstructured), volume and velocity. They have also challenged the relevance and adaptability of traditional BI solutions designed around data generated from **OLTP** (operational system)​ implying structured data type and manageable data volume.

### New Tools

Data deluge phenomenon has resulted in an equivalent tools deluge. The number of tools for doing data analytics is increasing at an unprecedented rate (even a [curated list](https://github.com/onurakpolat/awesome-bigdata) is too long), yet analytical project's challenges are rarely about technologies and algorithms but more about what is happening <u>before</u> data crunching can start!

The introduction of new tools is increasing BI environment complexity, requiring more than ever formal and proper architecture blueprint and principles. Otherwise entire BI platform integrity is jeopardized causing on­-premise TCO to increase even more. The solution to that is to rely on Cloud solution provider to provide solid architecture expertise and to offer new cost model with no initial cost investment.

Both the industry and open source communities were quick to devise new tools taking ideas from Google’s scalability architecture (​commodity​ ​hardware​ and **​map reduce**​ paradigm).  But these tools, loosely grouped under 'NoSQL'​, focus mostly on how to handle the sheer data volume and velocity or burst rate. And no matter how good they are at handling the ​[xV](https://datafloq.com/read/3vs-sufficient-describe-big-data/166)'s​ of big data, they fall short in meeting the most important aspect of any BI analytics solution: the **​Data integration**​ bit!

### Data Integration and Preparation

Anyone today is seeking to extract useful information from raw data in order to gain knowledge and make better and informed decision (i.e. data­-driven decision). No matter how valuable your data asset is, there will be many shortcomings if kept in raw format.

 Data preparation implies applying some rules/checks to this raw data to standardize and harmonize it across all sources. It includes many time-consuming steps:

* Data source identification and analysis
* Data Quality assessment, profiling and audit
* Data modeling and semantic definition
* Data transformation and rules specification
* Data integration process (enforcing harmonization, standardization and conformance throughout sources)
* Development and test of etl/pipeline jobs
* Operating, maintaining and evolving these jobs
* Data profiling and job monitoring

Data preparation and integration, when done correctly and integration leads to "desired" qualities, i.e. the five C's of data (see [Rick Sherman BI guidebook](https://www.safaribooksonline.com/library/view/business-intelligence-guidebook/9780124114616/)):

1. **Clean** (dirty and missing data treated)
2. **Consistent** (knowing which version of data is right)
3. **Conform** (data comparable across all sources)
4. **Current** (data latency adapted to needs and context)
5. **Comprehensive** (integrating many sources)

 It is real hard work, time­-consuming and requires a lot of thinking... but there is no alternative. Don’t believe in
any magic solution or silver­ bullet tool that promise to transform raw data into actionable information!

We are faced with a multi­-source data integration problem, and the new source of data deluge should be <u>integrating</u> and <​u>complementing​</u> the existing BI data layers in some form or another (consolidated/aggregated), and not merely bury us with massive and unwieldy data, i.e. the deluge!

### Data Modeling

Working with **raw data** and semi-structured data is a common big data settings where data exploratory is done on machine-generated logs. However, comes a time when data must be integrated to other source of data, and then you will invariably face challenges, because raw data suffers from a lot of symptoms.  It is inconsistent, incomplete, plagued with error, unconstrained, unformatted, outdated, etc.

This step will produce **schema-based** models implying that data/referential integrity are applied along with rules/checks, standardization and harmonization throughout all sources. Data become comparable and conform across source! Skimming through the modeling step of data preparation will result in bad quality and of limited use datasets (garbage in...).
