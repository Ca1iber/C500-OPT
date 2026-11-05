# Restart submission SOTA promotion contract

## Invariant

Treat `race_tests/moe/restart-submission/` as the promotion history of globally best, OJ-verified submissions. Its performance must be monotonic across every official OJ case. It is not a candidate archive and it is not a record of versions that merely beat their direct parent.

Archive every named experiment in the four evidence roots. A local improvement, a recovery from a regressed parent, or an OJ-correct candidate remains an experiment until it defeats the incumbent SOTA under the gate below.

## Resolve the incumbent before each experiment

Read `race_tests/moe/restart-submission/SOTA.json`. Record its iteration ID, submission SHA-256, OJ metric, per-case score vector, and evidence source in the new experiment manifest before changing code. If the registry is missing or inconsistent, reconstruct it only from OJ-verified evidence; never infer SOTA from the latest version number, latest commit, branch parent, local benchmark, or profiler result. Stop promotion work until the incumbent is unambiguous.

## Stage candidates outside restart-submission

Build the self-contained OJ candidate under `/tmp` or `restart-experiments/<id>/candidate_submission.py`. Run import validation, correctness, official benchmark, exact local OJ benchmark, and the external OJ submission from that exact SHA-256. Do not create `restart-submission/<id>/` while OJ results are missing or pending.

## Monotonic promotion gate

Promote only when all conditions hold:

1. Incumbent and candidate use the same official OJ cases and score definition.
2. The exact candidate SHA-256 passes import validation and correctness.
3. Every official OJ case has a numeric incumbent and candidate result.
4. Candidate performance is non-regressing in every case.
5. Candidate performance is strictly better in at least one case.

For a higher-is-better score, require `candidate >= incumbent` in every case and `candidate > incumbent` in at least one. For a lower-is-better metric such as latency, reverse the inequalities. If a case regresses, the candidate is not SOTA even when total score, a different case, a local benchmark, or a profiler metric improves. If complete comparable OJ results are unavailable, use `inconclusive`; correctness-only OJ success is not performance evidence.

OJ results outrank local timings for promotion. A local winner that loses on OJ must be rejected as a SOTA candidate and must not receive a submission directory.

## Promotion transaction

After the gate passes:

1. Create `restart-submission/<id>/` from the exact OJ-tested bytes.
2. Save import validation and `submission.sha256`.
3. Add this object to the evidence manifest:

```json
{
  "status": "accepted",
  "sota_gate": {
    "authority": "oj-platform",
    "incumbent_id": "vNNN_...",
    "incumbent_submission_sha256": "...",
    "candidate_submission_sha256": "...",
    "metric": "display_score",
    "higher_is_better": true,
    "official_case_count": 3,
    "cases": [
      {"case": 1, "incumbent": 0, "candidate": 0},
      {"case": 2, "incumbent": 0, "candidate": 0},
      {"case": 3, "incumbent": 0, "candidate": 0}
    ],
    "all_cases_non_regressing": true,
    "at_least_one_case_improved": true
  }
}
```

4. Update `restart-submission/SOTA.json` to the candidate ID, hash, metric, and exact score vector.
5. Run strict iteration validation and commit the four evidence directories, submission directory, and SOTA registry atomically with `opt(moe)`.

Do not create a new submission directory containing a copy of the old incumbent merely to close an experiment. Rejected, failed, inconclusive, local-only, and OJ-pending versions use only the four evidence directories and `exp(moe)`.
