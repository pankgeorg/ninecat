"""Revision 3

Revision ID: 06ee186e1290
Revises: e91873662656
Create Date: 2020-08-25 18:16:32.026739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "06ee186e1290"
down_revision = "e91873662656"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "duty",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("fsa_id", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("area", sa.String(), nullable=True),
        sa.Column("time", sa.String(), nullable=True),
        sa.Column("date", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="fsa",
    )
    op.create_table(
        "pharmacy",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("fsa_id", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("area", sa.String(), nullable=True),
        sa.Column("tel", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="fsa",
    )
    op.create_table(
        "place_text_search",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("text_input", sa.String(), nullable=True),
        sa.Column("input_type", sa.String(), nullable=True),
        sa.Column("locationbias", sa.String(), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=True),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="places",
    )
    op.create_table(
        "onecall_result",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("lon", sa.String(), nullable=True),
        sa.Column("lat", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("info", sa.String(), nullable=True),
        sa.Column("code", sa.Integer(), nullable=True),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="weather",
    )
    op.create_table(
        "place_id_detail",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("gmaps_id", sa.String(), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=True),
        sa.Column("search_id", sa.Integer(), nullable=True),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(
            ["search_id"], ["places.place_text_search.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="places",
    )
    op.drop_table("dim_date")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "dim_date",
        sa.Column("dt", sa.DATE(), autoincrement=False, nullable=True),
        sa.Column(
            "yr",
            sa.INTEGER(),
            sa.Computed("date_part('year'::text, dt)", persisted=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "week",
            sa.INTEGER(),
            sa.Computed(
                "((date_part('DOY'::text, dt))::integer / 7)", persisted=True
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "isoweek",
            sa.INTEGER(),
            sa.Computed("date_part('week'::text, dt)", persisted=True),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_table("place_id_detail", schema="places")
    op.drop_table("onecall_result", schema="weather")
    op.drop_table("place_text_search", schema="places")
    op.drop_table("pharmacy", schema="fsa")
    op.drop_table("duty", schema="fsa")
    # ### end Alembic commands ###
