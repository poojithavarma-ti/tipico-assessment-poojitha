{{ config(
    materialized='table',
    schema='core'
) }}

with raw_markets as (
    select
        raw_data.id as event_id,
        m
    from
        {{ ref('tipico_raw_data') }} a, a.markets as m
)

select
    m.id market_id,
    m.name,
    m.type,
    m.status,
    cast(m.mostBalancedLine as boolean) as most_balanced_line,
    cast(m.sgpEligable as boolean) as sgp_eligible,
    event_id
from
    raw_markets
