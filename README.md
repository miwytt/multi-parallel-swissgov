# SwissGov for document-level translation evaluation

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

Document-quadruples are ranked by their difference score and filtered based on a threshold determined by manual inspection. Documents were manually inspected from lowest difference score in ascending order to determine the threshold after which the documents are considered semantically and structurally too different to be included as strictly multi-parallel document quadruples. Obseravations from documents below the threshold reveal the following:

TODO: adjust descriptions
* ~0.0: effectively equivalent texts
* ~0.1–0.2: small phrasing differences, minor explicitations
* ~-0.5: a mix of meaningful omissions and heavy reformulations
* \>0.5: almost certainly major structural divergences, whole paragraphs missing or completely rewritten

### 2. Benchmarking Machine Translation Systems
TODO
- apertus v1
- Tower
- Shy
- translategemma

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



