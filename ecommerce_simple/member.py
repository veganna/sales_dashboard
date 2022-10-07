from dataclasses import dataclass, field
from .models import Membership
from datetime import datetime, timedelta

@dataclass
class MemberCore:
    user : object = field(default_factory=object)
    membership : object = field(init=False, default_factory=object)

    def __post_init__(self):
        self.membership = self.get_membership()

    def get_membership(self):
        membership = Membership.objects.filter(membership_user=self.user).order_by('-created_at').first()
        return membership

    def is_member(self):
        try:
            if self.membership.membership_is_available:
                return True
        except:
            return False
        return False

    def check_membership(self):
        if self.is_member():
            if not self.membership.membership_is_available: return False
            life_time = self.membership.membership_life_time
            life_time = life_time.split(' ')
            if life_time[1] == 'day':
                life_time = timedelta(days=int(life_time[0]))
            elif life_time[1] == 'week':
                life_time = timedelta(weeks=int(life_time[0]))
            elif life_time[1] == 'month':
                life_time = timedelta(months=int(life_time[0]))
            elif life_time[1] == 'year':
                life_time = timedelta(years=int(life_time[0]))
            else:
                life_time = timedelta(days=0)

            if self.membership.updated_at + life_time < datetime.now():
                self.membership.membership_is_available = False
                self.membership.save()
                return False

            return True

        return False

    def renew_membership(self, membership=None):
        if not membership.membership_user == self.user: 
            raise Exception("Membership does not belong to user")

        if membership.is_abstract:
            raise Exception("Membership is abstract")

        if not membership:
            membership = self.membership
        
        if not self.membership and not membership:
            raise Exception("No membership found")

        membership.membership_is_available = False
        membership.save()
        return True

    def create_membership(self, membership_model_id=None):
        if not membership_model_id and not self.membership:
            raise Exception("No membership found")

        if not self.user:
            raise Exception("No user found")

        model_abstraction = Membership.objects.get(id=membership_model_id)

        new_membership = Membership(
            membership_user=self.user,
            membership_name=model_abstraction.membership_name,
            membership_price=model_abstraction.membership_price,
            membership_description=model_abstraction.membership_description,
            membership_life_time=model_abstraction.membership_life_time,
            membership_is_available=True,
            is_abstract=False
        )
        new_membership.save()
        return new_membership

    def get_members(self):
        members = Membership.objects.filter(membership_is_available=True, is_abstract = False).order_by('-membership_user__first_name')    
        users = ()
        for member in members:
            if member.membership_user not in users:
                users += (member.membership_user,) 
     
        return users

    def get_member(self, user_id):
        member = Membership.objects.filter(membership_is_available=True, is_abstract = False, membership_user=user_id).order_by('-created_at').first()
        user = member.membership_user
        return user

    def get_plans(self):
        plans = Membership.objects.filter(is_abstract=True)
        return plans
    



