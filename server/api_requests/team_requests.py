'''
Team Requests
'''


def get_teams(client):
    db = client['epl']
    collection = db['teams']
    cursor = collection.find({})
    return cursor


def get_teams_stats(client):
    pipeline = [
        {
            "$group": {
                "_id": "$team_id",
                "assists": {"$sum": "$assists"},
                "goals": {"$sum": "$goals_scored"},
                "expected_assists_total": {"$sum": "$expected_assists_total"},
                "expected_goals_total": {"$sum": "$expected_goals_total"},
                "total_points": {"$sum": "$total_points"},
            }
        }
    ]
    db = client['epl']
    collection = db['players']
    cursor = collection.aggregate(pipeline)
    return cursor


def get_stats_gameweek(client):
    pipeline = [
        {
            "$group": {
                "_id": {
                    "team_id": "$team",  # Group by team_id from Stats collection
                    "gameweek": "$gameweek"  # Group by gameweek
                },
                # Sum goals for each team-gameweek
                "goals": {"$sum": "$goals_scored"},
                # Sum assists for each team-gameweek
                "assists": {"$sum": "$assists"},
                # Sum goals conceded for each team-gameweek
                "goals_conceded": {"$max": "$goals_conceded"}
            }
        },
        {
            # Sort gameweeks within each team (ascending order)
            "$sort": {"_id.gameweek": 1, "_id.team_id": 1}
        },
        {
            "$group": {
                "_id": "$_id.team_id",  # Group by final team_id
                "gameweeks": {
                    "$push": {
                        "gameweek": "$_id.gameweek",
                        "goals": "$goals",
                        "assists": "$assists",
                        "goals_conceded": "$goals_conceded"
                    }
                }
            }
        },
        {
            "$sort": {"_id": 1}
        }
    ]
    db = client['epl']
    collection = db['stats']
    cursor = collection.aggregate(pipeline)
    return cursor
