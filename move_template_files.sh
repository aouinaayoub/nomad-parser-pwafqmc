#!/bin/sh

if ! command -v /usr/bin/rsync &> /dev/null; then
  echo "rsync required, but not installed!"
  exit 1
else
  /usr/bin/rsync -avh nomad-parser-pwafqmc/ .
  rm -rfv nomad-parser-pwafqmc
fi
