with founders_source as (
    select
        Founder, Company, Gender
    from {{ source("startups","founders") }}
)

select * from founders_source