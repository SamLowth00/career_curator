"""Add ON DELETE CASCADE to job_skills.job_id

Revision ID: 7b6e0536b19e
Revises: 
Create Date: 2025-07-27 18:06:10.717718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b6e0536b19e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Drop the old foreign key constraint
    op.drop_constraint('job_skills_job_id_fkey', 'job_skills', type_='foreignkey')
    # Add the new foreign key constraint with ON DELETE CASCADE
    op.create_foreign_key(
        'job_skills_job_id_fkey',
        'job_skills', 'jobs',
        ['job_id'], ['id'],
        ondelete='CASCADE'
    )

def downgrade():
    # Drop the new constraint
    op.drop_constraint('job_skills_job_id_fkey', 'job_skills', type_='foreignkey')
    # Recreate the old constraint without ON DELETE CASCADE
    op.create_foreign_key(
        'job_skills_job_id_fkey',
        'job_skills', 'jobs',
        ['job_id'], ['id']
        # No ondelete
    )
