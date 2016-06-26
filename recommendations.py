__author__ = 'wangwei'

# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}


import math

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs, person1, person2):
    # Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    # if they ha ve no ratings in common, return 0
    if len(si) == 0:
        return 0
    # Add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])
    return 1 / (1 + sum_of_squares)


def sim_distance2(usersprefs, userid1, userid2):
    si = {}
    for item in usersprefs[userid1]:
        if item in usersprefs[userid2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    distance = sum([pow(usersprefs[userid1][item] - usersprefs[userid2][item], 2)
                    for item in usersprefs[userid1] if item in usersprefs[userid2]])
    return 1 / (1 + distance)

# Returns a Pearson-correlation based similarity score for person1 and person2
def sim_pearson(usersprefs, userid1, userid2):
    si = {}
    for item in usersprefs[userid1]:
        if item in usersprefs[userid2]:
            si[item] = 1
    n = len(si)
    if n == 0: return 0
    sum1 = sum([usersprefs[userid1][item] for item in si])
    sum2 = sum([usersprefs[userid2][item] for item in si])

    sum1sq = sum([pow(usersprefs[userid1][item], 2) for item in si])
    sum2sq = sum([pow(usersprefs[userid2][item], 2) for item in si])

    psum = sum([usersprefs[userid1][item] * usersprefs[userid2][item] for item in si])

    # calculate the pearson score
    num = psum - (sum1*sum2/n)
    den = math.sqrt((sum1sq-pow(sum1, 2)/n)*(sum2sq-pow(sum2, 2)/n))

    if den == 0:
        return 0
    r = num / den
    return r


# Returns the best matches for person from the 'usersprefs' dictionary.
# Number of results and similarity function are optional params.
def topMatches(usersprefs, userid1, n=5, similarity=sim_pearson):
    scores = [(similarity(usersprefs, userid1, other), other) for other in usersprefs if other != userid1]

    # sort the list
    scores.sort()
    scores.reverse()
    return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(usersprefs, userid1, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in usersprefs:
        # don't compare me to myself
        if other == userid1: continue
        sim = similarity(usersprefs, userid1, other)

        if sim <= 0: continue
        for item in usersprefs[other]:
            # only score movies I haven't seen yet
            if item not in usersprefs[userid1] or usersprefs[userid1] == 0:
                totals.setdefault(item, 0)
                totals[item] += sim * usersprefs[other][item]
                simSums.setdefault(item, 0)
                simSums[item] += sim
    #print totals.items()
    rankings = [(totals[item]/simSums[item], item) for item in totals]
    # another way is
    # rankings = [(total/simSums[item], item) for item,total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings
