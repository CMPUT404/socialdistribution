from django.utils.six import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from author.models import (
    UserDetails,
    FollowerRelationship,
    FriendRelationship,
    FriendRequest )
from author.serializers import (
    UserSerializer,
    UserDetailSerializer,
    FollowerRelationshipSerializer,
    FriendRelationshipSerializer,
    FriendRequestSerializer )


from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class RegistrationForm(forms.Form):

    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class MultipleFieldLookupMixin(object):
    """Allows the lookup of multiple fields in an url for mixins"""
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)

# GET /author/:uuid
class GetUserDetails(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailSerializer
    lookup_fields = ('uuid')

# GET /author/friends/:uuid
class GetAuthorFriends(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = FriendRelationship.objects.all()
    serializer_class = FriendRelationshipSerializer
    lookup_fields = ('uuid')

# GET /author/followers/:uuid
class GetAuthorFollowers(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = FollowerRelationship.objects.all()
    serializer_class = FollowerRelationshipSerializer
    lookup_fields = ('uuid')

# GET /author/friendrequests/:uuid
class GetAuthorFriendRequests(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    lookup_fields = ('uuid')

# PUT /author/update

# Account registration
@csrf_exempt
def AuthorRegistration(request):
    # permission_classes = (AllowAny,)
    # user_serializer_class = UserDetailsSerializer
    # allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    # try:
    #     User.objects.get(username=request.post.get('username', ''))
    # except:
    #      return Response({"failed": "User already exists."}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return JSONResponse({'ok':'ok'}, status=201)
    else:
        form = RegistrationForm()
        variables = RequestContext(request, {'form': form})

    return JSONResponse({'ok':'ok'}, status=400)

    # Create the user
    # if request.method == "POST":
    #     import pdb;pdb.set_trace()
    #
    #     stream = BytesIO(content)
    #     data = JSONParser().parse(stream)
    #     serializer = RegistrationSerializer(data=data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JSONResponse(serializer.data, status=201)
    #     return JSONResponse("BAD", status=400)
