# import os
# import csv
# import time
# import requests
# from background_task import background
# from django.conf import settings
# from django.utils import timezone
# from .models import ProcessController
# BASE_URL = "https://instagram-scraper-2022.p.rapidapi.com/ig"
# headers = {
# 	"X-RapidAPI-Key": "eae1b73cb9mshc5dece8c05b7c84p172949jsned39caa145b8",
# 	"X-RapidAPI-Host": "instagram-scraper-2022.p.rapidapi.com"
# }

# # followers_list = []

# def append_row_to_csv(file_path, row_data):
#     file_exists = os.path.isfile(file_path)
#     mode = "a" if file_exists else "w"
#     if mode == "w":
#         header = [
#             "Username",
#             "FullName",
#             "Followers Count",
#             "Public Email",
#             "Country Code",
#             "Public Phone",
#             "Whatsapp Number",
#         ]
#         with open(file_path, mode, newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)
#             writer.writerow(header)
#     with open(file_path, "a", newline="", encoding="utf-8") as file:
#         writer = csv.writer(file)
#         writer.writerow(row_data)

# def getUserId(username):
#     param = {
#         "user":username
#     }
#     res = requests.get(
#         f"{BASE_URL}/info_username/",headers=headers,params=param
#     )

#     data = res.json()
#     if data.get('status',None) == "ok":
#         return data.get('user').get('pk')

# def getUser(username):
#     param = {
#         "user":username
#     }
#     res = requests.get(
#         f"{BASE_URL}/info_username/",headers=headers,params=param
#     )

#     data = res.json()
#     if data.get('status',None) == "ok":
#         return data.get('user')
    
# def getFollowers(followers_list,userId,max_id = None):
#     param = {
#         'id_user':userId
#     }
#     if max_id is not None:
#         param['next_max_id'] = max_id
#     request = requests.get(
#         f"{BASE_URL}/followers/",headers=headers,params=param
#     )
#     res = request.json()
#     if res.get('status',None) == "ok" and res.get('next_max_id',None) is not None:

#         users = res.get('users',[])
#         public_users = [item for item in users if not item["is_private"]]
#         followers_list.extend(public_users)
#         print("fetched and again call")
#         getFollowers(followers_list,userId=userId,max_id=res.get('next_max_id'))
#     elif res.get('status',None) == "ok":
#         users = res.get('users',[])
#         public_users = [item for item in users if not item["is_private"]]
#         followers_list.extend(public_users)
#         print("finished")

# @background(schedule=0)
# def run_background_task(obj):
#     followers_list = []
#     # page = input("Enter Instagram Page Name: ")
#     obj_controller = ProcessController.objects.get(pk=obj)
#     page = obj_controller.username
#     file_path = os.path.join(settings.MEDIA_ROOT,obj_controller.file)
#     user = getUserId(page)
#     print(user,page)
#     getFollowers(followers_list,userId=user)
#     print(followers_list)
#     obj_controller.total_acc = len(followers_list)
#     obj_controller.save()
#     for i in followers_list:
#         obj_controller = ProcessController.objects.get(pk=obj)
#         if obj_controller.isStop:
#             break
#         usr = getUser(i['username'])
#         print("run")
#         if usr.get('public_email',None) is not None and usr.get('public_email',None) != "":
#             temp = [
#                     usr.get("username", ""),
#                     usr.get("full_name", ""),
#                     usr.get("follower_count", ""),
#                     usr.get("public_email",""),
#                     usr.get("public_phone_country_code", ""),
#                     usr.get("public_phone_number", ""),
#                     usr.get("whatsapp_number", ""),
#                 ]
#             append_row_to_csv(file_path=file_path,row_data=temp)
#             obj_controller = ProcessController.objects.get(pk=obj)
#             obj_controller.scraped_email = obj_controller.scraped_email + 1
#             obj_controller.save()
#     obj_controller = ProcessController.objects.get(pk=obj)
#     obj_controller.isRuning = False
#     obj_controller.isComplete = True
#     obj_controller.complete_date = timezone.now()
#     obj_controller.save()


import os
import csv
import time
import requests
from background_task import background
from django.conf import settings
from django.utils import timezone
from .models import ProcessController

BASE_URL = "https://instagram-scraper-2022.p.rapidapi.com/ig"
headers = {
    "X-RapidAPI-Key": "",
    "X-RapidAPI-Host": "instagram-scraper-2022.p.rapidapi.com"
}

def append_row_to_csv(file_path, row_data):
    file_exists = os.path.isfile(file_path)
    mode = "a" if file_exists else "w"
    if mode == "w":
        header = [
            "Username",
            "FullName",
            "Followers Count",
            "Public Email",
            "Country Code",
            "Public Phone",
            "Whatsapp Number",
        ]
        with open(file_path, mode, newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(row_data)

def getUserId(username):
    param = {
        "user": username
    }
    res = requests.get(
        f"{BASE_URL}/info_username/", headers=headers, params=param
    )

    data = res.json()
    if data.get('status', None) == "ok":
        return data.get('user').get('pk')

def getUser(username):
    param = {
        "user": username
    }
    res = requests.get(
        f"{BASE_URL}/info_username/", headers=headers, params=param
    )

    data = res.json()
    if data.get('status', None) == "ok":
        return data.get('user')

def getFollowers(followers_set, userId, max_id=None):
    param = {
        'id_user': userId
    }
    if max_id is not None:
        param['next_max_id'] = max_id
    request = requests.get(
        f"{BASE_URL}/followers/", headers=headers, params=param
    )
    res = request.json()
    if res.get('status', None) == "ok" and res.get('next_max_id', None) is not None:
        users = res.get('users', [])
        public_users = [item for item in users if not item["is_private"]]
        followers_set.update(public_users)
        print("fetched and again call")
        getFollowers(followers_set, userId=userId, max_id=res.get('next_max_id'))
    elif res.get('status', None) == "ok":
        users = res.get('users', [])
        public_users = [item for item in users if not item["is_private"]]
        followers_set.update(public_users)
        print("finished")

@background(schedule=0)
def run_background_task(obj):
    followers_set = set()
    obj_controller = ProcessController.objects.get(pk=obj)
    page = obj_controller.username
    file_path = os.path.join(settings.MEDIA_ROOT, obj_controller.file)
    user = getUserId(page)
    print(user, page)
    getFollowers(followers_set, userId=user)
    followers_list = list(followers_set)
    print(followers_list)
    obj_controller.total_acc = len(followers_list)
    obj_controller.save()
    for i in followers_list:
        obj_controller = ProcessController.objects.get(pk=obj)
        if obj_controller.isStop:
            break
        usr = getUser(i['username'])
        print("run")
        if usr.get('public_email', None) is not None and usr.get('public_email', None) != "":
            temp = [
                usr.get("username", ""),
                usr.get("full_name", ""),
                usr.get("follower_count", ""),
                usr.get("public_email", ""),
                usr.get("public_phone_country_code", ""),
                usr.get("public_phone_number", ""),
                usr.get("whatsapp_number", ""),
            ]
            append_row_to_csv(file_path=file_path, row_data=temp)
            obj_controller = ProcessController.objects.get(pk=obj)
            obj_controller.scraped_email = obj_controller.scraped_email + 1
            obj_controller.save()
    obj_controller = ProcessController.objects.get(pk=obj)
    obj_controller.isRuning = False
    obj_controller.isComplete = True
    obj_controller.complete_date = timezone.now()
    obj_controller.save()
