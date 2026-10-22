# Policy sources and evidence review

## Primary sources

Read current pages, follow official redirects, and record the date. Rules can change; this skill is not a frozen policy copy.

- [Google OSS VRP rules](https://bughunters.google.com/about/rules/open-source/google-open-source-software-vulnerability-reward-program-rules)
- [OSS VRP rule updates, March 19 2026, including April update](https://bughunters.google.com/blog/ossvrp-rule-updates-2026)
- [Updated Report Quality Framework, September 22 2025](https://bughunters.google.com/blog/level-up-your-reports-introducing-our-updated-report-quality-framework)
- [Program routing overview](https://bughunters.google.com/about/rules/about-this-section)
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [GitHub workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [GitHub security guidance](https://docs.github.com/en/actions/reference/security/secure-use)
- [Python urllib.parse.urljoin](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urljoin)

Read [the dated Vietnamese policy digest](google-rules-snapshot.vi.md) and [source provenance](policy-sources.json). Refresh the linked official sources for each new eligibility decision. The digest is a summary, not a full mirror or a permanent policy guarantee.

The remaining sections are internal audit guidance, not additional Google eligibility rules.

## Internal package QA

| Check | Evidence | What it does not prove |
|---|---|---|
| README outside/inside ZIP | Same exact bytes and SHA-256 | Vulnerability correctness |
| Encoding/newlines | BOM, LF, CRLF, byte counts | LF is a Google acceptance rule |
| Source fidelity | Fetch immutable 40-hex commit raw source; compare bytes | Current deploy configuration |
| Excerpts/citations | Exact code/comments and matching cited source lines | Reachable attack path |
| Patch consistency | README diff matches patch; scratch `git apply --check` | Secure or compatible behavior |
| Runtime evidence | Exact event, run/job/step, artifact source, approval state | Secret value or unauthorized impact |

If upstream uses CRLF or includes emoji/license headers, preserve its original bytes. Record differences instead of normalizing source to satisfy an internal preference. Scan collector markers without deleting authentic metadata. A patch may legitimately omit environment secret provisioning or IAM changes if those administrative steps are explicitly documented as outside the source patch.

## Security claim contract

For each claimed outcome record: attacker role and exact controllable fields; event and immutable workflow version; existing approval/label/reviewer checks; transformation and sink; actual job token and permissions; affected asset; reproducer or passive evidence; unresolved assumptions. Keep a separate hypothesis when any dependency is unknown.

- `pull_request` and `pull_request_target` execute different workflow/ref contexts. Check documentation and actual run metadata before saying a PR can or cannot edit the executing workflow. A permission-declining action may exit successfully; subsequent steps need their own authorization condition. `author_association` does not establish write permission.
- GitHub-hosted and self-hosted/custom labels are not interchangeable. Secrets in a later job do not leak into a prior job. Host authentication does not establish guest VM/container access. An exploit verification service may intentionally run attacker code; the report must show escape from its intended trust boundary.
- A `workflow_run` job may access privileged resources, but check the upstream event and success, actual artifact producer, association to the triggering run, and any approvals. Artifact producer code can rewrite metadata after tests; runner `event.json` can be refreshed between steps. Show the submitted bytes reach the consumer, rather than assume an early write persists.
- `GITHUB_ENV`/`GITHUB_OUTPUT` writes are data sinks. Trace resulting variables/outputs into commands, checkout targets or privileged APIs. `$()` text stored in a variable is not recursively evaluated as shell code merely by later expansion. Word splitting and option injection require a concrete affected command and valid option behavior.
- Secret references and auth actions demonstrate configured access paths, not that secrets were non-empty, read, exfiltrated, or authorized for every actor. Public successful job/step data can disprove a guessed permission blocker. Do not assert runtime denial solely because `actions: read` is absent if successful same-source runs exist.
- A real run's `head_branch: main` describes the downstream workflow context; it does not alone prove the checked-out code came from a fork or identify the triggering run. Bind provenance with payload/artifact/job data where available. Correlated actor and timestamps are supporting evidence, not definitive linkage.
- LLM tool availability is not prompt-injection success. Show reachability, permitted tools, token scopes, deterministic boundary failure and unauthorized outcome. A GraphQL node prefix does not bind the current discussion or repository. A `urljoin` override can affect returned links without demonstrating an HTTP request or credential leak.
- When validating paths, inspect resolved symlinks, alternate roots, `.git` files/worktrees, local Git configuration and hooks. New hooks may require executable permission; a file write alone does not establish hook execution.

## Remediation review

Check supported events (`push`, `merge_group`, PR events, dispatch and reusable calls), skipped/failed dependencies, required status aggregators, and secrets scope. A static gate copied into all jobs can add approvals to trusted CI; splitting branches requires updating aggregate `needs` and result selection. Do not demand duplicated jobs if a supported, verified expression solves the problem. Uncertainty about an empty environment name calls for validation or a supported alternative, not a claim of confirmed invalid syntax.

Label-only gates change auto-update and dispatch behavior. Approvals should bind the actual code revision; consider stale labels after `synchronize`. Fetching authentic PR metadata does not make attacker-selected branch names safe for downstream baseline keys. Quote arguments, use `--` where supported, bind PR IDs to the triggering repository/run, and evaluate how ordinary successful users are affected.

## Evidence levels and verdicts

- **Verified:** Exact inspected source or observed safe local/passive result supports the precise claim.
- **Conditional:** A real path depends on an explicitly unknown secret, IAM scope, permission, model behavior or artifact control condition.
- **Contradicted:** The inspected source/runtime evidence opposes the statement; cite the counterexample.
- **Unverified:** Required data could not be retrieved or the step was not checked.

Readiness combines these independent results. All package checks passing is never a 100% Google acceptance verdict. Offer the minimal supported revision and evidence needed to resolve each blocker; do not repeatedly expand the checklist without a demonstrated reason.
