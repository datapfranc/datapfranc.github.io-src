Title: Why Book Review?
Date: 2016-3-14 11:15
Tags: BRD
Slug: brd_why
Author: Martin Ouellet
<!-- Status: draft -->

### Passion

To keep on working on any personal project you need (above all) **motivation**.  Without any constraints or external pressure to work on something, what can help you maintain motivation? Can factors like potential gain, popularity or recognition help? Answer from personal experience: no.. these probably help at beginning, but on the long run they'll leave you unfulfilled.

So what else can bring you lasting motivation? One word: passion!  Working on stuff compatible with personal interest make your work less like *work* and more like *leisure*! Personally, I enjoy working on data-oriented projects so I only need to find a subject that is appealing to me. Like most people, there are a lot of subjects I find interesting, but the challenge is to find one with digital data content available to be integrated inside a database.

While procrastinating on book reviews sites, it hit me... that's it, I had found it, [BRD]({filename}pages/Home.md) was just born!  Although I would not qualify myself as a literary person, I enjoy reading books and reviews like [this one](https://www.librarything.com/work/23078/reviews/67790839) or [that one](https://www.goodreads.com/review/show/9230871?book_show_action=true&from_review_page=1) could convince anyone to (re)read any book!


### Report on Book review

I'm not sure how valuable these book reviews are by themselves... but they are certainly interesting and fun to read!  What sort of questions could we get from a BRD dataset?  Here are some thoughts:

1. Trend of rating in time
2. Reader appreciation in terms of their demographics
3. Difference in rating depending on how helpful reviews are
4. Reviews/rating statistics difference per site
5. Finding same or similar reviews and reviewer

There are certainly many more I can't envision at this time.

### Next steps

To make this happen, I need to work on quite a few things: 1) design a data model, 2) develop pipeline from harvesting step to loading into a database, 3) setting up the DB and pipeline workflow environment, 4) define and implement visualization tool, 5) define the backend Cloud provider, etc.

Technology wise, here are some libraries/tools I plan to use:

* Postgres for the DB storing integration data locally (not for presentation)
* [Luigi](https://github.com/spotify/luigi) used as the elt/pipeline framework (plus customization)
* [Scrapy](scrapy.org) for the web harvesting bit
* Still not sure on the visualization side
* [Python](https://www.python.org) for pretty much all the glue around each component

So let's jump at it.
