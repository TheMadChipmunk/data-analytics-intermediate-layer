WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

payments AS (
    SELECT
        order_id,
        COUNT(*)     AS payment_count,
        SUM(amount)  AS total_amount
    FROM {{ ref('stg_payments') }}
    GROUP BY order_id
    -- GROUP BY AVANT la jointure pour éviter la multiplication des lignes
),

int_orders_with_payments AS (
    SELECT
        orders.order_id,
        orders.customer_id,
        orders.order_date,
        orders.status,
        COALESCE(payments.payment_count, 0)  AS payment_count,
        COALESCE(payments.total_amount, 0)   AS total_amount
    FROM orders
    LEFT JOIN payments ON orders.order_id = payments.order_id
    -- LEFT JOIN : garder TOUTES les commandes, même sans paiement
)

SELECT * FROM int_orders_with_payments
