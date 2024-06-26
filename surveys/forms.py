from django import forms
from django.utils import timezone
from django.db.models import Max
from .models import Survey

class SurveyAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # 初期化
        super(SurveyAddForm, self).__init__(*args, **kwargs)
        # データベースに格納されているidのうち最大のもの+1の値を設定する（インクリメントの実装）
        max_id = Survey.objects.all().aggregate(max_id=Max('id'))['max_id']
        next_id = max_id + 1 if max_id is not None else 1
        self.fields['id'].initial = next_id
        # create_atに現在時刻を初期値として設定
        self.fields['create_at'].initial = timezone.now().strftime('%Y-%m-%dT%H:%M')
        # タイムゾーンの設定がおかしいため要修正（9時間前が指定される）
        # pytzライブラリが必要になりそう（コンテナ側に設定が必要）
        # tokyo_tz = pytz.timezone('Asia/Tokyo')

    # モデルに関するオプション
    class Meta:
        model = Survey
        fields = ['id', 'title', 'url', 'create_at', 'create_user', 'delete_flag']

    # 入力にカレンダーを利用できるようにする
    create_at = forms.DateTimeField(
        label='作成日時',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=True,
    )
    # URL入力欄にリンクの先頭部分を先に記入しておく
    url = forms.URLField(
        initial='https://',
        label='URL',
        required=True,
    )
