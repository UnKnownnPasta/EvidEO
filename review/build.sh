#!/bin/sh
# Rebuild figures and review/REVIEW.pdf. Run from the repo root.
python review/figures.py
cd review
pandoc REVIEW.md -f gfm -t html5 -s --embed-resources --metadata pagetitle="Answering with evidence" --css review.css -o REVIEW.html
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$(cygpath -w "$PWD/REVIEW.pdf")" "file:///$(cygpath -m "$PWD/REVIEW.html")"
rm REVIEW.html
