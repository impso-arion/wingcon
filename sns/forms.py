from django import forms
from.models import Message,Group,Friend,Good
from django.contrib.auth.models import User

# Messageのフォーム（未使用）
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['owner','group','content']
# Groupのフォーム（未使用）
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['owner', 'title']
# Friendのフォーム（未使用）
class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['owner', 'user', 'group']
# Goodのフォーム（未使用）
class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['owner', 'message']

# 検索フォーム
class SearchForm(forms.Form):
    search = forms.CharField(label='メッセージ検索', max_length=100)

# Groupのチェックボックスフォーム
'''
このクラスではフィールドを設定した変数がありませんその代わりにあるのが
初期化のためのメソッドです

__init__というのがインスタンスを作成する際に呼び出される
初期化メソッドです。ここではselfの後にuserという引数が用意されています。
これはGroupを取得するUserを引数として渡すためのものです。
ここではsuper()というもので基底クラスの__init__メソッドを呼び出します
初期化の処理はこのクラスにしかないとは限りません。
基底クラス(継承する元になっているクラス)にも__init__が用意されていて
そこに初期化処理が用意されているかもしれないのです

そこで__init__メソッドの最初に、規定クラスの__init__を呼び出して初期化処理を
実行させておきます。super関数は第一引数にクラス、第二引数にインスタンス自身(self)を指定して
呼び出すことで、そのインスタンスの規定クラスのインスタンスにあるメソッドを呼び出します。

なんだかよくわからないという人は「super(GroupCheckForm,self)の後にメソッドを書いて呼び出せばOKと覚えておいてください

'''
class GroupCheckForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupCheckForm, self).__init__(*args, **kwargs)
        public = User.objects.filter(username='public').first()
        self.fields['groups'] = forms.MultipleChoiceField(
            choices=[(item.title, item.title) for item in \
                 Group.objects.filter(owner__in=[user,public])],
            widget=forms.CheckboxSelectMultiple(), label='絞り込みグループ',
        )

# Groupの選択メニューフォーム
class GroupSelectForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupSelectForm, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-','-')] + [(item.title, item.title) \
                 for item in Group.objects.filter(owner=user)],
        )

# Friendのチェックボックスフォーム
class FriendsForm(forms.Form):
    def __init__(self, user, friends=[], vals=[], *args, **kwargs):
        super(FriendsForm, self).__init__(*args, **kwargs)
        self.fields['friends'] = forms.MultipleChoiceField(
            choices=[(item.user, item.user) for item in friends],
            widget=forms.CheckboxSelectMultiple(),
            initial=vals
        )

# Group作成フォーム
class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=50)

# 投稿フォーム
class PostForm(forms.Form):
    content = forms.CharField(max_length=500, \
            widget=forms.Textarea)
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        public = User.objects.filter(username='public').first()
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-','-')] + [(item.title, item.title) \
                     for item in Group.objects. \
                     filter(owner__in=[user,public])],
        )
