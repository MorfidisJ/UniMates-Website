import numpy as np
from collections import Counter

def question_entropy(answers):
    # answers: list of values for a question across users
    counts = Counter(answers)
    total = sum(counts.values())
    probs = [c/total for c in counts.values()]
    return -sum(p * np.log2(p) for p in probs if p > 0)

def select_next_question(user_responses, all_user_responses, question_ids):
    # user_responses: dict of question_id -> answer for the current user
    # all_user_responses: list of dicts for all users
    # question_ids: list of all question ids
    unanswered = [qid for qid in question_ids if qid not in user_responses]
    entropies = {}
    for qid in unanswered:
        answers = [u.get(qid) for u in all_user_responses if qid in u]
        if answers:
            entropies[qid] = question_entropy(answers)
    if not entropies:
        return None
    # Return the question with highest entropy (most informative)
    return max(entropies, key=entropies.get) 