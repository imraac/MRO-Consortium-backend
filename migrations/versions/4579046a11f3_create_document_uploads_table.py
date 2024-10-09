"""Create document_uploads table

Revision ID: 4579046a11f3
Revises: 
Create Date: 2024-10-09 12:52:03.420715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4579046a11f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document_uploads', schema=None) as batch_op:
        batch_op.add_column(sa.Column('upload_date', sa.DateTime(), nullable=False))
        batch_op.alter_column('registration_certificate',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('agency_profile',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('audit_report',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('ngo_consortium_mandate',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('icrc_code_of_conduct',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.drop_column('additional_accounts')
        batch_op.drop_column('full_name')
        batch_op.drop_column('email_copy')
        batch_op.drop_column('mailing_list')
        batch_op.drop_column('email_address')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document_uploads', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email_address', sa.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('mailing_list', sa.TEXT(), nullable=False))
        batch_op.add_column(sa.Column('email_copy', sa.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('full_name', sa.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('additional_accounts', sa.INTEGER(), nullable=False))
        batch_op.alter_column('icrc_code_of_conduct',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)
        batch_op.alter_column('ngo_consortium_mandate',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)
        batch_op.alter_column('audit_report',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)
        batch_op.alter_column('agency_profile',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)
        batch_op.alter_column('registration_certificate',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)
        batch_op.drop_column('upload_date')

    # ### end Alembic commands ###
