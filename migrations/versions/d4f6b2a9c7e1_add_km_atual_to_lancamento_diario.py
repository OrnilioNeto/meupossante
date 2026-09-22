"""add km_atual to lancamento_diario

Revision ID: d4f6b2a9c7e1
Revises: c1d3a1f8b9e2
Create Date: 2026-09-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4f6b2a9c7e1'
down_revision = 'c1d3a1f8b9e2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('lancamento_diario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('km_atual', sa.Integer(), nullable=True))


def downgrade():
    with op.batch_alter_table('lancamento_diario', schema=None) as batch_op:
        batch_op.drop_column('km_atual')
