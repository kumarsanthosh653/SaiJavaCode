terraform {
  required_version = "~> 1.7"

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.79.0"

    }

  }
}

provider "aws" {
   region = "us-east-2"
  


}


resource "aws_s3_bucket" "s3" {
 bucket = "bbbbccckkkkk"
 

}


