# example-org/sample-repo: Unvalidated artifact input written to GITHUB_OUTPUT in `.github/workflows/ci.yml` (SYNTHETIC DEMO)

## Summary
This is a **100% synthetic demonstration package** included in `GOOGLE_VRP_STARTER_KIT` to verify the 6 mechanical QA gates (`audit_package.py`) without exposing any live vulnerability reports.

1. The workflow reads `pr_number.txt` from an untrusted artifact without numeric validation.
2. Writing multi-line content into `$GITHUB_OUTPUT` allows output key injection.

## Affected Files
- Repository: `example-org/sample-repo` (Synthetic Example)
- Commit SHA: `0123456789abcdef0123456789abcdef01234567`
- File: [`.github/workflows/ci.yml`](https://github.com/example-org/sample-repo/blob/0123456789abcdef0123456789abcdef01234567/.github/workflows/ci.yml#L1-L14)

## Technical Details
```yaml
name: CI Check
on:
  workflow_run:
    workflows: ["PR Build"]
    types: [completed]
jobs:
  comment:
    runs-on: ubuntu-latest
    steps:
      - name: Read PR number
        run: |
          PR_NUM=$(cat pr_number.txt)
          echo "pr=$PR_NUM" >> "$GITHUB_OUTPUT"
```

## Verification Evidence
See `evidence/sample_checks.json` inside `sample-ci-confinement-demo.zip`.

## Impact
If a downstream step consumes the injected output key in a privileged context, an attacker can alter control flow.

## Suggested Fix
Validate that `PR_NUM` is strictly numeric before writing to `$GITHUB_OUTPUT`:

```diff
diff --git a/workflows/.github/workflows/ci.yml b/workflows/.github/workflows/ci.yml
index e69de29..b6fc4c6 100644
--- a/workflows/.github/workflows/ci.yml
+++ b/workflows/.github/workflows/ci.yml
@@ -10,4 +10,7 @@ jobs:
       - name: Read PR number
         run: |
           PR_NUM=$(cat pr_number.txt)
+          if ! [[ "$PR_NUM" =~ ^[0-9]+$ ]]; then
+            exit 1
+          fi
           echo "pr=$PR_NUM" >> "$GITHUB_OUTPUT"
```
