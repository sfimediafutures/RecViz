import json
with open('/Users/snorrealvsvag/MediaFutures/codeprojects/recommender-framework/backend/data/recommendations/users.json') as f:
    data = json.load(f)
for item in data:
    for recommender in item['recommendations'].keys():
        print(recommender, item['recommendations'][recommender], item['userId'])
        print(item['user_description_short'])
        print(item['user_description_long'])

        print(item['recommendations'][recommender])
        # original {'movieIds': [123, 412, 54123, 5123]} 123123




