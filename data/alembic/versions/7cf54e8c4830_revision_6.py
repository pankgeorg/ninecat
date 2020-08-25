"""Revision 6

Revision ID: 7cf54e8c4830
Revises: ef1800e283e6
Create Date: 2020-08-25 18:30:54.672813

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7cf54e8c4830"
down_revision = "ef1800e283e6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("sunspotgroupdata", schema="solardynamo")
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
    op.create_table(
        "sunspotgroupdata",
        sa.Column(
            "obs_dt_moment",
            sa.VARCHAR(length=11),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("dt", sa.DATE(), autoincrement=False, nullable=True),
        sa.Column(
            "obs_moment", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "kislovodsk_ssg", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "latitude",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "longitude",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "dist_to_center",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "obs_ssg_area", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "corr_ssg_area", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "largest_spot_area",
            sa.INTEGER(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "quantity", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "meridian_time",
            sa.VARCHAR(length=20),
            autoincrement=False,
            nullable=True,
        ),
        schema="solardynamo",
    )
    # ### end Alembic commands ###
