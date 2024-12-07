with categories_split as (
    select
        Company, split(categories, ', ') categories
    from {{ ref('stg_startups__companies') }}
)
, categories_exploded as (
    select
        i.company, fi.value category
    from categories_split i, lateral flatten(input => i.categories) fi
)
select * from categories_exploded