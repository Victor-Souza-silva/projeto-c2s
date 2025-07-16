from sqlalchemy.orm import Session
from typing import Any, Type

class PostgreSQL:
    def __init__(self, SessionLocal):
        self.SessionLocal = SessionLocal

    def insert_one(self, entity: Any) -> Any:
        session: Session = self.SessionLocal()
        try:
            session.add(entity)
            session.commit()
            session.refresh(entity)  
            return entity
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_one(self, model: Type[Any], entity_id: Any, updated_entity: dict) -> Any:
        session: Session = self.SessionLocal()
        try:
            obj = session.query(model).filter(model.id == entity_id).first()
            if not obj:
                return None
            for key, value in updated_entity.items():
                setattr(obj, key, value)
            session.commit()
            session.refresh(obj)
            return obj
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_one(self, model: Type[Any], entity_id: Any) -> Any:
        session: Session = self.SessionLocal()
        try:
            obj = session.query(model).filter(model.id == entity_id).first()
            if not obj:
                return None
            session.delete(obj)
            session.commit()
            return obj
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def fetch_one(self, query: str, params: dict or None) -> Any:
        session: Session = self.SessionLocal()
        try:
            result = session.execute(query, params)
            return result.fetchone()
        finally:
            session.close()

    def fetch_all(self, query: str, params: dict or None) -> Any:
        session: Session = self.SessionLocal()
        try:
            result = session.execute(query, params)
            return result.fetchall()
        finally:
            session.close()
