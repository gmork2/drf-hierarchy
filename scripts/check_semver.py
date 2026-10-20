import argparse
import os
import re
import sys
from pathlib import Path

import tomllib

SEMVER_CORE_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def load_project_version(pyproject_path: Path) -> str:
    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]


def ensure_core_semver(version: str) -> None:
    if not SEMVER_CORE_RE.match(version):
        raise ValueError(
            f"project.version must use SemVer core format X.Y.Z. Got: {version!r}"
        )


def parse_release_tag(tag: str) -> str:
    if not tag:
        raise ValueError("Release tag is empty.")
    if not tag.startswith("v"):
        raise ValueError(f"Release tag must start with 'v'. Got: {tag!r}")
    version = tag[1:]
    if not SEMVER_CORE_RE.match(version):
        raise ValueError(
            f"Release tag must match vX.Y.Z with SemVer core numbers. Got: {tag!r}"
        )
    return version


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SemVer usage.")
    parser.add_argument("--pyproject", default="pyproject.toml")
    parser.add_argument("--tag", default=os.environ.get("GITHUB_REF_NAME", ""))
    parser.add_argument("--check-tag-match", action="store_true")
    args = parser.parse_args()

    project_version = load_project_version(Path(args.pyproject))
    ensure_core_semver(project_version)
    print(f"project.version uses SemVer core: {project_version}")

    if args.check_tag_match:
        tag_version = parse_release_tag(args.tag)
        if project_version != tag_version:
            raise ValueError(
                "Release tag and project.version mismatch: "
                f"tag={tag_version!r}, project.version={project_version!r}"
            )
        print(f"Release tag matches project.version: v{project_version}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
