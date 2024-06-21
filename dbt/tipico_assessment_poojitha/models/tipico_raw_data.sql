{{ config(
    materialized='view',
    schema='core'
) }}

select
    *
from
    tipico_raw_data_updated
