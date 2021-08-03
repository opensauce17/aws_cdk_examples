#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd.service
systemctl enable httpd.service
echo "Hello World from $(hostname -f)" > /var/www/html/index.html
# Add apache logs to cloudwatch
cat << 'EOF' >> /etc/awslogs/awslogs.conf
[apache logs]
datetime_format = %b %d %H:%M:%S
file = /var/log/httpd/access_log
buffer_duration = 5000
log_stream_name = weblogs
initial_position = start_of_file
log_group_name = apaches_logs
EOF
sudo systemctl start awslogsd
sudo chkconfig awslogsd on
sudo systemctl enable awslogsd.service
sudo curl localhost
