# Python_vectorization_cut
Deal with 1.4 million data only cost 0.12 second. It is good to use `pandas.cut` to segment and sort data values into bins.

# Data sample
~~~
220.181.89.156 - - [30/05/2013:23:59:59 +0800] "GET /thread-7467-1-1.html HTTP/1.1" 200 38651
222.36.188.206 - - [31/05/2013:00:00:01 +0800] "GET /static/image/common/none.gif HTTP/1.1" 304 -
66.249.74.211 - - [30/05/2013:23:59:59 +0800] "GET /archiver/tid-42707.html HTTP/1.1" 200 7838
~~~

Skill
~~~
pd.cut(x=df.index, bins=ip_list, include_lowest=True, labels=index).astype(int)
~~~
