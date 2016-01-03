from verak.settings import vote_range
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
    if vote not in vote_range:
        return response_error("Invalid vote")

    vote = DbDoobieVote(user_id=user_id,
                        doobie_id=doobie_id,
                        vote=vote)

    session.add(vote)
    session.commit()

    return True
