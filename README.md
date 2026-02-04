# Todo Evolution - From CLI to Cloud-Native AI Systems

This project demonstrates the evolution of a simple todo application through five phases, following Spec-Driven Development (SDD) principles with AI-native architecture.

## Project Structure

This project follows the mandatory monorepo structure as defined in the constitution:

```
evolution-of-todolist/
├── constitution.md                 # The Supreme Law (Principles & Constraints)
├── AGENTS.md                      # AI Agent Instructions (The "How-To")
├── CLAUDE.md                      # Claude Code entry point (Shim to AGENTS.md)
├── README.md                      # Project onboarding
│
├── .specify/                      # SpecifyPlus Tool Configuration
├── specs/                         # The Source of Truth (Lifecycle Stages)
│   ├── 1-specify/                # STEP 1: WHAT (Requirements & Context)
│   ├── 2-plan/                   # STEP 2: HOW (Architecture & Design)
│   └── 3-tasks/                  # STEP 3: EXECUTE (Atomic Units)
│
├── src/                           # STEP 4: IMPLEMENTATION (Phase I)
├── frontend/                      # STEP 4: IMPLEMENTATION (Phase II+)
├── backend/                       # STEP 4: IMPLEMENTATION (Phase II+)
└── infra/                         # STEP 4: INFRASTRUCTURE (Phase IV+)
```

## Phases

### Phase I: Console App
- **Technology**: Python 3.13+, UV package manager
- **Storage**: In-memory only
- **Purpose**: Foundation with core functionality

### Phase II: Web Application
- **Frontend**: Next.js 16+ (App Router)
- **Backend**: Python FastAPI
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT

### Phase III: AI Chatbot
- **Chat UI**: OpenAI ChatKit
- **AI Framework**: OpenAI Agents SDK
- **MCP**: Official MCP SDK (Python)

### Phase IV: Local Kubernetes
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Minikube)
- **Package Manager**: Helm Charts

### Phase V: Cloud Deployment
- **Cloud Platform**: Azure (AKS) / Google Cloud (GKE) / Oracle (OKE)
- **Event Streaming**: Kafka
- **Runtime**: Dapr (Distributed Application Runtime)

## Setup

1. Clone the repository
2. Install dependencies based on the phase you're working on
3. Configure environment variables as needed

## Development Workflow

This project follows the SDD Loop:
```
Specify (WHAT) → Plan (HOW) → Tasks (BREAKDOWN) → Implement (CODE)
```

## Contributing

Please follow the constitutional principles outlined in `constitution.md` when contributing to this project.

## License

See the LICENSE file for licensing information.