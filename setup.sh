#!/bin/bash
cp -f /root/config.json.simple /root/conf/
chmod -R 755 /root/
python3 /root/scraper.py > /dev/null 2>&1