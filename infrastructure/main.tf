provider "aws" {
  region = "eu-central-1"
}

resource "aws_security_group" "instance_sg" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "instance-1" {
  ami                         = "ami-04a5bacc58328233d"
  instance_type               = "t3.small"
  key_name                    = "whxper"
  monitoring                  = true
  vpc_security_group_ids      = [aws_security_group.instance_sg.id]

  tags = {
    Name = "instance-1"
  }

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y unzip curl wget
              cd /opt
              wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
              dpkg -i -E ./amazon-cloudwatch-agent.deb

              cat > /opt/cw-config.json << EOC
              {
                "agent": {
                  "metrics_collection_interval": 60,
                  "logfile": "/opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log"
                },
                "metrics": {
                  "append_dimensions": {
                    "InstanceId": "\${aws:InstanceId}"
                  },
                  "metrics_collected": {
                    "mem": {
                      "measurement": ["mem_used_percent"],
                      "metrics_collection_interval": 60
                    },
                    "cpu": {
                      "measurement": ["cpu_usage_idle", "cpu_usage_iowait"],
                      "metrics_collection_interval": 60,
                      "totalcpu": true
                    },
                    "diskio": {
                      "measurement": ["io_time"],
                      "metrics_collection_interval": 60
                    },
                    "swap": {
                      "measurement": ["swap_used_percent"],
                      "metrics_collection_interval": 60
                    }
                  }
                }
              }
              EOC

              /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \\
                -a fetch-config -m ec2 -c file:/opt/cw-config.json -s
              EOF
}
