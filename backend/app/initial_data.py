from app.auth.security import create_salt_and_hashed_password
from app.config import get_settings
from app.database import get_db
from app.users.enums import RoleEnum
from app.users.models import User


def initial_data():
    print("start Initial data")

    db = next(get_db())

    user_db = db.query(User).where(User.role == RoleEnum.ADMIN).first()
    if user_db:
        return

    password = create_salt_and_hashed_password(password=get_settings().INIT_ADMIN_PASSWORD)
    user_db = User(
        nama="admin",
        email=get_settings().INIT_ADMIN_EMAIL,
        username=get_settings().INIT_ADMIN_USERNAME,
        password=password.password,
        salt=password.salt,
        role=RoleEnum.ADMIN,
    )

    db.add(user_db)
    db.commit()
    db.refresh(user_db)


if __name__ == "__main__":
    initial_data()
