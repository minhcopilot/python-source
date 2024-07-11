from datetime import datetime
import sys
import os
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
# from app.config.email import fm
from app.config.database import Base, get_session
from app.models.user import User
from app.config.security import hash_password
# from app.services.user import _generate_tokens

USER_NAME = "Minh"
USER_EMAIL = "bai1bai0147@gmail.com"
USER_PASSWORD = "minhdev#123"
#Quản lý các phiên kiểm thử các phiên kết nối csdl
engine = create_engine("sqlite:///./fastapi.db")
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#Trả về phiên kết nối cơ sở dữ liệu
@pytest.fixture(scope="function")
def test_session() -> Generator:
    session = SessionTesting()
    try:
        yield session
    finally:
        session.close()

#Tạo ra các bảng rồi trả về app rồi kiểm thử sau đó xoá toàn bộ các bảng vừa tạo
@pytest.fixture(scope="function")
def app_test():
    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)

#Mô phỏng các yêu cầu HTTP đến server và tắt việc gửi email
@pytest.fixture(scope="function")
def client(app_test, test_session):
    def _test_db():
        try:
            yield test_session
        finally:
            pass

    app_test.dependency_overrides[get_session] = _test_db
    # fm.config.SUPPRESS_SEND = 1
    return TestClient(app_test)
#Xác thực client bằng token
@pytest.fixture(scope="function")
def auth_client(app_test, test_session, user):
    def _test_db():
        try:
            yield test_session
        finally:
            pass

    app_test.dependency_overrides[get_session] = _test_db
    # fm.config.SUPPRESS_SEND = 1
    data = _generate_tokens(user, test_session)
    client = TestClient(app_test)
    client.headers['Authorization'] = f"Bearer {data['access_token']}"
    return client

#Tạo các đối tượng không hoạt động, đã xác minh, chưa xác minh
@pytest.fixture(scope="function")
def inactive_user(test_session):
    model = User()
    model.name = USER_NAME
    model.email = USER_EMAIL
    model.password = hash_password(USER_PASSWORD)
    model.updated_at = datetime.utcnow()
    model.is_active = False
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model

@pytest.fixture(scope="function")
def user(test_session):
    model = User()
    model.name = USER_NAME
    model.email = USER_EMAIL
    model.password = hash_password(USER_PASSWORD)
    model.updated_at = datetime.utcnow()
    model.verified_at = datetime.utcnow()
    model.is_active = True
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model

@pytest.fixture(scope="function")
def unverified_user(test_session):
    model = User()
    model.name = USER_NAME
    model.email = USER_EMAIL
    model.password = hash_password(USER_PASSWORD)
    model.updated_at = datetime.utcnow()
    model.is_active = True
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model