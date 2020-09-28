from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _


class User(AbstractUser):
    pass


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_Listing")
    title = models.CharField(max_length=64, help_text="The title to be displayed for the listing")
    description = models.CharField(max_length=2048, help_text="Tell users more about your product! (Hint, make it interesting) "
                                                              )
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2, help_text="Starting price (in USD) "
                                                                                 "of product ")
                                                                                 
    image_url = models.CharField(max_length=2048, blank=True, help_text="Optional, but if you want to "
                                                                        "include an image for your product, "
                                                                        "use url format(http://....jpg)!")
    category = models.CharField(max_length=64, blank=True, help_text="Optional (e.g.Fashion, Toys, Electronics, Home, etc.)"
                                                                    )
    watchlist_users = models.ManyToManyField(User, blank=True, related_name="watchlist_items")

    closed = models.BooleanField(default=False)

    def current_price(self):
        return max([bid.value_offer for bid in self.bids.all()]+[self.starting_bid])

    def no_of_bids(self):
        return len(self.bids.all())

    def current_winning_bidder(self):
        return self.bids.get(value_offer=self.current_price()).user if self.no_of_bids() > 0 else None

    def __str__(self):
        return f'{self.title} by {self.owner}: {self.description}'


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    value_offer = models.DecimalField(max_digits=8, decimal_places=2, help_text="How much are you offering to pay for "
                                                                                "this item?")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_made")

    def clean(self):
        # Do not accept offer lower than current price of listing
        print(self.value_offer)
        print(self.listing.current_price())
        if self.value_offer and self.listing.current_price():
            if self.value_offer <= self.listing.current_price():
                raise ValidationError({'value_offer': _('Your bid must be higher than the current '
                                                        'price of the item!')})

    def __str__(self):
        return f"{self.user} offers to pay ${self.value_offer} for the listing: {self.listing}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=2048)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.author} says {self.content} for listing: {self.listing}"
