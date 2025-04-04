from sqlalchemy import Table, Column, ForeignKey
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from infrastructure.db.models.registry import mapper_registry

# Association Table between User and Client
user_client_association_table = Table(
    "user_client_association",
    mapper_registry.metadata,
    Column("id", sa.Integer, primary_key=True, autoincrement=True),
    Column(
        "user_id", PGUUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    ),
    Column("client_id", sa.Integer, ForeignKey("client.id"), nullable=False),
)

user_role_association = Table(
    "user_role_association",
    mapper_registry.metadata,
    Column("id", sa.Integer, primary_key=True, autoincrement=True),
    Column(
        "user_id", PGUUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    ),
    Column("role_id", sa.Integer, ForeignKey("role.id"), nullable=False),
)

# user_strategy_association_table = Table(
#     "user_strategy_association",
#     mapper_registry.metadata,
#     Column("id", sa.Integer, primary_key=True, autoincrement=True),
#     Column(
#         "user_id", PGUUID(as_uuid=True), ForeignKey("user.id"), nullable=False
#     ),
#     Column(
#         "strategy_id",
#         PGUUID(as_uuid=True),
#         ForeignKey("strategy.id"),
#         nullable=False,
#     ),
#     Column("portfolio", JSONB),
#     Column("current_balance", sa.Float),
#     Column("start_date", sa.Date),
#     Column("end_date", sa.Date),
#     Column("in_process", sa.Boolean, default=True),
# )
