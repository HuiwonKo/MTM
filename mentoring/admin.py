from django.contrib import admin

from .models import Post_By_Mentor, Post_By_Mentee, Bid_By_Mentee, Bid_By_Mentor, Comment, Like, Matched_Bid_By_Mentee, Matched_Bid_By_Mentor

admin.site.register(Post_By_Mentor)
admin.site.register(Post_By_Mentee)
admin.site.register(Bid_By_Mentor)
admin.site.register(Bid_By_Mentee)
admin.site.register(Matched_Bid_By_Mentor)
admin.site.register(Matched_Bid_By_Mentee)
admin.site.register(Comment)
