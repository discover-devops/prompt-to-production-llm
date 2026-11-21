# Latest Ubuntu 24.04 LTS image from Canonical
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# SSH key: Terraform creates it, AWS gets the public half, we keep the private half
resource "tls_private_key" "ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "ssh" {
  key_name   = "${var.project}-key"
  public_key = tls_private_key.ssh.public_key_openssh
}

# Private key saved in Downloads, never in the project folder (it goes to GitHub)
resource "local_sensitive_file" "pem" {
  content         = tls_private_key.ssh.private_key_pem
  filename        = "${pathexpand(var.key_save_dir)}/${var.project}-key.pem"
  file_permission = "0400"
}

# The workstation: a plain Ubuntu machine, tools are installed live in class
resource "aws_instance" "workstation" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.workstation.id]
  key_name               = aws_key_pair.ssh.key_name

  root_block_device {
    volume_size = var.root_volume_gb
    volume_type = "gp3"
  }

  metadata_options {
    http_tokens = "required"
  }

  tags = { Name = "${var.project}-workstation" }
}
