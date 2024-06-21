{{ config(
    materialized='table',
    schema='core'
) }}

with raw_participants as (
    select
        raw_data.id as event_id,
        p
    from
        {{ ref('tipico_raw_data') }} a, a.participants as p   
)

select
    cast(p.id as bigint) as participant_id,
    event_id,
    p.name as name,
    p.position as position,
    p.abbreviation as abbreviation
from
    raw_participants
