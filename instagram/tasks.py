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
    "X-RapidAPI-Key": "eae1b73cb9mshc5dece8c05b7c84p172949jsned39caa145b8",
    "X-RapidAPI-Host": "instagram-scraper-2022.p.rapidapi.com",
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
    param = {"user": username}
    res = requests.get(f"{BASE_URL}/info_username/", headers=headers, params=param)

    data = res.json()
    if data.get("status", None) == "ok":
        return data.get("user").get("pk")


def getUser(username):
    param = {"user": username}
    res = requests.get(f"{BASE_URL}/info_username/", headers=headers, params=param)

    data = res.json()
    if data.get("status", None) == "ok":
        return data.get("user")


def getFollowers(file_path, obj, userId, next_cursor=None):
    url = "https://instagram28.p.rapidapi.com/followers"

    querystring = {"user_id": userId, "batch_size": "49"}
    if next_cursor is not None:
        querystring["next_cursor"] = next_cursor

    headers = {
        "X-RapidAPI-Key": "eae1b73cb9mshc5dece8c05b7c84p172949jsned39caa145b8",
        "X-RapidAPI-Host": "instagram28.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    res = response.json()
    if res.get("status", None) == "ok":
        usersdata = res.get("data", {}).get("user", {}).get("edge_followed_by", {})
        users = usersdata.get("edges", [])
        page_info = usersdata.get("page_info", None)
        obj_controller = ProcessController.objects.get(pk=obj)
        obj_controller.total_count = usersdata.get('count',0)
        obj_controller.save()
        print(page_info)
        if (
            page_info is not None
            and page_info.get("end_cursor", "") != ""
            and page_info.get("has_next_page", False)
        ):
            public_users = [item for item in users if not item["node"]["is_private"]]
            # obj_controller = ProcessController.objects.get(pk=obj)
            print(len(public_users), " saved")
            # obj_controller.list_data.extend(public_users)
            # obj_controller.save()
            time.sleep(2)
            for i in public_users:
                time.sleep(1)
                obj_controller = ProcessController.objects.get(pk=obj)
                if obj_controller.isStop:
                    print("---------break--------")
                    break
                usr = getUser(i["node"]["username"])
                print("run")
                obj_controller.total_acc = obj_controller.total_acc + 1
                obj_controller.save()
                if (
                    usr.get("public_email", None) is not None
                    and usr.get("public_email", None) != ""
                ):
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
            if not obj_controller.isStop:
                print("------------------")    
                print("fetched and again call")
                getFollowers(
                        file_path=file_path,
                        obj=obj,
                        userId=userId,
                        next_cursor=page_info.get("end_cursor", None),
                    )
        elif len(users) > 0:
            public_users = [item for item in users if not item["node"]["is_private"]]
            print(len(public_users), " saved")
            
            for i in public_users:
                time.sleep(1)
                obj_controller = ProcessController.objects.get(pk=obj)
                if obj_controller.isStop:
                    print("---------break--------")
                    break
                usr = getUser(i["node"]["username"])
                print("run")
                obj_controller.total_acc = obj_controller.total_acc + 1
                obj_controller.save()
                if (
                    usr.get("public_email", None) is not None
                    and usr.get("public_email", None) != ""
                ):
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
            
            print("finished")
        else:
            print(res)


# def getFollowers(obj,userId,max_id = None):
# param = {
#     'id_user':userId
# }
# if max_id is not None:
#     param['next_max_id'] = max_id
# request = requests.get(
#     f"{BASE_URL}/followers/",headers=headers,params=param
# )
# res = request.json()
# # print(res)
# if res.get('status',None) == "ok" and res.get('next_max_id',None) is not None:

#     users = res.get('users',[])
#     public_users = [item for item in users if not item["is_private"]]
#     obj_controller = ProcessController.objects.get(pk=obj)
#     obj_controller.list_data.extend(public_users)
#     obj_controller.save()
#     print("fetched and again call")
#     time.sleep(10)
#     getFollowers(obj=obj,userId=userId,max_id=res.get('next_max_id'))

# elif res.get('status',None) == "ok" and len(res.get('users',[])) > 0:
#     users = res.get('users',[])
#     public_users = [item for item in users if not item["is_private"]]
#     obj_controller = ProcessController.objects.get(pk=obj)
#     obj_controller.list_data.extend(public_users)
#     obj_controller.save()
#     print("finished")
# else:
#     print(res)


@background(schedule=0)
def run_background_task(obj):
    obj_controller = ProcessController.objects.get(pk=obj)
    page = obj_controller.username
    file_path = os.path.join(settings.MEDIA_ROOT, obj_controller.file)
    user = getUserId(page)
    print(user, page)
    getFollowers(file_path=file_path, obj=obj, userId=user)
    obj_controller = ProcessController.objects.get(pk=obj)
    obj_controller.isRuning = False
    obj_controller.isComplete = True
    obj_controller.complete_date = timezone.now()
    obj_controller.save()
    # obj_controller = ProcessController.objects.get(pk=obj)
    # obj_controller.total_acc = len(obj_controller.list_data)
    # obj_controller.save()
    # followers_list = obj_controller.list_data
    # for i in followers_list:
    #     obj_controller = ProcessController.objects.get(pk=obj)
    #     if obj_controller.isStop:
    #         break
    #     usr = getUser(i["node"]["username"])
    #     print("run")
    #     if (
    #         usr.get("public_email", None) is not None
    #         and usr.get("public_email", None) != ""
    #     ):
    #         temp = [
    #             usr.get("username", ""),
    #             usr.get("full_name", ""),
    #             usr.get("follower_count", ""),
    #             usr.get("public_email", ""),
    #             usr.get("public_phone_country_code", ""),
    #             usr.get("public_phone_number", ""),
    #             usr.get("whatsapp_number", ""),
    #         ]
    #         append_row_to_csv(file_path=file_path, row_data=temp)
    #         obj_controller = ProcessController.objects.get(pk=obj)
    #         obj_controller.scraped_email = obj_controller.scraped_email + 1
    #         obj_controller.save()
    # obj_controller = ProcessController.objects.get(pk=obj)
    # obj_controller.isRuning = False
    # obj_controller.isComplete = True
    # obj_controller.complete_date = timezone.now()
    # obj_controller.save()
