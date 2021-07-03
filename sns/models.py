from django.db import models
from django.contrib.auth.models import User

#Message クラス
'''
ここではownerとgroupがmodels.ForeignKeyで他のモデルと連携しています
また,Metaクラスで並び順のorderingの設定をしています
よく見ると、ordering=('-pub_date',)となっていますこれで降順昇順を入れ替えます
またこのMessageではget_shareというメソッドを追加しています
これはこのMessageのshare_idで設定されているMessage(つまりシェア元のメッセージ)
を取得して返すもので、テンプレートでの表示で利用しています。

'''
#ownerID 投稿者
#groupID 投稿先のグループ
#content コンテンツ
#shareID シェアした投稿のID
#good count いいねした数
#share_count shareされた回数
#pub_date 投稿日時
class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, \
            related_name='message_owner')
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    share_id = models.IntegerField(default=-1)
    good_count = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.content) + ' (' + str(self.owner) + ')'
    
    def get_share(self):
        return Message.objects.get(id=self.share_id)
        
    class Meta:
        ordering = ('-pub_date',)

#Group クラス
'''
Groupではownerにmodels.ForeignKeyで設定してモデルと連携しています
タイトルはCharFielsを使用しています
'''
#ownerID 登録者のアカウント
#title グループ名
class Group(models.Model):
        owner = models.ForeignKey(User, on_delete=models.CASCADE, \
            related_name='group_owner')
        title = models.CharField(max_length=100)
        
        def __str__(self):
            return self.title

#Friendクラス
'''
owner user groupの3つの項目すべてがmodels.ForeignKeyで関連する他のモデルと
連携しています。クラス自体はほかに項目を持たないシンプルな形です
'''
#ownerID 登録者のカウント
#userID バインドされるユーザーアカウント
#groupID 登録されているグループID

class Friend(models.Model):
        owner = models.ForeignKey(User, on_delete=models.CASCADE, \
            related_name='friend_owner')
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        group = models.ForeignKey(Group, on_delete=models.CASCADE)
        
        def __str__(self):
            return str(self.user) + '(group:"' + str(self.group) + '")'


#Good クラス
'''
owner とmessageのmodels.ForeignKeyが用意されています
これも両者の関連を示すだけのモデルなのでシンプルです
'''



#ownerID goodしたユーザーのID
#messageID goodしたメッセージのID

class Good(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, \
            related_name='good_owner')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'good for "' + str(self.message) + '"(by ' + \
                str(self.owner) + ')'
                
    
    
