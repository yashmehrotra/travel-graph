from verak.helpers import response_error
from verak.models import (
    DbDoobieVote,
    session
)


def vote_doobie(user_id, doobie_id, vote):
    """
    Vote a doobie
    """
    # Fixed Vote Range
    if vote not in (1, -1):
        return response_error("Invalid vote")

    existing = session.query(DbDoobieVote).\
                filter(DbDoobieVote.user_id == user_id,
                       DbDoobieVote.doobie_id == doobie_id).\
                first()
    if existing:
        existing.vote = vote
        session.add(existing)
        session.commit()
        return True

    vote = DbDoobieVote(user_id=user_id,
                        doobie_id=doobie_id,
                        vote=vote)

    session.add(vote)
    session.commit()

    return True
