#!/usr/bin/env python3
"""
Script kiểm tra toàn bộ môi trường, công cụ và chạy thử kiểm định 6 cổng
trên bộ hồ sơ giả lập mẫu (01_sample-ci-confinement-demo) trong GOOGLE_VRP_STARTER_KIT.
"""
import os
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

KIT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_cmd(name, args=["--version"]):
    path = shutil.which(name)
    if not path:
        print(f"[MISSING] '{name}' chưa được cài đặt hoặc chưa có trong PATH.")
        return False
    try:
        res = subprocess.run([path] + args, capture_output=True, text=True, timeout=10)
        first_line = (res.stdout or res.stderr).strip().splitlines()[0] if (res.stdout or res.stderr) else "OK"
        print(f"[OK]      {name:<12} -> {first_line}")
        return True
    except Exception as e:
        print(f"[WARN]    {name:<12} -> Lỗi khi chạy: {e}")
        return False


def check_python_pkg(pkg_name, import_name=None):
    import_name = import_name or pkg_name
    try:
        __import__(import_name)
        print(f"[OK]      Python pkg '{pkg_name}' đã cài đặt.")
        return True
    except ImportError:
        print(f"[MISSING] Python pkg '{pkg_name}' chưa cài. Chạy: pip install {pkg_name}")
        return False


def main():
    print("=" * 72)
    print("KIỂM TRA MÔI TRƯỜNG & CÔNG CỤ SĂN BUG GOOGLE OSS VRP")
    print("=" * 72)

    ok = True
    ok &= check_cmd("python")
    ok &= check_cmd("git")
    ok &= check_cmd("gh")
    check_cmd("zizmor")  # Optional static scanner

    ok &= check_python_pkg("requests")
    ok &= check_python_pkg("pyyaml", "yaml")

    print("-" * 72)
    print("KIỂM TRA XÁC THỰC GITHUB API (gh auth status):")
    gh_path = shutil.which("gh")
    if gh_path:
        res = subprocess.run([gh_path, "auth", "status"], capture_output=True, text=True)
        if res.returncode == 0:
            print("[OK]      GitHub CLI đã đăng nhập sẵn sàng.")
        else:
            print("[ACTION]  Chưa đăng nhập GitHub CLI. Hãy chạy: gh auth login")

    print("-" * 72)
    print("CHẠY THỬ KIỂM ĐỊNH 6 CỔNG TRÊN BỘ HỒ SƠ GIẢ LẬP MẪU (01_sample-ci-confinement-demo):")
    audit_script = os.path.join(KIT_ROOT, "04_QA_AND_MAIL_AUTOMATION", "audit_package.py")
    examples_dir = os.path.join(KIT_ROOT, "05_GOLD_STANDARD_EXAMPLES")
    if os.path.exists(audit_script) and os.path.exists(examples_dir):
        res = subprocess.run([sys.executable, audit_script, examples_dir], capture_output=True, text=True)
        print(res.stdout.strip())
        if res.returncode != 0:
            print(res.stderr.strip())
            ok = False
    else:
        print("[ERROR]   Không tìm thấy audit_package.py hoặc 05_GOLD_STANDARD_EXAMPLES.")
        ok = False

    print("=" * 72)
    if ok:
        print("KẾT LUẬN: MÔI TRƯỜNG ĐÃ SẴN SÀNG 100% ĐỂ BẮT ĐẦU SĂN BUG GOOGLE VRP!")
    else:
        print("KẾT LUẬN: Vui lòng cài đặt các mục báo [MISSING] ở trên trước khi bắt đầu.")
    print("=" * 72)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
