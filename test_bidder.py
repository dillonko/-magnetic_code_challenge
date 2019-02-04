import unittest

from bidder import Campaign, choose_best_campaign_for_user


# Sample campaigns for testing - the apple_mac and apple_ios campaigns have one keyword 
# in common 'apple'
apple_mac_campaign = Campaign(
    name="Apple Mac Products",
    bid_price=1.00,
    target_keywords=["apple", "macbook", "macbook pro", "imac", "power mac", "mavericks"],
)

apple_ios_campaign = Campaign(
    name="Apple IOS Products",
    bid_price=1.50,
    target_keywords=["apple", "ipad", "iphone", "ios", "appstore", "siri"],
)

marvel_comics_campaign = Campaign(
    name="Marvel Comics",
    bid_price=0.50,
    target_keywords=["spiderman", "hulk", "wolverine", "ironman", "captain america"],
)

marvel_heroes_campaign = Campaign(
    name="Marvel Heroes",
    bid_price=0.75,
    target_keywords=["spiderman", "wanda maximoff", "wolverine", "ironman", "black panther"],
)


class Matching(unittest.TestCase):
    def test_matching_None(self):
        matching = marvel_heroes_campaign.matching(["batman"])
        self.assertEqual(matching, 0)

    def test_matching_one(self):
        matching = marvel_heroes_campaign.matching(["batman", "spiderman"])
        self.assertEqual(matching, 1)
    
    def test_matching_more(self):
        matching = marvel_heroes_campaign.matching(["spiderman", "wanda maximoff"])
        self.assertEqual(matching, 2)

class BidderTest(unittest.TestCase):

    def test_it_picks_no_campaign_if_no_keywords_match(self):
        chosen_campaign = choose_best_campaign_for_user(
            user_search_terms=["batman"],
            campaigns=[marvel_comics_campaign],
        )
        self.assertIsNone(chosen_campaign)

    def test_it_chooses_a_campaign_if_search_terms_match_keywords(self):
        chosen_campaign = choose_best_campaign_for_user(
            user_search_terms=["spiderman"],
            campaigns=[marvel_comics_campaign],
        )
        self.assertEqual(marvel_comics_campaign, chosen_campaign)

    def test_it_chooses_campaign_with_most_overlapping_keywords(self):
        chosen_campaign = choose_best_campaign_for_user(
            user_search_terms=["spiderman"],
            campaigns=[marvel_comics_campaign, marvel_heroes_campaign],
        )
        self.assertEqual(marvel_heroes_campaign, chosen_campaign)

    def test_it_chooses_campaign_with_most_overlapping_keywords_and_campaigns(self):
        chosen_campaign = choose_best_campaign_for_user(
            user_search_terms=["spiderman", "wolverine"],
            campaigns=[marvel_comics_campaign, marvel_heroes_campaign],
        )
        self.assertEqual(marvel_heroes_campaign, chosen_campaign)
    
    def test_it_chooses_campaign_with_most_overlapping_keywords_and_campaigns_2(self):
        chosen_campaign = choose_best_campaign_for_user(
            user_search_terms=["spiderman", "wanda maximoff"],
            campaigns=[marvel_comics_campaign, marvel_heroes_campaign],
        )
        self.assertEqual(marvel_heroes_campaign, chosen_campaign)
    
    def test_it_chooses_campaign_with_most_overlapping_keywords_and_campaigns_3(self):
        chosen_campaign = choose_best_campaign_for_user(
            user_search_terms=["spiderman", "wanda maximoff"],
            campaigns=[marvel_heroes_campaign, marvel_comics_campaign],
        )
        self.assertEqual(marvel_heroes_campaign, chosen_campaign)
    
    def test_it_chooses_campaign_with_most_overlapping_keywords_and_campaigns_4(self):
        chosen_campaign = choose_best_campaign_for_user(
            user_search_terms=["spiderman", "hulk"],
            campaigns=[marvel_comics_campaign, marvel_heroes_campaign],
        )
        self.assertEqual(marvel_comics_campaign, chosen_campaign)


if __name__ == '__main__':
    unittest.main()
