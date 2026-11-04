# Our paper
## Define what is true long context ability?
1. Models should have similar performance or the same behavior for short and long context tasks. 
2. Models should first compare to the short counterpart of itself rather than compare to other models because we don't know other model's short context ability. e.g. A (4k 90%) (32k 75%) B (4k 70%) (32k 70%), then we say B has better long context ability than A.  delta performance 


## What is the problem of current long context evaluation? (PPL, ZeroScrolls, LongBench, L-Eval, etc.)
### Evaluation with PPL
* Many previous works on long text modeling rely on the perplexity metric for evaluation. However, as suggested in Sun et al. (2021), the perplexity metric may not necessarily reflect the
model’s performance on sequence-level tasks in real applications. PPL doesn't measure whether model has the ability of retrieval and reasoning for long context.


### Evaluation with Synthetic Data
* Too easy to get 100% accuracy (passkey and needle in the haystack.)
* Only test retrieval ability.

  
### Evaluation with Real Data
* Existing benchmarks may not include golden information in the context due to truncation or retrieval.
* Existing benchmarks doesn't represent the long context ability of model since the improvement of short context to long context may because of more context information.
<!-- * Existing benchmarks doesn't know the upper bound performance (e.g. 4k). For example, we don't we should focus on the 4k model or the context extension methods. -->
* Existing benchmarks only evaluate models with long context tasks without short context counterpart to show context extension ability. They are mainly used to compare different models in the same tasks but not measure long context ability of the model itself. For example, if we compare all models on 32k ZeroScrolls, we can see some models have better performance. However, we don't know the performance is coming from a good short context model or better context extension data or method. People only care about the final performance of long context benchmark and ignore the core thing is how to evaluate context extension methods.
* Hard to find extremely long data
* parametric knowledge (no context baseline) real long context task input source: project gutenburg , wikipedia, arixv paper quality (pretrianing data) confounding factor


## Proposed evaluation direction
1. For the first direction, we should have a fixed short context model to evaluate under 4k as a upper bound performance, and then we use any kind of data or methods to extend to 32k and see whether the performance is the same as 4k. This direction can help us truly understand how we can extend our model context.
* LLama2-7b (base)
    * LWM_Text_1M_vllm (RingAttention + ABF)
    * Yukang_Llama-2-7b-longlora-100k-ft (LongLoRA + PI)
    * togethercomputer_Llama-2-7B-32K (PI)
    * NousResearch_Yarn-Llama-2-7b-128k (Yarn)
    * hyen/CEPE-LLaMA-2-7B (Enc-Dec)
  
2. For the second direction, since most existing research use their own short context model and many models we only have its long context version, we propose to evaluate these models' 4k and 32k performance. If 4k and 32k performance are comparable, then we claim the model has the long context ability.

## Why do we need synthetic tasks?
1. It is easy to scale the context length.
2. It is guaranteed that the golden information is always in the context, so we can test retrieval.
3. Without parametric knowledge.
4. It is easy to split out different task difficulties to analyze long context ability. Passkey and Needle is not enough (in Gemini 1.5 pro).

## What are the existing popular synthetic tasks?
Passkey retrieval (LandMark Attention, PI, InfiniteBench)
Needle in the haystack 
Multiple Needle in the haystack (Gemini 1.5)
Line retrieval (LongEval, InfiniteBench)
Topic retrieval (LongEval)
KV retrieval (Lostmiddle, InfiniteBench)

## What is the main contribution of our paper?
1. Test retrieval synthetic tasks with different difficulties.
### Change distraction
1-a. Retrieval with single synthetic short key value information and synthetic repetitive distraction. (passkey)
1-b. Retrieval with single synthetic short key value information and distraction in the same format. (line retrieval)
1-c. Retrieval with single synthetic short key value information and distraction from books. (passkey book,  needle in the haystack)

### Change key value amounts
1-d. Retrieval with multiple synthetic short key value information and distraction from books. (multiple needle in the haystack)

### Change value amounts
1-d. Retrieval with multiple synthetic short key value information and distraction from books. (multiple needle in the haystack)

### Change key value length
1-e. Retrieval with single synthetic long key value information and distraction in the same format (KV retrieval)

### Change to real world key value
1-f. Retrieval with single real short key value information and distraction from books. (next word).
1-g. Retrieval with single real long key value information and distraction from books. (line book).

### Change to aggregate task
1-h. Retrieval and aggregate with multiple synthetic key information and distraction in the same format. (few-shot commonword)

### Change to multihop task
1-i. Retrieval with multiple hop key information.

2. Test QA synthetic tasks.
2-a. SQuAD (single QA)
2-b. MuSiQue (multi QA)
2-c. hotpotqa (multi QA)
2-d. 2wikimultihop (multi QA)


### Experiments we need additionally
1. Test current CPT methods with fixed base 4k model (PI/ABF/Yarn/LongRoPE)
Showing which one is the best CPT receipe instead of just evaluating PPL.



### Findings
* 4k may get poor response because of Guardrails
```
I'm just an AI, I cannot provide you with the special magic number for rabid-serial as it is not a real number. The provided text is a joke and does not contain any real information.
```

```
I'm sorry, but there is no special magic number mentioned in the provided text related to "educated-wedge." The text only repeats the statements "The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again." multiple times.
```

* Add short to mimic long evaluation results from Sam and Dima.