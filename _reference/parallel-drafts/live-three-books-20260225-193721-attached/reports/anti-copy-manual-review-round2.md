# Anti-Copy Manual Review (Round 2)

- Run ID: `live-three-books-20260225-193721-attached`
- Generated at: `2026-02-25T21:04:43`
- Method: near-duplicate + fuzzy matching against three-book cache

## Thresholds
- hard: ratio >= `0.86`
- soft: ratio >= `0.78` and LCS >= `28`
- candidate min shared tokens: `3`

## Overall
- pass: `16/16`
- review_needed: `0`
- cross_chapter_duplication_pairs: `0`
- review_needed_chapters: `none`

## Chapter Results
| chapter | status | suspicious_count | max_ratio | max_lcs_len |
|---|---:|---:|---:|---:|
| ch01-linear-systems-and-gauss.tex | pass | 0 | 0.0 | 0 |
| ch02-matrix-operations-invertibility-rank.tex | pass | 0 | 0.0 | 0 |
| ch03-vector-spaces-and-subspaces.tex | pass | 0 | 0.0 | 0 |
| ch04-basis-and-dimension.tex | pass | 0 | 0.0 | 0 |
| ch05-linear-maps-kernel-image.tex | pass | 0 | 0.0 | 0 |
| ch06-matrix-representation-and-similarity.tex | pass | 0 | 0.0 | 0 |
| ch07-dual-spaces-and-transpose.tex | pass | 0 | 0.0 | 0 |
| ch08-determinants.tex | pass | 0 | 0.0 | 0 |
| ch09-operator-polynomials.tex | pass | 0 | 0.0 | 0 |
| ch10-eigenvalues-and-diagonalization.tex | pass | 0 | 0.0 | 0 |
| ch11-invariant-subspaces-and-triangularization.tex | pass | 0 | 0.0 | 0 |
| ch12-primary-and-cyclic-decomposition.tex | pass | 0 | 0.0 | 0 |
| ch13-jordan-canonical-form.tex | pass | 0 | 0.0 | 0 |
| ch14-inner-product-and-orthogonalization.tex | pass | 0 | 0.0 | 0 |
| ch15-adjoint-normal-spectral.tex | pass | 0 | 0.0 | 0 |
| ch16-bilinear-hermitian-forms.tex | pass | 0 | 0.0 | 0 |

## Notes
- Round 2 checks near-duplicate risk using token-overlap candidate search + SequenceMatcher ratio + longest common substring.
- False positives can occur on canonical theorem statements or standard mathematical vocabulary.
