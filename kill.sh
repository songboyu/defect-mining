sudo ps -ef|grep celery|grep -v grep|cut -c 9-15|xargs kill -9
sudo ps -ef|grep mining|grep -v grep|cut -c 9-15|xargs kill -9
rm -rf output/*
redis-cli flushdb
