def save(session, asset):
    session.add(asset)
    session.commit()
