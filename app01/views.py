from django.shortcuts import render,redirect,HttpResponse
from django.forms import Form,ModelForm
from django.forms import fields as ffields
from django.forms import widgets as fwidgets
from app01 import models

"""
class TestForm(Form):
    user = fields.CharField()
    email = fields.EmailField()
    ug_id = fields.ChoiceField(
        widget=widgets.Select,
        choices=[]
    )

    def __init__(self,*args,**kwargs):
        super(TestForm,self).__init__(*args,**kwargs)

        self.fields['ug_id'].choices = models.UserGroup.objects.values_list('id','title')


def test(request):
    if request.method == "GET":
        form = TestForm()
        context = {
            'form': form
        }
        return render(request,'test.html',context)
    else:
        form = TestForm(request.POST)
        if form.is_valid():
            # {ug:1}
            models.UserInfo.objects.create(**form.cleaned_data)
            return redirect('http://www.baidu.com')
        context = {
            'form': form
        }
        return render(request, 'test.html', context)
"""

# Create your views here.
class TestModelForm(ModelForm):
    #Meta指定ModelForm对哪一个数据表进行操作，只能单个表
    class Meta:
        model = models.UserInfo
        #需要使用或显示数据表的字段
        fields = "__all__"
        #错误信息
        error_messages = {
            'user': {'required': '用户名不能为空'},
            'email': {'required': '邮箱不能为空', 'invalid': '邮箱格式错误'},
        }
        #HTML标签lable
        labels = {
            'user': '用户名',
            'email': "邮箱"
        }
        #帮助信息，后缀
        help_texts = {
            'user': "帮你一下"
        }
        #设置字段生成的标签以及属性
        # widgets = {
        #     'user': fwidgets.Textarea(attrs={'class':'c1'})
        # }


def test(request):
    """
    GET:新增用户输入页面
    POST:新增用户写入数据库
    :param request:
    :return:
    """
    if request.method == "GET":
        form = TestModelForm()
        context = {'form':form}

        return render(request,'test.html',context)
    else:
        form = TestModelForm(request.POST)
        if form.is_valid():
            #不同于常规的create数据字典,这里直接save()就能新增
            form.save()
            return redirect("http://www.baidu.com")

        context = {'form': form}
        return render(request, 'test.html', context)

def edit(request,nid):
    """
    GET：显示单个用户的详细信息
    POST:修改选择用户的信息
    :param request:
    :param nid:
    :return:
    """
    obj = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        #instance将单行数据传入即可在页面上显示默认值
        form = TestModelForm(instance=obj)
        context = {'form': form}
        return render(request, 'edit.html', context)

    else:
        #拿到所有修改的该行数据，files为文件
        form = TestModelForm(instance=obj,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("http://www.baidu.com")
        context = {'form': form}
        return render(request,'test.html',context)