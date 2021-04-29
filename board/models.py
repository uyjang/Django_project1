from django.db import models

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=128, verbose_name='제목')
    contents = models.TextField(verbose_name='내용')  # textfield는 길이에 제한이 없다
    writer = models.ForeignKey( # DB에서 각 테이블마다 가지고 있는 id로 연결해서 사용하는 ForeignKey , fcuser에있는 FCUSER모델을 사용하겠다. , 사용자가 탈퇴하면 사용자가 작성한 글들은 모두 삭제하겠다.
        'fcuser.Fcuser', on_delete=models.CASCADE, verbose_name='작성자') # 또한 여기에서 포린키는 1대n의 관계이다. 한명의 작성자가 여러가지의 글을 사용할 수 있다
    tags = models.ManyToManyField('tag.Tag', verbose_name='태그') # 태그는 n대n의 관계이다.왜냐면 하나의 태그가 여러글에 들어갈 수 있고 여러태그가 하나의 글에 들어갈 수 있다
    regstered_dttm = models.DateTimeField(
        auto_now_add=True, verbose_name='등록시간')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'fastcampus_board'
        verbose_name = '패스트캠퍼스 게시글'
        verbose_name_plural = '패스트캠퍼스 게시글'
