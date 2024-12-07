with companies_source as (
    select
        Company, Status, Year_Founded, Categories, Investors, Amounts_raised,
        Headquarters_City, Headquarters_State, Headquarters_Country
    from {{ source('startups', 'companies') }}
)

select * from companies_source