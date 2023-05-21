#!/usr/bin/env bash

echo -e "\033[34m--------------------wsgi process--------------------\033[0m"

ps -ef|grep uwsgi.ini | grep -v grep

sleep 0.5

echo -e '\n--------------------going to close--------------------'

ps -ef |grep uwsgi.ini | grep -v grep | awk '{print $2}' | xargs kill -9

sleep 0.5

echo -e '\n----------check if the kill action is correct----------'

/home/zishuq/djgPro/venv/bin/uwsgi --ini uwsgi.ini & >/dev/null

echo -e '\n\033[42;lm--------------------started...--------------------\033[0m'
sleep 1

ps -ef |grep uwsgi.ini | grep -v grep
