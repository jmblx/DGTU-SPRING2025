"""empty message

Revision ID: 870b98d95a0e
Revises: 
Create Date: 2025-04-05 15:44:55.236160

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Float, String

# revision identifiers, used by Alembic.
revision: str = "870b98d95a0e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "race",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "runner",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("colour", sa.String(length=20), nullable=False),
        sa.Column(
            "reaction_time",
            sa.Float(precision=3, decimal_return_scale=2),
            nullable=False,
        ),
        sa.Column(
            "acceleration",
            sa.Float(precision=4, decimal_return_scale=2),
            nullable=False,
        ),
        sa.Column(
            "max_speed", sa.Float(precision=4, decimal_return_scale=2), nullable=False
        ),
        sa.Column(
            "speed_decay", sa.Float(precision=4, decimal_return_scale=3), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "race_result",
        sa.Column("race_id", sa.Integer(), nullable=False),
        sa.Column("runner_id", sa.Integer(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column(
            "finish_time", sa.Float(precision=5, decimal_return_scale=2), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["race_id"],
            ["race.id"],
        ),
        sa.ForeignKeyConstraint(
            ["runner_id"],
            ["runner.id"],
        ),
        sa.PrimaryKeyConstraint("race_id", "runner_id"),
    )
    runners_data = [
        {
            "colour": "красный",
            "reaction_time": 0.12,
            "acceleration": 3.80,
            "max_speed": 9.85,
            "speed_decay": 0.085,
        },
        {
            "colour": "синий",
            "reaction_time": 0.18,
            "acceleration": 4.20,
            "max_speed": 10.10,
            "speed_decay": 0.120,
        },
        {
            "colour": "жёлтый",
            "reaction_time": 0.23,
            "acceleration": 3.60,
            "max_speed": 9.75,
            "speed_decay": 0.140,
        },
        {
            "colour": "зелёный",
            "reaction_time": 0.15,
            "acceleration": 3.95,
            "max_speed": 10.25,
            "speed_decay": 0.095,
        },
        {
            "colour": "фиолетовый",
            "reaction_time": 0.22,
            "acceleration": 4.05,
            "max_speed": 9.65,
            "speed_decay": 0.110,
        },
        {
            "colour": "чёрный",
            "reaction_time": 0.10,
            "acceleration": 4.50,
            "max_speed": 10.50,
            "speed_decay": 0.050,
        },
    ]

    op.bulk_insert(
        sa.table(
            "runner",
            sa.Column("colour", String(20)),
            sa.Column("reaction_time", Float(precision=3, decimal_return_scale=2)),
            sa.Column("acceleration", Float(precision=4, decimal_return_scale=2)),
            sa.Column("max_speed", Float(precision=4, decimal_return_scale=2)),
            sa.Column("speed_decay", Float(precision=4, decimal_return_scale=3)),
        ),
        runners_data,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("race_result")
    op.drop_table("runner")
    op.drop_table("race")
    # ### end Alembic commands ###
