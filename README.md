## Context

In the previous challenge, you completed the staging layer — three clean models, one per source table, all consistently renamed, typed, and documented. Staging gives you clean, individually prepared datasets; the intermediate layer is where you join them together and apply business logic before the data reaches marts.

## Objective

Create an intermediate model that joins orders with their payments:

- `int_orders_with_payments.sql` - Orders enriched with payment totals

## 0. Copy Your Project and Set Up Database

**📍 In your terminal**, navigate to the challenge directory and copy your previous work:

```bash
cp -rP ../../../{{ local_path_to("03-Data-Transformation/09-Data-Layers-And-Intro-DBT/04-Complete-Staging-Layer") }}/jaffle_shop_dbt .

```

Then commit so you have a clean starting point for this challenge:

```bash
git add jaffle_shop_dbt
git commit -m "Copied setup from previous challenge"
git push origin master
```

<details>
<summary markdown="span">**🔧 Troubleshooting**</summary>

**Symlink verification:**

```bash
ls -l jaffle_shop_dbt/dev.duckdb
```

Should show: `jaffle_shop_dbt/dev.duckdb -> ../../../dbt-shared/dev.duckdb`

**If symlink is broken:**

```bash
rm -f jaffle_shop_dbt/dev.duckdb
ln -s ../../../dbt-shared/dev.duckdb jaffle_shop_dbt/dev.duckdb
```

**DBeaver connection:**

- Use your existing **jaffle_shop_shared** connection
- No need to update path - it points to the shared database!

</details>

## 1. Join Orders with Payments

### 1.1. Create Intermediate Folder

```bash
mkdir -p jaffle_shop_dbt/models/intermediate
```

### 1.2. Understanding the ref() Macro

**`{{ ref('model_name') }}`** references other dbt models — not raw sources.

**Benefits:**

- dbt builds models in the correct order automatically
- Automatically resolves the correct schema
- Tracks lineage for the full DAG
- Enables selective runs (`dbt run --select +model_name`)

**Example dependency chain:**

```markdown
 jaffle_shop.orders  -→  stg_orders   🯓
                                       🯟→  int_orders_with_payments
jaffle_shop.payments -→ stg_payments  🯑
```

dbt ensures staging models run before intermediate models.

### 1.3. Create int_orders_with_payments.sql

**Your Challenge:** Create an intermediate model that enriches orders with their payment data.

**Requirements:**

1. **File location:** `models/intermediate/int_orders_with_payments.sql`
2. **Use the CTE pattern** (same as your staging models)
3. **Reference staging models** with `{{ ref() }}` — NOT `{{ source() }}`
4. **The model must:**
   - Pull from `stg_orders` and `stg_payments`
   - Aggregate payments per order (some orders have multiple payments)
   - Join aggregated payments back to orders
   - Preserve **all** orders, even those with no payments
5. **Output columns:** `order_id`, `customer_id`, `order_date`, `status`, `payment_count`, `total_amount`

**Create the file:**

```bash
cd jaffle_shop_dbt
```

```bash
code models/intermediate/int_orders_with_payments.sql
```

**📝 In VS Code**, write your SQL using the CTE pattern.

<details>
<summary markdown="span">**💡 Hint: Aggregating payments per order**</summary>

Some orders have **multiple payments** (e.g., credit card + gift card split). You need to aggregate them before joining:

- Use `COUNT(*)` to count the number of payments per order
- Use `SUM(amount)` to total the payment amounts
- Use `GROUP BY order_id` to get one row per order

**🗄️ In DBeaver**, check the source data first:

```sql
SELECT order_id, COUNT(*) AS payment_count
FROM main_staging.stg_payments
GROUP BY order_id
ORDER BY payment_count DESC
LIMIT 10;
```

</details>

<details>
<summary markdown="span">**💡 Hint: Which JOIN type preserves all orders?**</summary>

Should orders with no payments still appear in the result?

- **INNER JOIN** — only orders with at least one matching payment ❌
- **LEFT JOIN** — **all** orders, with NULL for payment columns if no match

Use LEFT JOIN to ensure no orders are dropped from your result.

</details>

### 1.4. Test and Verify

**🗄️ Note:** If DBeaver is connected, disconnect it first (right-click connection → Disconnect) to avoid database locks.

**Compile** (check SQL without running):

```bash
dbt compile --select int_orders_with_payments
```

**Run** (execute and create view):

**🗄️ Note:** If DBeaver is connected, disconnect it first (right-click connection → Disconnect) to avoid database locks.

```bash
dbt run --select int_orders_with_payments
```

<details>
<summary markdown="span">**Expected output**</summary>

```plaintext
Done. PASS=1 WARN=0 ERROR=0 SKIP=0 TOTAL=1
```

</details>

**Verify your join and aggregation are correct:**

**🗄️ In DBeaver**, connect to `jaffle_shop_shared` and run:

```sql
-- Check all expected columns exist
SELECT order_id, customer_id, order_date, status, payment_count, total_amount
FROM main_intermediate.int_orders_with_payments
LIMIT 10;
```

**Verify you see these columns:** `order_id`, `customer_id`, `order_date`, `status`, `payment_count`, `total_amount`

```sql
-- Verify row count matches stg_orders (LEFT JOIN keeps all orders)
SELECT COUNT(*) FROM main_intermediate.int_orders_with_payments;
-- Compare with:
SELECT COUNT(*) FROM main_staging.stg_orders;
-- These should be equal — fewer rows means you used INNER JOIN!
```

```sql
-- Check orders with multiple payments are aggregated correctly
SELECT *
FROM main_intermediate.int_orders_with_payments
WHERE payment_count > 1
LIMIT 5;
-- Should show rows with payment_count 2+ and correctly summed total_amount
```

**❌ Common mistakes to check:**

- Row count less than `stg_orders`? You used INNER JOIN — switch to LEFT JOIN!
- Missing `payment_count`? Did you use `COUNT(*)` in your aggregation CTE?
- `total_amount` looks wrong? Check you used `SUM(amount)` from `stg_payments`

<details>
<summary markdown="span">**💡 Why main_intermediate schema?**</summary>

dbt creates schemas based on your config:

- `+schema: intermediate` → creates `main_intermediate` schema
- `+schema: staging` → creates `main_staging` schema

The `main_` prefix comes from your profile's default schema.

</details>

### 🧪 Checkpoint 1: Push Intermediate Model

**Before pushing, verify your model passes the tests:**

**📍 In your terminal**, if you are not already in the challenge directory, navigate there now:

```bash
cd ..
```

Then run the checkpoint 1 tests:

```bash
pytest tests/test_intermediate_model.py -v
```

**If tests pass**, commit and push your work:

```bash
git add jaffle_shop_dbt/models/intermediate/
git commit -m "Add int_orders_with_payments model"
git push origin master
```

`int_orders_with_payments` is running — orders and payments joined, one row per order. Now you need to tell dbt where to put intermediate models by configuring the new layer in `dbt_project.yml`.

## 2. Configure the Intermediate Layer

### 2.1. Update dbt_project.yml

Your `dbt_project.yml` currently only has a `staging:` section. Add an `intermediate:` section under `models:` to tell dbt where to put intermediate models and how to materialise them:

```yaml
models:
  jaffle_shop_dbt:
    +materialized: view
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: view
      +schema: intermediate
```

### 🧪 Checkpoint 2: Push Configuration

**📍 In your terminal**, if you are not already in the challenge directory, navigate there now:

```bash
cd ..
```

Then run the checkpoint 2 tests:

```bash
pytest tests/test_intermediate_config.py -v
```

**If tests pass**, commit and push your work:

```bash
git add jaffle_shop_dbt/dbt_project.yml
git commit -m "Configure intermediate layer"
git push origin master
```

dbt now routes intermediate models to their own `main_intermediate` schema. The final step is to document this model so downstream mart builders know what each calculated column means.

### 2.2. Document in schema.yml

Create `models/intermediate/schema.yml` and document `int_orders_with_payments` and each of its output columns.

You wrote `schema.yml` files in the previous challenge — follow the same pattern here. A few things to note for intermediate models:

- The file lives at `models/intermediate/schema.yml` — a separate file from your staging `schema.yml`
- There are no `sources:` in this file — intermediate models reference other models via `{{ ref() }}`, not sources
- Document every output column; pay particular attention to calculated columns like `payment_count` and `total_amount` — explain what they represent, not just their names

<details>
<summary markdown="span">**💡 Hint: file skeleton**</summary>

```yaml
version: 2

models:
  - name: int_orders_with_payments
    description: "..."
    columns:
      - name: order_id
        description: "..."
      - name: ...
```

</details>

### 🧪 Checkpoint 3: Push Documentation

**📍 In your terminal**, if you are not already in the challenge directory, navigate there now:

```bash
cd ..
```

Then run the checkpoint 3 tests:

```bash
pytest tests/test_documentation.py -v
```

**If tests pass**, commit and push your work:

```bash
git add jaffle_shop_dbt/models/intermediate/schema.yml
git commit -m "Add intermediate model documentation"
git push origin master
```

The intermediate layer is built, configured, and documented. The pipeline is now three layers deep: staging → intermediate, with marts still to come.

## 3. Verify the Full Pipeline

**📍 In your terminal (inside `jaffle_shop_dbt/`)**, confirm all four models still build cleanly together:

**🗄️ Note:** If DBeaver is connected, disconnect it first (right-click connection → Disconnect) to avoid database locks.

```bash
dbt run
```

You should see 4 models complete successfully — 3 staging + 1 intermediate. If any fail, dbt will tell you which model and why.

> **Coming up in DBT Advanced:** dbt can generate interactive documentation that visualises the full dependency graph of your models — showing exactly how `stg_orders` and `stg_payments` feed into `int_orders_with_payments`. You'll learn how to generate and explore that lineage view in the next unit.

<details>
<summary markdown="span">**📚 Quick Reference**</summary>

```bash
# Run models
dbt run --select model_name
dbt run --select 'intermediate.*'
dbt run --select +model_name      # Model + upstream
dbt run --select model_name+      # Model + downstream

# Debug
dbt compile --select model_name
```

```sql
-- Reference models
SELECT * FROM {{ ref('model_name') }}

-- Template
WITH upstream_model AS (
    SELECT * FROM {{ ref('upstream') }}
),

calculations AS (
    SELECT
        col1,
        CAST(col2 * col3 AS DECIMAL(10,2)) AS calculated
    FROM upstream_model
)

SELECT * FROM calculations
```

</details>

---

## 🎉 Challenge Complete

The intermediate layer is where business logic lives — between clean staging models and stakeholder-facing marts.

**Key takeaways:**

- `{{ ref() }}` is how models depend on each other — never hardcode schema names
- Complex joins and aggregations belong in intermediate, so mart models stay simple
- If a JOIN produces more rows than expected, check for a missing `GROUP BY`
