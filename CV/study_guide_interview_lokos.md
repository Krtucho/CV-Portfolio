# Guía de Estudio: DevOps & Cybersecurity — Lokos.ai

> Basado en la conversación con Diane y los requisitos del puesto.
> Empresa: https://lokos.ai | Entrevista técnica directa con el dueño en ~2 semanas.

---

## 📅 Plan de Estudio (14 Días)

| Día | Tema | Prioridad |
|-----|------|-----------|
| 1-2 | Terraform (IaC) | 🔴 Alta |
| 3-4 | Penetration Testing | 🔴 Alta |
| 5-6 | Cryptography | 🔴 Alta |
| 7 | Docker & Kubernetes | 🟡 Media |
| 8 | GitHub Actions + DevSecOps CI/CD | 🟡 Media |
| 9 | FastAPI + Python Security | 🟡 Media |
| 10 | AWS/GCP Networking & IAM | 🟡 Media |
| 11 | SAST/DAST + Vulnerability Scanning | 🟡 Media |
| 12 | Secret Management + Hardening | 🔵 Media-Baja |
| 13 | Incident Response + Threat Monitoring | 🔵 Media-Baja |
| 14 | Repaso general + práctica proyectos | 🔴 Alta |

---

## 1. Terraform (IaC) — 🔴 Prioridad Alta

> La recruiter dijo explícitamente: _"Estudiate Terraform"_

### Qué saber para la entrevista
- Declarative vs imperative (HCL vs procedural)
- Core workflow: `init -> plan -> apply -> destroy`
- State management (local vs remote: S3 + DynamoDB locking)
- Modules: cómo crear módulos reutilizables
- Variables, outputs, `terraform.tfvars`
- Providers (AWS, GCP, Kubernetes)
- `terraform_remote_state`, data sources
- Terragrunt (opcional, pero suma puntos)
- Seguridad en Terraform: **Checkov**, **tfsec**

### Recursos
- **Curso oficial HashiCorp:** https://developer.hashicorp.com/terraform/tutorials
- **FreeCodeCamp Guide:** https://www.freecodecamp.org/news/a-beginners-guide-to-terraform-infrastructure-as-code-in-practice/
- **YouTube — FreeCodeCamp Terraform Course (3h):** https://youtu.be/SLB_c_ayRMo
- **YouTube — TechWorld with Nana Terraform (1h):** https://youtu.be/7xngnjfIlK4
- **YouTube — Learn DevOps Terraform Playlist:** https://youtube.com/playlist?list=PL9nWRykSBSFgCw1cONux6a4EaJY_rZ7Qq

### Ejercicios prácticos
```
1. terraform init && terraform plan && terraform apply (provisionar un S3 bucket)
2. Crear un módulo reutilizable de VPC con subnets públicas/privadas
3. Usar remote state con S3 + DynamoDB
4. Integrar Checkov: checkov -d . --framework terraform
5. Desplegar un EC2 instance con security group restrictivo
6. Usar workspaces para dev/staging/prod
7. Hacer un módulo de EKS con node groups
```

---

## 2. Penetration Testing — 🔴 Prioridad Alta

> La recruiter dijo explícitamente: _"Estudiate Penetration Testing"_

### Qué saber para la entrevista
- Fases del pentesting: Reconnaissance → Scanning → Gaining Access → Maintaining Access → Covering Tracks
- OWASP Top 10 (2021): SQLi, XSS, Broken Auth, SSRF, etc.
- Herramientas: **Nmap**, **Metasploit**, **Burp Suite**, **OWASP ZAP**, **Kali Linux**
- Tipos de pruebas: Black box, White box, Grey box
- Web app pentesting vs network pentesting vs API pentesting
- Reportes: cómo documentar hallazgos (severidad, CVSS, remediation)

### Recursos
- **EC-Council Ethical Hacking Essentials (FREE):** https://www.eccouncil.org/cybersecurity-exchange/ethical-hacking/free-ethical-hacking-courses/
- **Cisco Ethical Hacking Certificate (FREE):** https://www.cisco.com/site/us/en/learn/training-certifications/certifications/ethical-hacker/index.html
- **Great Learning Free Course:** https://www.mygreatlearning.com/academy/learn-for-free/courses/introduction-to-ethical-hacking
- **YouTube — The Cyber Mentor (canal completo):** https://youtube.com/@TheCyberMentor
- **YouTube — Practical Ethical Hacking (12h):** https://youtu.be/3FNYvj2U0HM
- **YouTube — OWASP Top 10 explicado:** https://youtu.be/r4pDEdd3Uic

### Ejercicios prácticos
```
1. Escanear una red con nmap: nmap -sV -sC target.com
2. Instalar Kali Linux (VM o WSL) y probar Metasploit
3. Hacer un OWASP ZAP baseline scan contra un sitio de prueba (DVWA, bwapp)
4. Probar SQL injection en DVWA
5. Probar XSS (reflejado, almacenado, DOM-based)
6. Escanear puertos y servicios con masscan + nmap
7. Hacer un reporte de hallazgos simulado
```

---

## 3. Cryptography — 🔴 Prioridad Alta

> La recruiter dijo explícitamente: _"Estudiate Cryptography"_

### Qué saber para la entrevista
- Symmetric encryption: AES-256-GCM, ChaCha20-Poly1305 (AEAD)
- Asymmetric encryption: RSA-OAEP, ECIES
- Hashing: SHA-256/512, bcrypt, Argon2id, PBKDF2
- Digital signatures: Ed25519, ECDSA, RSA-PSS
- Key exchange: Diffie-Hellman, ECDH, X25519
- PKI: Certificates, CAs, TLS handshake
- Key management: KMS, HSM, Vault, secret rotation
- Common attacks: Padding oracle, timing attacks, hash length extension
- Forward secrecy, perfect forward secrecy

### Recursos
- **Dan Boneh Cryptography Course (Stanford/Coursera):** http://crypto.stanford.edu/~dabo/courses/OnlineCrypto/
- **Coursera — Encryption & Cryptography Essentials (FREE):** https://www.coursera.org/learn/encryption-and-cryptography-essentials
- **Alison — Introduction to Cryptography (FREE):** https://alison.com/course/an-introduction-to-cryptography
- **Great Learning — Encryption Basics (FREE):** https://www.mygreatlearning.com/academy/learn-for-free/courses/encryption
- **YouTube — Cryptography for Beginners (freeCodeCamp):** https://youtu.be/6_Cxj5WKpIw
- **YouTube — Computerphile Cryptography Playlist:** https://youtube.com/playlist?list=PL9nWRykSBSFgCw1cONux6a4EaJY_rZ7Qq

### Ejercicios prácticos
```
1. Encriptar/desencriptar con AES-256-GCM usando pycryptodome o cryptography
2. Generar par de llaves RSA 2048, encriptar y desencriptar
3. Firmar y verificar con Ed25519
4. Hashear passwords con bcrypt (cost=12) y Argon2id
5. Implementar Shamir's Secret Sharing
6. Verificar integridad de un archivo con SHA-256
7. Probar openssl: openssl s_client -connect example.com:443
```

---

## 4. Docker & Kubernetes — 🟡 Prioridad Media

### Qué saber
- Docker: Dockerfile (multi-stage builds), docker-compose, volumes, networks
- K8s: Pods, Deployments, Services (ClusterIP, NodePort, LoadBalancer), Ingress
- ConfigMaps, Secrets
- Health probes: liveness, readiness, startup
- HPA (Horizontal Pod Autoscaler)
- Network policies, security contexts
- RBAC en K8s
- Helm charts (básico)

### Recursos
- **Docker Docs — Deploy to Kubernetes:** https://docs.docker.com/guides/kube-deploy/
- **YouTube — Docker in 1h (TechWorld with Nana):** https://youtu.be/3c-iBn73dDE
- **YouTube — Kubernetes in 2h (TechWorld with Nana):** https://youtu.be/X48VuDVv0do
- **KodeKloud — Kubernetes Labs (FREE):** https://kodekloud.com/blog/kubernetes-tutorial-for-beginners-2025/
- **YouTube — Docker to K8s Production Journey:** https://youtu.be/X48VuDVv0do

### Ejercicios
```
1. Escribir Dockerfile multi-stage para app Python
2. docker-compose con app + postgres + redis
3. kubectl create deployment + expose
4. Escribir manifests: deployment.yaml, service.yaml, ingress.yaml
5. Configurar liveness/readiness probes
6. Crear un ConfigMap y un Secret
7. Hacer rolling update: kubectl set image
```

---

## 5. GitHub Actions + DevSecOps CI/CD — 🟡 Prioridad Media

### Qué saber
- Estructura de workflow: events, jobs, steps, actions
- Matrices (strategy.matrix) para test multi-versión
- Secrets y environments
- Actions marketplace: checkout, setup-python, docker/login, etc.
- DevSecOps integration: SAST (Bandit, Semgrep), DAST (ZAP), SCA (Snyk, pip-audit), Container scan (Trivy)

### Recursos
- **Real Python — GitHub Actions for Python:** https://realpython.com/github-actions-python/
- **GitHub Docs — Building and Testing Python:** https://github.com/github/docs/blob/main/content/actions/tutorials/build-and-test-code/python.md
- **DevSecOps Pipeline con GitHub Actions:** https://dev.to/herjean7/implement-a-devsecops-pipeline-with-github-actions-2lbb
- **YouTube — GitHub Actions CI/CD (1h):** https://youtu.be/R8_veQiYBjI
- **YouTube — DevSecOps Pipeline with GitHub Actions:** https://youtu.be/nN1r0RkIHII

### Ejercicios
```
1. Crear workflow .github/workflows/ci.yml con lint + test + bandit
2. Agregar pip-audit para dependencias
3. Agregar Trivy para escanear imagen Docker
4. Agregar OWASP ZAP (DAST) contra staging
5. Usar matrix para Python 3.11, 3.12
6. Configurar environments con protección manual para prod
```

---

## 6. FastAPI + Python Security — 🟡 Prioridad Media

### Qué saber
- FastAPI: Path operations, dependency injection, Pydantic models
- Auth: JWT, OAuth2, API keys
- Rate limiting, CORS, security headers
- Input validation con Pydantic
- SQLAlchemy + Alembic (async)
- Sentry integration
- Buenas prácticas: repository pattern, services layer

### Recursos
- **FastAPI Official Docs:** https://fastapi.tiangolo.com/
- **Microservicios con FastAPI (GeeksforGeeks):** https://www.geeksforgeeks.org/python/microservice-in-python-using-fastapi/
- **FastAPI Microservice Production Guide:** https://oneuptime.com/blog/post/2025-07-02-python-microservices-architecture/view
- **YouTube — FastAPI Full Course (4h):** https://youtu.be/7t2alSnE2-I
- **YouTube — FastAPI + SQLAlchemy:** https://youtu.be/NNqolPLCf-s

### Ejercicios
```
1. Crear API CRUD con FastAPI + SQLAlchemy async
2. Implementar JWT auth con refresh tokens
3. Agregar rate limiting con Redis
4. Validar inputs con Pydantic (strict)
5. Integrar Sentry
6. Escribir tests con pytest-asyncio
```

---

## 7. AWS/GCP IAM & Networking — 🟡 Prioridad Media

### Qué saber
- IAM: Users, Groups, Roles, Policies (managed vs inline), trust policies
- Least privilege principle
- IAM Access Analyzer
- VPC: subnets (public/private), NAT Gateways, Security Groups, NACLs
- VPC Flow Logs
- S3 bucket policies + block public access
- AWS WAF, Shield
- GCP: IAM roles, service accounts, VPC-native clusters

### Recursos
- **AWS IAM Best Practices:** https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- **AWS Least Privilege Guide:** https://aws.amazon.com/blogs/security/strategies-for-achieving-least-privilege-at-scale-part-1/
- **YouTube — AWS IAM Complete Guide:** https://youtu.be/fcyrcc4F5gQ
- **YouTube — AWS VPC Explained:** https://youtu.be/g2JwB2WjWCM

### Ejercicios
```
1. Crear IAM role con política de least-privilege (solo S3 GetObject)
2. Configurar S3 bucket policy bloqueando acceso público
3. Crear VPC con subnets públicas/privadas + NAT Gateway
4. Configurar Security Groups restrictivos
5. Habilitar VPC Flow Logs y revisar logs
6. Usar IAM Access Analyzer
```

---

## 8. SAST/DAST + Vulnerability Scanning — 🟡 Prioridad Media

### Qué saber
- SAST: Bandit (Python), Semgrep, SonarQube/Cloud
- DAST: OWASP ZAP
- SCA: Snyk, pip-audit, Dependabot
- Container scanning: Trivy, Docker Scout
- Secret scanning: gitleaks, truffleHog
- Infra scanning: Checkov, tfsec
- CVE, CVSS scoring

### Recursos
- **OWASP Source Code Analysis Tools:** https://owasp.org/www-community/Source_Code_Analysis_Tools
- **Semgrep Getting Started:** https://dev.to/semgrep/getting-started-with-sast-and-semgrep-cli-1cc1
- **Bandit Python Security:** https://bandit.readthedocs.io/en/latest/
- **YouTube — SAST with Semgrep:** https://youtu.be/vuFyZ7N7b7M

### Ejercicios
```
1. bandit -r app/ (escanear proyecto Python)
2. semgrep --config=auto . (escanear con reglas automáticas)
3. pip-audit (escanear dependencias)
4. trivy image myapp:latest (escanear imagen)
5. checkov -d . (escanear Terraform)
6. OWASP ZAP baseline scan contra webapp
```

---

## 9. Secret Management + Hardening — 🔵 Prioridad Media-Baja

### Qué saber
- HashiCorp Vault: dynamic secrets, transit engine, auth methods
- AWS Secrets Manager / GCP Secret Manager
- KMS (Key Management Service) en AWS/GCP
- Hardening: distroless images, non-root users, read-only filesystem
- Container security contexts (K8s)
- Secret rotation, encryption at rest/transit

### Recursos
- **HashiCorp Vault Tutorials:** https://developer.hashicorp.com/vault/tutorials
- **YouTube — HashiCorp Vault (1h):** https://youtu.be/VYfl7F6i4N0
- **AWS Secrets Manager Docs:** https://docs.aws.amazon.com/secretsmanager/

---

## 10. Incident Response + Threat Monitoring — 🔵 Prioridad Media-Baja

### Qué saber
- Incident response lifecycle: Preparation → Detection → Containment → Eradication → Recovery → Lessons Learned
- SIEM basics: log aggregation, correlation rules
- Threat detection: Sigma rules, GuardDuty, CloudTrail
- Playbooks: compromised instance, data breach, DDoS
- NIST SP 800-61: Incident Handling Guide
- SOC2 / ISO 27001 awareness: controles, auditoría

### Recursos
- **YouTube — Incident Response Playbook:** https://youtu.be/eM7Ys4MuX9A
- **NIST SP 800-61 (FREE):** https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final
- **Sigma Rules GitHub:** https://github.com/SigmaHQ/sigma

---

## 🧪 Proyectos que ya tienes (portfolio)

Usa los proyectos ya creados como base de estudio y demo:

```
projects/secure-fastapi-devsecops/
  → Practica: FastAPI, CI/CD, Docker, K8s, SAST/DAST, Terraform

projects/multi-cloud-terraform/
  → Practica: Terraform modules, AWS VPC, GCP GKE, IAM, Checkov

projects/security-automation-toolkit/
  → Practica: SAST scanning, secret scanning, threat detection, incident response

projects/cryptography-security-library/
  → Practica: AES-256-GCM, RSA-OAEP, Ed25519, Argon2id, Shamir
```

---

## 🎯 Preparación para la Entrevista Técnica

### Preguntas probables por tema

#### Terraform
- "Explica el workflow de Terraform" → `init, plan, apply, destroy`
- "¿Cómo manejas el estado?" → Remote state con S3 + DynamoDB locking
- "¿Qué son los módulos y por qué usarlos?" → Reusabilidad, organización
- "¿Cómo aseguras tu infraestructura?" → Checkov, tfsec, least-privilege IAM

#### Penetration Testing
- "¿Cuáles son las fases de un pentest?" → Recon, scanning, exploitation, post-exploitation, reporting
- "¿Qué es OWASP Top 10?" → Listar las principales 10 vulnerabilidades web
- "¿Cómo probarías SQL injection?" → ' OR 1=1 --, UNION-based, blind SQLi

#### Cryptography
- "Diferencia entre hashing y encryption" → Hashing es one-way, encryption es two-way
- "¿Qué es AEAD?" → Authenticated Encryption with Associated Data (GCM, ChaCha20-Poly1305)
- "¿Por qué no usar MD5/SHA1?" → Colisiones demostradas, usar SHA-256 o SHA-3
- "¿Qué cifrado usas para passwords?" → bcrypt (cost 12+) o Argon2id

#### Docker/K8s
- "Diferencia entre Docker y K8s" → Docker corre contenedores, K8s los orquesta
- "¿Qué son los probes?" → liveness (container alive), readiness (puede servir tráfico), startup (inicio lento)
- "¿Cómo haces rolling update?" → kubectl set image deployment, estrategia RollingUpdate

#### GitHub Actions
- "¿Cómo estructuras un pipeline DevSecOps?" → lint → SAST → test → dependency scan → container scan → DAST → deploy
- "¿Qué es un action matrix?" → Test multi-versión de Python

#### AWS/GCP
- "¿Qué es least privilege?" → Mínimos permisos necesarios
- "Diferencia entre Security Group y NACL" → SG: stateful, nivel instancia. NACL: stateless, nivel subnet
- "¿Cómo cifras datos en reposo?" → KMS, S3-SSE, RDS encryption

---

## 📎 Resumen de links importantes

| Tema | Link |
|------|------|
| Terraform tutorial oficial | https://developer.hashicorp.com/terraform/tutorials |
| Terraform en español (YouTube) | https://youtu.be/7xngnjfIlK4 |
| Pentesting gratis (EC-Council) | https://www.eccouncil.org/...free-ethical-hacking-courses/ |
| Pentesting The Cyber Mentor | https://youtube.com/@TheCyberMentor |
| Cryptography Dan Boneh | http://crypto.stanford.edu/~dabo/courses/OnlineCrypto/ |
| Cryptography freeCodeCamp | https://youtu.be/6_Cxj5WKpIw |
| GitHub Actions + Python | https://realpython.com/github-actions-python/ |
| FastAPI docs | https://fastapi.tiangolo.com/ |
| AWS IAM best practices | https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html |
| Docker a Kubernetes | https://docs.docker.com/guides/kube-deploy/ |
| K8s para beginners | https://kodekloud.com/blog/kubernetes-tutorial-for-beginners-2025/ |
| OWASP SAST tools | https://owasp.org/www-community/Source_Code_Analysis_Tools |
| Semgrep getting started | https://dev.to/semgrep/getting-started-with-sast-and-semgrep-cli-1cc1 |
| DevSecOps CI/CD | https://dev.to/herjean7/implement-a-devsecops-pipeline-with-github-actions-2lbb |
| HashiCorp Vault | https://developer.hashicorp.com/vault/tutorials |
| Sigma rules | https://github.com/SigmaHQ/sigma |
| NIST 800-61 (IR) | https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final |

---

## ⚡ Tips rápidos para la entrevista

1. **Habla en términos de seguridad primero** — Menciona "least privilege", "defense in depth", "shift left security"
2. **Menciona tu experiencia con IA** — El dueño usa Codex/Claude full agentic; di cómo los usas para generar infraestructura, debugging, tests
3. **Relaciona networking con seguridad** —VNets, security groups, WAF, network policies
4. **Si no sabes algo, di cómo lo aprenderías** — La empresa busca personas motivadas a aprender
5. **Proyectos de portfolio** — Menciona los 4 proyectos que creaste y lo que demuestran
6. **Pregunta sobre el stack** — "¿Usan AWS o GCP? ¿Qué herramientas de seguridad ya tienen implementadas?"
