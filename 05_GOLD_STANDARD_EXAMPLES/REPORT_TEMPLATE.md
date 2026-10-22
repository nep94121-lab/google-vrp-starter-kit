# Mẫu Báo Cáo Lỗi Chuẩn Google OSS VRP (Supply Chain / GitHub Actions)

> **Nơi nộp:** https://bughunters.google.com/report (Chọn mục **Open Source Software VRP** -> **Supply Chain Compromise**)

---

## 1. Title (Tiêu đề)
`[Supply Chain / GitHub Actions] <Loại lỗi: Pwn Request / Command Injection> in <org>/<repo> (<tên-file>.yml) allows <Tác động: repository write access / secret exfiltration>`

## 2. Target Repository & File (Mục tiêu)
- **Organization / Repository:** `https://github.com/<org>/<repo>`
- **Workflow File:** `https://github.com/<org>/<repo>/blob/<branch>/.github/workflows/<file>.yml#L<start>-L<end>`
- **Trigger Event:** `<pull_request_target / workflow_run / issue_comment / pull_request>`
- **Token Permissions / Secrets Exposed:** `<write-all / contents: write / NPM_TOKEN / PYPI_TOKEN>`

## 3. Vulnerability Summary (Tóm tắt kỹ thuật)
The GitHub Actions workflow `<file>.yml` in `<org>/<repo>` is triggered by `<trigger>`, which runs in the context of the base repository with access to `<permissions/secrets>`.

At lines `<Lxx-Lyy>`, the workflow `<checks out untrusted code from the pull request head / interpolates untrusted user input ${{ ... }} directly into a shell script>` and subsequently executes `<command>`.

## 4. Steps to Reproduce / Proof of Concept (Các bước tái hiện an toàn - KHÔNG khai thác phá hoại)
*(Lưu ý: Tuyệt đối không gửi PR chứa mã độc lên repo thật của Google! Hãy fork repo về tài khoản cá nhân của bạn và chạy thử trên repo fork để chụp màn hình/log chứng minh).*

1. Inspect the workflow file at `https://github.com/<org>/<repo>/blob/main/.github/workflows/<file>.yml`.
2. Observe the trigger configuration on line `<X>`:
   ```yaml
   on:
     pull_request_target:
   ```
3. Observe the unsafe operation on line `<Y>`:
   ```yaml
   # Đoạn code lỗi
   ```
4. **Safe Verification on a Personal Fork:**
   - Fork `<org>/<repo>` to a private/personal test account.
   - Open a test Pull Request on the personal fork modifying `<file/title>`.
   - Observe in the GitHub Actions run log on the personal fork that arbitrary commands execute with `GITHUB_TOKEN` write permissions (see attached screenshot/log).

## 5. Attack Scenario & Impact (Kịch bản tấn công & Tác động)
An external attacker can open a Pull Request (or post a comment/issue) containing a crafted payload. When the workflow triggers automatically:
- The attacker gains arbitrary code execution inside the GitHub Actions runner.
- The attacker can exfiltrate `<SECRETS>` or use the privileged `GITHUB_TOKEN` (`contents: write`) to push malicious commits directly to the repository or publish compromised packages to `<PyPI/NPM/Maven>`.
