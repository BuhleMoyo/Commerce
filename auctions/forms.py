from django.forms import ModelForm, Textarea
from auctions.models import Listing, Bid


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 6}),
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['value_offer']