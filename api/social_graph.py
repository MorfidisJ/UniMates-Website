def get_social_score(user1, user2):
    # user1, user2: dicts with 'friends', 'avoid', 'past_roommates' lists
    boost = 0
    if 'friends' in user1 and user2['user_id'] in user1['friends']:
        boost += 0.1
    if 'avoid' in user1 and user2['user_id'] in user1['avoid']:
        boost -= 0.5
    if 'past_roommates' in user1 and user2['user_id'] in user1['past_roommates']:
        boost -= 0.2
    return boost

def diversity_regularization(user, candidate, all_matches):
    # Penalize if user is too similar to all previous matches
    similarities = [candidate['similarity'] for candidate in all_matches]
    if not similarities:
        return 0
    avg_sim = sum(similarities) / len(similarities)
    # Encourage diversity if avg_sim is high
    return -0.1 * (avg_sim > 0.8) 