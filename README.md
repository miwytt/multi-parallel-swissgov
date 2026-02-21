# SwissGov-Multiparallel

This repository contains a subset of the SwissGov-RSD dataset ([Wastl et al., 2025](https://www.arxiv.org/abs/2512.07538)) optimized for translation (evaluation) purposes in a multiparallel way between English, French, German, and Italian. 

## Source Data

SwissGov-RSD is a human-annotated, document-level, cross-lingual dataset collected from the Swiss government portal admin.ch, which publishes content in parallel across German, French, Italian, and English (as well as Romansh to some extent). The full dataset comprises 224 multi-parallel documents annotated with token-level semantic differences on a five-point scale across three language pairs (EN-DE, EN-FR, EN-IT). Annotations distinguish between bilateral differences (spans labeled on both sides) and asymmetric differences (omissions or additions labeled on one side only). Find the original repo [here](https://github.com/ZurichNLP/SwissGov-RSD).

## Parallel Dataset Construction

### 1. Scoring Documents by Semantic Difference

To identify the cleanest translation pairs, each document is assigned a difference score that aggregates its token-level annotations into a single normalized value. The score is computed as follows.

**Weighted token counts.** Annotated tokens are grouped by their label value. Since the label range is `[0.2, 0.4, 0.6, 0.8, 1.0]`, each group receives a severity weight from 1 to 5 respectively. Label 1.0 is additionally doubled, since asymmetric annotations (omissions/additions) are only labeled on one side — doubling normalizes them to be comparable with bilateral labels which are counted on both sides. This gives effective per-label weights of 1, 2, 3, 4, and 10.

**Aggregation.** The weighted counts across all label groups are summed into a single raw difference score per document.

**Length normalization.** The raw score is divided by the document length in tokens (measured on the English and other language side combined) to make scores comparable across documents of varying length.

**Averaging across languages.** Since every English file is paired with another language 3 times in the original SwissGov-RSD dataset, the difference scores for each pair are averaged to a single cross-lingual difference score.

The resulting score distribution:

<img width="1489" height="490" alt="image" src="https://github.com/user-attachments/assets/3e9c8546-a49f-4370-a80e-afb07b002e77" />


### 2. Filtering by Difference Score

Document-quadruples are ranked by their difference score and filtered based on a threshold determined by manual inspection. Candidate thresholds were identified from the score distribution above: the steep elbow region (~0.4–0.5), a mid-range region (~0.1–0.2), the near-zero tail (~0.0), as well as the top outliers (~1.0). Documents sampled from just below each candidate threshold were inspected manually to calibrate what score levels correspond to in terms of actual crosslingual correspondence resulting in the following observations:

* ~0.0: effectively equivalent texts
* ~0.1–0.2: small phrasing differences, minor explicitations
* ~0.4–0.5: (the elbow region): a mix of meaningful omissions and heavy reformulations
* \>1.0 (the top outliers): almost certainly major structural divergences, whole paragraphs missing or completely rewritten

Based on these observations we split the dataset according to two cutoff points into the following three multiparallel datasets:

* (filename) <0.2: small phrasing differences, minor explicitations
* (filename) <0.5: (the elbow region): a mix of meaningful omissions and heavy reformulations, including the same small phrasing differences, minor explicitations as above
* (filename) full dataset: almost certainly major structural divergences, whole paragraphs missing or completely rewritten, including the same mix of meaningful omissions and heavy reformulations as well as the small phrasing differences and minor explicitations as above

## Citation

If you use this dataset, please cite the original SwissGov-RSD paper:
```bibtex
@misc{wastl2025swissgovrsdhumanannotatedcrosslingualbenchmark,
      title={SwissGov-RSD: A Human-annotated, Cross-lingual Benchmark for Token-level Recognition of Semantic Differences Between Related Documents}, 
      author={Michelle Wastl and Jannis Vamvas and Rico Sennrich},
      year={2025},
      eprint={2512.07538},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2512.07538}, 
}
```
