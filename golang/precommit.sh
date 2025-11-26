#!/bin/bash
# Backend/golang/precommit.sh

set -e

cd "$(dirname "$0")"  # go into Backend/golang directory

echo "Running Go pre-commit checks..."

# 1. Check goimports
echo "Checking goimports formatting..."
unformatted=$(goimports -l .)
if [ -n "$unformatted" ]; then
  echo "❌ The following files are not formatted:"
  echo "$unformatted"
  echo "Run 'goimports -w .' to fix formatting."
  exit 1
fi

# 2. Lint
if command -v golangci-lint >/dev/null 2>&1; then
  echo "Running golangci-lint..."
  golangci-lint run
fi

echo "✅ All pre-commit checks passed!"
