#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT_TOML = PROJECT_ROOT / "pyproject.toml"

def run_command(cmd, cwd=PROJECT_ROOT, dry_run=False):
    """Runs a shell command."""
    print(f"Running: {cmd}")
    if not dry_run:
        subprocess.check_call(cmd, shell=True, cwd=cwd)

def get_current_version():
    """Reads the version from pyproject.toml."""
    content = PYPROJECT_TOML.read_text()
    match = re.search(r'^version\s*=\s*"(.*?)"', content, re.MULTILINE)
    if not match:
        print("Error: Could not find version in pyproject.toml")
        sys.exit(1)
    return match.group(1)

def update_version(new_version):
    """Updates the version in pyproject.toml."""
    content = PYPROJECT_TOML.read_text()
    new_content = re.sub(r'^version\s*=\s*".*?"', f'version = "{new_version}"', content, count=1, flags=re.MULTILINE)
    PYPROJECT_TOML.write_text(new_content)
    print(f"Updated pyproject.toml to version {new_version}")

def bump_version(current_version, new_version_arg=None):
    """Interactively asks for new version or uses provided argument."""
    print(f"Current version: {current_version}")
    parts = [int(x) for x in current_version.split('.')]
    next_patch = f"{parts[0]}.{parts[1]}.{parts[2] + 1}"
    
    if new_version_arg:
        new_version = new_version_arg
    else:
        new_version = input(f"Enter new version [{next_patch}]: ").strip()
    
    if not new_version:
        new_version = next_patch
    
    return new_version

def main():
    parser = argparse.ArgumentParser(description="Release script for cwe-tree")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing them")
    parser.add_argument("--version", help="Specify the new version number (non-interactive)")
    args = parser.parse_args()

    # 1. Check prerequisites
    # Ensure git is clean
    if not args.dry_run:
        status = subprocess.check_output("git status --porcelain", shell=True, cwd=PROJECT_ROOT).decode().strip()
        if status:
            print("Error: Git working directory is not clean. Please commit or stash changes.")
            sys.exit(1)

    # 2. Bump version
    current_version = get_current_version()
    new_version = bump_version(current_version, args.version)
    
    if not args.dry_run:
        update_version(new_version)
    else:
        print(f"[Dry Run] Would update pyproject.toml to {new_version}")

    # 3. Build
    clean_cmd = "rm -rf dist/"
    
    # Check if 'uv' is available
    has_uv = False
    try:
        subprocess.check_call("uv --version", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        has_uv = True
    except subprocess.CalledProcessError:
        pass

    if has_uv:
        print("Using 'uv' for build and upload...")
        build_cmd = "uv run --with build python -m build"
        upload_cmd = "uv run --with twine twine upload dist/*"
    else:
        print("Using standard python for build and upload...")
        build_cmd = "python3 -m build"
        upload_cmd = "twine upload dist/*"
    
    run_command(clean_cmd, dry_run=args.dry_run)
    run_command(build_cmd, dry_run=args.dry_run)

    # 4. Upload
    if not args.dry_run:
        # Ask for confirmation
        if input(f"Ready to upload version {new_version} to PyPI? [y/N] ").lower() != 'y':
            print("Aborting upload.")
            sys.exit(0)

    run_command(upload_cmd, dry_run=args.dry_run)

    # 5. Git Tag & Push
    git_commit_cmd = f"git commit -am 'Release v{new_version}'"
    git_tag_cmd = f"git tag v{new_version}"
    git_push_cmd = "git push && git push --tags"

    if not args.dry_run:
        # Check if there are changes to commit
        status = subprocess.check_output("git status --porcelain", shell=True, cwd=PROJECT_ROOT).decode().strip()
        if status:
            run_command(git_commit_cmd, dry_run=args.dry_run)
        else:
            print("No changes to commit (version unchanged). Skipping commit.")

    run_command(git_tag_cmd, dry_run=args.dry_run)
    run_command(git_push_cmd, dry_run=args.dry_run)

    print(f"Successfully released v{new_version}!")

if __name__ == "__main__":
    main()
