with int_companies_source as (
    select
        Company, Status, Year_Founded,
        Headquarters_City, Headquarters_State, Headquarters_Country
    from {{ ref('stg_startups__companies') }}
)

select * from int_companies_source