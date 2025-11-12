# Q1 – Tooling Comparison for CI/CD Migrations (MySQL)

## Flyway (SQL-first, lightweight)
- Versioned SQL (`V1__...sql`), tracks state in `flyway_schema_history`
- Simple CLI/Docker, easy in CI
- Baseline/repair/repeatable migrations

## Liquibase (rich changelogs + rollbacks)
- YAML/JSON/XML/SQL changelogs
- Built-in rollback, diff/generateChangeLog
- Strong governance/reporting

### Comparison

| Criterion          | Flyway                                  | Liquibase                                  |
|-------------------|------------------------------------------|---------------------------------------------|
| Ease of Use       | Simple SQL, fast onboarding              | More concepts, steeper learning             |
| CI/CD Integration | Excellent (CLI/Docker)                   | Excellent (CLI/Docker; more governance)     |
| Supported DBs     | MySQL, Postgres, SQL Server, Oracle …    | MySQL, Postgres, SQL Server, Oracle …       |

### CI/CD Strategy
1. Checkout code
2. Start MySQL service
3. Create app user
4. Apply **V1** initial
5. Apply **V2** incremental (**list both locations**)
6. Run **pytest**
7. Echo deployment summary

```mermaid
flowchart LR
  A[Push] --> B[GitHub Actions]
  B --> C[MySQL Service]
  C --> D[Flyway: V1]
  D --> E[Flyway: V2 (both locations)]
  E --> F[Pytest CRUD]
  F --> G[Echo done for commit]