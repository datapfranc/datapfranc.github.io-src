Title: Loading into Redshift
Date: 2016-6-22 13:35
Tags: dataset, redshift
Slug: brd_loading_rs
Author: Martin Ouellet
Status: draft

This post will go through the steps needed to set-up a new Redshift cluster and get data into it.  We'll be using a standard approach but there are many  alternatives, see [here](http://thelink) for more details.  For the sake of simplicity, we assume a number of ETL jobs already exist to generate the presentation-layer data as flat files.  In real life, these ETL jobs would hold and maintain our set of Business rules and transformation logic required by our project, but for now we only focus on loading mechanisms involved with Redshift.


### Setting up an Amazon Redshift Cluster

The pre-requisite for setting-up the Cluster are:
  1. [**AWS account**](http://aws.amazon.com/) with a valid phone number
  2. [**IAM role**](http://docs.aws.amazon.com/redshift/latest/mgmt/configure-jdbc-connection.html) for granting access from one AWS resource to another one (in our case Redshift cluster connecting to our S3 bucket needed by the `COPY` command)
  3. SQL client (any JDBC/ODBC compatible client)
  4. [Redshift JDBC driver](http://docs.aws.amazon.com/redshift/latest/mgmt/configure-jdbc-connection.html#download-jdbc-driver), note the jdbc URL format for Redshift cluster: `jdbc:redshift://endpoint:port/databasename`

Once we have our pre-requisite cleared, we can spawn a new Cluster using the Amazon Redshift [console](https://console.aws.amazon.com/redshift) and follow basic instructions.  Important parameters to set are:

  - Cluster identifier (unique key to identify our cluster)
  - Physical location or region where our cluster will live
  - Database name and port (default port is 5439)
  - Master username and password ("superuser" of our database having same privileges as database owners but for all databases)
  - [Node type](http://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html):
      * Dense storage suited for large data workloads based on HDD storage: **DS1** & **DS2** (both have same storage but DS2 has more RAM/CPU) with different sizes (xlarge and 8xlarge)
      * Dense compute suited for performance intensive workloads based on SDD storage: **DC1** with different size (large and 8xlarge)
  - Cluster type (single or multiple nodes)
  - Some other advanced parameters like type of Platform (EC2-Classic and EC2-VPC), Encryption, CloudWatch alarm, ...(more info here).
  - **IAM role** associated with the cluster
      * Here we set the role explained in pre-requisite that lets Redshift accessing S3 in read-only

Finally before being able to connect to the cluster, we need to configure authorization by defining a [security group](http://docs.aws.amazon.com/redshift/latest/gsg/rs-gsg-authorize-cluster-access.html). Different parameters like protocol, port range and connecting IP inbound rules need to be set and vary slightly depending on the type of platform created earlier (either a classic or a VPC).


At this stage, we can finally connect to the Cluster using various client like the terminal-based [psql](http://www.postgresql.org/docs/8.4/static/app-psql.html) or any GUI like SQuirreL SQL or Workbench/J.  The connection details to provide are the host (the endpoint defined previously), the userid (our master username), the port and the database name we decided to use.  




### Loading into Redshift

Assuming we have our physical data model created in the database (DDL commands executed) we can start loading data into Redshift (link to previous post).

The recommended approach for loading flat files is to first dump the files into a [S3 bucket] (http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html), i.e. an URI named resource that stores files onto Amazon Cloud storage service.  We could use the same AWS account created to launch our Amazon Redshift cluster (credentials: an access key ID
and secret access key).


The generic [`LOAD`](http://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html) command supports various input type (S3 bucket, DynamoDB table, local files, remote files accessed though SSH...) and offers a array of parameters to tune and customize the load.  

For instance, for loading DIM_DATE:

```sql
copy dim_date from 's3://awssample/dimdate.txt'
credentials 'aws_iam_role=arn:aws:iam::462971347104:role/readonly_redshift_role'
delimiters '|' region 'eu-central-1a';
```




#### Splitting input files

COPY command can take advantage of MPP to parallelize the loading of large files. This requires to split input files as a multiple of number of slices present in our cluster.  For example, this command would split 'dim_book.txt' files into chunk of 100MB files all prefixed by 'dimbook_split' :

```bash
split -b 100m dim_book.txt dimbook_split
```






### About text attributes


The default expected date format is 'YYYY-MM-DD', if you're exporting data from Postgres, it uses same default so noting to do, otherwise you'll have to define the data conversion parameter: `DATEFORMAT [AS] {'dateformat_string' | 'auto' }`.  do as it  





Also recommended is to pre-sort data along the key order so that we can eliminate the need to `VACUUM`.  
