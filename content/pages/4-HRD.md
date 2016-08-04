Date: 2016-8-02 15:23
Author: Martin Ouellet
Title: HRD
Slug: hrd_intro
Status: draft

### Preamble

BRD was created as a fun experiment to test and validate the implementation of DataPlatform Franchising concept.  **HRD** on the other hand, is chosen because of its impact on the public in general and on the travel and tourism industry in particular. The accommodation sector is one among many sectors witnessing what is now called the [uberization of the economy](https://theautarkist.wordpress.com/2015/07/01/the-uberization-of-the-economy-airbnb-uber-and-the-new-entrepreneur) and no one can predict its longterm social and economical impact. HRD will help those looking for answers in this regard.   

Follow-up latest news at [HRD]({tag}BRD).

### HRD: House Renting DataPlatform Franchising

**HRD** or **House Renting Dataset** is a [rich dataset](http://www.techradar.com/news/world-of-tech/why-big-data-is-crude-oil-while-rich-data-is-refined-and-the-ultimate-in-bi-1289628) gathering millions of house/apartment/rooms (let's call them *places*) for rent referenced in most popular websites.

It provides anonymized geo-located data of places available for rent, along with their status, their reviews/ratings and additional physical characteristics.  

It is meant for ad-hoc study and research purposes and certainly not to organize your next vacations. It provides a high-quality dataset relevant for many analytical needs, data mining and machine learning and online analytical processing (OLAP), etc.  It is useful for anyone looking to gain insights on:

* Spatial distribution of places for rent
* Impact on the accommodation industry
* Density of places in neighborhood of interest
* Market evolution analysis (new places growth and places closing)
* Real estate impact cross analysis
* Places ratings evolution timeline
* Investigation on places for tax purposes and/or target advertising

It provides ready-­to-­be­-consumed Place data:

* **Address**​ (normalized)
* **Geolocation*
* **Nb of bedrooms**
* **Nb of bathrooms**
* **Nb of people**
* **Property type**
* **Price per night**

It contains millions of places collected from listed sites (feel free to contact us if you’re running a website):

1. [AirBnB](airbnb.com)
2. [rewreGoodreads](rrrrrgoodreads.com)
3. [Amazon](amazon.com)
5. [Babelio](babelio.fr)

With HRD, you can start doing analytics on all Renting places without any initial investment!

### Benefits for website owner

First off, HRD has a pay­-per-­use cost policy applicable to all registered users. A percentage of benefit generated is shared with site’s owner pro­-rata (i.e. using number of places/rating).

Besides monetizing your data asset, HRD provides transparency to this growing market for official and government agencies. This helps mitigates the risk of being shut-down and excluded from [specific region] (http://www.theverge.com/2016/5/2/11564370/airbnb-berlin-illegal-apartment-housing-price). Longterm sustainability of your industry cannot be viewed independently from its legality.   

You can also enhance your own analytical capability by extending your database and see who cross-reference their places in difference sites. HRD focus is not about offering an entry to users interested in renting.  

It targets those doing research and market analysis or investigation. HRD does not hold information on renter or website registered users. If you choose to participate to BRD, you can also take advantage of BRD data integrity checks and obtain special reports on:

* Data anomalies
* Places referenced across different sites
* Fake sites or spam
* Other on-demand analysis

### Benefits for researcher

Real estate researcher, local government agencies and territory planner  will all benefit from HRD and its convenient dashboarding/visualization web access to a centralised and maintained database.      

--------------

rendu la

### HRD Data Integration

BRD collects and integrates heterogeneous and multi-­source dataset into its Cloud­-based solution. All reviews are reported at Work and language level. **Work** is the main integration point that consolidate reviews assigned to all **Books** regardless of their editions, translations, format (print, digital or other form). Refer to LT’s [Work](https://www.librarything.com/concepts) definition.  For simplicity both terms are used interchangeably.

### BRD Data Cleansing

BRD applies procedure to cleanse, conform and validate data:

1. Review Data is de-duped
    * Spot reader making same reviews within/across sites
2. Data Error correction
    * Review with data issues can be flagged/corrected
    * Reviews too small or considered non meaningful can be filter out
3. Data harmonization
    * Rating are normalized to a 10 point scale to account for full stars only or half­-star
    * Tag can be aggregated across site and report as-­is or reformat to merge similar Tag (case insensitive and singular form)

### BRD initial steps

The initial goal is to get enough reviews (maybe for 10-15% of Book from Librarything) to validate the Cloud DW design choice and produce realistic experimentation with the analytic/visualization applications.

I'll contact site owners so they are aware of this experiment and my intention to harvest reviews for these books.  Although the data is publicly available, it does not give me legal [right](https://www.quora.com/Is-website-scraping-legal-and-ethical) to harvest their sites (*web harvesting is a huge business on Internet, yet no clear [jurisprudence](https://www.quora.com/What-is-the-legality-of-web-scraping) still exist*).   Among other things, you need to respect site licensing, limit your hitting rate, and a lot more issues that are over my head... in other words be a [good citizen](http://programmers.stackexchange.com/questions/91760/how-to-be-a-good-citizen-when-crawling-web-sites).
