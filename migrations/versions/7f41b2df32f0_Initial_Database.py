"""Initial Database

Revision ID: 7f41b2df32f0
Revises: None
Create Date: 2016-06-21 15:23:54.909713

"""

# revision identifiers, used by Alembic.
revision = '7f41b2df32f0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_role_created_at'), 'role', ['created_at'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_created_at'), 'users', ['created_at'], unique=False)
    op.create_table('user_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'role_id', name='un_user_role')
    )
    op.create_index(op.f('ix_user_role_created_at'), 'user_role', ['created_at'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_user_role_created_at'), table_name='user_role')
    op.drop_table('user_role')
    op.drop_index(op.f('ix_users_created_at'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_role_created_at'), table_name='role')
    op.drop_table('role')