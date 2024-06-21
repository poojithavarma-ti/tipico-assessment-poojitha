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
),
market_outcomes as (
    select m.id, outcomes
    from raw_markets rm, rm.m.outcomes as outcomes
)
select
    id as market_id,
    outcomes.id as outcome_id,
    outcomes.name as name,
    cast(outcomes.isTraded as boolean) as is_traded,
    cast(outcomes.formatDecimal as float) as format_decimal,
    outcomes.formatAmerican as format_american,
    outcomes.status as status,
    cast(outcomes.trueOdds as float) as true_odds
from market_outcomes
