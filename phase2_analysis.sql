--COLLECTION OF QUERIES SO FAR
---------------------------------------
--1. CUSTOMER CONVERSION FUNNEL (QUERY)
---------------------------------------
WITH session_funnel AS (
        SELECT
            session_id,
            MAX(CASE WHEN event_type = 'product_view' THEN 1 ELSE 0 END) AS product_view,
            MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 ELSE 0 END) AS add_to_cart,
            MAX(CASE WHEN event_type = 'checkout' THEN 1 ELSE 0 END) AS checkout,
            MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchase
        FROM events
        GROUP BY session_id
    ),

    funnel_counts AS (
        SELECT
            COUNT(*) AS sessions,
            SUM(product_view) AS product_views,
            SUM(add_to_cart) AS add_to_cart,
            SUM(checkout) AS checkout,
            SUM(purchase) AS purchase
        FROM session_funnel
    ),

    funnel_steps AS (
        SELECT
            1 AS step_order, 'Sessions' AS step, sessions
        FROM funnel_counts

        UNION ALL

        SELECT
            2, 'Product View', product_views
        FROM funnel_counts

        UNION ALL

        SELECT
            3, 'Add to Cart', add_to_cart
        FROM funnel_counts

        UNION ALL

        SELECT
            4, 'Checkout', checkout
        FROM funnel_counts

        UNION ALL

        SELECT
            5, 'Purchase', purchase
        FROM funnel_counts
    ),

    funnel_with_previous AS (
        SELECT
            step_order,
            step,
            sessions,
            LAG(sessions) OVER (ORDER BY step_order) AS previous_sessions
        FROM funnel_steps
    )

    SELECT
        step_order,
        step,
        sessions,
        ROUND(
            100 * sessions / NULLIF((SELECT sessions FROM funnel_steps WHERE step_order = 1), 0), 2
        )::float AS overall_conversion_pct,

        CASE
            WHEN previous_sessions IS NULL THEN 100.00
            ELSE ROUND(100 * sessions / NULLIF(previous_sessions, 0), 2)
        END::float AS step_conversion_pct,

        CASE
            WHEN previous_sessions IS NULL THEN 0
            ELSE previous_sessions - sessions
        END AS dropoff_sessions,

        CASE
            WHEN previous_sessions IS NULL THEN 0
            ELSE ROUND(100 * (previous_sessions - sessions) / NULLIF(previous_sessions, 0), 2)
        END::float AS dropoff_pct
    FROM funnel_with_previous
    ORDER BY step_order;


--------------------------------
--2. DEVICE PERFORMANCE (QUERY)
--------------------------------
 WITH session_summary AS(
        
        SELECT
            session_id, MAX(device) AS device, 
            MAX(CASE
                    WHEN event_type = 'purchase'
                    THEN 1
                    ELSE 0
                END
            ) AS purchased,
             
            SUM(
                CASE
                    WHEN event_type = 'purchase'
                    THEN revenue
                    ELSE 0
                END
            ) AS revenue
        
        FROM events
        
        GROUP BY session_id
    )
     
    SELECT
        device, COUNT(*) AS  sessions, SUM(purchased) AS purchases,
        ROUND (100 * SUM(purchased)/ NULLIF(COUNT(*), 0), 2)::float AS  conversion_rate,
        ROUND (SUM(revenue), 2)::float AS revenue,
        ROUND(SUM(revenue)/NULLIF(SUM(purchased), 0), 2)::float AS average_order_value,
        ROUND(SUM(revenue)/NULLIF(COUNT(*), 0), 2)::float AS revenue_per_session
    
    FROM session_summary
    GROUP BY device
    ORDER BY revenue DESC; 


----------------------------------
--3. PRODUCT PERFOMANCE (QUERY)
----------------------------------
WITH product_sessions AS(
        SELECT
            session_id, product_id, 
            MAX(CASE
                    WHEN event_type = 'product_view'
                    THEN 1
                    ELSE 0
                END) AS viewed,
            MAX(CASE
                    WHEN event_type = 'add_to_cart'
                    THEN 1 
                    ELSE 0
                END)AS added_to_cart,
            MAX(CASE
                    WHEN event_type = 'purchase'
                    THEN 1
                    ELSE 0
                END)AS purchased,
            SUM(CASE
                    WHEN event_type = 'purchase'
                    THEN revenue
                    ELSE 0
                END)AS revenue

        FROM events
        WHERE product_id IS NOT NULL
        GROUP BY session_id, product_id
    ),

    product_performance AS(
        SELECT
            product_id,
            SUM(viewed) AS product_views,
            SUM(added_to_cart) AS cart_sessions,
            SUM(purchased) AS purchases,
            ROUND(SUM(revenue),2)::float AS revenue,
            ROUND(100 * SUM(added_to_cart)/ NULLIF(SUM(viewed), 0), 2):: float AS view_to_cart_rate,
            ROUND(100 * SUM(purchased)/ NULLIF(SUM(viewed), 0), 2)::float AS view_to_purchase_rate
        
        FROM product_sessions
        GROUP BY product_id     
    )
    
    SELECT
        product_id, product_views, cart_sessions, purchases, revenue, view_to_cart_rate,
        view_to_purchase_rate,
        DENSE_RANK()
        OVER(ORDER BY revenue DESC) AS revenue_rank
    FROM product_performance
    ORDER BY revenue DESC;

--------------------------
--4. DAILY PERFORMANCE (QUERY)
--------------------------
 SELECT
        event_time::date AS event_date,
        COUNT(DISTINCT session_id) AS sessions,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN session_id END) AS purchases,
        ROUND(
            100 * COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN session_id END) 
            / NULLIF(COUNT(DISTINCT session_id), 0), 2)::float AS conversion_rate,
        ROUND(SUM(CASE WHEN event_type = 'purchase' THEN revenue ELSE 0 END), 2):: float AS revenue
        
    FROM events
    GROUP BY event_time::date
    ORDER BY event_date;

--------------------------
--5. CUSTOMER SEGMENTATION (QUERY)
---------------------------
 WITH customer_summary AS(
        SELECT
            user_id, COUNT(DISTINCT session_id) AS sessions,
            COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN session_id END) AS purchases,
            SUM(CASE WHEN event_type = 'purchase' THEN revenue ELSE 0 END) AS revenue
        
        FROM events
        GROUP BY user_id
    ),

    customer_segments AS(
        SELECT
            user_id, sessions, purchases, revenue,
            CASE
                WHEN purchases>=2 THEN 'Repeat Buyer'
                WHEN purchases = 1 THEN 'One-Time Buyer'
                ELSE 'Browser'
            END AS customer_segment
        
        FROM customer_summary
    )

    SELECT
        customer_segment, COUNT(*) AS customers, 
        SUM(sessions) AS sessions, SUM(purchases) AS purchases, SUM(revenue) AS revenue,
        ROUND(AVG(revenue), 2)::float AS revenue_per_customer
    FROM customer_segments
    GROUP by customer_segment
