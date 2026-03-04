# Anti-Copy Manual Review (Round 1)

- Run ID: `live-three-books-20260225-193721-attached`
- Generated at: `2026-02-25T20:47:39`
- Scope: `ch01-ch16`

## Checklist
- C1: No visible source tags (출처/참고문헌/Ref./References) in chapter body
- C2: No visible citation command or footnote command (\cite, \footnote)
- C3: No long contiguous English sequence (10+ and 18+ words)
- C4: No exact sentence substring match (len>=35) against three-book caches
- C5: No 9-gram token overlap hit against three-book caches
- C6: Manual spot check of intro + first theorem + proof strategy + interpretation anchors

## Overall
- pass: `16/16`
- review_needed: `0`
- review_needed_chapters: `none`

## Chapter Results
| chapter | status | exact_sentence_matches | ngram_hits | strategy_anchor | interpretation_anchor |
|---|---:|---:|---:|---:|---:|
| ch01-linear-systems-and-gauss.tex | pass | 0 | 0 | 24 | 53 |
| ch02-matrix-operations-invertibility-rank.tex | pass | 0 | 0 | 46 | 104 |
| ch03-vector-spaces-and-subspaces.tex | pass | 0 | 0 | 44 | 69 |
| ch04-basis-and-dimension.tex | pass | 0 | 0 | 25 | 50 |
| ch05-linear-maps-kernel-image.tex | pass | 0 | 0 | 32 | 63 |
| ch06-matrix-representation-and-similarity.tex | pass | 0 | 0 | 47 | 71 |
| ch07-dual-spaces-and-transpose.tex | pass | 0 | 0 | 27 | 65 |
| ch08-determinants.tex | pass | 0 | 0 | 32 | 64 |
| ch09-operator-polynomials.tex | pass | 0 | 0 | 36 | 66 |
| ch10-eigenvalues-and-diagonalization.tex | pass | 0 | 0 | 37 | 60 |
| ch11-invariant-subspaces-and-triangularization.tex | pass | 0 | 0 | 38 | 74 |
| ch12-primary-and-cyclic-decomposition.tex | pass | 0 | 0 | 40 | 75 |
| ch13-jordan-canonical-form.tex | pass | 0 | 0 | 37 | 53 |
| ch14-inner-product-and-orthogonalization.tex | pass | 0 | 0 | 38 | 80 |
| ch15-adjoint-normal-spectral.tex | pass | 0 | 0 | 16 | 60 |
| ch16-bilinear-hermitian-forms.tex | pass | 0 | 0 | 29 | 50 |

## Residual Risk
- Common mathematical terminology and canonical formulas can naturally overlap across textbooks.
- This first pass focuses on direct copy-risk signals, not semantic similarity beyond exact/near-exact patterns.
