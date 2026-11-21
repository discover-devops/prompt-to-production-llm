variable "region" {
  description = "AWS region for the lab"
  type        = string
  default     = "ap-south-1"
}

variable "project" {
  description = "Name prefix for every resource"
  type        = string
  default     = "shipit"
}

variable "vpc_cidr" {
  description = "Address range of our private network"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Address range of the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "instance_type" {
  description = "Size of the EC2 workstation (Docker builds need 4 GB RAM)"
  type        = string
  default     = "t3.medium"
}

variable "root_volume_gb" {
  description = "Disk size in GB (Docker images need space)"
  type        = number
  default     = 30
}

variable "allowed_cidr" {
  description = "Who may SSH in. Put your own IP like 49.37.10.20/32 for safety"
  type        = string
  default     = "0.0.0.0/0"
}

variable "key_save_dir" {
  description = "Folder on your laptop where the .pem key is saved (never inside the project)"
  type        = string
  default     = "~/Downloads"
}
