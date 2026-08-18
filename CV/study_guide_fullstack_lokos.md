# Plan Intensivo: Full Stack React + Python + AI Workflow — Lokos.ai

> Stack real: React • Python/FastAPI • PostgreSQL • GCP • Kubernetes • GitHub Actions
> Workflow: AI genera código (Codex/Claude) → Tú revisas, testeas y deployas en staging

---

## ⚡ Priorización para 1-3 días

| Día | Mañana (3h) | Tarde (3h) | Noche (2h) |
|-----|-------------|------------|------------|
| **1** | React + FastAPI (lo que más pesa) | AI Workflow con Codex/Claude | PostgreSQL + GCP básico |
| **2** | Kubernetes + GitHub Actions | ML/Data Science (plus) | Repaso + practicar storytelling |
| **3** | Simulacro de entrevista | Repaso de puntos débiles | Descanso y confianza |

---

## 1. React + FastAPI (Full Stack) — LO QUE MÁS PESARÁ

El dueño quiere saber que puedes trabajar con **React frontend + Python/FastAPI backend** en un flujo donde **la IA escribe el código inicial y tú lo revisas/testeas**.

### React — Qué saber sí o sí

```
- Functional components + Hooks (useState, useEffect, useContext, useReducer)
- Props, estado, eventos
- Fetching data: fetch API, axios, React Query
- Manejo de formularios y validación
- Routing con React Router
- Componentes reutilizables
- Styling: CSS modules, TailwindCSS (lo más común hoy)
- Testing: Jest, React Testing Library
```

### FastAPI — Qué saber sí o sí

```
- Path operations (@app.get, @app.post, etc.)
- Pydantic models (request/response validation)
- Dependency Injection (Depends)
- SQLAlchemy async + Alembic migrations
- JWT authentication
- CORS, middleware
- Testing con pytest + httpx (TestClient)
```

### Recursos rápidos (máximo 2h cada uno)

- **React** — Tutorial oficial (tic-tac-toe): https://react.dev/learn
- **React + Hooks** — Video 1h: https://youtu.be/9xhKH43MhCE
- **FastAPI docs** — https://fastapi.tiangolo.com/tutorial/ (solo los primeros 7 capítulos)
- **FastAPI full app** — Video 2h: https://youtu.be/0sOvCWFmrtA
- **FastAPI + SQLAlchemy async** — https://fastapi.tiangolo.com/tutorial/sql-databases/

### Ejercicio práctico clave (hacerlo sí o sí)

```bash
# 1. Crear un React app que lista items desde una API
npx create-react-app my-app
# Componente: <ItemList /> que fetchea de /api/items

# 2. Crear FastAPI con un endpoint /api/items
# Usar Pydantic para validar
# Usar SQLAlchemy async + PostgreSQL

# 3. Conectar frontend con backend
# fetch desde React al backend FastAPI

# 4. Probar el flujo AI:
# - Codex genera el CRUD completo
# - Tú revisas: ¿los Pydantic models son correctos?
# - ¿Maneja errores? ¿Auth? ¿Validación?
```

---

## 2. AI-Driven Workflow (Codex + Claude) — TU DIFERENCIADOR

> Esto es lo que más les importa. El workflow es: **AI genera → Tú revisas → Testeas en staging → Deployas**.

### Qué tienes que saber explicar

```
1. Cómo usas Codex/Claude Code para generar código inicial
2. Cómo revisas el código generado (seguridad, calidad, patrones)
3. Cómo testeas en staging antes de pasar a producción
4. Cómo estructuras prompts efectivos (prompt engineering)
5. Cómo manejas edge cases que la IA no contempla
```

### Ejemplos de prompts que DEBES saber dar

```
"Genera un FastAPI endpoint POST /api/users con:
- Pydantic model para email, password (hasheado con bcrypt), name
- SQLAlchemy async insert a PostgreSQL
- Validación de email único
- Manejo de errores con HTTPException
- Tests con pytest y httpx"

"Genera un componente React <UserTable /> que:
- Fetch de /api/users
- Muestra tabla con nombre, email, fecha
- Botón de eliminar con confirmación
- Estados: loading, empty, error
- TailwindCSS styling"

"Dame el GitHub Actions workflow para:
- Testear Python con pytest
- Lint con ruff
- Build y push Docker a GCR
- Deploy a GKE en staging
- Escanear con Trivy"
```

### Lo que el dueño va a evaluar

- **¿Sabes dirigir a la IA para que produzca código correcto?**
- **¿Sabes identificar cuándo el código de la IA tiene errores?**
- **¿Testeas antes de confiar en el código generado?**
- **¿Entiendes el código que la IA produce o solo lo copias?**

### Recursos

- **OpenAI Codex Guide:** https://platform.openai.com/docs/guides/code
- **Claude Code (Anthropic):** https://docs.anthropic.com/en/docs/claude-code
- **Prompt Engineering Guide:** https://www.promptingguide.ai/
- **YouTube — GitHub Copilot + Codex workflow:** https://youtu.be/Ek5R7k_Sv-E

---

## 3. GCP Cloud — Conceptos clave

### Qué saber para la entrevista

```
- GKE (Google Kubernetes Engine): clústeres, node pools, auto-scaling
- Cloud SQL: PostgreSQL administrado, backups, alta disponibilidad
- Cloud Storage: buckets, IAM, encryption
- Cloud Build: CI/CD nativo de GCP
- Secret Manager: gestión de secretos
- IAM: roles, service accounts, políticas
- VPC: redes, subnets, firewall rules, Cloud NAT
- Cloud Logging + Cloud Monitoring
```

### Recursos

- **GKE Quickstart:** https://cloud.google.com/kubernetes-engine/docs/quickstart
- **Cloud SQL + Python:** https://cloud.google.com/sql/docs/postgres/connect-app-engine
- **YouTube — GCP Essentials Playlist:** https://youtube.com/playlist?list=PLIivdWyY5sqJ6K4w2Vh4mLtE4E0Rq5sCz
- **YouTube — GKE for Beginners:** https://youtu.be/2h4Rq4F4-5k

---

## 4. Kubernetes — Lo mínimo indispensable

### Qué saber

```
- Pod, Deployment, Service, Ingress
- ConfigMap, Secret
- kubectl: get, describe, logs, apply, delete, rollout
- Health probes: liveness, readiness, startup
- HPA (Horizontal Pod Autoscaler)
- RBAC básico
- Namespaces
- Deploy en GKE específicamente
```

### Recursos exprés

- **Kubernetes en 30 min (TechWorld):** https://youtu.be/7XzI1pBCYqk
- **Kubectl Cheat Sheet:** https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- **KodeKloud Free Labs:** https://kodekloud.com/p/free-labs

---

## 5. PostgreSQL — Lo que te van a preguntar

### Qué saber

```
- Consultas básicas: SELECT, JOIN, GROUP BY, subqueries
- Índices: B-tree, partial, composite (cuándo usarlos)
- Migraciones con Alembic (Python)
- Conexión segura: SSL/TLS, IAM-based auth en GCP Cloud SQL
- Buenas prácticas: prepared statements (SQLAlchemy lo hace solo), connection pooling
- Backup y restauración (Cloud SQL lo maneja)
```

### Ejercicio rápido

```sql
-- Practicar estas consultas
SELECT u.name, COUNT(o.id) as orders
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 5
ORDER BY orders DESC;
```

---

## 6. GitHub Actions — Para CI/CD

### Qué saber

```
- Workflow: eventos (push, pull_request), jobs, steps
- Actions: checkout, setup-python, setup-node, docker/login
- Secrets y environment variables
- Matrix builds
- Deploy a GKE: google-github-actions/gke-deploy
- Tests + lint en cada PR
```

### Workflow mínimo que debes saber escribir

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest
      - run: ruff check .
```

### Deploy a GKE

```yaml
- id: deploy
  uses: google-github-actions/gke-deploy@v2
  with:
    cluster: ${{ vars.GKE_CLUSTER }}
    location: ${{ vars.GKE_ZONE }}
    image: gcr.io/${{ vars.GCP_PROJECT }}/app:${{ github.sha }}
```

---

## 7. ML/Data Science (Plus) — Si preguntan

### Qué saber (conceptos básicos)

```
- Diferencia entre supervised, unsupervised, reinforcement learning
- Modelos comunes: regresión lineal, random forest, redes neuronales
- Train/test split, overfitting, underfitting
- APIs de ML: TensorFlow Serving, FastAPI para servir modelos
- Lo más relevante para ellos: cómo integrar un modelo ML en una API FastAPI
```

### Cómo integrar ML con FastAPI

```python
from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load("model.pkl")

@app.post("/predict")
async def predict(features: list[float]):
    prediction = model.predict([features])
    return {"prediction": prediction.tolist()}
```

---

## 🎯 Guía rápida para la entrevista

### Storytelling: cómo presentarte

```
"Trabajo con React + Python/FastAPI en un flujo full agentic con Codex y Claude.
La IA genera el código inicial — yo me encargo de:
1. Revisar que sea seguro y siga buenas prácticas
2. Escribir tests antes de confiar en el código
3. Desplegar en staging con GitHub Actions + GKE
4. Monitorear con logs y métricas en GCP

Para el frontend uso React con hooks y TailwindCSS,
el backend es FastAPI con SQLAlchemy async + PostgreSQL en Cloud SQL,
y todo corre en Kubernetes en GKE."
```

### Preguntas que probablemente harán

| Pregunta | Respuesta clave |
|----------|-----------------|
| "¿Cómo usas Codex/Claude en tu día a día?" | "Generación de código, debugging, tests, infraestructura. Siempre reviso antes de aceptar." |
| "¿Cómo testeas el código que genera la IA?" | "Tests unitarios + integración en staging environment antes de prod." |
| "¿Has trabajado con React + FastAPI?" | "Sí, React para frontend, FastAPI para backend con SQLAlchemy async." |
| "¿Cómo deployas en GCP?" | "GitHub Actions → Cloud Build → GKE. Usando Google GitHub Actions." |
| "¿Sabes Kubernetes?" | "Deployments, Services, Ingress, HPA, probes. He trabajado con GKE." |
| "¿Y ML?" | (Si preguntan) "He integrado modelos ML en APIs con FastAPI. Conceptos básicos de supervised learning." |
| "¿Has trabajado con PostgreSQL?" | "Consultas complejas, índices, migraciones con Alembic, connection pooling." |

### Si no sabes algo

```
"Todavía no he trabajado profundamente con [tema], pero conozco los fundamentos
y con el workflow de Codex/Claude puedo aprenderlo rápido y generar código
funcional mientras estudio la documentación oficial."
```

---

## 📦 Proyectos que ya tienes para mostrar

| Proyecto | Demuestra |
|----------|-----------|
| `secure-fastapi-devsecops/` | FastAPI + CI/CD + Docker + K8s |
| `multi-cloud-terraform/` | GCP + IaC + infraestructura |
| `security-automation-toolkit/` | Python + automatización |
| `cryptography-security-library/` | Python + criptografía |

Usa **`secure-fastapi-devsecops/`** como tu proyecto estrella para esta entrevista: tiene React-ready (puedes decir que el frontend se conecta), FastAPI, GitHub Actions, GKE deployments, PostgreSQL.

---

## ⏱️ Checklist final (noche antes)

- [ ] Puedo explicar el workflow AI-driven en 2 minutos
- [ ] Puedo escribir un componente React funcional básico
- [ ] Puedo escribir un endpoint FastAPI con Pydantic + SQLAlchemy
- [ ] Puedo escribir un GitHub Actions workflow básico
- [ ] Sé los comandos kubectl esenciales (get, describe, logs, apply)
- [ ] Sé conceptos de GCP (GKE, Cloud SQL, Cloud Storage)
- [ ] Tengo 2-3 proyectos en GitHub para mostrar
- [ ] Preparé 2-3 preguntas para hacerles a ellos
