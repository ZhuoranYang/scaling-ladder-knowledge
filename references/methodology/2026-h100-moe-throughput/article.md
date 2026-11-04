<div class="main-content col-lg-9 col-md-9 mt-0" role="main">

<div class="post-card--single">

<div class="row">

<div class="col-lg-12 mb-0">

<div class="card--post-attributes">

<span class="category-name content-s"> <a href="https://developer.nvidia.com/blog/category/generative-ai/" data-wpel-link="internal" rel="follow" target="_self">Agentic AI / Generative AI</a> </span> <span class="post-rate-widget content-s"></span> <span class="post-lang-switcher"> </span>

<div class="posts-filter-form">

<div class="filter-item form-type-select">

English中文

</div>

</div>

</div>

# Democratizing Large-Scale Mixture-of-Experts Training with NVIDIA PyTorch Parallelism

<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-1024x576-jpg.webp" class="attachment-full-page-width size-full-page-width wp-post-image" decoding="async" fetchpriority="high" sizes="(max-width: 1024px) 100vw, 1024px" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-1024x576-jpg.webp 1024w, https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-300x169-jpg.webp 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-625x352-jpg.webp 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-179x101-jpg.webp 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-768x432-jpg.webp 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-645x363-jpg.webp 645w, https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-660x370-jpg.webp 660w, https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-500x281-jpg.webp 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-160x90-jpg.webp 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-362x204-jpg.webp 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-195x110-jpg.webp 195w, https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-960x540-jpg.webp 960w, https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/image2-1-jpg.webp 1208w" width="1024" height="576" />

<div class="post-info">

<div class="post-published-date">

Nov 06, 2025

</div>

<div class="post-authors">

By <a href="https://developer.nvidia.com/blog/author/hemildesai/" class="author url fn" data-wpel-link="internal" rel="author follow" target="_self" title="Posts by Hemil Desai">Hemil Desai</a>, <a href="https://developer.nvidia.com/blog/author/bernardn/" class="author url fn" data-wpel-link="internal" rel="author follow" target="_self" title="Posts by Bernard Nguyen">Bernard Nguyen</a>, <a href="https://developer.nvidia.com/blog/author/wenweng/" class="author url fn" data-wpel-link="internal" rel="author follow" target="_self" title="Posts by Wenwen Gao">Wenwen Gao</a> and <a href="https://developer.nvidia.com/blog/author/gneskovic/" class="author url fn" data-wpel-link="internal" rel="author follow" target="_self" title="Posts by Gordana Neskovic">Gordana Neskovic</a>

</div>

<div class="card--post-attributes-secondary card--post-attributes-header">

<div class="post--rate secondary--attribute">

<div class="wpulike wpulike-heart">

<div class="wp_ulike_general_class wp_ulike_is_not_liked">

<span class="count-box wp_ulike_counter_up" ulike-counter-value="+17"></span>

</div>

</div>

Like

</div>

<div class="post--comments-count secondary--attribute">

[ Discuss (0)](#entry-content-comments)

</div>

</div>

</div>

</div>

</div>

</div>

<div class="entry-meta-social">

- <a href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Faccelerating-large-scale-mixture-of-experts-training-in-pytorch%2F" class="for-linkedin" data-wpel-link="external" rel="follow" target="_blank">L</a>
- <a href="https://twitter.com/intent/tweet?text=Democratizing+Large-Scale+Mixture-of-Experts+Training+with+NVIDIA+PyTorch+Parallelism+%7C+NVIDIA+Technical+Blog+https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Faccelerating-large-scale-mixture-of-experts-training-in-pytorch%2F" class="for-twitter" data-wpel-link="external" rel="follow" target="_blank">T</a>
- <a href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Faccelerating-large-scale-mixture-of-experts-training-in-pytorch%2F" class="for-facebook" data-wpel-link="external" rel="follow" target="_blank">F</a>
- <a href="https://www.reddit.com/submit?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Faccelerating-large-scale-mixture-of-experts-training-in-pytorch%2F&amp;title=Democratizing+Large-Scale+Mixture-of-Experts+Training+with+NVIDIA+PyTorch+Parallelism+%7C+NVIDIA+Technical+Blog" class="for-reddit" data-wpel-link="external" rel="follow" target="_blank">R</a>
- <a href="mailto:?subject=I&#39;d%20like%20to%20share%20a%20link%20with%20you&amp;body=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Faccelerating-large-scale-mixture-of-experts-training-in-pytorch%2F" class="for-mail">E</a>

</div>

<img src="data:image/svg+xml;base64,PHN2ZyBhcmlhLWhpZGRlbj0idHJ1ZSIgY2xhc3M9Im52LWFpLXN1bW1hcnlfX2ljb24iIGZpbGw9Im5vbmUiIGhlaWdodD0iMjUiIHZpZXdib3g9IjAgMCAyNSAyNSIgd2lkdGg9IjI1IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0yMi40OTE1IDE1LjMwMTlDMjIuMjk0IDE1LjMwNDcgMjIuMDk3NiAxNS4zMzE2IDIxLjkwNjYgMTUuMzgxOUwyMC4yNTQgMTIuOTAxOUwyMS45MDUgMTAuNDIxOUMyMi4wOTY3IDEwLjQ3MzEgMjIuMjkzMyAxMC40OTg3IDIyLjQ5MTUgMTAuNTAxOUMyMi44ODQ0IDEwLjUwMzIgMjMuMjcxNiAxMC40MDc4IDIzLjYxOSAxMC4yMjQxQzIzLjk2NjUgMTAuMDQwNCAyNC4yNjM1IDkuNzc0MDUgMjQuNDgzOSA5LjQ0ODQ1QzI0LjcwNDQgOS4xMjI4NSAyNC44NDE1IDguNzQ3OTkgMjQuODgzMiA4LjM1Njg3QzI0LjkyNSA3Ljk2NTc1IDI0Ljg3MDEgNy41NzAzNSAyNC43MjMzIDcuMjA1NDdDMjQuNTc2NiA2Ljg0MDU5IDI0LjM0MjUgNi41MTc0MSAyNC4wNDE3IDYuMjY0MzdDMjMuNzQwOSA2LjAxMTM0IDIzLjM4MjUgNS44MzYyIDIyLjk5ODIgNS43NTQzN0MyMi42MTM5IDUuNjcyNTUgMjIuMjE1NCA1LjY4NjU0IDIxLjgzNzggNS43OTUxMkMyMS40NjAxIDUuOTAzNyAyMS4xMTQ5IDYuMTAzNTQgMjAuODMyNiA2LjM3NzA2TDE1LjI3MDkgMy41OTMwNUMxNS4yODY4IDMuNDk3MDUgMTUuMjk2NCAzLjM5OTQ2IDE1LjI5OTYgMy4zMDE4NkMxNS4yOTk2IDIuNjY1MzQgMTUuMDQ3MSAyLjA1NDg5IDE0LjU5NzUgMS42MDQ4QzE0LjE0NzkgMS4xNTQ3MSAxMy41MzgxIDAuOTAxODU1IDEyLjkwMjMgMC45MDE4NTVDMTIuMjY2NSAwLjkwMTg1NSAxMS42NTY4IDEuMTU0NzEgMTEuMjA3MiAxLjYwNDhDMTAuNzU3NiAyLjA1NDg5IDEwLjUwNTEgMi42NjUzNCAxMC41MDUxIDMuMzAxODZDMTAuNTA4MyAzLjM5OTQ2IDEwLjUxNzggMy40OTcwNSAxMC41MzM4IDMuNTkzMDVMNC45NzIxMSA2LjM3NzA2QzQuNjg5NzYgNi4xMDI2NyA0LjM0NDMzIDUuOTAyMDIgMy45NjYyNiA1Ljc5MjgxQzMuNTg4MTggNS42ODM2IDMuMTg5MDggNS42NjkxOCAyLjgwNDEyIDUuNzUwODJDMi40MTkxNiA1LjgzMjQ1IDIuMDYwMTggNi4wMDc2NCAxLjc1ODggNi4yNjA5M0MxLjQ1NzQzIDYuNTE0MjMgMS4yMjI5MiA2LjgzNzg2IDEuMDc1OTUgNy4yMDMyOUMwLjkyODk4MSA3LjU2ODcyIDAuODc0MDU4IDcuOTY0NzQgMC45MTYwMjggOC4zNTY0NEMwLjk1Nzk5OCA4Ljc0ODEzIDEuMDk1NTcgOS4xMjM0OCAxLjMxNjYyIDkuNDQ5MzlDMS41Mzc2NyA5Ljc3NTMgMS44MzU0IDEwLjA0MTggMi4xODM1OCAxMC4yMjUzQzIuNTMxNzYgMTAuNDA4OCAyLjkxOTcgMTAuNTAzOCAzLjMxMzE5IDEwLjUwMTlDMy41MTEzNiAxMC40OTg3IDMuNzA3OTQgMTAuNDcxNSAzLjg5ODEzIDEwLjQyMTlMNS41NTA2NiAxMi45MDE5TDMuODk5NzMgMTUuMzgxOUMzLjcwODE4IDE1LjMzMTQgMy41MTEyMiAxNS4zMDQ2IDMuMzEzMTkgMTUuMzAxOUMyLjkyMDI5IDE1LjMwMDUgMi41MzMwOCAxNS4zOTU5IDIuMTg1NjUgMTUuNTc5NkMxLjgzODIyIDE1Ljc2MzMgMS41NDEyMiAxNi4wMjk3IDEuMzIwNzcgMTYuMzU1M0MxLjEwMDMyIDE2LjY4MDkgMC45NjMxODkgMTcuMDU1NyAwLjkyMTQ0MiAxNy40NDY4QzAuODc5Njk1IDE3LjgzOCAwLjkzNDYxMyAxOC4yMzM0IDEuMDgxMzYgMTguNTk4MkMxLjIyODExIDE4Ljk2MzEgMS40NjIxOSAxOS4yODYzIDEuNzYzMDEgMTkuNTM5M0MyLjA2MzgyIDE5Ljc5MjQgMi40MjIxNSAxOS45Njc1IDIuODA2NDYgMjAuMDQ5M0MzLjE5MDc3IDIwLjEzMTIgMy41ODkyOCAyMC4xMTcyIDMuOTY2OTEgMjAuMDA4NkM0LjM0NDU1IDE5LjkgNC42ODk3NCAxOS43MDAyIDQuOTcyMTEgMTkuNDI2N0wxMC41MzM4IDIyLjIxMDdDMTAuNTE3OCAyMi4zMDY3IDEwLjUwODMgMjIuNDA0MyAxMC41MDUxIDIyLjUwMTlDMTAuNTA1MSAyMy4xMzg0IDEwLjc1NzYgMjMuNzQ4OCAxMS4yMDcyIDI0LjE5ODlDMTEuNjU2OCAyNC42NDkgMTIuMjY2NSAyNC45MDE5IDEyLjkwMjMgMjQuOTAxOUMxMy41MzgxIDI0LjkwMTkgMTQuMTQ3OSAyNC42NDkgMTQuNTk3NSAyNC4xOTg5QzE1LjA0NzEgMjMuNzQ4OCAxNS4yOTk2IDIzLjEzODQgMTUuMjk5NiAyMi41MDE5QzE1LjI5NTggMjIuNDA0MyAxNS4yODYyIDIyLjMwNzEgMTUuMjcwOSAyMi4yMTA3TDIwLjgzMjYgMTkuNDI2N0MyMS4xMTQ5IDE5LjcwMSAyMS40NjA0IDE5LjkwMTcgMjEuODM4NCAyMC4wMTA5QzIyLjIxNjUgMjAuMTIwMSAyMi42MTU2IDIwLjEzNDUgMjMuMDAwNiAyMC4wNTI5QzIzLjM4NTUgMTkuOTcxMyAyMy43NDQ1IDE5Ljc5NjEgMjQuMDQ1OSAxOS41NDI4QzI0LjM0NzMgMTkuMjg5NSAyNC41ODE4IDE4Ljk2NTkgMjQuNzI4NyAxOC42MDA0QzI0Ljg3NTcgMTguMjM1IDI0LjkzMDYgMTcuODM5IDI0Ljg4ODcgMTcuNDQ3M0MyNC44NDY3IDE3LjA1NTYgMjQuNzA5MSAxNi42ODAyIDI0LjQ4ODEgMTYuMzU0M0MyNC4yNjcgMTYuMDI4NCAyMy45NjkzIDE1Ljc2MTkgMjMuNjIxMSAxNS41Nzg0QzIzLjI3MjkgMTUuMzk0OSAyMi44ODUgMTUuMjk5OSAyMi40OTE1IDE1LjMwMTlaTTEyLjg4ODQgMi41MDI3NEMxMy4wMTg1IDIuNTAzMjQgMTMuMTQ2NSAyLjUzNTUyIDEzLjI2MTMgMi41OTY3OUMxMy4zNzYxIDIuNjU4MDUgMTMuNDc0MiAyLjc0NjQ0IDEzLjU0NzEgMi44NTQyOUMxMy42MiAyLjk2MjE0IDEzLjY2NTUgMy4wODYxNyAxMy42Nzk3IDMuMjE1NjNDMTMuNjkzOSAzLjM0NTA5IDEzLjY3NjMgMy40NzYwNSAxMy42Mjg0IDMuNTk3MTRMMTMuNjA2IDMuNjQxOTRDMTMuNTQyOSAzLjc3OTgxIDEzLjQ0MTYgMy44OTY2NCAxMy4zMTQxIDMuOTc4NTVDMTMuMTg2NiA0LjA2MDQ1IDEzLjAzODMgNC4xMDM5OSAxMi44ODY4IDQuMTAzOTlDMTIuNzM1MyA0LjEwMzk5IDEyLjU4NyA0LjA2MDQ1IDEyLjQ1OTYgMy45Nzg1NUMxMi4zMzIxIDMuODk2NjQgMTIuMjMwNyAzLjc3OTgxIDEyLjE2NzYgMy42NDE5NEwxMi4xNDUzIDMuNTk4NzRDMTIuMDk3IDMuNDc3MzEgMTIuMDc5MSAzLjM0NTg5IDEyLjA5MzMgMy4yMTU5NkMxMi4xMDc0IDMuMDg2MDMgMTIuMTUzMiAyLjk2MTU2IDEyLjIyNjUgMi44NTM0MkMxMi4yOTk4IDIuNzQ1MjggMTIuMzk4NSAyLjY1Njc4IDEyLjUxMzkgMi41OTU2NEMxMi42MjkzIDIuNTM0NTEgMTIuNzU3OSAyLjUwMjYxIDEyLjg4ODQgMi41MDI3NFpNMjMuMjc2NyA4LjEwMjc0QzIzLjI3NjcgOC4zMTQ5MSAyMy4xOTI1IDguNTE4NCAyMy4wNDI2IDguNjY4NDNDMjIuODkyOCA4LjgxODQ1IDIyLjY4OTUgOC45MDI3NCAyMi40Nzc2IDguOTAyNzRDMjIuMjY1NiA4LjkwMjc0IDIyLjA2MjQgOC44MTg0NSAyMS45MTI1IDguNjY4NDNDMjEuNzYyNyA4LjUxODQgMjEuNjc4NSA4LjMxNDkxIDIxLjY3ODUgOC4xMDI3NEMyMS42Nzg1IDcuODkwNTcgMjEuNzYyNyA3LjY4NzA4IDIxLjkxMjUgNy41MzcwNUMyMi4wNjI0IDcuMzg3MDIgMjIuMjY1NiA3LjMwMjc0IDIyLjQ3NzYgNy4zMDI3NEMyMi42ODk1IDcuMzAyNzQgMjIuODkyOCA3LjM4NzAyIDIzLjA0MjYgNy41MzcwNUMyMy4xOTI1IDcuNjg3MDggMjMuMjc2NyA3Ljg5MDU3IDIzLjI3NjcgOC4xMDI3NFpNMi41MDAxNyA4LjEwMjc0QzIuNTAzIDcuOTIzMDUgMi41NjYxNyA3Ljc0OTU2IDIuNjc5NTEgNy42MTAyQzIuNzkyODUgNy40NzA4NSAyLjk0OTc2IDcuMzczNzYgMy4xMjQ5NSA3LjMzNDU4QzMuMzAwMTQgNy4yOTU0IDMuNDgzNCA3LjMxNjQxIDMuNjQ1MiA3LjM5NDIzQzMuODA3IDcuNDcyMDUgMy45Mzc5MiA3LjYwMjE0IDQuMDE2ODUgNy43NjM1NEw0LjAzOTIzIDcuODA4MzRDNC4wOTg3MSA3Ljk1MzA2IDQuMTEzNzYgOC4xMTIyNSA0LjA4MjQ0IDguMjY1NThDNC4wNTExMyA4LjQxODkgMy45NzQ4OCA4LjU1OTQxIDMuODYzNDMgOC42NjkxNEMzLjc1MTU4IDguNzgwNzYgMy42MDkyMSA4Ljg1NjcgMy40NTQyOCA4Ljg4NzM3QzMuMjk5MzYgOC45MTgwNSAzLjEzODgzIDguOTAyMDcgMi45OTI5NyA4Ljg0MTQ3QzIuODQ3MSA4Ljc4MDg2IDIuNzIyNDUgOC42NzgzNSAyLjYzNDc0IDguNTQ2ODdDMi41NDcwMyA4LjQxNTM5IDIuNTAwMiA4LjI2MDg0IDIuNTAwMTcgOC4xMDI3NFpNMi41MDAxNyAxNy43MDI3QzIuNTAwMTcgMTcuNDkwNiAyLjU4NDM2IDE3LjI4NzEgMi43MzQyMiAxNy4xMzcxQzIuODg0MDggMTYuOTg3IDMuMDg3MzMgMTYuOTAyNyAzLjI5OTI3IDE2LjkwMjdDMy41MTEyIDE2LjkwMjcgMy43MTQ0NSAxNi45ODcgMy44NjQzMSAxNy4xMzcxQzQuMDE0MTcgMTcuMjg3MSA0LjA5ODM2IDE3LjQ5MDYgNC4wOTgzNiAxNy43MDI3QzQuMDk4MzYgMTcuOTE0OSA0LjAxNDE3IDE4LjExODQgMy44NjQzMSAxOC4yNjg0QzMuNzE0NDUgMTguNDE4NSAzLjUxMTIgMTguNTAyNyAzLjI5OTI3IDE4LjUwMjdDMy4wODczMyAxOC41MDI3IDIuODg0MDggMTguNDE4NSAyLjczNDIyIDE4LjI2ODRDMi41ODQzNiAxOC4xMTg0IDIuNTAwMTcgMTcuOTE0OSAyLjUwMDE3IDE3LjcwMjdaTTEyLjg4ODQgMjMuMzAyN0MxMi43NTY2IDIzLjMwMjggMTIuNjI2OCAyMy4yNzAyIDEyLjUxMDYgMjMuMjA3OEMxMi4zOTQ0IDIzLjE0NTUgMTIuMjk1NSAyMy4wNTUzIDEyLjIyMjUgMjIuOTQ1NEMxMi4xNDk2IDIyLjgzNTUgMTIuMTA0OSAyMi43MDkyIDEyLjA5MjYgMjIuNTc3OEMxMi4wODAyIDIyLjQ0NjQgMTIuMTAwNSAyMi4zMTQgMTIuMTUxNyAyMi4xOTIzQzEyLjIxMjggMjIuMDUxOSAxMi4zMTI5IDIxLjkzMTkgMTIuNDQwMSAyMS44NDY4QzEyLjU2NzMgMjEuNzYxNiAxMi43MTYzIDIxLjcxNDggMTIuODY5MyAyMS43MTJDMTMuMDIyMyAyMS43MDkxIDEzLjE3MjkgMjEuNzUwMyAxMy4zMDMyIDIxLjgzMDZDMTMuNDMzNiAyMS45MTEgMTMuNTM4MSAyMi4wMjcxIDEzLjYwNDQgMjIuMTY1MUwxMy42MjY4IDIyLjIwOTlDMTMuNjg2OCAyMi4zNTQxIDEzLjcwMjQgMjIuNTEyOSAxMy42NzE2IDIyLjY2NTlDMTMuNjQwOSAyMi44MTkgMTMuNTY1MSAyMi45NTk0IDEzLjQ1NDIgMjMuMDY5MUMxMy4zNzk4IDIzLjE0MzQgMTMuMjkxNiAyMy4yMDIyIDEzLjE5NDUgMjMuMjQyM0MxMy4wOTc0IDIzLjI4MjQgMTIuOTkzNCAyMy4zMDI5IDEyLjg4ODQgMjMuMzAyN1pNMjIuNDc3NiAxOC41MDI3QzIyLjMyNjcgMTguNTAxNiAyMi4xNzkzIDE4LjQ1NzcgMjIuMDUyMyAxOC4zNzYxQzIxLjkyNTMgMTguMjk0NiAyMS44MjQgMTguMTc4NyAyMS43NiAxOC4wNDE5TDIxLjczNzYgMTcuOTk3MUMyMS42OTgxIDE3LjkwMjkgMjEuNjc3NyAxNy44MDE3IDIxLjY3NzcgMTcuNjk5NUMyMS42Nzc3IDE3LjU5NzMgMjEuNjk4MSAxNy40OTYyIDIxLjczNzYgMTcuNDAxOUwyMS43NTIgMTcuMzc0N0MyMS44MDk4IDE3LjI0MjIgMjEuOTAyMyAxNy4xMjc5IDIyLjAxOTkgMTcuMDQzOEMyMi4xMzc0IDE2Ljk1OTggMjIuMjc1NSAxNi45MDkyIDIyLjQxOTQgMTYuODk3NEMyMi41NjMzIDE2Ljg4NTcgMjIuNzA3OCAxNi45MTMyIDIyLjgzNzMgMTYuOTc3MUMyMi45NjY5IDE3LjA0MDkgMjMuMDc2OCAxNy4xMzg4IDIzLjE1NTIgMTcuMjYwMUMyMy4yMzM3IDE3LjM4MTUgMjMuMjc3OCAxNy41MjE5IDIzLjI4MyAxNy42NjY0QzIzLjI4ODEgMTcuODEwOSAyMy4yNTQgMTcuOTU0MSAyMy4xODQzIDE4LjA4MDhDMjMuMTE0NiAxOC4yMDc0IDIzLjAxMiAxOC4zMTI4IDIyLjg4NzIgMTguMzg1N0MyMi43NjI1IDE4LjQ1ODYgMjIuNjIwNCAxOC40OTYzIDIyLjQ3NiAxOC40OTQ3TDIyLjQ3NzYgMTguNTAyN1pNMTguMDE4NiA5LjgwODM0TDIwLjE3MTQgOC43MzE1NEMyMC4xNTU0IDguNjM1NTQgMjAuMTQ1OCA4LjUzNzk0IDIwLjE0MjYgOC40NDAzNEMyMC4xNDU4IDguMzQyNzQgMjAuMTU1NCA4LjI0NTE0IDIwLjE3MTQgOC4xNDkxNEwxNS4yODQxIDUuNzAyNzRMMTguMDE4NiA5LjgwODM0Wk0xMC42MTU4IDUuNzA0MzRMNS43MzAxMiA4LjE0OTE0QzUuNzQ1NDUgOC4yNDU1NSA1Ljc1NTA1IDguMzQyNzkgNS43NTg4OCA4LjQ0MDM0QzUuNzU1NjkgOC41Mzc5NCA1Ljc0NjEgOC42MzU1NCA1LjczMDEyIDguNzMxNTRMNy44ODI4OCA5LjgwODM0TDEwLjYxNTggNS43MDQzNFpNNS43MzAxMiAxNy43NDkxTDcuODgyODggMTYuNjcyM0wxMC42MTc0IDIwLjc3NzlMNS43MzAxMiAxOC4zMzE1QzUuNzQ2MSAxOC4yMzU1IDUuNzU1NjkgMTguMTM3OSA1Ljc1ODg4IDE4LjA0MDNDNS43NTUwNSAxNy45NDI4IDUuNzQ1NDUgMTcuODQ1NiA1LjczMDEyIDE3Ljc0OTFaTTEyLjIxMDggMTMuNTM2M0wxMi4yMzMyIDEzLjU3OTVIMTIuMjM2NEMxMi4zIDEzLjcxNzUgMTIuNDAyMSAxMy44MzQxIDEyLjUzMDMgMTMuOTE1NUMxMi42NTg1IDEzLjk5NjggMTIuODA3NCAxNC4wMzk1IDEyLjk1OTIgMTQuMDM4M0MxMy4xMTA5IDE0LjAzNzEgMTMuMjU5MiAxMy45OTIxIDEzLjM4NjEgMTMuOTA4OEMxMy41MTMgMTMuODI1NSAxMy42MTMyIDEzLjcwNzIgMTMuNjc0NyAxMy41NjgzTDEzLjY4OTEgMTMuNTQxMUMxMy43MjkyIDEzLjQ0NCAxMy43NDk4IDEzLjMzOTggMTMuNzQ5NyAxMy4yMzQ3QzEzLjc0OTYgMTMuMTI5NiAxMy43Mjg4IDEzLjAyNTUgMTMuNjg4NSAxMi45Mjg0QzEzLjY0ODIgMTIuODMxMyAxMy41ODkyIDEyLjc0MzEgMTMuNTE0OCAxMi42Njg4QzEzLjQ0MDUgMTIuNTk0NiAxMy4zNTIzIDEyLjUzNTcgMTMuMjU1MiAxMi40OTU1QzEzLjE1ODEgMTIuNDU1NCAxMy4wNTQxIDEyLjQzNDggMTIuOTQ5MSAxMi40MzQ5QzEyLjg0NDEgMTIuNDM1IDEyLjc0MDEgMTIuNDU1OSAxMi42NDMxIDEyLjQ5NjJDMTIuNTQ2MSAxMi41MzY1IDEyLjQ1ODEgMTIuNTk1NiAxMi4zODM5IDEyLjY3QzEyLjMwOTcgMTIuNzQ0NCAxMi4yNTA5IDEyLjgzMjggMTIuMjEwOCAxMi45Mjk5QzEyLjE3MDYgMTMuMDI2IDEyLjE0OTkgMTMuMTI5IDEyLjE0OTkgMTMuMjMzMUMxMi4xNDk5IDEzLjMzNzMgMTIuMTcwNiAxMy40NDAzIDEyLjIxMDggMTMuNTM2M1pNMTQuNjA5NyAxNC45NzE1QzE0LjM2MzcgMTUuMjA2NiAxNC4wNzA2IDE1LjM4NjYgMTMuNzQ5OCAxNS40OTk1VjIwLjE5ODdMMTYuNTc4NiAxNS45NTcxTDE0LjYwOTcgMTQuOTcxNVpNMTUuMzQ4IDEzLjI0MDNDMTUuMzQ0OCAxMy4zMzk1IDE1LjMzNTMgMTMuNDM4NyAxNS4zMTkzIDEzLjUzNzlMMTcuNDczNiAxNC42MDgzTDE4LjM4NDYgMTMuMjQwM0wxNy40NzIgMTEuODcyM0wxNS4zMTkzIDEyLjk0OTFDMTUuMzM0NiAxMy4wNDU2IDE1LjM0NDIgMTMuMTQyOCAxNS4zNDggMTMuMjQwM1pNMTMuNzQ5OCAxMC45OTM5QzE0LjA3MDYgMTEuMTA2OSAxNC4zNjM3IDExLjI4NjkgMTQuNjA5NyAxMS41MjE5TDE2LjU3ODYgMTAuNTI5OUwxMy43NDk4IDYuMjgxOTRWMTAuOTkzOVpNMTIuMTUxNyAxMC45ODc1VjYuMjgxOTRMOS4zMjI4NSAxMC41Mjk5TDExLjI5MTggMTEuNTE1NUMxMS41Mzc4IDExLjI4MDUgMTEuODMwOSAxMS4xMDA1IDEyLjE1MTcgMTAuOTkzOVpNMTAuNTUzNSAxMy4yNDAzQzEwLjU1NjcgMTMuMTQyNyAxMC41NjYyIDEzLjA0NTEgMTAuNTgyMiAxMi45NDkxTDguNDI3ODcgMTEuODcyM0w3LjUxNjkgMTMuMjQwM0w4LjQyOTQ2IDE0LjYwODNMMTAuNTgyMiAxMy41MzE1QzEwLjU2NjIgMTMuNDM1NSAxMC41NTY3IDEzLjMzNzkgMTAuNTUzNSAxMy4yNDAzWk0xMi4xNTE3IDE1LjQ5MzFDMTEuODMwOSAxNS4zODAyIDExLjUzNzggMTUuMjAwMiAxMS4yOTE4IDE0Ljk2NTFMOS4zMjI4NSAxNS45NTA3TDEyLjE1MTcgMjAuMTk4N1YxNS40OTMxWk0yMC4xNzE0IDE3Ljc0OTFMMTguMDE4NiAxNi42NzIzTDE1LjI4NDEgMjAuNzc3OUwyMC4xNzE0IDE4LjMzMTVDMjAuMTU1NCAxOC4yMzU1IDIwLjE0NTggMTguMTM3OSAyMC4xNDI2IDE4LjA0MDNDMjAuMTQ1OCAxNy45NDI3IDIwLjE1NTQgMTcuODQ1MSAyMC4xNzE0IDE3Ljc0OTFaTTE4LjkxMiAxNS4zMjk5TDIwLjIwNDkgMTUuOTc3OUwxOS4zNDM1IDE0LjY4MDNMMTguOTEyIDE1LjMyOTlaTTIwLjIwNDkgMTAuNTAyN0wxOC45MTIgMTEuMTUwN0wxOS4zNDM1IDExLjgwMDNMMjAuMjA0OSAxMC41MDI3Wk02Ljk4OTQ5IDExLjE0NDNMNS42OTY1NiAxMC41MDQzTDYuNTU3OTggMTEuODAwM0w2Ljk4OTQ5IDExLjE0NDNaTTUuNjk2NTYgMTUuOTc3OUw2Ljk4OTQ5IDE1LjMyOTlMNi41NTc5OCAxNC42ODAzTDUuNjk2NTYgMTUuOTc3OVoiIGZpbGw9ImN1cnJlbnRDb2xvciIgZmlsbC1ydWxlPSJldmVub2RkIiAvPgo8L3N2Zz4=" class="nv-ai-summary__icon" />

## AI-Generated Summary

<img src="data:image/svg+xml;base64,PHN2ZyBhcmlhLWhpZGRlbj0idHJ1ZSIgY2xhc3M9Im52LWFpLXN1bW1hcnlfX3RvZ2dsZS1pY29uIiBmaWxsPSJub25lIiBoZWlnaHQ9IjkiIHZpZXdib3g9IjAgMCAxNCA5IiB3aWR0aD0iMTQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xMi41NzQyIDJMNy40NDkyMyA3TDIuMzI0MjUgMiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS1saW5lY2FwPSJzcXVhcmUiIHN0cm9rZS13aWR0aD0iMiIgLz4KPC9zdmc+" class="nv-ai-summary__toggle-icon" />

<div class="nv-ai-summary__body">

<div class="nv-ai-summary__content">

- <a href="https://github.com/NVIDIA-NeMo/Automodel" data-wpel-link="external" rel="follow" target="_blank">NVIDIA NeMo Automodel</a> is an open-source library within the NeMo framework that enables large-scale mixture-of-experts model training directly in PyTorch using native distributed parallelisms.
- The library combines Fully Sharded Data Parallelism, Expert Parallelism, Pipeline Parallelism, and Context Parallelism with NVIDIA Transformer Engine kernels such as CUDNN RMSNorm, CUDNN Linear, and DotProductAttention to accelerate transformer blocks.
- Advanced token routing and computation components from Megatron-Core, including the DeepEP token dispatcher and GroupedGEMM for MoE experts, reduce communication overhead and improve GPU occupancy at massive scale.
- Benchmark results on DGX H100 systems with BF16 precision show sustained performance of 190 to 280 TFLOPs/sec per GPU and up to 13,000 tokens/sec per GPU, with DeepSeek V3 671B reaching 250 TFLOPs/sec per GPU on 256 GPUs.
- Developers benefit from faster iteration cycles, lower training costs, near-linear scaling from eight to over 1,000 GPUs, and production-ready configurations for leading open-source MoE architectures.

### Next Steps

- Explore the <a href="https://github.com/NVIDIA-NeMo/Automodel" data-wpel-link="external" rel="follow" target="_blank">NeMo Automodel repository</a> to access benchmark scripts and configuration files.
- Run a <a href="https://github.com/NVIDIA-NeMo/Automodel/blob/main/docs/performance-summary.md" data-wpel-link="external" rel="follow" target="_blank">performance documentation</a> review to understand implementation details and reproduce benchmark results.
- Contribute feedback through <a href="https://github.com/NVIDIA-NeMo/Automodel/issues" data-wpel-link="external" rel="follow" target="_blank">GitHub Issues</a> to help shape future development of scalable open AI training tools.

</div>

<div class="nv-ai-summary__disclosure">

Powered by NVIDIA Nemotron. AI-generated content may summarize information incompletely. Verify important information. <a href="https://www.nvidia.com/en-us/agreements/trustworthy-ai/terms/" data-wpel-link="internal" rel="noreferrer noopener follow" target="_self">Learn more</a>

</div>

</div>

<div class="entry-content">

Training massive <a href="https://www.nvidia.com/en-us/glossary/mixture-of-experts/" data-wpel-link="internal" rel="noreferrer noopener follow" target="_self">mixture-of-experts</a> (MoE) models has long been the domain of a few advanced users with deep infrastructure and distributed-systems expertise. For most developers, the challenge wasn’t building smarter models—it was scaling them efficiently across hundreds or even thousands of GPUs without breaking the bank.

With NVIDIA <a href="https://github.com/NVIDIA-NeMo/Automodel" data-wpel-link="external" rel="follow" target="_blank">NeMo Automode</a>l, an open-source library within NVIDIA <a href="https://github.com/NVIDIA-NeMo/" data-wpel-link="external" rel="follow" target="_blank">NeMo framework</a>, developers can now train large-scale MoE models directly in PyTorch—using the same familiar tools they already know. Built on accelerated <a href="https://docs.pytorch.org/docs/stable/distributed.html" data-wpel-link="external" rel="follow" target="_blank">PyTorch distributed</a> with NVIDIA performance optimizations, NeMo Automodel democratizes large-scale MoE training—making it:

- **Simple** – Train billion-parameter models directly in PyTorch without managing complex parallelism or specialized systems.
- **Accessible** – Empower researchers, startups, and enterprises to experiment with MoE architectures previously out of reach.
- **Efficient** – Scale from eight to over 1,000 GPUs while maintaining strong performance and cost-effectiveness through built-in optimizations.

In this post, you’ll see how NeMo Automodel combines PyTorch-native distributed parallelism with NVIDIA acceleration to make large-scale MoE training easier, faster, and more accessible than ever. You’ll also find a detailed quick-start guide to reproduce benchmark results, run your own experiments, and explore configuration options—so you can experience the benefits firsthand.

## Why training large MoEs is hard<a href="#why_training_large_moes_is_hard" class="heading-anchor-link" aria-label="Scroll to Why training large MoEs is hard section"><em></em></a>

Training MoEs efficiently at scale requires solving several interconnected challenges:

1.  **Expert parallelism**: Distribute hundreds of experts across GPUs without overwhelming communication bandwidth.
2.  **Token routing overhead**: Move tokens quickly and efficiently to the correct experts.
3.  **Memory management**: Shard massive parameter sets to fit within GPU memory constraints.
4.  **Communication-computation fusion**: Minimize latency from all-to-all communication and token permutation operations.

As a result of these system challenges, achieving more than 150 TFLOPs/GPU on H100 systems at BF16 precision has historically been difficult—leaving performance untapped.

NVIDIA <a href="https://github.com/NVIDIA-NeMo/Automodel" data-wpel-link="external" rel="follow" target="_blank">NeMo Automodel</a>, an open-source library within the NVIDIA <a href="https://github.com/NVIDIA-NeMo/" data-wpel-link="external" rel="follow" target="_blank">NeMo framework</a>, removes these barriers by building on top of native PyTorch parallelisms. It incorporates advanced infrastructure optimizations—previously reserved for expert ML engineers—directly into the PyTorch ecosystem. 

Developers can now use PyTorch APIs while achieving over 200 TFLOPs per GPU on H100s with BF16 precision for a variety of popular 100B+ MoE architectures. For instance, DeepSeek V3 reached 250 TFLOPs/sec/GPU on 256 GPUs.

This makes large-scale MoE training accessible—empowering the broader community to research, experiment, and innovate with billion-parameter models. 

## Inside NeMo Automodel: architecture and optimizations<a href="#inside_nemo_automodel_architecture_and%C2%A0optimizations" class="heading-anchor-link" aria-label="Scroll to Inside NeMo Automodel: architecture and optimizations section"><em></em></a>

NeMo AutoModel bridges PyTorch native distributed parallelisms with NVIDIA acceleration technologies, creating a unified, high-performance training stack for MoEs.

### **Scaling efficiently via PyTorch distributed parallelisms**<a href="#scaling_efficiently_via_pytorch_distributed_parallelisms" class="heading-anchor-link" aria-label="Scroll to Scaling efficiently via PyTorch distributed parallelisms section"><em></em></a>

Built on <a href="https://docs.pytorch.org/docs/stable/distributed.html" data-wpel-link="external" rel="follow" target="_blank">PyTorch distributed</a>, NeMo Automodel seamlessly scales models using:

- <a href="https://docs.pytorch.org/docs/stable/distributed.fsdp.fully_shard.html" data-wpel-link="external" rel="follow" target="_blank"><strong>Fully Sharded Data Parallelism (FSDP)</strong></a>: Shards model parameters, gradients, and optimizer states across data-parallel ranks to minimize memory use.
- <a href="https://github.com/NVIDIA-NeMo/Automodel/blob/main/nemo_automodel/components/moe/parallelizer.py#L49" data-wpel-link="external" rel="follow" target="_blank"><strong>Expert Parallelism (EP)</strong></a>: Distributes MoE experts efficiently across GPUs for hundreds of experts per model.
- <a href="https://docs.pytorch.org/docs/stable/distributed.pipelining.html" data-wpel-link="external" rel="follow" target="_blank"><strong>Pipeline Parallelism (PP)</strong></a>: Splits model layers into stages for memory-efficient multi-node large model training.
- <a href="https://github.com/NVIDIA-NeMo/Automodel/blob/main/nemo_automodel/components/moe/parallelizer.py#L183" data-wpel-link="external" rel="follow" target="_blank"><strong>Context Parallelism (CP)</strong></a>**:** Partitions long sequences for extended-context training.

### **Accelerating training with NVIDIA Transformer Engine**<a href="#accelerating_training_with_nvidia_transformer_engine" class="heading-anchor-link" aria-label="Scroll to Accelerating training with NVIDIA Transformer Engine section"><em></em></a>

Using <a href="https://github.com/NVIDIA/TransformerEngine" data-wpel-link="external" rel="follow" target="_blank">NVIDIA Transformer Engine</a> kernels—including <a href="https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/api/pytorch.html#transformer_engine.pytorch.RMSNorm" data-wpel-link="internal" rel="follow" target="_self">CUDNN RMSNorm</a>, <a href="https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/api/pytorch.html#transformer_engine.pytorch.Linear" data-wpel-link="internal" rel="follow" target="_self">CUDNN Linear</a>, and <a href="https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/api/pytorch.html#transformer_engine.pytorch.DotProductAttention" data-wpel-link="internal" rel="follow" target="_self">DotProductAttention</a>—NeMo Automodel accelerates transformer blocks and supports different attention mechanisms such as multi-head latent attention (MLA), grouped-query attention (GQA), and sliding-window attention (SWA).

### **Smarter expert routing and computation with Megatron-Core DeepEP and GroupedGEMM**<a href="#smarter_expert_routing_and_computation_with_megatron-core_deepep_and_groupedgemm" class="heading-anchor-link" aria-label="Scroll to Smarter expert routing and computation with Megatron-Core DeepEP and GroupedGEMM section"><em></em></a>

To achieve high efficiency at massive scale, NeMo Automodel integrates advanced token routing and expert computation components from <a href="https://github.com/NVIDIA/Megatron-LM/tree/main/megatron/core/transformer/moe" data-wpel-link="external" rel="follow" target="_blank">Megatron-Core</a>, designed specifically for MOE training.

- <a href="https://github.com/NVIDIA-NeMo/Automodel/blob/main/nemo_automodel/components/moe/megatron/token_dispatcher.py" data-wpel-link="external" rel="follow" target="_blank"><strong>DeepEP token dispatcher</strong></a> (Experimental): Scales token routing to 64+ expert parallelism degrees with highly efficient all-to-all communication and  optional permute/unpermute fusion. By leveraging <a href="https://github.com/deepseek-ai/deepep" data-wpel-link="external" rel="follow" target="_blank">DeepSeek’s DeepEP</a> optimization, NeMo Automodel minimizes communication overhead and maintains balanced expert utilization, enabling smoother scaling across hundreds of GPUs.
- <a href="https://github.com/NVIDIA-NeMo/Automodel/tree/main/nemo_automodel/components/moe/megatron" data-wpel-link="external" rel="follow" target="_blank"><strong>GroupedGEMM for MoE Experts</strong></a>:  Aggregates multiple local expert computations into a single batched GEMM operation. This reduces kernel launches overhead, increases GPU occupancy, and significantly improves throughput and hardware utilization—especially when multiple experts share the same device..

## Breakthrough performance: cost-effective MoE training for everyone<a href="#breakthrough_performance_cost-effective_moe_training_for_everyone" class="heading-anchor-link" aria-label="Scroll to Breakthrough performance: cost-effective MoE training for everyone section"><em></em></a>

The table below shows pre-training benchmarks on DGX H100 systems with BF16 precision across major MoE architectures:

<figure class="wp-block-table aligncenter">
<table class="has-fixed-layout" style="width:100%;">
<colgroup>
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr>
<th><strong>Model</strong></th>
<th><strong>#GPUs</strong></th>
<th><strong>GBS (Global Batch Size)</strong></th>
<th><strong>Parallelism<br />
[TP,PP,CP,EP,VP, FSDP]</strong></th>
<th><strong>Optimizations</strong></th>
<th><strong>TFLOPs<br />
/sec/GPU</strong></th>
<th><strong>Tokens/sec/GPU</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>DeepSeek V3 671B</td>
<td>256</td>
<td>512</td>
<td>1,4,1,64,8,64</td>
<td>TE + DeepEP</td>
<td><strong>250</strong></td>
<td>1,002</td>
</tr>
<tr>
<td>DeepSeek V3 671B</td>
<td>1024</td>
<td>8192</td>
<td>1,4,1,64,8,256</td>
<td>TE + DeepEP</td>
<td><strong>216</strong></td>
<td>865</td>
</tr>
<tr>
<td>Kimi K2</td>
<td>256</td>
<td>512</td>
<td>1,8,1,32,4,32</td>
<td>TE + DeepEP</td>
<td><strong>189</strong></td>
<td>924</td>
</tr>
<tr>
<td>Qwen3 MoE 30B</td>
<td>8</td>
<td>512</td>
<td>1,1,1,8,-,8</td>
<td>TE + DeepEP</td>
<td><strong>277</strong></td>
<td>12,040</td>
</tr>
<tr>
<td>GPT-OSS 20B</td>
<td>8</td>
<td>256</td>
<td>1,1,1,-,-,8</td>
<td>TE + DeepEP + FlexAttn</td>
<td><strong>279</strong></td>
<td>13,058</td>
</tr>
<tr>
<td>GPT-OSS 120B</td>
<td>64</td>
<td>512</td>
<td>1,1,1,-,-,64</td>
<td>TE + DeepEP + FlexAttn</td>
<td><strong>231</strong></td>
<td>7,626</td>
</tr>
</tbody>
</table>
<figcaption><em>Table 1. Pre-training performance of representative mixture-of-experts (MoE) architectures on DGX H100 systems (BF16 precision)</em>. <em>Note: All benchmarks use consistent measurement methodology with mock data, for a sequence length of 4096, and balanced expert routing. Peak H100 BF16 performance is 989 TFLOPs.</em></figcaption>
</figure>

NeMo Automodel delivers industry-leading efficiency and scalability across diverse MoE architectures and GPU counts. Models sustain 190 to 280 TFLOPs/sec per GPU and process up to 13,000 tokens/sec, demonstrating near-linear scaling from eight to 1,024 GPUs, with DeepSeek V3 671B model reaching 250 TFLOPs/sec per GPU on 256 GPUs. All of these are done via native PyTorch parallelisms coupled with NVIDIA optimizations, unlocking peak hardware utilization and cost-effective large-scale MoE training for everyone in the PyTorch community.

If you need even more speed beyond native PyTorch parallelism, <a href="https://github.com/NVIDIA-NeMo/Megatron-Bridge" data-wpel-link="external" rel="noreferrer noopener follow" target="_blank">NeMo Megatron-Bridge</a> provides additional performance optimizations.

## Empowering developers through native PyTorch distributed training<a href="#empowering_developers_through_native_pytorch_distributed_training" class="heading-anchor-link" aria-label="Scroll to Empowering developers through native PyTorch distributed training section"><em></em></a>

By leveraging native PyTorch distributed parallelisms, NeMo Automodel brings high-performance large-scale MOE training directly into the PyTorch ecosystem. This approach eliminates dependency on external or proprietary model-parallel libraries, giving developers full flexibility to scale using tools and APIs they already know.

Most importantly, it reflects NVIDIA commitment to strengthening PyTorch and the broader open source AI ecosystem—making large-model training not just faster, but more open, interoperable, and accessible to the entire developer community.

**Key benefits for developers:**

- **Faster iteration cycles**: Achieve higher throughput for quicker experimentation and model development.
- **Lower training costs**: Better GPU utilization means fewer GPU-hours per training run.
- **Scalable performance**: Consistent, near-linear scaling from eight GPUs to over 1,000 GPUs enables flexible infrastructure planning.
- **Native PyTorch integration**: Leveraged PyTorch distributed to remove reliance on external model-parallel frameworks—keeping everything within the PyTorch workflow. 
- **Ecosystem commitment**: Demonstrates NVIDIA long-term investment in advancing PyTorch, ensuring future innovations are directly integrated into the core framework.
- **Production-ready**: Includes proven, battle-tested configurations for leading open-source MoE architectures.

## Quick start: train and benchmark large MoE models<a href="#quick_start_train_and_benchmark_large_moe_models" class="heading-anchor-link" aria-label="Scroll to Quick start: train and benchmark large MoE models section"><em></em></a>

Getting started with <a href="https://github.com/NVIDIA-NeMo/Automodel" data-wpel-link="external" rel="follow" target="_blank">NeMo Automodel</a> is fast and familiar for any PyTorch developer.

You can use the provided benchmark scripts and configuration files to reproduce results or train your own large-scale MoE models with NVIDIA-optimized performance.

**Minimum requirements**

At least eight GPUs (80 GB memory each) are recommended to reproduce the benchmark results and run fine-tuning experiments efficiently.

Follow these simple steps to run a benchmark or fine-tuning experiment: 

<div class="wp-block-syntaxhighlighter-code">

``` brush:

# 1. Pull the NeMo docker image and start a container
docker pull nvcr.io/nvidia/nemo:25.09
docker run -it -d --ulimit memlock=-1 --ulimit stack=67108864 --gpus all nvcr.io/nvidian/nemo:25.09 bash

# 2. Once  inside the container, clone the repo and navigate to Automodel
git clone https://github.com/NVIDIA-NeMo/Automodel.git
cd Automodel
```

</div>

**Run a benchmark**

Example: Benchmark Qwen3 MoE 30B on eight GPUs

<div class="wp-block-syntaxhighlighter-code">

``` brush:

torchrun --nproc-per-node 8 nemo_automodel/recipes/llm/benchmark.py \
  --config examples/benchmark/configs/qwen3_moe_30b_te_deepep.yaml
```

</div>

**Run fine-tuning**

Example: Fine-tune Qwen3 MoE 30B

Note: 

- You’ll need to download the model checkpoint from Hugging Face first: *`hf download Qwen/Qwen3-30B-A3B`*
- If you encounter a dataset instantiation error, upgrade the *datasets* library: *`pip install --upgrade datasets`*

<div class="wp-block-syntaxhighlighter-code">

``` brush:

torchrun --nproc-per-node 8 examples/llm_finetune/finetune.py --config examples/llm_finetune/qwen/qwen3_moe_30b_te_deepep.yaml
```

</div>

**Available configuration files:**

- `deepseek_v3_te_deepep.yaml` – DeepSeek V3 (671B parameter)
- `kimi_k2_te_deepep.yaml` – Optimized configuration for Kimi K2 
- `qwen3_moe_30b_te_deepep.yaml` – Qwen3 MoE 30B with full NVIDIA optimizations
- `gptoss_20b_te_deepep.yaml` – GPT-OSS 20B with FlexAttention
- `gptoss_120b_te_deepep.yaml` – GPT-OSS 120B production configuration

Check out <a href="https://github.com/NVIDIA-NeMo/Automodel/blob/main/docs/performance-summary.md" data-wpel-link="external" rel="follow" target="_blank">docs</a> for complete performance documentation and implementation details.

## Join us in democratizing open MoE training with native PyTorch<a href="#join_us_in_democratizing_open_moe_training_with_native_pytorch" class="heading-anchor-link" aria-label="Scroll to Join us in democratizing open MoE training with native PyTorch section"><em></em></a>

This release marks a major milestone in democratizing large-scale mixture-of-experts (MoE) training with accelerated PyTorch. But it’s only the beginning.

We’re actively working on:

**Expanding model support:** Adding new MoE and hybrid architectures.

- **Deeper optimizations**: Further kernel-level and communication improvements for even higher efficiency.
- **Technical deep dives**: Detailed explainers of NeMo AutoModel MoE design and performance techniques.
- **Broader benchmarking**: Extending performance validation across diverse hardware and cluster configurations.

We’d love for you to get started with <a href="https://github.com/NVIDIA-NeMo/Automodel" data-wpel-link="external" rel="follow" target="_blank">NeMo Automodel</a> and be part of this journey—try the configurations, share your results, and contribute feedback through <a href="https://github.com/NVIDIA-NeMo/Automodel/issues" data-wpel-link="external" rel="follow" target="_blank">GitHub Issues</a>. Your insights help shape the next generation of scalable, open AI training tools.

Learn how NVIDIA Blackwell NVL72 runs 10x faster and delivers 1/10 the token cost for MoE models in this <a href="https://blogs.nvidia.com/blog/mixture-of-experts-frontier-models/" data-wpel-link="internal" rel="follow" target="_self">blog</a>.

</div>

<div class="card--post-attributes-secondary">

<div class="post--comments-count secondary--attribute">

[ Discuss (0)](#entry-content-comments)

</div>

<div class="post--rate secondary--attribute">

<div class="wpulike wpulike-heart">

<div class="wp_ulike_general_class wp_ulike_is_not_liked">

<span class="count-box wp_ulike_counter_up" ulike-counter-value="+17"></span>

</div>

</div>

Like

</div>

</div>

<div class="card--post-attributes-secondary tags">

<div class="caption">

## Tags

</div>

<div class="content-s post-tags--list mt-0">

<a href="https://developer.nvidia.com/blog/category/generative-ai/" data-wpel-link="internal" rel="follow" target="_self">Agentic AI / Generative AI</a> \| <a href="https://developer.nvidia.com/blog/recent-posts/?industry=General" data-wpel-link="internal" rel="follow" target="_self">General</a> \| <a href="https://developer.nvidia.com/blog/recent-posts/?products=NeMo" data-wpel-link="internal" rel="follow" target="_self">NeMo</a> \| <a href="https://developer.nvidia.com/blog/recent-posts/?learning_levels=Beginner+Technical" data-wpel-link="internal" rel="follow" target="_self">Beginner Technical</a> \| <a href="https://developer.nvidia.com/blog/tag/featured/" data-wpel-link="internal" rel="follow" target="_self">featured</a> \| <a href="https://developer.nvidia.com/blog/tag/llm-techniques/" data-wpel-link="internal" rel="follow" target="_self">LLM Techniques</a> \| <a href="https://developer.nvidia.com/blog/tag/large-language-models/" data-wpel-link="internal" rel="follow" target="_self">LLMs</a> \| <a href="https://developer.nvidia.com/blog/tag/mixture-of-experts-moe/" data-wpel-link="internal" rel="follow" target="_self">Mixture of Experts (MoE)</a> \| <a href="https://developer.nvidia.com/blog/tag/open-source/" data-wpel-link="internal" rel="follow" target="_self">Open Source</a> \| <a href="https://developer.nvidia.com/blog/tag/pytorch/" data-wpel-link="internal" rel="follow" target="_self">PyTorch</a> \| <a href="https://developer.nvidia.com/blog/tag/training-ai-models/" data-wpel-link="internal" rel="follow" target="_self">Training AI Models</a>

</div>

</div>

<div class="post-authors-list">

<div class="entry-content-author">

<div class="caption">

## About the Authors

</div>

<div class="media author-info">

<div class="author-media-left media-left">

<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/cropped-image3-131x131.png" class="avatar avatar-131 photo" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/cropped-image3-262x262.png 2x" width="131" height="131" alt="Avatar photo" />

<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E" class="lazyload avatar avatar-131 photo" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/cropped-image3-131x131.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/cropped-image3-262x262.png 2x" decoding="async" width="131" height="131" alt="Avatar photo" />

</div>

<div class="author-media-body media-body">

**About Hemil Desai**\
Hemil Desai is a senior software engineer at NVIDIA, where he focuses on building scalable, high-performance infrastructure for generative AI and large-scale models. His technology interests span deep learning systems, distributed training frameworks, and optimizing PyTorch workloads at GPU-scale. Hemil holds a master’s in computer science from University of California, Los Angeles and a bachelor’s in computer science from Purdue University.

<div id="author-link">

<a href="https://developer.nvidia.com/blog/author/hemildesai/" data-wpel-link="internal" rel="author follow" target="_self">View all posts by Hemil Desai<img src="data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9IjE2IiB2aWV3Ym94PSIwIDAgMzIwIDYxMiIgd2lkdGg9IjE2IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==" /></a>

</div>

</div>

</div>

<div class="media author-info">

<div class="author-media-left media-left">

<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2025/05/cropped-Bernard-Profile-131x131.png" class="avatar avatar-131 photo" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2025/05/cropped-Bernard-Profile-262x262.png 2x" width="131" height="131" alt="Avatar photo" />

<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E" class="lazyload avatar avatar-131 photo" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2025/05/cropped-Bernard-Profile-131x131.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2025/05/cropped-Bernard-Profile-262x262.png 2x" decoding="async" width="131" height="131" alt="Avatar photo" />

</div>

<div class="author-media-body media-body">

**About Bernard Nguyen**\
Bernard Nguyen is a deep learning engineering director at NVIDIA. He leads development of the NVIDIA NeMo Framework for GPU accelerated, distributed pre-training, and post-training of generative AI models from single GPU to thousand-node clusters. Previously, he led the development of PyTorch distributed and large-scale AI systems at Meta.

<div id="author-link">

<a href="https://developer.nvidia.com/blog/author/bernardn/" data-wpel-link="internal" rel="author follow" target="_self">View all posts by Bernard Nguyen<img src="data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9IjE2IiB2aWV3Ym94PSIwIDAgMzIwIDYxMiIgd2lkdGg9IjE2IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==" /></a>

</div>

</div>

</div>

<div class="media author-info">

<div class="author-media-left media-left">

<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/08/Wenwen-Headshot-131x131.jpg" class="avatar avatar-131 photo" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/08/Wenwen-Headshot-262x262.jpg 2x" width="131" height="131" alt="Wenwen Gao" />

<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E" class="lazyload avatar avatar-131 photo" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/08/Wenwen-Headshot-131x131.jpg" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/08/Wenwen-Headshot-262x262.jpg 2x" decoding="async" width="131" height="131" alt="Wenwen Gao" />

</div>

<div class="author-media-body media-body">

**About Wenwen Gao**\
Wenwen Gao is a senior product manager for NeMo at NVIDIA, focusing on LLM training framework and microservices. Her past experience include LLM inference (NIM) and recommender systems (Merlin). She holds a B.S. in computer science from the University of Toronto and an M.B.A. from the MIT Sloan School of Management.

<div id="author-link">

<a href="https://developer.nvidia.com/blog/author/wenweng/" data-wpel-link="internal" rel="author follow" target="_self">View all posts by Wenwen Gao<img src="data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9IjE2IiB2aWV3Ym94PSIwIDAgMzIwIDYxMiIgd2lkdGg9IjE2IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==" /></a>

</div>

</div>

</div>

<div class="media author-info">

<div class="author-media-left media-left">

<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2021/09/Gordana-Neskovic.jpg" class="avatar avatar-131 photo" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2021/09/Gordana-Neskovic.jpg 2x" width="131" height="131" alt="Avatar photo" />

<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E" class="lazyload avatar avatar-131 photo" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2021/09/Gordana-Neskovic.jpg" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2021/09/Gordana-Neskovic.jpg 2x" decoding="async" width="131" height="131" alt="Avatar photo" />

</div>

<div class="author-media-body media-body">

**About Gordana Neskovic**\
Gordana Neskovic is on the AI / DL product marketing team responsible for NVIDIA Maxine. Gordana has held various product marketing, data scientist, AI architect, and engineering roles at VMware, Wells Fargo, Pinterest, SFO-ITT, and KLA-Tencor before joining NVIDIA. She holds a Ph.D. from Santa Clara University and master’s and bachelor's degrees in electrical engineering from the University of Belgrade, Serbia.

<div id="author-link">

<a href="https://developer.nvidia.com/blog/author/gneskovic/" data-wpel-link="internal" rel="author follow" target="_self">View all posts by Gordana Neskovic<img src="data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9IjE2IiB2aWV3Ym94PSIwIDAgMzIwIDYxMiIgd2lkdGg9IjE2IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==" /></a>

</div>

</div>

</div>

</div>

</div>

<div id="entry-content-comments" class="entry-content-comments">

<div id="pf-disqus-thread" class="container">

<div id="respond" class="row">

<div class="col-md-12 related-posts-comments mb-0">

## Comments

</div>

</div>

<div class="row">

<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">

<div id="wpdc-comments" class="wpdc-comments-loading" post-id="108259">

</div>

</div>

</div>

</div>

</div>

<div id="main-content-end">

</div>

</div>
