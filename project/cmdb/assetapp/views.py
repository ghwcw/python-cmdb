import json

from assetapp import assetapp_handler_view
from assetapp import models
from assetapp.models import Asset
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # 忽略csrf验证
def report(request):
    if request.method == 'POST':
        asset_data = request.POST.get('asset_data', None)
        data = json.loads(asset_data)
        # 此处忽略了数据验证！
        if not data:
            return HttpResponse('没有数据！')
        if not isinstance(data, dict):
            return HttpResponse('数据必须为字典格式！')
        # 判断是否携带sn资产序列号,为真，进入审批流程
        sn = data.get('sn', None)
        if sn:
            # 首先判断是否在上线资产中存在该sn
            asset_obj = Asset.objects.filter(sn=sn)
            if asset_obj:
                # 进入已上线资产的数据更新流程
                update_asset = assetapp_handler_view.UpdateAsset(request, asset_obj[0], data)
                update_asset.asset_update()
                return HttpResponse('资产数据已经更新！')
            else:
                # asset_obj不存在，就更新或新建
                asset_new = assetapp_handler_view.NewAsset(request, data)
                resp = asset_new.add_to_new_assets_zone()
                return HttpResponse(resp)
        else:
            return HttpResponse('没有该资产序列号，请检查数据！')


# 资产总表，表格的形式展示资产信息
def index(request):
    assets = models.Asset.objects.all()
    return render(request=request, template_name='assetapp/index.html', context=locals())


# 仪表盘，图形化的数据展示
def dashboard(request):
    asset_obj=models.Asset.objects
    total=asset_obj.count()
    upline=asset_obj.filter(status=0).count()       # 在线
    offline=asset_obj.filter(status=1).count()      # 下线
    unknown =asset_obj.filter(status=2).count()     # 未知
    breakdown =asset_obj.filter(status=3).count()   # 故障
    backup =asset_obj.filter(status=4).count()      # 备用
    up_rate=round(upline/total*100)
    o_rate=round(offline/total*100)
    un_rate=round(unknown/total*100)
    bd_rate=round(breakdown/total*100)
    bu_rate=round(backup/total*100)

    server_number=models.Server.objects.count()
    networkdevice_number=models.NetworkDevice.objects.count()
    storagedevice_number=models.StorageDevice.objects.count()
    securitydevice_number=models.SecurityDevice.objects.count()
    software_number=models.Software.objects.count()

    return render(request, template_name='assetapp/dashboard.html', context=locals())


# 单个资产的详细信息页面
def detail(request, asset_id):
    """以显示服务器类型资产详细为例，安全设备、存储设备、网络设备等参照此例。"""
    asset = get_object_or_404(models.Asset, id=asset_id)
    return render(request, 'assetapp/detail.html', context=locals())
