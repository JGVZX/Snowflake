with investors_split as (
    select
        Company, split(investors, ', ') investors
    from {{ ref('stg_startups__companies') }}
)
, investors_exploded as (
    select
        i.company, fi.value investor
    from investors_split i, lateral flatten(input => i.investors) fi
)
select * from investors_exploded