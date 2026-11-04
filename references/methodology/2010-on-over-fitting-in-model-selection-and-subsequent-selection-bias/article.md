---
title: "JMLR 11"
source: "https://www.jmlr.org/papers/v11/cawley10a.html"
---

<div id="fixed">

\
<a href="/" data-align="right" target="_top"><img src="/img/jmlr.jpg" class="jmlr" data-align="right" data-border="0" /></a>

\
\

[Home Page](/)

[Papers](/papers)

[Submissions](/author-info.html)

[News](/news.html)

[Editorial Board](/editorial-board.html)

[Special Issues](/special_issues/)

[Open Source Software](/mloss)

[Proceedings (PMLR)](https://proceedings.mlr.press/)

[Data (DMLR)](https://data.mlr.press/)

[Transactions (TMLR)](/tmlr)

[Search](/search-jmlr.html)

[Statistics](/stats.html)

[Login](/manudb)

[Frequently Asked Questions](/faq.html)

[Contact Us](/contact.html)

\
\

[<img src="/img/RSS.gif" class="rss" alt="RSS Feed" />](/jmlr.xml)

</div>

<div id="content">

## On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation

***Gavin C. Cawley, Nicola L. C. Talbot***; 11(70):2079−2107, 2010.

### Abstract

Model selection strategies for machine learning algorithms typically involve the numerical optimisation of an appropriate model selection criterion, often based on an estimator of generalisation performance, such as *k*-fold cross-validation. The error of such an estimator can be broken down into bias and variance components. While unbiasedness is often cited as a beneficial quality of a model selection criterion, we demonstrate that a low variance is at least as important, as a non-negligible variance introduces the potential for over-fitting in model selection as well as in training the model. While this observation is in hindsight perhaps rather obvious, the degradation in performance due to over-fitting the model selection criterion can be surprisingly large, an observation that appears to have received little attention in the machine learning literature to date. In this paper, we show that the effects of this form of over-fitting are often of comparable magnitude to differences in performance between learning algorithms, and thus cannot be ignored in empirical evaluation. Furthermore, we show that some common performance evaluation practices are susceptible to a form of selection bias as a result of this form of over-fitting and hence are unreliable. We discuss methods to avoid over-fitting in model selection and subsequent selection bias in performance evaluation, which we hope will be incorporated into best practice. While this study concentrates on cross-validation based model selection, the findings are quite general and apply to any model selection practice involving the optimisation of a model selection criterion evaluated over a finite sample of data, including maximisation of the Bayesian evidence and optimisation of performance bounds.

\[abs\]

\[<a href="/papers/volume11/cawley10a/cawley10a.pdf" id="pdf" target="_blank">pdf</a>\]\[<a href="/papers/v11/cawley10a.bib" id="bib">bib</a>\]       

|  |
|---:|
| © <a href="https://www.jmlr.org" target="_top">JMLR</a> 2010. ([edit](https://github.com/JmlrOrg/v11/tree/main/cawley10a), [beta](http://jmlr.org/beta/papers/v11/cawley10a.html)) |

</div>

<a href="https://sigmoid.social/@jmlr" rel="me" style="font-size: 0">Mastodon</a>

