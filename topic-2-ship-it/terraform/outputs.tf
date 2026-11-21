output "public_ip" {
  description = "Public IP of the workstation"
  value       = aws_instance.workstation.public_ip
}

output "key_file" {
  description = "Where the private key was saved"
  value       = local_sensitive_file.pem.filename
}

output "ssh_command" {
  description = "Copy and paste this in Git Bash"
  value       = "ssh -i ${local_sensitive_file.pem.filename} ubuntu@${aws_instance.workstation.public_ip}"
}

output "fastapi_url" {
  description = "Used in Topic 3 and 4"
  value       = "http://${aws_instance.workstation.public_ip}:8000"
}
