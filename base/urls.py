# -*- coding: utf-8 -*-
"""
Copyright © 2012-2020 OpsAny. All Rights Reserved.
""" # noqa
from django.urls import path, include
from base import base_views, views

urlpatterns = [
    # 基础接口
    path("get-menu/", base_views.DeployMenuStrategyCtrl.as_view()),  # 获取导航拦
    path("guide/", base_views.GuideCtrl.as_view()),  # 获取导航拦
    path('user-info/', base_views.GetUserInfoCtrl.as_view()),  # 获取用户信息
    path("get-nav-and-collection/", base_views.GetNavCollectionView.as_view()),  # 获取导航收藏
    path("collection/", base_views.CollectionNavView.as_view()),  # 收藏操作
    path("get-user-message/", base_views.GetUserMessageView.as_view()),  # 获取站内信
    path("read-all-message/", base_views.ReadAllMessageView.as_view()),  # 全部已读操作
    path("copyright-config/", base_views.CopyrightConfigView.as_view()),  # 底部版权信息

    # 通用接口
    path("update-director/", base_views.UpdateDirectorView.as_view()),  # 被动同步rbac用户到本地


    # 概览页
    path("home-page/", base_views.HomePageView.as_view()),  # 概览页右侧
    path("home-page-left/", base_views.HomePageLeftView.as_view()),  # 概览页左侧

]

