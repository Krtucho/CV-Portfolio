.PHONY: init plan apply destroy fmt validate clean

ENV ?= dev
CLOUD ?= aws

init:
	cd environments/$(ENV)/$(CLOUD) && terraform init

plan:
	cd environments/$(ENV)/$(CLOUD) && terraform plan

apply:
	cd environments/$(ENV)/$(CLOUD) && terraform apply -auto-approve

destroy:
	cd environments/$(ENV)/$(CLOUD) && terraform destroy -auto-approve

fmt:
	terraform fmt -check -recursive

validate:
	terraform validate -recursive

clean:
	rm -rf environments/*/*/.terraform
	rm -f environments/*/*/.terraform.lock.hcl

checkov:
	checkov -d . --framework terraform --quiet

tfsec:
	tfsec .

plan-all:
	find environments -type f -name "main.tf" -exec dirname {} \; | while read dir; do \
		cd $$dir && terraform init && terraform plan && cd -; \
	done
