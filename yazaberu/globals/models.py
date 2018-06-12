from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class SocialNetwork(models.Model):
    class Meta:
        abstract = True
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    sn_id = models.CharField(max_length=512)
        
class Facebook(SocialNetwork):
    @classmethod
    def register_user(cls, provider):
        print('Facebook.register_user', provider.info)
        #user_id, first_name, last_name, email, password=None, company=None, photo=None
        p = Profile.create( user_id=provider.info['email'], 
                            first_name=provider.info['first_name'],
                            last_name=provider.info['last_name'],
                            email=provider.info['email'],
                            photo=Avatar.create(url=provider.info['picture']['data']['url'])
                            )
        print(provider.info)
        sn = Facebook(name='Facebook', sn_id=provider.info['link'])
        sn.profile = p
        sn.save()
        return p, sn
        
    @classmethod
    def update_user(cls, profile, provider):
        profile.update(
            first_name=provider.info['first_name'],
            last_name = provider.info['last_name'],
            email=provider.info['email'],
            photo={'url':provider.info['picture']['data']['url'], })
    
class Vkontakte(SocialNetwork):
    @classmethod
    def register_user(cls, provider):
        p = Profile.create(first_name=provider.info['first_name'], last_name=provider.info['last_name'], email='')
        #print(provider.info)
        sn = Vkontakte(sn_id=provider.info['uid'])
        sn.profile = p
        sn.save()
        return p, sn
        
class Yandex(SocialNetwork):
    @classmethod
    def register_user(cls, provider):
        p = Profile.create(first_name=provider.info['first_name'], last_name=provider.info['last_name'], email='')
        print(provider.info)
        sn = Yandex(sn_id=provider.info['id'])
        sn.profile = p
        sn.save()
        return p, sn
        
class Odnoklassniki(SocialNetwork):
    @classmethod
    def register_user(cls, provider):
        p = Profile.create(first_name=provider.info['first_name'], last_name=provider.info['last_name'], email='')
        print(provider.info)
        sn = Odnoklassniki(sn_id=provider.info['id'])
        sn.profile = p
        sn.save()
        return p, sn

class GooglePlus(SocialNetwork):
    @classmethod
    def register_user(cls, provider):
        p = Profile.create(first_name=provider.info['given_name'], last_name=provider.info['family_name'], email=provider.info['email'])
        print(provider.info)
        sn = GooglePlus(sn_id=provider.info['link'])
        sn.profile = p
        sn.save()
        return p, sn
        
    @classmethod
    def update_user(cls, profile, provider):
        profile.update(
            user_id=provider.info['email'],
            first_name=provider.info['given_name'],
            last_name = provider.info['family_name'],
            email=provider.info['email'],
            photo={'url':provider.info['picture'], })

class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=32)
    avatar = models.OneToOneField('Avatar', null=True, on_delete=models.CASCADE)
    rider_rating = models.IntegerField(default=0)
    sender_rating = models.IntegerField(default=0)
    join_date = models.DateTimeField(auto_now_add=True)
    #don't calculate every time, update counters on delivery completion
    sent_parcel_count = models.IntegerField(default=0)
    completed_delivery_count = models.IntegerField(default=0)
    
    @staticmethod
    def create(first_name, last_name, email, phone='', password=None, company=None, photo=None):
        u = User(
            username = str(uuid.uuid4()),
            first_name = first_name,
            last_name = last_name,
            email = email)
        p = Profile()
        u.profile = p
        p.first_name = first_name
        p.last_name = last_name
        p.phone = phone
        
        if password is not None:
            u.set_password(password)
        u.save()
        p.user = u
        #p.user_id = u.id
        p.save()
        if photo:
            p.avatar = photo
        else:
            a = Avatar()
            a.save()
            p.avatar = a
        p.save()
        return p
    
    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)
        
    def notify(self, topic, text):
        #TODO: notify method can be phone, email or both
        print('{0} should be notified of {1} ({2})'.format(self.name_public, topic, text) )
        
    @property
    def name_public(self):
        return '{0} {1}.'.format(self.first_name, self.last_name[0])
        
    def get_avatar(self):
        if self.avatar.image:
            return self.avatar.image.url
        else:
            return "/static/files/no-avatar.png"
            
    def get_url(self):
        return '/user/{0}'.format(self.id)
        
    @staticmethod
    def find(session):
        try:
            #find socialnetwork by id
            print('find', session.id, session.socialnetwork_model)
            sn = session.socialnetwork_model.objects.get(sn_id=session.id)
            p = sn.profile
            return p, sn
        except session.socialnetwork_model.DoesNotExist:
            #try email and phone
            try:
                id = session.email
                try:
                    u=User.objects.get(email=id)
                    p=Profile.objects.get(user=u)
                except User.DoesNotExist:
                    try:
                        p = Profile.objects.get(phone=id)
                    except Profile.DoesNotExist:
                        raise
                try:
                    sn = session.socialnetwork_model.objects.get(profile=p)
                    return p, sn
                except session.socialnetwork_model.DoesNotExist:
                    print('no SN found for user {0}'.format(p))
                    return p, None
            except KeyError:
                raise Profile.DoesNotExist()

class Avatar(models.Model):
    image=models.ImageField(blank=True, null=True)
    
    @staticmethod
    def create(url=None, content=None):
        a = Avatar()
        return a

class Notification(models.Model):
    content = models.CharField(max_length=500)
    url = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    viewed=models.BooleanField(default=True)