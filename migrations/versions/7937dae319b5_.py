"""empty message

Revision ID: 7937dae319b5
Revises: ba778ef9c615
Create Date: 2020-09-21 17:17:10.542429

"""
from alembic import op
import requests


# revision identifiers, used by Alembic.
revision = "7937dae319b5"
down_revision = "ba778ef9c615"
branch_labels = None
depends_on = None
nominatim_base_url = "https://nominatim.openstreetmap.org"
nominatim_data_format = "&format=jsonv2&accept-language=en"


def upgrade():
    conn = op.get_bind()
    # fetch existing country names
    fetch_countries = (
        "select distinct(unnest(country)) from projects where country is not null;"
    )
    countries = conn.execute(fetch_countries)
    for country in countries:
        country = country[0]
        # search by name
        url = nominatim_base_url + "/search?country=" + country + nominatim_data_format
        country_search = requests.get(url).json()
        if country_search == []:
            url = nominatim_base_url + "/search?q=" + country + nominatim_data_format
            country_search = requests.get(url).json()
        lat = country_search[0].get("lat")
        lng = country_search[0].get("lon")
        # reverse geocode to fetch English names
        url = "{0}/reverse?lat={1}&lon={2}{3}".format(
            nominatim_base_url, lat, lng, nominatim_data_format
        )
        country_info = requests.get(url).json()
        if country_info != []:
            updated_country_name = country_info.get("address").get("country")
            if country != updated_country_name:
                special_char = updated_country_name.find("'")
                if special_char >= 0:
                    updated_country_name = (
                        updated_country_name[:special_char]
                        + "'"
                        + updated_country_name[special_char:]
                    )
                update_project = (
                    "update projects set country = '{\""
                    + updated_country_name
                    + "\"}' where country @> ARRAY['"
                    + country
                    + "']::varchar[]"
                    + ";"
                )
                conn.execute(update_project)


def downgrade():
    pass
