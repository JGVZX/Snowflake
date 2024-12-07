with founders_source as (
    select
        f.Founder, f.Company, f.Gender
    from {{ ref('stg_startups__founders') }} f
    full join {{ ref('stg_startups__companies') }} c
    on c.Company = f.Company
    where c.Company is not null and f.founder is not null
)

select * from founders_source