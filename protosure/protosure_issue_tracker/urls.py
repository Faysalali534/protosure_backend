from django.urls import path

from protosure_issue_tracker import views

urlpatterns = [
    path('repo/issues/<str:owner>/<str:repo>', views.RepoInfo.as_view(), name='all_issues')]
