"""Manually removing user_email

Revision ID: remove_user_email
Revises: aaf6aa684c07
Create Date: 2025-04-02 01:03:31.433274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'remove_user_email'
down_revision = 'aaf6aa684c07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_column('user_email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_email', sa.VARCHAR(length=100), server_default=sa.text("'temp@example.com'"), nullable=False))

    # ### end Alembic commands ###
