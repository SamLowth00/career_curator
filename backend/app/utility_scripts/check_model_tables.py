from app.db import Base
from app.models import Job, Skill, JobSkill
from app.auth.models import User
def list_registered_models():
    print("📦 Registered tables in Base.metadata:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")

    print("\n🧠 Mapped model classes:")
    for mapper in Base.registry.mappers:
        print(f"  - {mapper.class_.__name__} ({mapper.class_})")

if __name__ == "__main__":
    list_registered_models()