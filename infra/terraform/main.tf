# SkillForge infra — scoped to what a hackathon team can realistically provision
# and verify: a managed Postgres database and a container registry to push
# service images to. Kubernetes cluster provisioning (EKS) is deliberately left
# out — most teams will run K8s manifests against a local cluster (kind/minikube)
# for the demo rather than standing up a real EKS cluster under time pressure.
#
# Usage:
#   cd infra/terraform
#   terraform init
#   terraform plan -var="db_password=<secret>"
#   terraform apply -var="db_password=<secret>"

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "db_password" {
  description = "Password for the SkillForge Postgres instance"
  type        = string
  sensitive   = true
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "hackathon-demo"
}

# ---------- Networking (default VPC, kept minimal on purpose) ----------

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_security_group" "skillforge_db" {
  name        = "skillforge-db-${var.environment}"
  description = "Allow Postgres access from within the VPC"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.default.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ---------- Managed Postgres ----------

resource "aws_db_subnet_group" "skillforge" {
  name       = "skillforge-${var.environment}"
  subnet_ids = data.aws_subnets.default.ids
}

resource "aws_db_instance" "skillforge" {
  identifier             = "skillforge-${var.environment}"
  engine                 = "postgres"
  engine_version         = "16"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  db_name                = "skillforge"
  username               = "skillforge"
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.skillforge.name
  vpc_security_group_ids = [aws_security_group.skillforge_db.id]
  skip_final_snapshot    = true
  publicly_accessible    = false
}

# ---------- Container registry (one per service) ----------

resource "aws_ecr_repository" "services" {
  for_each             = toset(["auth", "core", "analyzer", "ai", "gateway", "frontend"])
  name                 = "skillforge-${each.key}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "db_endpoint" {
  value = aws_db_instance.skillforge.endpoint
}

output "ecr_repository_urls" {
  value = { for k, v in aws_ecr_repository.services : k => v.repository_url }
}
