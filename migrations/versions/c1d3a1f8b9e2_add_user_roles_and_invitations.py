"""add user roles and invitations

Revision ID: c1d3a1f8b9e2
Revises: bae5c57e99f5
Create Date: 2026-07-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1d3a1f8b9e2'
down_revision = 'bae5c57e99f5'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))

    op.create_table(
        'invitation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.Column('created_by_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    op.create_index(op.f('ix_invitation_email'), 'invitation', ['email'], unique=False)
    op.create_index(op.f('ix_invitation_token'), 'invitation', ['token'], unique=False)

    op.execute("UPDATE user SET role='user' WHERE role IS NULL")
    op.execute("UPDATE user SET is_active=1 WHERE is_active IS NULL")


def downgrade():
    op.drop_index(op.f('ix_invitation_token'), table_name='invitation')
    op.drop_index(op.f('ix_invitation_email'), table_name='invitation')
    op.drop_table('invitation')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_active')
        batch_op.drop_column('role')
