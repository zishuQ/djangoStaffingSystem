from django.http import JsonResponse
from django.shortcuts import render


def chart_list(request):
    """ 数据统计页面 """
    return render(request, "chart_list.html")


def chart_bar(request):
    """ 构造柱状图的数据 """
    # 数据可以去数据库中获取
    legend = ['zishuQ']
    series_list = [
        {
            "name": "zishuQ",
            "type": "bar",
            "data": [15, 20, 36, 10, 10, 10]
        },
    ]
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    """ 构造饼状图的数据"""
    db_data_list = [
        {"value": 1048, "name": 'IT部门'},
        {"value": 735, "name": '运营部'},
        {"value": 580, "name": '新媒体'},
        {"value": 484, "name": '营销部'},
        {"value": 300, "name": '后勤部'}
    ]

    result = {
        "status": True,
        "data": db_data_list,
    }
    return JsonResponse(result)


def chart_line(request):
    """ 构造折线图 """
    legend = ['上海', '北京']
    series_list = [
        {
            "name": "上海",
            "type": "line",
            "stack": 'Total',
            "data": [15, 20, 36, 80, 20, 30]
        },
        {
            "name": "北京",
            "type": "line",
            "stack": 'Total',
            "data": [15, 20, 36, 30, 20, 40]
        },
    ]
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月', '7月 ']

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }
    }
    return JsonResponse(result)
