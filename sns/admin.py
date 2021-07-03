from django.contrib import admin
from .models import Message,Friend,Group,Good

admin.site.register(Message)
admin.site.register(Friend)
admin.site.register(Group)
admin.site.register(Good)

#これでDjangoの管理ツールでSNSのモデル類が編集できるようになります
#アプリのプログラム作成に進む前に、管理ツールで必要なデータを作成しておきましょう


