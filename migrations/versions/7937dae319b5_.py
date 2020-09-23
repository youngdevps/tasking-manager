"""empty message

Revision ID: 7937dae319b5
Revises: ba778ef9c615
Create Date: 2020-09-21 17:17:10.542429

"""
from alembic import op
import sqlalchemy as sa
import requests


# revision identifiers, used by Alembic.
revision = "7937dae319b5"
down_revision = "ba778ef9c615"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    fetch_country_combinations = (
        "select distinct(unnest(country)) from projects where country is not null;"
    )
    country_combinations = conn.execute(fetch_country_combinations)
    for country in country_combinations:
        country = country[0]
        print(country)
        url = (
            "https://nominatim.openstreetmap.org/search?country="
            + country
            + "&format=jsonv2&accept-language=en"
        )
        print(url)
        country_search = requests.get(url).json()
        print(country_search)
        print(country_search[0].get("display_name"))
        lat = country_search[0].get("lat")
        lng = country_search[0].get("lon")
        print(lat, lng)
        print("search done")
        url = "{0}/reverse?format=jsonv2&lat={1}&lon={2}&accept-language=en".format(
            "https://nominatim.openstreetmap.org", lat, lng
        )
        print(url)
        country_info = requests.get(url).json()
        if country_info is not None:
            print(country_info)
        # update_project = "update projects set country ="+ country_name + "where country=" + country + ";"
        # conn.execute(update_project)
        # print(country_search)
        # if country_search:


def downgrade():
    pass
