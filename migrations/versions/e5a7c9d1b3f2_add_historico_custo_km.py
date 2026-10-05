"""add historico_custo_km

Revision ID: e5a7c9d1b3f2
Revises: d4f6b2a9c7e1
Create Date: 2026-10-05 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5a7c9d1b3f2'
down_revision = 'd4f6b2a9c7e1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'historico_custo_km',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.String(length=20), nullable=False),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('km_base', sa.Float(), nullable=True),
        sa.Column('preco_litro', sa.Float(), nullable=True),
        sa.Column('consumo', sa.Float(), nullable=True),
        sa.Column('data_registro', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_historico_custo_km_user_id'), 'historico_custo_km', ['user_id'], unique=False
    )


def downgrade():
    op.drop_index(op.f('ix_historico_custo_km_user_id'), table_name='historico_custo_km')
    op.drop_table('historico_custo_km')
