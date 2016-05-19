Title: How to do data integration, BRD example (part3)
Date: 2016-5-24 9:07
Tags: BRD, data integration
Slug: BRD_DI_part3
Author: Martin Ouellet
Status: draft
Series: BRD-DI
Series_index: 3


## Linking reviews

There is no direct way from our source data to link/merge same user from different sites.  One (indirect) way, could be to use review raw text and measure their similarity index against each other. We could have received a business rules similar to :  *Flag user from different sites as being the same use whenever more than, say 3 review have similarity close to*.

talk about which distance/algo to use

### Similarity calculation

present the code sql used ...

```sql
select * from dummy
```


### Result Example
