#!/bin/bash
until ./pyBot.py; do
	echo "Bot crashed, restarting" >&2
	sleep 1
done
