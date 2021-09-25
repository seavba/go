###############################################################################
# AWS VPC
###############################################################################

variable "aws_region" {
  default = "eu-west-1"
}

variable "azs" {
  default = "eu-west-1a,eu-west-1b,eu-west-1c"
}

variable "vpc_name" {
  default = "vpc_fargate"
}

variable "vpc_cdir" {
  default = "10.99.0.0/16"
}


###############################################################################
# fargate ECS
###############################################################################

variable "num_containers" {
  default = 2
}

variable "target_group_port"{
  default = 8080
}

variable "target_group_protocol"{
  default = "HTTP"
}

variable "cloudwatch_group" {
  default = "fargateCW"
}

variable "ecr_image_tag" {
  default = "latest"
}

variable "ecr_repo" {
  default = "docker_images/fargate"
}

variable "ingress_rules" {
    type = list(object({
      from_port   = number
      to_port     = number
      protocol    = string
      cidr_block  = string
    }))
    default     = [
        {
          from_port   = 443
          to_port     = 8080
          protocol    = "tcp"
          cidr_block  = "0.0.0.0/0"
        }
    ]
}

###############################################################################
# HTTPS and DNS
###############################################################################

variable "domain_name" {
  default = "myapp.ssans.es"
}

variable "zone_name" {
  default = "ssans.es"
}

###############################################################################
# DATA BLOCK
###############################################################################

data "aws_caller_identity" "current" {}
