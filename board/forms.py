from django import forms  # 장고안에 있는 폼


class BoardForm(forms.Form): # 글쓰기 기능을 가지고 있는 폼
    # title,contents,tags는 모두 다 필드 네임들임
    title = forms.CharField(
        error_messages={'required': '제목을 입력해주세요.'}, max_length=128, label="제목")
    contents = forms.CharField(
        error_messages={'required': '내용을 입력해주세요.'}, widget=forms.Textarea, label="내용")
    tags = forms.CharField(
        required=False, label="태그")  # required가 False는 필수적인 구성요소가 아니란 것임.
