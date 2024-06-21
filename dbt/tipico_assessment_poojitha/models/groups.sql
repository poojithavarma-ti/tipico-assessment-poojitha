{{ config(
    materialized='table',
    schema='core'
) }}

with raw_groups as (
    select
        cast(json_extract_path_text(json_serialize(raw_data), 'id') as bigint) as event_id,
        group_info,
        json_extract_path_text(json_serialize(group_info), 'parentGroup') as parent_group,
        json_extract_path_text(json_serialize(group_info), 'parentGroup', 'parentGroup') as parent_parent_group
    from
        {{ ref('tipico_raw_data') }}
)

select
    cast(json_extract_path_text(json_serialize(group_info), 'id') as bigint) as group_id,
    event_id,
    json_extract_path_text(json_serialize(group_info), 'name') as name,
    cast(json_extract_path_text(json_serialize(json_parse(parent_group)), 'id') as bigint) as parent_group_id,
    json_extract_path_text(json_serialize(json_parse(parent_group)), 'name') as parent_group_name,
    cast(json_extract_path_text(json_serialize(json_parse(parent_parent_group)), 'id') as bigint) as parent_parent_group_id,
    json_extract_path_text(json_serialize(json_parse(parent_parent_group)), 'name') as parent_parent_group_name
from
    raw_groups
