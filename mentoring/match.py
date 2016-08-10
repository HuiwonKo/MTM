from mentoring.models import Matched_Bid_By_Mentee, Matched_Bid_By_Mentor, Bid_By_Mentee, Post_By_Mentor
'''
views.py에서? 어떤 mentoring.models의 datetime-1주일이 오늘(timezone.now)과 같다면
이 함수를 호출하는 그 부분이 만들어져야함. 또 그 인자로 mentor의 이름을 받도록.
또 Bid_By_Mentee에서 mentor든 mentee든 id 값으로 받아와야 될듯.
author가 어떤 건지 잘 모르겠다.
post와 bid의 연관성 부족.
지금대로라면 Post의 id도 인자로 넘겨줘야됨.
'''
def auction_algo(mentor,post_id):
	bid_list = list(Bid_By_Mentee.objects.filter(mentor=mentor).values())
	sorted_bid_list = sorted(sorted(bid_list,key=lambda bid_list:bid_list["created_at"]),key=lambda bid_list:bid_list["price"],reverse=True)
	capacity = list(Post_By_Mentor.objects.filter(author=mentor).values())
	li_ranked = li_sorted[:mentee_num]
	return li_ranked