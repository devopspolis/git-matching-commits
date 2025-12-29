#!/usr/bin/env bash
set -e

mkdir merge-repo
cd merge-repo
git init

echo base > file.txt
git add .
git commit -m "base"

git checkout -b feature
echo hotfix > file.txt
git commit -am "hotfix commit"

git checkout main
git merge --no-ff feature -m "Merge PR #1"

git tag v1.0.1

