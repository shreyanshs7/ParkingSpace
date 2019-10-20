from models import db

def upsert(user):
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return user