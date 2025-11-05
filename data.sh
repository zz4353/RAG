#!/usr/bin/env bash

if [ ! -d ".env" ]; then
    cp .env.example .env
fi
python crawl.py