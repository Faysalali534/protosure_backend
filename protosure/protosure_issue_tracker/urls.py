from django.urls import path

from protosure_issue_tracker import views

urlpatterns = [
    path('repo/issues/<str:owner>/<str:repo>', views.RepoInfo.as_view(), name='all_issues'),
    path('repo/issues/<str:owner>/<str:repo>/comment/<int:issue>', views.IssueComment.as_view(), name='issue_comment'),
    path('repo/issues/<str:owner>/<str:repo>/filter', views.IssueDataFilter.as_view(), name='filter_data'),

]
