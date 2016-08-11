from .model

def auction_algo():
    for post in Post_By_Mentor.objects.all():
        if post.date == timezone.now():
            mentee_num = post.capacity
            li = list(Bid_By_Mentee.objects.filter(mentor == post.author))
            li_sorted = sorted(sorted(li, key=lambda li:li["price"]),key=lambda li:li["time"],reverse=True)
            li_ranked = li_sorted[:mentee_num]
            for i in range(mentee_num):
                li_ranked[i].price = li_ranked[mentee_num-1].price