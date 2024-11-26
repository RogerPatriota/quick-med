"""Initial Migration

Revision ID: 7e8f36b5e2d5
Revises: 
Create Date: 2024-11-20 10:44:31.774703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e8f36b5e2d5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hospitais',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=150), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('endereco', sa.String(length=50), nullable=True),
    sa.Column('especialidade', sa.String(length=50), nullable=True),
    sa.Column('senha', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=150), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('senha', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('consultas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('idUser', sa.Integer(), nullable=True),
    sa.Column('idHospitail', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['idHospitail'], ['hospitais.id'], ),
    sa.ForeignKeyConstraint(['idUser'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('consultas')
    op.drop_table('usuarios')
    op.drop_table('hospitais')
    # ### end Alembic commands ###
