terraform {
  required_version = ">= 1.5.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}
# Safe learning example: this creates a local file, not cloud resources.
resource "local_file" "project_info" {
  filename = "${path.module}/project-info.txt"
  content  = "DevOps Log Monitoring learning project. Read README.md first.\n"
}
