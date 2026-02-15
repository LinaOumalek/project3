## 📅 Week 3 – Goals

### 🎯 Practical Goals (80%) – Improve Current Project

We will focus on **making the system more realistic and production-ready**. The three main areas:

1. **Concurrency**
   - Learn about race conditions and how multiple requests can affect shared data.
   - Apply row-level locking (`SELECT ... FOR UPDATE`) to withdrawals and transfers to ensure consistency.

2. **Testing**
   - Write automated tests using pytest and FastAPI TestClient.
   - Test edge cases like insufficient funds, invalid input, and successful transactions.

3. **Structure**
   - Refactor the project into layers:
     - `routes/` → handle HTTP requests and responses  
     - `services/` → business logic, transactions, validation  
     - `db/` → raw SQL queries  
     - `models/` → Pydantic schemas
   - Goal: each file has one responsibility, easier to maintain and scale.

---

### 📚 Theory Goals (20%) – System Design Foundations

The aim is to **build intuition for how backend systems are structured**.

#### 1. How Computers Work (CS / OS Foundations)
- Understand the basics of computer systems relevant to backend engineering:
  - topic of the week : Network Security

#### 2. How Systems Are Structured (Step 1 & 2)
- **Step 1: Understand End-to-End Request Flow**
  - Map the path of a user request from client → API server → service layer → database → response.
  - Recognize the role of each layer and where validation, business logic, and transactions happen.

- **Step 2: Core System Components**
  - Learn the function of typical components in a backend system:
    - Database → store data reliably
    - Cache → reduce database load and speed up reads
    - Queue → handle background or async tasks
    - Load balancer → distribute traffic across servers
    - API Gateway → authentication, rate limiting, logging
  - Goal: understand what each component solves conceptually, even if not implementing yet.

---

