Title: Why Book Review?
Date: 2016-4-14 11:15
Tags: BRD
Slug: brd_why
Author: Martin Ouellet
<!-- Status: draft -->

### Passion

To keep on working on any personal project you need motivation, that's a given. Without any constraints or external pressure to work on something, what else can help you maintain motivation? Are external factors like potential gain, popularity or recognition enough? Not sure (speaking by experience).. these probably help at the beginning of a long journey, but on the long run they'll leave you unfulfilled.

So what else can bring you lasting motivation? One word: passion!  Working on stuff compatible with personal interest will make work less like work and more like leisure! Personally, I enjoy working on data-oriented projects. So if I can find a subject that is appealing to me, then I'm all well. Like most people, there are a lot of subjects I find interesting, but the challenge is to find one where data content can be easily acquired and integrated inside a database.

While procrastinating on book reviews sites, it hit me... that's it, I had found it, [BRD]({filename}../Home.md) was just born!  Although I would not qualify myself as a literary person, I enjoy reading books especially after I stumble upon excellent [reviews](https://www.librarything.com/profile_reviews.php?view=arouse77) or [one](https://www.goodreads.com/review/show/9230871?book_show_action=true&from_review_page=1) as sublime as the book itself.


### Report on Book review

I'm not sure these book reviews are very valuable by themselves... but they are certainly interesting and fun to read!  What report or questions could we get from a BRD dataset?  Here are a few thoughts:

1. Trend of rating in time
2. Reader appreciation in terms of their demographics
3. Difference in rating depending on how helpful reviews are
4. Reviews/rating statistics difference per site
5. Finding same or similar reviews and reviewer

There are certainly many more I can't envision at this time. We'll see how it turns out.

### Next steps

To make this happen, I need to work on quite a few things: 1) design a data model, 2) develop pipeline from harvesting step to loading into a database, 3) setting up the DB and pipeline workflow environment, 4) define and implement visualization tool, 5) define the backend Cloud provider, etc.    

Technology wise, here are some libraries/tools I'll be using:

* Postgres for the DB (planning to store the integration data myself and not in Cloud)
* [Luigi](https://github.com/spotify/luigi) used as the elt framework (requiring some customization)
* [Scrapy](scrapy.org) for the web harvesting bit
* Still not sure on the visualization side
* [Python](https://www.python.org) for pretty much all the glue around each component

So let's jump at it.
