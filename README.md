# docker-ebs-snapshot

Creates an EBS snapshot for all EBS's with a tag called "backup"|"Backup", with a default rentention period of 10 days. Can be overridden with a tag on the EBS called "Rentention"

## Usage

### Environment Variables

* `AWS_ACCESS_KEY_ID` - The AWS Access Key ID to use
* `AWS_SECRET_ACCESS_KEY` - The AWS Secret Access Key to use
* `AWS_DEFAULT_REGION` - The default AWS Region
