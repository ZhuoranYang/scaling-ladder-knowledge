---
title: "openathena.ai/blog/marin-data-pipeline-overview"
source: "https://openathena.ai/blog/marin-data-pipeline-overview/"
---

<div class="nav-padding-global">

<div class="nav-inner">

<div class="nav-container">

<a href="/" class="nav-brand" aria-label="Open Athena Home"></a>

<div class="nav-logo">

</div>

<div class="nav-links">

<a href="/projects/" class="nav-link">Projects</a> <a href="/blog/" class="nav-link">Blog</a> <a href="/about/" class="nav-link">About</a>

</div>

<span class="burger-lines"> <span class="burger-line"></span> <span class="burger-line"></span> </span>

</div>

</div>

</div>

<div class="section blog-post">

<div class="blog-post-header">

# Curating 25 Trillion Tokens for LLM Pretraining

<div class="blog-post-meta">

September 11, 2026 · Will Held ·

<div class="resource-type-tag">

MARIN

</div>

</div>

</div>

<div class="blog-post-body">

<div class="blog-toc-title">

Contents

</div>

Contents

<div class="blog-post-content project-detail-body">

Pretraining a large language model requires many trillions of tokens of text and code from a wide range of sources and topics. Some documents demonstrate key skills and knowledge and are worth repeating many times; others are relatively low-quality but still useful, as much of what the model encounters in the world will be messy. To train a good model, we need to choose what it sees and how often with some care.

Datakit is the Marin team’s pipeline for turning more than a hundred open datasets into such a pretraining mixture. It catalogues all the data used in the Marin project, globally deduplicates and decontaminates it, groups it into semantic categories, and then lets us learn empirically how much data to sample from each category.

For our most recent large-scale run, Datakit began with 18.71 billion raw documents containing 25.25 trillion Llama 3 tokens. We globally deduplicated and decontaminated those documents, categorized them by both quality and topic, and then ran just over 1,000 small-scale training experiments to fit a regression that estimates benchmark performance from the sampling weights over those topic and quality buckets. Our [source registry](https://github.com/marin-community/marin/blob/64a9483cf1a928e6db97b83130d8a5d171a4aead/lib/marin/src/marin/datakit/sources.py), [processing code](https://github.com/marin-community/marin/tree/64a9483cf1a928e6db97b83130d8a5d171a4aead/lib/marin/src/marin/datakit), and [proxy-run dataset](https://huggingface.co/datasets/marin-community/grug-moe-mix-swarm) are all open source. Future posts will explore parts of this pipeline in more depth.

<figure class="plotly-figure-block">
<div class="plotly-frame-outer">
<div class="plotly-frame-title">
How data flows through Datakit
</div>
<div class="plotly-frame-inner">
<div class="d3-figure" aria-label="How data flows through Datakit. Datakit removes most tokens during deduplication, then learns how to sample the retained corpus from 200 topic-quality buckets. Ribbon width shows token volume through curation and across 40 topics; the separate bar shows five quality bands. The inset uses PCA to project the initial weights of 872 proxy runs, with nearby points marking similar mixtures. Evaluations of those runs feed a regression that guides the final weights." data-d3-renderer="data-loop" data-d3-src="/assets/images/blog/marin-data-pipeline-overview/data-loop.json" role="group" style="min-height:390px">

</div>
</div>
</div>
<figcaption>Datakit removes most tokens during deduplication, then learns how to sample the retained corpus from 200 topic-quality buckets. Ribbon width shows token volume through curation and across 40 topics; the separate bar shows five quality bands. The inset uses PCA to project the initial weights of 872 proxy runs, with nearby points marking similar mixtures. Evaluations of those runs feed a regression that guides the final weights.</figcaption>
</figure>

**Summary**

- Datakit starts with 152 open datasets containing 25.25 trillion tokens, although most of that volume comes from just a handful of open-source labs.
- Global deduplication removes 2.33 billion documents—2.13 trillion tokens.
- Decontamination—removing benchmark answers from our training data—using exact 13-word n-gram matching, removes every flagged document, another 13.66 billion tokens under the current policy.
- Each document is assigned to one of 40 topics using an unsupervised embedding model, while a supervised quality scorer places it in one of five quality bands, with quality thresholds calibrated separately by content type, such as code, prose, and mathematics. Together these form 200 sampling buckets.
- More than 1,000 small proxy runs fit a regression that predicts benchmark performance from candidate weights over those buckets.

## Beauty and Chaos in Open Data<a href="#beauty-and-chaos-in-open-data" class="heading-anchor" aria-label="Link to section: Beauty and Chaos in Open Data"></a>

Training a capable model requires not only good data but an enormous amount of it: recent open-weight models train on anywhere from 15 to 40 trillion tokens. Assembling that much data while keeping it high-quality, well licensed, and openly accessible is difficult. Thankfully, open-source work is a community effort. Many other big labs, academic groups, and individual developers have put enormous effort into building open datasets, most of them easily reached on the HuggingFace Hub. The attractive course, whenever possible, is thus to stand on the shoulders of these giants and use the open data that already exists.

But what does “using existing data” actually mean? It turns out that many datasets are largely duplicates, often derived from the same sources (the Common Crawl, for example). Some are tiny and exceptionally high-quality, while others are enormous but have relatively little information per example. A single dataset may cover topics as broad as the whole web or as narrow as a set of LeetCode interview questions. And even the labels can be misleading: a split called `train` may contain the `test` set of an existing benchmark.

Even if all you want to do is reuse existing data, you still need tools for curating it. For this blog, I’ll divide the pipeline into three stages. First, we prepare the data so documents from different sources can be used together. Then we organize those documents into buckets by topic and quality. Finally, we learn a mixture by testing how often to sample from each bucket.

## 1. Prepare the data<a href="#1-prepare-the-data" class="heading-anchor" aria-label="Link to section: 1. Prepare the data"></a>

Datakit first rewrites every source into a standard data format, and then applies the same corpus-wide cleanup for duplication and contamination. Downstream experiments can therefore reasonably assume that the data has passed the same checks, without source-specific special-casing.

### Download and normalize<a href="#download-and-normalize" class="heading-anchor" aria-label="Link to section: Download and normalize"></a>

A good curator begins by writing down what there is to work with. In Datakit, we catalogue our data in [code](https://github.com/marin-community/marin/blob/64a9483cf1a928e6db97b83130d8a5d171a4aead/lib/marin/src/marin/datakit/sources.py), tracking the provenance of 152 data sources as of the time this post is written. Most of the data comes from a few datasets produced by major open-source modeling organizations: [AI2](https://allenai.org/), [NVIDIA](https://huggingface.co/nvidia), [HuggingFace](https://huggingface.co), and [the EU's High-Performance Language Technologies project](https://hplt-project.org/about). These major sources are derived from general purpose public crawls such as the [Internet Archive](https://archive.org), the [Software Heritage Archive](https://archive.softwareheritage.org), and the [Common Crawl](https://data.commoncrawl.org). But there is also a long tail of high-quality, targeted data from smaller, one-off sources: [papers from Eleuther AI](https://huggingface.co/datasets/common-pile/arxiv_papers_filtered), [books from the Institutional Data Initiative](https://huggingface.co/collections/institutional/institutional-books), [mathematics problems and solutions from Project Numina](https://huggingface.co/datasets/AI-MO/NuminaMath-1.5), [agent traces from Kevin Xiang Li](https://huggingface.co/datasets/AlienKevin/SWE-ZERO-12M-trajectories)<sup>[1](#fn-1)</sup>, and [SVG illustrations from SVGFind](https://huggingface.co/datasets/nyuuzyou/svgfind).

<figure class="plotly-figure-block">
<div class="plotly-frame-outer">
<div class="plotly-frame-title">
Standing on the Shoulders of Giant Datasets
</div>
<div class="plotly-frame-inner">
<div class="d3-figure" aria-label="Standing on the Shoulders of Giant Datasets. A few datasets supply most of the tokens, followed by a long tail spanning nearly eight orders of magnitude. Bars rank 152 dataset groups by token count on a logarithmic scale (with our own Ben Feuer&#39;s 142 trace datasets treated as one group). The black line shows cumulative token share, and the gold marker shows where it reaches 80%." data-d3-renderer="catalog-heavy-tail" data-d3-src="/assets/images/blog/marin-data-pipeline-overview/catalog-heavy-tail.json" role="group" style="min-height:460px">

</div>
</div>
</div>
<figcaption>A few datasets supply most of the tokens, followed by a long tail spanning nearly eight orders of magnitude. Bars rank 152 dataset groups by token count on a logarithmic scale (with our own Ben Feuer's 142 trace datasets treated as one group). The black line shows cumulative token share, and the gold marker shows where it reaches 80%.</figcaption>
</figure>

Each entry in the catalogue records where Marin obtained the data and as much version info as is available, usually a HuggingFace repository pinned to a particular commit. Many datasets require extra formatting or processing, which is recorded as part of the download step within Marin. We ingest datasets which either have broadly permissive licensing from the creator or explicitly permit model training. You can view the datasets, along with their licenses, provenance, and Llama 3 token count on our [token count viewer](https://huggingface.co/spaces/marin-community/token-count-viewer). The goal here is to have clean pipelines which allow anyone to replicate Marin’s ingestion process from the original sources we use. Notably, we do not republish duplicates of upstreamed data and do not plan to! While this creates some work when setting up a new cluster, it preserves attribution to the original creators and leaves them, rather than us, in control of their data. If a creator takes down all or part of a dataset, that decision carries through to Marin since our pipeline reads the data they maintain.

This choice does have an obvious downside compared with rehosting the data directly: some external reproducibility is lost! While pinning commits prevents minor or methodological drift, data that is taken down is unfortunately inherently unreproducible. Consider the [Stack v3](https://huggingface.co/datasets/HuggingFaceCode/stack-v3-train) from HuggingFace, which we use and which is regularly updated to respect [opt-out requests](https://huggingface.co/spaces/HuggingFaceCode/in-the-stack). Each time you use Datakit to download and normalize this source, a small fraction of the data may therefore have been removed. This makes the overall dataset not exactly reproducible, but this tradeoff is necessary to avoid hosting copies which create a sort of whack-a-mole for dataset creators or their underlying contributors.

Once a dataset is catalogued, we [normalize](https://github.com/marin-community/marin/blob/main/lib/marin/src/marin/datakit/normalize.py) its records and metadata into a common representation. Datakit writes the text to Parquet, together with a stable hash of the text, a `source_id`, and catch-all source-specific metadata. Along the way it removes empty records, compacts excess whitespace,<sup>[2](#fn-2)</sup> enforces some reasonable file/row-group sizes, and puts the records in a stable order. Ideally, normalization is uneventful: its only purpose is to let the corpus-wide operations that follow proceed efficiently and without any special casing!

### Deduplicate across sources<a href="#deduplicate-across-sources" class="heading-anchor" aria-label="Link to section: Deduplicate across sources"></a>

When training language models, epochs—the number of times data is repeated—can be an important factor in whether your model generalizes or memorizes. So in downstream experiments we want epoching behaviour to be a cleanly controlled hyperparameter. Unfortunately, individual data points are frequently duplicated, both within and especially across datasets! While natural duplication can carry information about document quality,<sup>[3](#fn-3)</sup> that is certainly not the case when repetition occurs instead because we have ingested two sources that parsed the same webpage, or for other non-natural reasons. Thus it's important that we have reasonable confidence that every document in our corpus occurs only once.

Datakit therefore deduplicates globally. It first catches exact duplicates using the hash produced during normalization. This amounts to around 500 million exact duplicates within sources with another 5 million or so exact duplicates across sources. But the same document can vary slightly because of parsing, boilerplate removal, or other minor formatting differences that leave its fundamental information unchanged. To find these fuzzy duplicates without comparing every pair of documents, Datakit uses locality-sensitive hashing (LSH) to retrieve likely near-copies from MinHash signatures computed over word 5-grams.<sup>[4](#fn-4)</sup>

Unfortunately, upon inspection, we found that LSH deduplication collapsed some datasets which were not highly duplicated semantically, such as our genetic sequence and tool-calling datasets, into only a few examples. Why? We tune LSH to tolerate small differences deliberately so it can catch near duplicates. For data in which small differences are meaningful—such as DNA, where a single base pair edit can change a gene’s function—that same tolerance causes false positives. To account for this, we apply additional heuristics that would be too expensive across the entire corpus but become practical once LSH has narrowed the search, to reduce false positives. We’ll explore them in a later post; for now, see the [pipeline implementation](https://github.com/marin-community/marin/blob/64a9483cf1a928e6db97b83130d8a5d171a4aead/experiments/datakit/reference_pipeline.py).

In our latest large-scale run, deduplication removed 2.33 billion documents—12.5% of the raw data pool—and 2.13 trillion tokens, or 8.4%. Most of these duplicates come from datasets that explicitly share source data. The largest source, for example, is the overlap between Nemotron’s processing of Common Crawl and its synthetic rephrasings of the same documents: many of the synthetic documents still overlap significantly with the real seed documents from which they were generated.

<figure class="plotly-figure-block">
<div class="plotly-frame-outer">
<div class="plotly-frame-title">
Which datasets share duplicate documents?
</div>
<div class="plotly-frame-inner">
<div class="d3-figure" aria-label="Which datasets share duplicate documents?. Three source pairs account for 93.2% of the 686 million verified duplicate links between sources. Rows contain removed copies; columns contain the representatives retained from their duplicate groups. Circle radius uses a logarithmic scale. Hover for exact aggregate counts." data-d3-renderer="dedup-source-overlap" data-d3-src="/assets/images/blog/marin-data-pipeline-overview/dedup-source-overlap.json" role="group" style="min-height:620px">

</div>
</div>
</div>
<figcaption>Three source pairs account for 93.2% of the 686 million verified duplicate links between sources. Rows contain removed copies; columns contain the representatives retained from their duplicate groups. Circle radius uses a logarithmic scale. Hover for exact aggregate counts.</figcaption>
</figure>

### Remove benchmark contamination<a href="#remove-benchmark-contamination" class="heading-anchor" aria-label="Link to section: Remove benchmark contamination"></a>

Despite entertaining papers to the [contrary](https://arxiv.org/abs/2309.08632), training on the test set is widely considered bad form. The most obvious reason is that contamination can dishonestly inflate benchmark scores.<sup>[5](#fn-5)</sup> More subtly, it can bias architecture research toward models with greater memorization capacity but limited generalization—leaving lasting harms even after the contamination is removed. Rigorous decontamination is therefore important both for internal development sets and for benchmarks that will be reported as test sets upon model release.

Fortunately decontamination is smaller scale than deduplication which makes costly, high-precision filtering tractable.<sup>[6](#fn-6)</sup> Datakit searches exactly for 13-word n-gram overlaps with the Artificial Analysis Intelligence Index and Marin’s pretraining evaluation sets. For each paragraph in the pretraining data, we ask what fraction of its eligible 13-gram occurrences also appear in the evaluation material (if an n-gram is repeated, we count every occurrence). Our threshold is 50%: if at least half of the eligible 13-gram occurrences in any one paragraph match, we flag the document.<sup>[7](#fn-7)</sup> This rule favours precision—it catches obvious copies, but misses paraphrases and some embedded examples. Even so, the figure below finds possible contamination in many of the large datasets we train on.

<figure class="plotly-figure-block">
<div class="plotly-frame-outer">
<div class="plotly-frame-title">
Which datasets contain benchmark overlap?
</div>
<div class="plotly-frame-inner">
<div class="d3-figure" aria-label="Which datasets contain benchmark overlap?. Benchmark overlap concentrates in particular source-benchmark pairs. Each square counts distinct overlapping documents, while the side bars show documents removed from each source. A document can appear in several squares, so the cells are not additive. The figure detects overlap, not its cause." data-d3-renderer="contamination-matrix" data-d3-src="/assets/images/blog/marin-data-pipeline-overview/contamination-matrix.json" role="group" style="min-height:460px">

</div>
</div>
</div>
<figcaption>Benchmark overlap concentrates in particular source-benchmark pairs. Each square counts distinct overlapping documents, while the side bars show documents removed from each source. A document can appear in several squares, so the cells are not additive. The figure detects overlap, not its cause.</figcaption>
</figure>

## 2. Organize the data into buckets<a href="#2-organize-the-data-into-buckets" class="heading-anchor" aria-label="Link to section: 2. Organize the data into buckets"></a>

Once we've normalized, deduplicated, and decontaminated each source, we can actually start training on this data. A simple sampling policy is to draw from each source in proportion to the number of tokens it contains. This approach, called proportional sampling, is a strong baseline\![^token-count-baseline\] Still, we might expect some of our data to be more useful than others, depending on our goals.

Let's say we want to make a model dedicated to solving math problems. We might reasonably want to upsample high-quality data related to mathematics. For some sources, the dataset description tells us that's what they contain. But math data also appears in larger, heterogeneous datasets like web crawls, jumbled up with recipes, advertisements, and much else.<sup>[8](#fn-8)</sup> A sampling policy expressed purely in terms of sources doesn't let us upweight these documents alongside the dedicated math data.

To enable policies that upsample data in this more intuitive, semantic fashion, we label each document with a quality score and a topic tag. These annotations route documents into buckets, grouping together data of similar topics and quality. One source can contribute to many buckets, and one bucket can contain documents from many sources.

A data mixture is then expressed as sampling weights over these buckets, with each weight specifying the fraction of training tokens its bucket supplies.<sup>[9](#fn-9)</sup> Whether that uses only part of the bucket or repeats its documents several times depends on how much data the bucket contains and how long we train. To learn this mixture, balancing tradeoffs across domains and making better use of our data, we train many small models on different mixtures, then fit a regression to estimate how their sampling weights affect performance.

<figure class="plotly-figure-block">
<div class="plotly-frame-outer">
<div class="plotly-frame-title">
Where does each data source land?
</div>
<div class="plotly-frame-inner">
<div class="d3-figure" aria-label="Where does each data source land?. Data sources have distinct topic and quality profiles. Select a source to see how its post-decontamination tokens divide by topic and quality; ribbon width represents token count. Topics accounting for less than 2% of the source are grouped as ‘Everything else.’" data-d3-renderer="topic-quality-sankey" data-d3-src="/assets/images/blog/marin-data-pipeline-overview/topic-quality-sankey.json" role="group" style="min-height:630px">

</div>
</div>
</div>
<figcaption>Data sources have distinct topic and quality profiles. Select a source to see how its post-decontamination tokens divide by topic and quality; ribbon width represents token count. Topics accounting for less than 2% of the source are grouped as ‘Everything else.’</figcaption>
</figure>

### Embed the documents<a href="#embed-the-documents" class="heading-anchor" aria-label="Link to section: Embed the documents"></a>

Our first order of business is to categorize the data. But how? Should we assign each document to one of a list of topics, as [*Organize the Web*](https://arxiv.org/html/2502.10341) does? Should we annotate separate properties, as [Propella](https://arxiv.org/html/2602.12414) does? Or should we take inspiration from librarians and use a Dewey-inspired system, as [Essential AI](https://arxiv.org/html/2506.14111) does?

All three are reasonable, and all draw distinctions that make sense when you look at the data. But it doesn't necessarily follow that they draw the best distinctions for training a model, especially as data distributions shift over time. Should code be a single bucket, or should we, for example, mix software repositories separately from agentic traces? Ideally, we could try different taxonomies flexibly and at relatively low compute cost.

To try and enable this, Datakit separates out the (expensive) work of mapping a document to features using a neural network from the (relatively cheaper) work of using those features to map a document to a human-interpretable class. We embed every document with [Harrier](https://huggingface.co/microsoft/harrier-oss-v1-0.6b), an open-source model from Microsoft. Harrier is a fine-tuned version of Qwen designed for prompt-guided retrieval, and its large, 1,024-dimensional embeddings precompute multifaceted aspects of a document for downstream use.

These embeddings themselves are not a taxonomy. They aren't human-interpretable, which means using them alone wouldn't allow us to sanity-check the reasonableness of our mixture. Nor are they magical: there are certainly some categorizations that they are unlikely to make separable in embedding space.<sup>[10](#fn-10)</sup> However, their precomputed representations allow us to iterate on different types and granularities of taxonomy relatively quickly using lightweight models conditioned on this more costly, relatively general-purpose representation.

### Cluster by topic<a href="#cluster-by-topic" class="heading-anchor" aria-label="Link to section: Cluster by topic"></a>

Data mixtures are best understood as upsampling or downsampling different topics compared to their natural frequency. However, since repetition is eventually harmful, we are limited in how much we can upsample any dataset. A topic with very few tokens therefore has limited influence over the overall mixture, even if it is very high quality. The effects of such small changes can be hard to measure, leaving the relative sizes of topics in the taxonomy to dictate much of the sampling policy. We therefore aim for evenly sized buckets, giving each weight comparable influence over what the model sees. With a fixed taxonomy, though, we have little reason to expect different topics to be equally represented in our data. Instead, we use an unsupervised clustering process in the Harrier embedding space to determine document topics, with the only constraint being to keep cluster size relatively uniform.

We first use spherical k-means to divide a sample of the corpus into 5,000 compact regions, then assign a much larger sample to those regions to estimate their sizes across the whole corpus. These fine-grained clusters are then agglomeratively merged into 40 larger topics, each containing at least 1% of the total data.

To iterate and measure progress on our clustering process, we adopt Chang et al.'s randomized [intruder study](https://proceedings.neurips.cc/paper/2009/hash/f92586a25bb3145facd64ab20fd554ff-Abstract.html) with an LLM judge. We show the judge several documents from the same cluster and a single document from another cluster: the intruder. The judge then tries to identify the intruder. In small intruder tests, the judge identified the odd document out in 84.4% of cases for the unagglomerated 1,000 clusters, and 62.5% for the margin-refined 40-topic taxonomy. Both exceed the 20% chance baseline, with p \< 0.001 under one-sided exact binomial tests. This does not prove that our taxonomy is unique or optimal, but it does give us a lightweight reliable measure to hill climb for the semantic coherence of our clusters.

### Score quality<a href="#score-quality" class="heading-anchor" aria-label="Link to section: Score quality"></a>

While upsampling relevant topics is great, upsampling bad data from relevant topics is not so great. As such, every document receives a second label which ultimately places it into one of five quality bands, with thresholds calibrated by content type. We combine this band with the document’s topic to select its sampling bucket. Our classifier follows the pattern established by [FineWeb-Edu](https://arxiv.org/abs/2406.17557), which first labels documents using a large model given a rubric for quality, then distills this into a lightweight classifier which can be used to label the entire corpus with scores.

Notably, we use these scores to group data rather than filter it in advance. Similar to our use of embedding, this is to avoid the need for reprocessing if our requirements change. In particular, data filtering has been repeatedly shown to be conditional on budget.<sup>[11](#fn-11)</sup> With a small amount of compute, data needs to be heavily filtered as flops should be spent on your best data. However, over a larger run, diversity can be worth decreased quality tradeoffs to avoid overfitting to a small number of documents. By scoring rather than filtering, Datakit allows downstream usage to be more easily re-calibrated depending on budget.

<figure class="plotly-figure-block">
<div class="plotly-frame-outer">
<div class="plotly-frame-title">
How much data is in each bucket?
</div>
<div class="plotly-frame-inner">
<div class="d3-figure" aria-label="How much data is in each bucket?. Each cell is one topic-quality bucket, labeled with its share of the 23.11 trillion available tokens. Darker cells contain more data. These are the proportions available before we learn how often to sample each bucket." data-d3-renderer="bucket-grid" data-d3-src="/assets/images/blog/marin-data-pipeline-overview/bucket-grid.json" role="group">

</div>
</div>
</div>
<figcaption>Each cell is one topic-quality bucket, labeled with its share of the 23.11 trillion available tokens. Darker cells contain more data. These are the proportions available before we learn how often to sample each bucket.</figcaption>
</figure>

## 3. Learn the data mixture<a href="#3-learn-the-data-mixture" class="heading-anchor" aria-label="Link to section: 3. Learn the data mixture"></a>

Crossing 40 topics with five quality bands gives us 200 independently weighted buckets. How do we choose among possible weights for each bucket to create a mixture which produces a strong model?

Trying to brute force the candidates at full scale would be ruinously expensive, so we train a swarm of small proxy models on different mixtures.<sup>[12](#fn-12)</sup> Each proxy gets a training budget proportional to its active parameter count, along with a proportionally scaled-down data pool for every bucket.<sup>[13](#fn-13)</sup> Under a given mixture, the proxy therefore repeats each bucket roughly as many times as the hero would: a short-run simulation of the hero’s epoching. This lets us explore the tradeoff between repeating higher-quality data and seeing more unique data that may be lower quality.

The pipeline described here is the one we used to prepare the data and learn the mixture for our most recent hero run. The proxy dataset now contains 872 observations from our smallest possible MoE setup. We fit a regression to the proxy evaluation results, then use it to predict and optimize the data mixture, using a functional form inspired by [Calvin Xu's work on the topic in Marin](https://github.com/marin-community/marin/pull/2393).<sup>[14](#fn-14)</sup> This procedure is increasingly common, though we plan to spend a future post in this series diving deeper into our approach and experiments.

<figure class="plotly-figure-block">
<div class="plotly-frame-outer">
<div class="plotly-frame-title">
Which buckets track performance?
</div>
<div class="plotly-frame-inner">
<div class="d3-figure" aria-label="Which buckets track performance?. The buckets associated with better performance change with the evaluation. Select an UncheatableEval subset to see the Spearman correlation between each bucket’s weight and BPB across 872 proxy runs, separately for pretraining and cooldown. Blue accompanies lower, better BPB; red accompanies higher, worse BPB; grey means the weight did not vary. These associations are not isolated effects because every mixture’s weights sum to one." data-d3-renderer="uncheatable-correlations" data-d3-src="/assets/images/blog/marin-data-pipeline-overview/uncheatable-correlations.json" role="group" style="min-height:900px">

</div>
</div>
</div>
<figcaption>The buckets associated with better performance change with the evaluation. Select an UncheatableEval subset to see the Spearman correlation between each bucket’s weight and BPB across 872 proxy runs, separately for pretraining and cooldown. Blue accompanies lower, better BPB; red accompanies higher, worse BPB; grey means the weight did not vary. These associations are not isolated effects because every mixture’s weights sum to one.</figcaption>
</figure>

Before launching the hero run, we compare the optimized mixture with proportional sampling—the naive baseline—across a ladder of larger models, asking whether its advantage survives scale.

## What's next<a href="#whats-next" class="heading-anchor" aria-label="Link to section: What&#39;s next"></a>

Among the follow-ups, we’ll look more closely at deduplication and decontamination; embeddings, topic clustering, and quality scoring; mixture experiment design, including surrogate modeling and optimization, validation, and proxy-to-target transfer; and the datasets Marin built itself for our most recent hero run.

As with all of Marin’s work, all software used is released openly:

- **Source registry:** the upstream repository, revision, and license for every source, recorded in a readable [`sources.py` catalogue](https://github.com/marin-community/marin/blob/64a9483cf1a928e6db97b83130d8a5d171a4aead/lib/marin/src/marin/datakit/sources.py)
- **Processing code:** normalization, deduplication, and decontamination in the [Datakit module](https://github.com/marin-community/marin/tree/64a9483cf1a928e6db97b83130d8a5d171a4aead/lib/marin/src/marin/datakit)
- **Proxy-run dataset:** the mixture weights and evaluation results behind the opening figure, at [marin-community/grug-moe-mix-swarm](https://huggingface.co/datasets/marin-community/grug-moe-mix-swarm)
- **Token counts and licenses:** per-source totals in the [token count viewer](https://huggingface.co/spaces/marin-community/token-count-viewer)

For the reasons above, we leave the upstream datasets with the people who made them. But if there’s a Datakit artifact you’d like us to release that we haven’t, let us know on [Discord](https://discord.com/invite/J9CTk7pqcM).

## Contributions and acknowledgments<a href="#contributions-and-acknowledgments" class="heading-anchor" aria-label="Link to section: Contributions and acknowledgments"></a>

- **[Rafal Wojdyla](https://github.com/ravwojdyla):** Implemented Datakit’s data-processing pipeline, including normalization, exact and fuzzy deduplication, decontamination, and the core infrastructure for quality classification.
- **[Will Held](https://github.com/Helw150):** Integrated data sources, implemented the Harrier embedding pipeline and mixture-swarm tooling, and developed topic clustering for the hero run. Prepared this post and its figures.
- **[Mark Muchane](https://github.com/muchanem):** Developed the quality classifier used for the hero run.
- **[Russell Power](https://github.com/rjpower) and [Will Moss](https://github.com/wmoss):** Built and improved the execution, storage, and resource-management infrastructure used to process the corpus at scale.
- **[Calvin Xu](https://github.com/Calvin-Xu):** Developed earlier mixture-learning experiments and regression methods that informed this approach.

We thank the dataset contributors who made this work possible: AI2, NVIDIA, Hugging Face, BigCode, EleutherAI, the Common Pile contributors, HPLT, the Institutional Data Initiative, Project Numina, Essential AI, Amazon Science, Alibaba Apsara, GAIR, Locus Lab, Nebius, Open Thoughts, PleIAs, Prime Intellect, SuperDoc, Teraflop AI, Together AI, Trillion Labs, Common Crawl, the National Science Foundation, the GHALogs contributors, [Ben Feuer](https://huggingface.co/penfever), [Kevin Xiang Li](https://kevinx.li/), [Tim O’Donnell](https://timodonnell.github.io/), [Andy Arditi](https://huggingface.co/andyrdt), [Kanta Hayashi](https://huggingface.co/KantaHayashiAI), [nyuuzyou](https://huggingface.co/nyuuzyou), and the Marin community.

We gratefully acknowledge the Jen-Hsun and Lori Huang Foundation for providing a computational grant used for this study.

We thank [Isaac Hodes](https://www.linkedin.com/in/isaachodes/), [Percy Liang](https://cs.stanford.edu/~pliang/), [David Hall](https://github.com/dlwh), and [Rafal Wojdyla](https://github.com/ravwojdyla) for feedback on this post.

<div class="section footnotes">

1.  <div id="fn-1">

    Kevin produced this massive trace dataset as part of an RAship [working on Marin at Stanford](https://x.com/kevin_x_li/status/2054600962137100493).<a href="#fnref-1" class="footnote">↩︎</a>

    </div>

2.  <div id="fn-2">

    We added this after truly heroic runs of whitespace consumed an entire tokenization job’s memory. Somewhere on the open web is a page that is 99% spacebar; we have met it.<a href="#fnref-2" class="footnote">↩︎</a>

    </div>

3.  <div id="fn-3">

    [Fang et al.](https://arxiv.org/html/2503.07879) found that duplicate count can signal document quality during subsampling, although retaining the duplicates themselves performed much worse.<a href="#fnref-3" class="footnote">↩︎</a>

    </div>

4.  <div id="fn-4">

    Marin’s [deduplication literature review](https://github.com/marin-community/marin/issues/2093#issuecomment-3609095675) led us to MinHash and LSH.<a href="#fnref-4" class="footnote">↩︎</a>

    </div>

5.  <div id="fn-5">

    Contamination can also lower a score: during the [Marin 32B Bison cooldown](https://marin.readthedocs.io/en/latest/reports/marin-32b-retro/#contamination-anomaly-gsm8k), seeing GSM8K test items in one prompt format made the model worse on another.<a href="#fnref-5" class="footnote">↩︎</a>

    </div>

6.  <div id="fn-6">

    Because evaluation sets are much smaller than training corpora, comparing each evaluation item with the corpus is far cheaper than all-pairs deduplication; Datakit makes it cheaper still by indexing evaluation n-grams first.<a href="#fnref-6" class="footnote">↩︎</a>

    </div>

7.  <div id="fn-7">

    We follow [Dolma](https://arxiv.org/abs/2402.00159) in using a Bloom filter for n-gram matching, with a guarded exact match for short alphabetic paragraphs that have no 13-grams.<a href="#fnref-7" class="footnote">↩︎</a>

    </div>

8.  <div id="fn-8">

    This is one of the key insights from [*Organize the Web*](https://arxiv.org/html/2502.10341v3). If we can “construct meaningful domains for monolithic web corpora,” we can produce much more expressive mixtures, as done in [*OLMix*](https://arxiv.org/abs/2602.12237) for OLMo 3. Both works are incredible reads for understanding the origins of our approach\!<a href="#fnref-8" class="footnote">↩︎</a>

    </div>

9.  <div id="fn-9">

    I am a broken record on this topic but filtering and mixing are subsets of the same policy space with mildly different constraints. Filtering can be expressed as a data mix where some weights are exactly zero. While filtering cannot represent downsampling or upsampling, it generally acts on a per example basis rather than on groups of data. Both are subsets of data selection with replacement.<a href="#fnref-9" class="footnote">↩︎</a>

    </div>

10. <div id="fn-10">

    Consider a collection of programs before and after off-by-one errors are fixed. While a single character can determine whether a program works, it minimally shifts the Harrier representation. We should not, as such, expect a linear classifier using the Harrier embeddings to distinguish buggy programs from correct ones.<a href="#fnref-10" class="footnote">↩︎</a>

    </div>

11. <div id="fn-11">

    [Vision-language](https://arxiv.org/html/2404.07177v1) and [language-model](https://arxiv.org/html/2605.19407v1) experiments both suggest that aggressive filtering helps at low compute, while broader pools can win once repetition becomes the bigger problem. [Nemotron-CC](https://arxiv.org/abs/2412.02595) offers the useful compromise of retaining quality scores and using them to control sampling.<a href="#fnref-11" class="footnote">↩︎</a>

    </div>

12. <div id="fn-12">

    The recipe follows [RegMix](https://arxiv.org/html/2407.01492v2)—train proxy models, fit a regression, and optimize the mixture—with [Calvin Xu’s work](https://github.com/marin-community/marin/pull/2393) motivating our treatment of repetition. Whether the fitted response transfers to larger models remains to be tested.<a href="#fnref-12" class="footnote">↩︎</a>

    </div>

13. <div id="fn-13">

    We chose the target training budget by balancing model size, measured throughput, and time reserved for post-training. The later hero scaling ladder used 791 tokens per active parameter to match an 18T-token run of the 22.76B-active-parameter model. For more details, see the [scaling experiments](https://github.com/marin-community/marin/issues/6074), [Floppy Phoenix planning discussion](https://github.com/marin-community/marin/issues/7673), and [hero scaling ladder](https://github.com/marin-community/marin/pull/8388).<a href="#fnref-13" class="footnote">↩︎</a>

    </div>

14. <div id="fn-14">

    The intuition is that loss falls nearly linearly at first, flattens as the data’s benefit saturates, then rises once repetition causes overfitting.<a href="#fnref-14" class="footnote">↩︎</a>

    </div>

</div>

<div class="section blog-post-citation" aria-labelledby="cite-heading">

## Cite this post

<div class="blog-post-citation-wrap">

``` blog-post-citation-bibtex
@misc{held2026_marin_data_pipeline_overview,
  author = {Held, Will},
  title = {Curating 25 Trillion Tokens for LLM Pretraining},
  year = {2026},
  month = {sep},
  howpublished = {\url{https://www.openathena.ai/blog/marin-data-pipeline-overview/}},
  note = {Open Athena Blog}
}
```

<img src="data:image/svg+xml;base64,PHN2ZyBhcmlhLWhpZGRlbj0idHJ1ZSIgY2xhc3M9Imljb24tY29weSIgZmlsbD0iY3VycmVudENvbG9yIiBoZWlnaHQ9IjE2IiB2aWV3Ym94PSIwIDAgMTYgMTYiIHdpZHRoPSIxNiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNNCAyYTIgMiAwIDAgMSAyLTJoOGEyIDIgMCAwIDEgMiAydjhhMiAyIDAgMCAxLTIgMkg2YTIgMiAwIDAgMS0yLTJ6bTItMWExIDEgMCAwIDAtMSAxdjhhMSAxIDAgMCAwIDEgMWg4YTEgMSAwIDAgMCAxLTFWMmExIDEgMCAwIDAtMS0xek0yIDVhMSAxIDAgMCAwLTEgMXY4YTEgMSAwIDAgMCAxIDFoOGExIDEgMCAwIDAgMS0xdi0xaDF2MWEyIDIgMCAwIDEtMiAySDJhMiAyIDAgMCAxLTItMlY2YTIgMiAwIDAgMSAyLTJoMXYxeiIgZmlsbC1ydWxlPSJldmVub2RkIiAvPjwvc3ZnPg==" class="icon-copy" /> <img src="data:image/svg+xml;base64,PHN2ZyBhcmlhLWhpZGRlbj0idHJ1ZSIgY2xhc3M9Imljb24tY2hlY2siIGZpbGw9ImN1cnJlbnRDb2xvciIgaGVpZ2h0PSIxNiIgdmlld2JveD0iMCAwIDE2IDE2IiB3aWR0aD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEzLjg1NCAzLjY0NmEuNS41IDAgMCAxIDAgLjcwOGwtNyA3YS41LjUgMCAwIDEtLjcwOCAwbC0zLjUtMy41YS41LjUgMCAxIDEgLjcwOC0uNzA4TDYuNSAxMC4yOTNsNi42NDYtNi42NDdhLjUuNSAwIDAgMSAuNzA4IDAiIC8+PC9zdmc+" class="icon-check" />

</div>

</div>

</div>

</div>

</div>

