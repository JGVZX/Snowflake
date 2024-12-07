with amounts_split as (
    select
        Company, split(amounts_raised, ', ') as amounts
    from {{ ref('stg_startups__companies') }}
)
, amounts_exploded as (
    select
        i.company, fi.value amount
    from amounts_split i, lateral flatten(input => i.amounts) fi
    where fi.value != 'undisclosed amount'
)
, amounts_converted as (
    select
        company, replace(replace(amount, '$', ''), ',', '')::int as amount
    from amounts_exploded
)
select * from amounts_converted