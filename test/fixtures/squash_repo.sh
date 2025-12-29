#!/usr/bin/env bash
set -e

mkdir squash-repo
cd squash-repo
git init

echo base > file.txt
git add .
git commit -m "base"

git checkout -b feature
echo hotfix > file.txt
git commit -am "hotfix commit"

git checkout main
git merge --squash feature
git commit -m "Squash PR #2"

git tag v1.0.1

