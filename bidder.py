"""
Simple ad-exchange bidder exercise.

The Magnetic Real-time-bidding (RTB) platform decides whether or not to bid to
show adverts to users on auctions sent out from ad-exchanges like DoubleClick. The
core goal of the system is to choose the advert which is most relevant to the end-user.

A large part of the logic for deciding whether or not to bid on an auction, and for
which campaign to choose, is based on whether the user has searched for any keywords
associated with campaigns in our system.

For example if we have a campaign for Phones4U we would be targeting keywords like
"iphone","android","nexus", "samsung galaxy", etc. The higher the overlap between
a user's search history and a campaign's keyword set the more relevant that advert
would be to the user.

The exercise below involves completing a simplified version of this bid-decision
algorithm.
"""
from collections import Counter, namedtuple
from operator import attrgetter

class Campaign:
    """An ad campaign we can serve to users."""

    def __init__(self, name, bid_price, target_keywords):
        """
        :param name: unique name for this campaign, e.g. "Nike Shoes Summer 2014"
        :param bid_price: amount to bid on any auctions when serving this campaign, e.g. 0.5
        :param target_keywords: list of keywords we are targeting for this campaign
        """

        self.name = name
        self.bid_price = bid_price
        self.target_keywords = target_keywords

    def __repr__(self):
        return (f"{self.__class__.__name__} ({self.name}, {self.bid_price}, {self.target_keywords})")

    def matching(self,user_search_terms):
        count = 0
        for word in self.target_keywords:
            if word in user_search_terms:
                count += 1
        return count


def choose_best_campaign_for_user(user_search_terms, campaigns):
    """Returns the best campaign to serve for a given user or None if
    no campaigns are applicable. A user can be served a campaign if they
    have searched for at least one keyword configured for the campaign.

    The "best" campaign to serve is the one with the most search term
    matches.

    If two or more campaigns have the same number of matches then the
    one with the highest bid_price should be served.

    If two or more campaigns have the same number of matches and the
    same bid_price, then either one may be returned.

    :param user_search_terms: list of search terms. assume normalized
    :param campaigns: a collection of Campaign objects
    :return: A single campaign object considered the 'best' campaign to show 
            for the search terms provided or None if no campaigns are eligible
    """

    # TODO: implement decision logic.
    total = []
    Campaign_metrics = namedtuple("Campaign_metrics", "number_of_matches campaign")
    for campaign in campaigns:
        total.append(Campaign_metrics(campaign.matching(user_search_terms), campaign))

    total = sorted(total, key=lambda tup: tup.number_of_matches, reverse=True)

    if len(total) == 1 and total[0].number_of_matches > 0:
        return total[0].campaign
    
    tied_campaign = []
    if len(total) >= 2:
        max_mataches = total[0].number_of_matches
        for number_of_matches, campaign in total:
            if number_of_matches == max_mataches:
                tied_campaign.append(campaign)
        return max(tied_campaign, key=attrgetter('bid_price'))
