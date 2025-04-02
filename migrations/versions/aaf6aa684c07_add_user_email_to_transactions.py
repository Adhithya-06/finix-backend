"""Add user_email to transactions

Revision ID: aaf6aa684c07
Revises: 
Create Date: 2025-04-01 23:39:55.643116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaf6aa684c07'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("transaction", schema=None) as batch_op:
        batch_op.drop_column("user_email")

def downgrade():
    with op.batch_alter_table("transaction", schema=None) as batch_op:
        batch_op.add_column(sa.Column(
            "user_email",
            sa.String(length=100),
            nullable=False,
            server_default="temp@example.com"
        ))

