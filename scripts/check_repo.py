#!/usr/bin/env python3
"""Dependency-free smoke checks for the public repository."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATED_LINK_FILE = ROOT / "project-template" / "STATUS.md"
REQUIRED = [
    "README.md",
    "QUICKSTART.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    "00-orchestrator/SKILL.md",
    "07-polish/SKILL.md",
]
STALE_TEXT = {
    "Я найду 200 реальных отзывов": "stale review-count promise",
    "component-library-choice.md": "conflicting artifact name",
    "git clone <этот репозиторий>": "non-runnable clone command",
    "данные стабилизировались": "unsupported review-saturation claim",
    "data stabilized": "unsupported review-saturation claim",
}
SECRET_PATTERNS = {
    "private key": re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    "Anthropic key": re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}"),
    "Stripe secret key": re.compile(r"\bsk_(?:live|test)_[A-Za-z0-9]{16,}"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{16,}"),
    "Google API key": re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "JWT": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    "Google service account": re.compile(r'"client_email"\s*:\s*"[^"]+\.gserviceaccount\.com"'),
}


def tracked_files() -> list[Path]:
    output = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        text=True,
    )
    return [ROOT / line for line in output.splitlines() if line]


def markdown_files() -> list[Path]:
    return [path for path in tracked_files() if path.suffix.lower() == ".md"]


def check_required(errors: list[str]) -> None:
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")


def check_skills(errors: list[str]) -> None:
    for skill in sorted(ROOT.glob("*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            errors.append(f"invalid frontmatter delimiters: {skill.relative_to(ROOT)}")
            continue
        frontmatter = text.split("---", 2)[1]
        for field in ("name:", "description:"):
            if not re.search(rf"(?m)^{re.escape(field)}\s*\S", frontmatter):
                errors.append(f"missing {field[:-1]}: {skill.relative_to(ROOT)}")


def check_links(errors: list[str]) -> None:
    link_re = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for path in markdown_files():
        if path == GENERATED_LINK_FILE:
            continue
        text = path.read_text(encoding="utf-8")
        for match in link_re.finditer(text):
            target = match.group(1).split("#", 1)[0]
            if not target or "://" in target or target.startswith(("#", "mailto:")):
                continue
            if not (path.parent / target).exists():
                line = text.count("\n", 0, match.start()) + 1
                errors.append(
                    f"broken local link: {path.relative_to(ROOT)}:{line} -> {target}"
                )


def check_content(errors: list[str]) -> None:
    for path in tracked_files():
        if not path.is_file() or path.stat().st_size > 2_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(ROOT)
        if relative != Path(__file__).resolve().relative_to(ROOT):
            for needle, label in STALE_TEXT.items():
                if needle in text:
                    errors.append(f"{label}: {relative}")
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    errors.append(f"possible {label}: {relative}")


def check_install_layout(errors: list[str]) -> None:
    if not os.access(ROOT / "install.sh", os.X_OK):
        errors.append("install.sh is not executable")
        return

    with tempfile.TemporaryDirectory(prefix="landing-pipeline-check-") as tmp:
        base = Path(tmp)
        dest = base / "skills"
        backups = base / "backups"
        env = os.environ.copy()
        env["LANDING_SKILLS_DIR"] = str(dest)
        env["LANDING_PIPELINE_BACKUP_DIR"] = str(backups)
        for args in (["bash", "install.sh"], ["bash", "install.sh", "--force"]):
            result = subprocess.run(
                args,
                cwd=ROOT,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            if result.returncode:
                errors.append(f"installer failed ({' '.join(args)}): {result.stdout.strip()}")
                return

        expected = [
            "landing-pipeline/SKILL.md",
            "landing-pipeline/project-template/STATUS.md",
            "landing-pipeline/DEPLOY.md",
            "landing-reviews-parser/SECURITY.md",
            "landing-synthetic-custdev/03-synthetic-custdev.md",
            "landing-generation/LANDING-RULES.md",
            "landing-generation/DEPLOY.md",
            "landing-polish/multilingual-single-file.md",
        ]
        for relative in expected:
            if not (dest / relative).is_file():
                errors.append(f"installed layout missing: {relative}")
        if (dest / ".landing-pipeline-backups").exists():
            errors.append("installer placed backups inside skill discovery root")
        if len([path for path in backups.iterdir() if path.is_dir()]) != 1:
            errors.append("force install did not create one external backup")


def main() -> int:
    errors: list[str] = []
    check_required(errors)
    check_skills(errors)
    check_links(errors)
    check_content(errors)
    check_install_layout(errors)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK: basic repository and isolated-install checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
