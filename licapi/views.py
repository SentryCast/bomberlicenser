import json
import requests
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import generic
from django.db.models import F, Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .models import License, User, TelegramBot


def IndexView(request):
    return HttpResponse("Index page of licenser")


@csrf_exempt
def RegView(request):
    if request.method == "POST":
        try:
            data = request.body
            data = data.decode('utf-8')
            data = json.loads(data)

            req_key = data["license_key"]
            req_computer_name = data["computer_name"]
            req_platform_system = data["platform_system"]
            req_platform_release = data["platform_release"]
            req_platform_architecture = data["platform_architecture"]
            req_mac_address = data["mac_address"]
            req_processor = data["processor"]
            req_ram = data["ram"]
        except KeyError:
            return JsonResponse(
                {'success': 'false',
                 'message': 'You did not provide credentials.'
                 }
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": "false", "message": "Json decode error"}
            )
        except Exception as e:
            return JsonResponse(
                {"success": "false",
                    "message": "Unexpected error", "error": str(e)}
            )
        try:
            lic = License.objects.all().get(
                license_code=req_key)
        except License.DoesNotExist as e:
            return JsonResponse({'success': 'false',
                                 'message': 'Your code is invalid.',
                                 })
        except License.MultipleObjectsReturned:
            return JsonResponse({'success': 'false',
                                 'message': 'Your code is invalid (multiple o error).'})
        except:
            return JsonResponse(
                {
                    "success": "false",
                    "message": "Unexpected error on license checking"
                }
            )
        if lic.obtained == True:
            primary_key_current = lic.pk
            try:
                usr = User.objects.all().get(license_code_id=primary_key_current)
            except User.DoesNotExist:
                return JsonResponse(
                    {
                        "success": "false",
                        "message": "A key is already obtained"
                    }
                )
            except User.MultipleObjectsReturned:
                return JsonResponse(
                    {
                        "success": "false",
                        "message": "Multiple users obtain the same code"
                    }
                )
            except:
                return JsonResponse(
                    {
                        "success": "false",
                        "message": "Unexpected error on getting user from db"
                    }
                )
            
            if usr.computer_name == req_computer_name and \
               usr.platform_system == req_platform_system and \
               usr.platform_release == req_platform_release and \
               usr.platform_architecture == req_platform_architecture and \
               usr.mac_address == req_mac_address and \
               usr.processor == req_processor and \
               usr.ram == req_ram:

                lic.obtained = True
                lic.obtainedTimes = F('obtainedTimes') + 1
                usr.save()
                lic.save()
                return JsonResponse({'success': 'true', 'message': 'Key accepted.'})
            # macaddress differs from origin
            elif usr.computer_name == req_computer_name and \
                usr.platform_system == req_platform_system and \
                usr.platform_release == req_platform_release and \
                usr.platform_architecture == req_platform_architecture and \
                usr.processor == req_processor and \
                usr.ram == req_ram and \
                lic.license_code.startswith('Special01'):
                    lic.obtained = True
                    lic.obtainedTimes = F('obtainedTimes') + 1
                    usr.mac_address = req_mac_address
                    usr.editedTimes = F('editedTimes') + 1
                    usr.save()
                    lic.save()
                    return JsonResponse({"success": "true", "message": "Key accepted."})
                
            
            else:
                return JsonResponse({"success": "false", "message": "A key is obtained by another user."})
        else:
            usr = User.objects.create(computer_name=req_computer_name,
                                      register_date=timezone.now(),
                                      license_code=lic,
                                      mac_address=req_mac_address,
                                      platform_architecture=req_platform_architecture,
                                      platform_release=req_platform_release,
                                      platform_system=req_platform_system,
                                      processor=req_processor,
                                      ram=req_ram)
            lic.obtained = True
            lic.obtainedTimes = F('obtainedTimes') + 1
            lic.save()
            usr.save()
            return JsonResponse({"success": "true", "message": "Key accepted."})
    else:
        return HttpResponse("Wrong req method.")

@csrf_exempt
def TgBotView(request):
    tgApiBaseUrl = "https://api.telegram.org/bot"
    tgApiSendMessage = "/sendMessage"
    # ENTER TOKEN HERE and provide url pattern in urls.py
    tgBotToken = "token here"
    
    
    update = request.body
    update = update.decode('utf-8')
    update = json.loads(update)
    
    message = update['message']
    text = message['text']
    chat_id = message['chat']['id']
    user = message['from']
    user_id = user['id']
    user_name = user['first_name']
    db_user = None
            
    
    answer = ""
    try:
        db_user = TelegramBot.objects.get(tg_user_id=user_id)
    except TelegramBot.DoesNotExist as e:
        db_user = TelegramBot.objects.create(tg_user_id=user_id, tg_chat_id=chat_id)
        db_user.save()
        for key in user.keys():
            if key == "username":
                db_user.tg_username = user['username']
                db_user.save()
        answer = "Добро пожаловать, " + user_name + ".\n"
    except TelegramBot.MultipleObjectsReturned as e:
        if db_user != None:
            try:
                for i in db_user:
                    i.banned = True
                    i.save()
            except Exception as e:
                print("Something went wrong on TelegramBot.MultipleObjectsReturned banning...")
        return JsonResponse({"method": "sendMessage",
                            "chat_id": str(chat_id),
                             "text": "Что-то пошло не так, обратитесь к администратору проекта."})
    except Exception as e:
        return JsonResponse({"method": "sendMessage",
                            "chat_id": str(chat_id),
                             "text": "Непредвиденная ошибка. обратитесь к администратору проекта. Ошибка: " + str(e) + " type: " + str(type(e))})
    
    
    # TODO Optional features: add custom keyboard on every step for maximum convenience
    if text == "/start" or text == "/addbomber":
        answer += "Введите лицензионный ключ Bomber.\n"
        
    elif (db_user.previous_command == "/start" or db_user.previous_command == "/addbomber") \
        and not text.startswith("/"):
        try:
            lic = License.objects.get(license_code=text)
            db_user.license_code.append(lic.license_code)
            db_user.save()
            answer += "Ключ добавлен! Напишите /addbomber, чтобы добавить еще один ключ, или /listen, чтобы начать отслеживание статуса.\n"
        except License.DoesNotExist:
            answer += "Неверный лицензионный ключ. Введите /addbomber, чтобы попробовать снова."
        except Exception:
            answer += "Непредвиденная ошибка при добавлении ключа. Введите /addbomber, чтобы попробовать снова."
    
    elif text.startswith("/start ") or text.startswith("/addbomber "):
        if text.startswith("/start "):
            code = text[7:]
        elif text.startswith("/addbomber "):
            code = text[11:]
        try:
            lic = License.objects.get(license_code=code)
            db_user.license_code.append(lic.license_code)
            db_user.save()
            answer += "Ключ добавлен! Напишите /addbomber, чтобы добавить еще один ключ, или /listen, чтобы начать отслеживание статуса.\n"
        except License.DoesNotExist:
            answer += "Неверный лицензионный ключ. Введите /addbomber, чтобы попробовать снова."
        except Exception:
            answer += "Непредвиденная ошибка при добавлении ключа. Введите /addbomber, чтобы попробовать снова."
    elif text == "/removebomber":
        answer += "Введите ключ для удаления из отслеживаемых."
    elif (db_user.previous_command == "/removebomber" or text.startswith("/removebomber ")) and not text.startswith("/"):
        if text.startswith("/removebomber "):
            code = text[14:]
        else:
            code = text
        # to prevent deleting default
        if code == "//empty//" or code == "/empty/":
            code = ""
        objToChange = TelegramBot.objects.filter(tg_user_id=user_id, license_code__contains=[code])
        if objToChange.exists():
            otc = objToChange[0]
            otc.license_code.remove(code)
            otc.save()
            answer += "Ключ успешено удалён."
        else:
            answer += "Ключ не найден."
            
    elif text == "/listen":
        if TelegramBot.objects.filter(Q(tg_user_id=user_id), Q(license_code__gt=1)) != None:
            db_user.listening = True
            db_user.save()
            answer += "Отлично! Бот работает. Не забудьте оставить уведомления включёнными, чтобы не пропустить сигналы!\n"        
        else:
            answer += "Чтобы получать сигналы, нужно добавить хотя бы один лицензионный ключ. Чтобы добавить его, введите /addbomber.\n"
    
    elif text == "/pause":
        db_user.listening = False
        db_user.save()
        answer += "Сигналы от бота приостановлены. Введите /listen, чтобы начать получать их снова.\n"

    elif text == "/help":
        answer += "Получайте уведомления о работе ботов в Телеграме!\n\
/addbomber - добавить лицензионный ключ для бомбера.\n\
/removebomber - удалить существующий ключ.\n\
/listen - начать отслеживать статус своих ботов.\n\
/pause - приостановить отслеживание статуса.\n"
    else:
        answer += "Команда не распознана. Введите /help для получения списка команд.\n"
        
    db_user.previous_command = text
    db_user.save()

    return JsonResponse({
            "method": "sendMessage", 
            "chat_id": str(chat_id), 
            "text": answer})