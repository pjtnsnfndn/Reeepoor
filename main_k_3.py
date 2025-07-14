#!/usr/bin/env python

# ┌──────────────────────────────────────┐
# │      $ pip install pyrogram==2.0.41  │
# │      $ pip install asyncio           │
# └──────────────────────────────────────┘

import os, random, asyncio, time
from pyrogram import Client, filters, errors
from pyrogram.raw import functions, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#           ---         ---         ---         #
api_id = 12134308  # main api id from my.telegram.org/apps
api_hash = '6d18eb5e69cfac7dfda54ce0fef6b07b'  # main api hash from my.telegram.org/apps
bot_token = '7929810959:AAFbc736ro5MrBljqKFxUDpd3Soq5cNa_zM'  # main bot token from @botFather
bot_admins = [7193257772, 7193257772]  # admin userID

#           ---         ---         ---         #
sleeping = 2  # main sleep time in sec ***[DO NOT EDIT]***
step = None  # current step ***[DO NOT EDIT]***
tempClient = dict()  # temporary client holder ***[DO NOT EDIT]***
isWorking = list()  # Temporary Active Eval Names ***[DO NOT EDIT]***
# Global variables for report message links
tempReportLink_other = ""
tempReportLink_scam = ""
# New global variables for group report buttons
tempReportLink_group_other = ""
tempReportLink_group_scam = ""
tempReportLink_group_spam = ""
tempReportLink_group_pornography = ""
tempReportLink_group_fake = ""
tempReportLink_group_violence = ""
tempReportLink_group_illegal = ""
#           ---         ---         ---         #

if not os.path.isdir('sessions'):
    os.mkdir('sessions')

if not os.path.isfile('app.txt'):
    with open('app.txt', 'w', encoding='utf-8') as file:
        file.write(str(api_id) + ' ' + api_hash)


async def randomString() -> str:
    '''Return a random string'''
    size = random.randint(4, 8)
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVLXYZ') for _ in range(size))


async def randomAPP():
    with open('app.txt', 'r', encoding='utf-8') as file:
        file = file.read().split('\n')
        app_id, app_hash = random.choice(file).split()
    return app_id, app_hash


async def accountList():
    return [myFile.split('.')[0] for myFile in os.listdir('sessions') if os.path.isfile(os.path.join('sessions', myFile))]


async def remainTime(TS):
    TS = time.time() - TS
    if TS < 60:
        return str(int(TS)) + ' ثانیه'
    else:
        mins = int(TS / 60)
        sec = TS % 60
        return str(int(mins)) + ' دقیقه و ' + str(int(sec)) + ' ثانیه'


bot = Client(
    "LampStack",
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash
)

try:
    os.system("clear")
except:
    os.system("cls")
print('Bot is Running ...')

# تعریف منوی اصلی با دکمه‌های مجاز
def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('افزودن اکانت ➕', callback_data='addAccount'),
         InlineKeyboardButton('✖️ حذف اکانت', callback_data='removeAccount')],
        [InlineKeyboardButton('⚫️ عملیات ری اکشن پست', callback_data='reActionEval')],
        [InlineKeyboardButton('🔴 عملیات ریپورت پست', callback_data='reportPostPublic')],
        [InlineKeyboardButton('🟢ریپورت بخش other', callback_data='reportOther'),
         InlineKeyboardButton('🟠ریپورت بخش اسکم', callback_data='reportScam')],
        [InlineKeyboardButton('لیست اکانت ها 📊', callback_data='accountsList'),
         InlineKeyboardButton('♻️ بررسی اکانت ها', callback_data='checkAccounts')],
        [InlineKeyboardButton('📛 لغو تمام عملیات ها', callback_data='endAllEvals')],
        [InlineKeyboardButton('☠Rᴇᴘᴏʀᴛ☠', callback_data='groupReport')]
    ])

#           StartCommand            #
@bot.on_message(filters.command(['start', 'cancel']) & filters.private & filters.user(bot_admins))
async def StartResponse(client, message):
    global step, tempClient, isWorking
    try:
        tempClient['client'].disconnect()
    except:
        pass
    tempClient = {}
    step = None
    await message.reply('<b>> به منوی اصلی خوش آمدید :</b>',
                        reply_markup=get_main_menu_keyboard(), quote=True)

#           StopEval            #
@bot.on_message(filters.regex('^/stop_\\w+') & filters.private & filters.user(bot_admins))
async def StopEval(client, message):
    global step, isWorking
    evalID = message.text.replace('/stop_', '')
    if evalID in isWorking:
        isWorking.remove(evalID)
        await message.reply(f'<b>عملیات با شناسه {evalID} با موفقیت خاتمه یافت ✅</b>')
    else:
        await message.reply(f'<b>عملیات موردنظر یافت نشد !</b>')

#           callback query            #
@bot.on_callback_query()
async def callbackQueries(client, query):
    global step, tempClient, isWorking, sleeping
    chat_id = query.message.chat.id
    message_id = query.message.id
    data = query.data
    query_id = query.id
    if chat_id in bot_admins:
        if data == 'backToMenu':
            try:
                tempClient['client'].disconnect()
            except:
                pass
            tempClient = {}
            step = None
            await bot.edit_message_text(chat_id, message_id, '<b>> به منوی اصلی خوش آمدید :</b>',
                                        reply_markup=get_main_menu_keyboard())
        elif data == 'endAllEvals':
            step = None
            evalsCount = len(isWorking)
            isWorking = list()
            await bot.invoke(functions.messages.SetBotCallbackAnswer(query_id=int(query_id), cache_time=1, alert=True, message=f'تمام {evalsCount} عملیات فعال با موفقیت متوقف شدند'))
        elif data == 'addAccount':
            step = 'getPhoneForLogin'
            await bot.edit_message_text(chat_id, message_id,
                                        '<b>- برای افزودن اکانت لطفا شماره مورد نظرتان را ارسال نمایید :</b>')
        elif data == 'removeAccount':
            step = 'removeAccount'
            await bot.edit_message_text(chat_id, message_id,
                                        '<b>- برای حذف اکانت لطفا شماره مورد نظرتان را ارسال نمایید :</b>')
        elif data == 'reportPostPublic':
            step = 'reportPostPublic'
            await bot.edit_message_text(chat_id, message_id,
                                        '<b>لطفا لینک پست کانال|گروه مورد نظر را ارسال نمایید :</b>')
        elif data == 'reportOther':
            step = 'reportOther_request_link'
            await bot.edit_message_text(chat_id, message_id,
                                        '<b>لطفاً لینک پیام را ارسال کنید :</b>')
        elif data == 'reportScam':
            step = 'reportScam_request_link'
            await bot.edit_message_text(chat_id, message_id,
                                        '<b>لطفاً ابتدا لینک پیام مورد نظر را ارسال کنید :</b>')
        elif data == 'reActionEval':
            step = 'reActionEval'
            await bot.edit_message_text(chat_id, message_id,
                                        '<b>لطفا در خط اول لینک پست، در خط دوم ایموجی‌ها و در خط سوم تعداد ری اکشن را وارد کنید :</b>')
        elif data == 'voteEval':
            step = 'voteEval'
            await bot.edit_message_text(chat_id, message_id,
                                        '<b>لطفا در خط اول لینک پست و در خط دوم شماره گزینه موردنظرتان را وارد کنید :</b>')
        elif data == 'blockEval':
            step = 'blockEval'
            await bot.edit_message_text(chat_id, message_id,
                                        '<b>یوزرنیم کاربر مورد نظرتان را با @ وارد کنید :</b>')
        # New group report submenu
        elif data == 'groupReport':
            my_keyboard_sub = InlineKeyboardMarkup([
                [InlineKeyboardButton('♛REPORT (scam)', callback_data='group_report_scam'),
                 InlineKeyboardButton('♛REPORT (other)', callback_data='group_report_other')],
                [InlineKeyboardButton('♛REPORT (spam)', callback_data='group_report_spam'),
                 InlineKeyboardButton('♛REPORT (pornography)', callback_data='group_report_pornography')],
                [InlineKeyboardButton('♛REPORT (fake)', callback_data='group_report_fake'),
                 InlineKeyboardButton('♛REPORT (Violence)', callback_data='group_report_violence'),
                 InlineKeyboardButton('♛REPORT (Illegal)', callback_data='group_report_illegal')],
                [InlineKeyboardButton('🔙', callback_data='backToMenu')]
            ])
            await bot.edit_message_text(chat_id, message_id, '<b>> لطفاً یکی از گزینه‌های گزارش را انتخاب کنید :</b>', reply_markup=my_keyboard_sub)
        elif data == 'group_report_other':
            step = 'group_report_other_request_link'
            await bot.edit_message_text(chat_id, message_id, '<b>لطفاً ابتدا لینک پیام مورد نظر را ارسال کنید :</b>')
        elif data == 'group_report_scam':
            step = 'group_report_scam_request_link'
            await bot.edit_message_text(chat_id, message_id, '<b>لطفاً ابتدا لینک پیام مورد نظر را ارسال کنید :</b>')
        elif data == 'group_report_spam':
            step = 'group_report_spam_request_link'
            await bot.edit_message_text(chat_id, message_id, '<b>لطفاً ابتدا لینک پیام مورد نظر را ارسال کنید :</b>')
        elif data == 'group_report_pornography':
            step = 'group_report_pornography_request_link'
            await bot.edit_message_text(chat_id, message_id, '<b>لطفاً ابتدا لینک پیام مورد نظر را ارسال کنید :</b>')
        elif data == 'group_report_fake':
            step = 'group_report_fake_request_link'
            await bot.edit_message_text(chat_id, message_id, '<b>لطفاً ابتدا لینک پیام مورد نظر را ارسال کنید :</b>')
        elif data == 'group_report_violence':
            step = 'group_report_violence_request_link'
            await bot.edit_message_text(chat_id, message_id, '<b>لطفاً ابتدا لینک پیام مورد نظر را ارسال کنید :</b>')
        elif data == 'group_report_illegal':
            step = 'group_report_illegal_request_link'
            await bot.edit_message_text(chat_id, message_id, '<b>لطفاً ابتدا لینک پیام مورد نظر را ارسال کنید :</b>')

#           Text Response            #
@bot.on_message(filters.text & filters.private & filters.user(bot_admins))
async def TextResponse(client, message):
    global step, isWorking, tempClient, api_hash, api_id, sleeping
    global tempReportLink_other, tempReportLink_scam
    global tempReportLink_group_other, tempReportLink_group_scam, tempReportLink_group_spam, tempReportLink_group_pornography
    global tempReportLink_group_fake, tempReportLink_group_violence, tempReportLink_group_illegal
    chat_id = message.chat.id
    text = message.text

    #                       Add Account                       #
    if step == 'getPhoneForLogin' and text.replace('+', '').replace(' ', '').replace('-', '').isdigit():
        phone_number = text.replace('+', '').replace(' ', '').replace('-', '')
        if os.path.isfile(f'sessions/{phone_number}.session'):
            await message.reply('<b>این شماره از قبل در پوشه sessions سرور موجود است !</b>')
        else:
            tempClient['number'] = phone_number
            tempClient['client'] = Client(f'sessions/{phone_number}', int(api_id), api_hash)
            await tempClient['client'].connect()
            try:
                tempClient['response'] = await tempClient['client'].send_code(phone_number)
            except (errors.BadRequest, errors.PhoneNumberBanned, errors.PhoneNumberFlood, errors.PhoneNumberInvalid):
                await message.reply('<b>خطایی رخ داد !</b>')
            else:
                step = 'get5DigitsCode'
                await message.reply(f'<b>کد 5 رقمی به شماره {phone_number} ارسال شد ✅</b>')
    elif step == 'get5DigitsCode' and text.replace(' ', '').isdigit():
        telegram_code = text.replace(' ', '')
        try:
            await tempClient['client'].sign_in(tempClient['number'], tempClient['response'].phone_code_hash, telegram_code)
            await tempClient['client'].disconnect()
            tempClient = {}
            step = 'getPhoneForLogin'
            await message.reply('<b>اکانت با موفقیت ثبت شد ✅\nدرصورتیکه قصد افزودن شماره دارید, شماره موردنظر را ارسال کنید</b>')
        except errors.PhoneCodeExpired:
            await tempClient['client'].disconnect()
            tempClient = {}
            step = None
            await message.reply('<b>کد ارسال شده منقضی شده است, لطفا عملیات را /cancel کنید و مجدد تلاش کنید.</b>')
        except errors.PhoneCodeInvalid:
            await message.reply('<b>کد وارد شده اشتباه است یا منقضی شده, لطفا دوباره تلاش کنید.</b>')
        except errors.BadRequest:
            await message.reply('<b>کد وارد شده اشتباه است یا منقضی شده, لطفا دوباره تلاش کنید.</b>')
        except errors.AuthKeyUnregistered:
            await asyncio.sleep(3)
            name = await randomString()
            try:
                await tempClient['client'].sign_up(tempClient['number'], tempClient['response'].phone_code_hash, name)
            except Exception:
                pass
            await tempClient['client'].disconnect()
            tempClient = {}
            step = 'getPhoneForLogin'
            await message.reply('<b>اکانت با موفقیت ثبت شد ✅\nدرصورتیکه قصد افزودن شماره دارید, شماره موردنظر را ارسال کنید</b>')
        except errors.SessionPasswordNeeded:
            step = 'SessionPasswordNeeded'
            await message.reply('<b>لطفا رمز تایید دو مرحله ای را وارد نمایید :</b>')
    elif step == 'SessionPasswordNeeded':
        twoFaPass = text
        try:
            await tempClient['client'].check_password(twoFaPass)
        except errors.BadRequest:
            await message.reply('<b>رمز وارد شده اشتباه میباشد, لطفا مجدد ارسال نمایید.</b>')
        else:
            await tempClient['client'].disconnect()
            tempClient = {}
            step = 'getPhoneForLogin'
            await message.reply('<b>اکانت با موفقیت ثبت شد ✅\nدرصورتیکه قصد افزودن شماره دارید, شماره موردنظر را ارسال کنید</b>')
    
    #                       Delete Account                       #
    if step == 'removeAccount':
        step = None
        phone_number = text.replace('+', '').replace(' ', '').replace('-', '')
        if not os.path.isfile(f'sessions/{phone_number}.session'):
            await message.reply('<b>شماره مورد نظر در سرور یافت نشد !</b>')
        else:
            await bot.send_document(message.chat.id, f'sessions/{phone_number}.session',
                                      caption='<b>شماره مورد نظر با موفقیت حذف شد ✅\nسشن پایروگرام حذف شده است.</b>')
            os.unlink(f'sessions/{phone_number}.session')
    
    #                       set Time                       #
    if step == 'setTime':
        step = None
        sleeping = float(text)
        await message.reply('<b>زمان جدید با موفقیت تنظیم شد ✅</b>')
    
    # سایر بخش‌ها (عضویت، خروج، ویو، ری اکشن، نظرسنجی، بلاک، ریپورت ...)
    # همان منطق اصلی حفظ شده است.
    
    if step == 'joinAccounts':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        link = text.split()[0].replace('@', '').replace('+', 'joinchat/')
        allAcccounts = len(await accountList())
        all = 0
        error = 0
        done = 0
        TS = time.time()
        msg = await message.reply('<b>عملیات عضویت شروع شد ...</b>')
        for session in await accountList():
            if evalID not in isWorking:
                break
            all += 1
            await asyncio.sleep(sleeping)
            try:
                api_id2, api_hash2 = await randomAPP()
                cli = Client(f'sessions/{session}', api_id2, api_hash2)
                await cli.connect()
                await asyncio.sleep(0.2)
                await cli.join_chat(link)
                await asyncio.sleep(0.2)
                await cli.disconnect()
            except Exception as e:
                try:
                    await cli.disconnect()
                except:
                    pass
                error += 1
            else:
                done += 1
            finally:
                spendTime = await remainTime(TS)
                await bot.edit_message_text(chat_id, msg.id,
                                            f'''♻️ عملیات عضویت اکانت های ربات ...
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
        try:
            isWorking.remove(evalID)
        except:
            pass
        spendTime = await remainTime(TS)
        await message.reply(f'''<b>عملیات عضویت با موفقیت به پایان رسید ✅
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}</b>''')
    
    if step == 'leaveAccounts':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        allAcccounts = len(await accountList())
        all = 0
        error = 0
        done = 0
        TS = time.time()
        msg = await message.reply('<b>عملیات خروج شروع شد ...</b>')
        for session in await accountList():
            if evalID not in isWorking:
                break
            all += 1
            await asyncio.sleep(sleeping)
            try:
                api_id2, api_hash2 = await randomAPP()
                cli = Client(f'sessions/{session}', api_id2, api_hash2)
                await cli.connect()
                await asyncio.sleep(0.2)
                await cli.leave_chat(int(text), delete=True)
                await asyncio.sleep(0.2)
                await cli.disconnect()
            except Exception as e:
                try:
                    await cli.disconnect()
                except:
                    pass
                error += 1
            else:
                done += 1
            finally:
                spendTime = await remainTime(TS)
                await bot.edit_message_text(chat_id, msg.id,
                                            f'''♻️ عملیات خروج اکانت های ربات ...
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
        try:
            isWorking.remove(evalID)
        except:
            pass
        spendTime = await remainTime(TS)
        await message.reply(f'''<b>عملیات خروج با موفقیت به پایان رسید ✅</b>
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''')
    
    if step == 'sendViewToPost':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        username = text.split('/')[3]
        msg_id = int(text.split('/')[4])
        allAcccounts = len(await accountList())
        all = 0
        error = 0
        done = 0
        TS = time.time()
        msg = await message.reply('<b>عملیات ویو پست کانال شروع شد ...</b>')
        for session in await accountList():
            if evalID not in isWorking:
                break
            try:
                await cli.disconnect()
            except:
                pass
            all += 1
            await asyncio.sleep(sleeping)
            try:
                api_id2, api_hash2 = await randomAPP()
                cli = Client(f'sessions/{session}', api_id2, api_hash2)
                await cli.connect()
                await asyncio.sleep(0.2)
                await cli.invoke(functions.messages.GetMessagesViews(peer=await cli.resolve_peer(username), id=[msg_id], increment=True))
                await asyncio.sleep(0.2)
                await cli.disconnect()
            except Exception as e:
                try:
                    await cli.disconnect()
                except:
                    pass
                error += 1
            else:
                done += 1
            finally:
                spendTime = await remainTime(TS)
                await bot.edit_message_text(chat_id, msg.id,
                                            f'''♻️ عملیات ارسال ویو اکانت های ربات ...
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
        try:
            isWorking.remove(evalID)
        except:
            pass
        spendTime = await remainTime(TS)
        await message.reply(f'''<b>عملیات بازدید پست کانال با موفقیت به پایان رسید ✅</b>
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''')
    
    if step == 'reportPostPublic':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        if text.split('/')[3] != 'c':
            peerID = '@' + text.split('/')[3]
            peerMessageID = int(text.split('/')[4])
        else:
            peerID = int('-100' + text.split('/')[4])
            peerMessageID = int(text.split('/')[5])
        allAcccounts = len(await accountList())
        all = 0
        error = 0
        done = 0
        TS = time.time()
        if text.split('/')[3].isdigit():
            await message.reply('<b>لینکی که برام ارسال کردی مربوط به یک چت خصوصی است ❗️</b>')
        else:
            msg = await message.reply('<b>عملیات ریپورت پست عمومی شروع شد ...</b>')
            for session in await accountList():
                if evalID not in isWorking:
                    break
                try:
                    await cli.disconnect()
                except:
                    pass
                all += 1
                await asyncio.sleep(sleeping)
                try:
                    api_id2, api_hash2 = await randomAPP()
                    cli = Client(f'sessions/{session}', api_id2, api_hash2)
                    await cli.connect()
                    await asyncio.sleep(0.2)
                    await cli.invoke(functions.messages.Report(
                        peer=await cli.resolve_peer(peerID),
                        id=[peerMessageID],
                        reason=types.InputReportReasonPornography(),
                        message=''))
                    await asyncio.sleep(0.2)
                    await cli.disconnect()
                except Exception as e:
                    try:
                        await cli.disconnect()
                    except:
                        pass
                    error += 1
                else:
                    done += 1
                finally:
                    spendTime = await remainTime(TS)
                    await bot.edit_message_text(chat_id, msg.id,
                                                f'''♻️ عملیات ریپورت پست کانال ...
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
            try:
                isWorking.remove(evalID)
            except:
                pass
            spendTime = await remainTime(TS)
            await message.reply(f'''<b>عملیات ریپورت پست با موفقیت به پایان رسید ✅</b>
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''')
    
    if step == 'reActionEval':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        peerID = '@' + text.split("\n")[0].split('/')[3]
        peerMessageID = int(text.split("\n")[0].split('/')[4])
        emojies = text.split("\n")[1].split()
        countOfWork = int(text.split("\n")[2])
        allAcccounts = len(await accountList())
        all = 0
        error = 0
        done = 0
        TS = time.time()
        if text.split("\n")[0].split('/')[3].isdigit():
            await message.reply('<b>لینکی که برام ارسال کردی مربوط به یک چت خصوصی است ❗️</b>')
        else:
            msg = await message.reply('<b>عملیات ارسال ری اکشن شروع شد ...</b>')
            for session in await accountList():
                if all >= countOfWork:
                    break
                if evalID not in isWorking:
                    break
                try:
                    await cli.disconnect()
                except:
                    pass
                all += 1
                await asyncio.sleep(sleeping)
                try:
                    api_id2, api_hash2 = await randomAPP()
                    cli = Client(f'sessions/{session}', api_id2, api_hash2)
                    await cli.connect()
                    await asyncio.sleep(0.2)
                    await cli.send_reaction(peerID, peerMessageID, random.choice(emojies))
                    await asyncio.sleep(0.2)
                    await cli.disconnect()
                except Exception as e:
                    try:
                        await cli.disconnect()
                    except:
                        pass
                    error += 1
                else:
                    done += 1
                finally:
                    spendTime = await remainTime(TS)
                    await bot.edit_message_text(chat_id, msg.id,
                                                f'''♻️ عملیات ارسال ری اکشن پست کانال ...
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
            try:
                isWorking.remove(evalID)
            except:
                pass
            spendTime = await remainTime(TS)
            await message.reply(f'''<b>عملیات ری اکشن پست با موفقیت به پایان رسید ✅</b>
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''')
    
    if step == 'voteEval':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        peerID = '@' + text.split("\n")[0].split('/')[3]
        peerMessageID = int(text.split("\n")[0].split('/')[4])
        opt = text.split("\n")[1]
        allAcccounts = len(await accountList())
        all = 0
        error = 0
        done = 0
        TS = time.time()
        if not opt.isdigit():
            await message.reply('<b>گزینه وارد شده صحیح نمیباشد ❗️</b>')
        else:
            msg = await message.reply('<b>عملیات ارسال نظرسنجی شروع شد ...</b>')
            for session in await accountList():
                if evalID not in isWorking:
                    break
                try:
                    await cli.disconnect()
                except:
                    pass
                all += 1
                await asyncio.sleep(sleeping)
                try:
                    api_id2, api_hash2 = await randomAPP()
                    cli = Client(f'sessions/{session}', api_id2, api_hash2)
                    await cli.connect()
                    await asyncio.sleep(0.2)
                    await cli.vote_poll(peerID, peerMessageID, int(opt))
                    await asyncio.sleep(0.2)
                    await cli.disconnect()
                except Exception as e:
                    try:
                        await cli.disconnect()
                    except:
                        pass
                    error += 1
                else:
                    done += 1
                finally:
                    spendTime = await remainTime(TS)
                    await bot.edit_message_text(chat_id, msg.id,
                                                f'''♻️ عملیات ارسال نظرسنجی ...
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
            try:
                isWorking.remove(evalID)
            except:
                pass
            spendTime = await remainTime(TS)
            await message.reply(f'''<b>عملیات نظرسنجی با موفقیت به پایان رسید ✅</b>
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''')
    
    if step == 'blockEval':
        step = None
        evalID = await randomString()
        isWorking.append(evalID)
        peerID = text.replace('@', '')
        allAcccounts = len(await accountList())
        all = 0
        error = 0
        done = 0
        TS = time.time()
        msg = await message.reply('<b>عملیات بلاک کاربر شروع شد ...</b>')
        for session in await accountList():
            if evalID not in isWorking:
                break
            try:
                await cli.disconnect()
            except:
                pass
            all += 1
            await asyncio.sleep(sleeping)
            try:
                api_id2, api_hash2 = await randomAPP()
                cli = Client(f'sessions/{session}', api_id2, api_hash2)
                await cli.connect()
                await asyncio.sleep(0.2)
                await cli.block_user(peerID)
                await asyncio.sleep(0.2)
                await cli.disconnect()
            except Exception as e:
                try:
                    await cli.disconnect()
                except:
                    pass
                error += 1
            else:
                done += 1
            finally:
                spendTime = await remainTime(TS)
                await bot.edit_message_text(chat_id, msg.id,
                                            f'''♻️ عملیات بلاک کاربر ...
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
        try:
            isWorking.remove(evalID)
        except:
            pass
        spendTime = await remainTime(TS)
        await message.reply(f'''<b>عملیات بلاک کاربر با موفقیت به پایان رسید ✅</b>
• اکانت های بررسی شده : {all}/{allAcccounts}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''')
    
    # ------------------ New Group Report Steps ------------------ #
    # For REPORT (other)
    elif step == 'reportOther_request_link':
         global tempReportLink_other
         tempReportLink_other = text.strip()
         step = 'reportOther'
         await message.reply('<b>در خط اول لینک پیام و در خط دوم متن ریپورت را وارد کنید :</b>')
    
    # --- Group Report: other with round-robin based on number of accounts and reports ---
    elif step == 'group_report_other_request_link':
         global tempReportLink_group_other
         tempReportLink_group_other = text.strip()
         step = 'group_report_other'
         await message.reply('<b>در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن گزارش را وارد کنید :</b>')
    elif step == 'group_report_other':
         evalID = await randomString()
         isWorking.append(evalID)
         parts = text.split("\n")
         if len(parts) < 3:
             await message.reply("<b>ورودی نامعتبر! لطفاً در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن گزارش را وارد کنید.</b>")
             return
         try:
             acc_count = int(parts[0].strip())
             rpt_count = int(parts[1].strip())
         except:
             await message.reply("<b>عدد وارد شده معتبر نیست!</b>")
             return
         report_text = parts[2]
         link_parts = tempReportLink_group_other.split('/')
         if link_parts[3] == "c":
             chat_id_extracted = int("-100" + link_parts[4])
             message_id_extracted = int(link_parts[5])
         else:
             chat_id_extracted = "@" + link_parts[3]
             message_id_extracted = int(link_parts[4])
         accounts = await accountList()
         chosen_accounts = accounts[:acc_count]
         total_reports = len(chosen_accounts) * rpt_count
         all_reports = 0
         error = 0
         done = 0
         TS = time.time()
         msg = await message.reply('<b>♻️ عملیات ریپورت بخش (other) شروع شد ...</b>')
         # اجرای گزارش به صورت round-robin روی اکانت‌های انتخاب‌شده
         for i in range(rpt_count):
             for session in chosen_accounts:
                 if evalID not in isWorking:
                     break
                 all_reports += 1
                 await asyncio.sleep(sleeping)
                 try:
                     api_id2, api_hash2 = await randomAPP()
                     cli = Client(f'sessions/{session}', api_id2, api_hash2)
                     await cli.connect()
                     await cli.invoke(functions.messages.Report(
                         peer=await cli.resolve_peer(chat_id_extracted),
                         id=[message_id_extracted],
                         reason=types.InputReportReasonOther(),
                         message=report_text))
                     await cli.disconnect()
                 except Exception as e:
                     try:
                         await cli.disconnect()
                     except:
                         pass
                     error += 1
                 else:
                     done += 1
                 spendTime = await remainTime(TS)
                 await bot.edit_message_text(chat_id, msg.id,
                     f'''♻️ عملیات ریپورت بخش (other)
• کل ریپورت ها : {total_reports}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
         try:
             isWorking.remove(evalID)
         except:
             pass
         spendTime = await remainTime(TS)
         await message.reply(f'''<b>♻️ عملیات ریپورت بخش (other) با موفقیت به پایان رسید ✅</b>
• کل ریپورت ها : {total_reports}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''')
    
    # For REPORT (scam)
    elif step == 'group_report_scam_request_link':
         global tempReportLink_group_scam
         tempReportLink_group_scam = text.strip()
         step = 'group_report_scam'
         await message.reply('<b>در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن ریپورت را وارد کنید :</b>')
    elif step == 'group_report_scam':
         evalID = await randomString()
         isWorking.append(evalID)
         parts = text.split("\n")
         if len(parts) < 3:
             await message.reply("<b>ورودی نامعتبر! لطفاً در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن ریپورت را وارد کنید.</b>")
             return
         try:
             acc_count = int(parts[0].strip())
             rpt_count = int(parts[1].strip())
         except:
             await message.reply("<b>عدد وارد شده معتبر نیست!</b>")
             return
         report_text = parts[2]
         link_parts = tempReportLink_group_scam.split('/')
         if link_parts[3] == "c":
             chat_id_extracted = int("-100" + link_parts[4])
             message_id_extracted = int(link_parts[5])
         else:
             chat_id_extracted = "@" + link_parts[3]
             message_id_extracted = int(link_parts[4])
         accounts = await accountList()
         chosen_accounts = accounts[:acc_count]
         total_reports = len(chosen_accounts) * rpt_count
         all_reports = 0
         error = 0
         done = 0
         TS = time.time()
         msg = await message.reply('<b>♻️ عملیات ریپورت بخش (scam) شروع شد ...</b>')
         for i in range(rpt_count):
             for session in chosen_accounts:
                 if evalID not in isWorking:
                     break
                 all_reports += 1
                 await asyncio.sleep(sleeping)
                 try:
                     api_id2, api_hash2 = await randomAPP()
                     cli = Client(f'sessions/{session}', api_id2, api_hash2)
                     await cli.connect()
                     await cli.invoke(functions.messages.Report(
                         peer=await cli.resolve_peer(chat_id_extracted),
                         id=[message_id_extracted],
                         reason=types.InputReportReasonScam(),
                         message=report_text))
                     await cli.disconnect()
                 except Exception as e:
                     try:
                         await cli.disconnect()
                     except:
                         pass
                     error += 1
                 else:
                     done += 1
                 spendTime = await remainTime(TS)
                 await bot.edit_message_text(chat_id, msg.id,
                     f'''♻️ عملیات ریپورت بخش (scam)
• کل ریپورت ها : {total_reports}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
         try:
             isWorking.remove(evalID)
         except:
             pass
         spendTime = await remainTime(TS)
         await message.reply(f'''<b>♻️ عملیات ریپورت بخش (scam) با موفقیت به پایان رسید ✅</b>
• کل ریپورت ها : {total_reports}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''')
    
    # For REPORT (spam)
    elif step == 'group_report_spam_request_link':
         global tempReportLink_group_spam
         tempReportLink_group_spam = text.strip()
         step = 'group_report_spam'
         await message.reply('<b>در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن ریپورت را وارد کنید :</b>')
    elif step == 'group_report_spam':
         evalID = await randomString()
         isWorking.append(evalID)
         parts = text.split("\n")
         if len(parts) < 3:
             await message.reply("<b>ورودی نامعتبر! لطفاً در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن ریپورت را وارد کنید.</b>")
             return
         try:
             acc_count = int(parts[0].strip())
             rpt_count = int(parts[1].strip())
         except:
             await message.reply("<b>عدد وارد شده معتبر نیست!</b>")
             return
         report_text = parts[2]
         link_parts = tempReportLink_group_spam.split('/')
         if link_parts[3] == "c":
             chat_id_extracted = int("-100" + link_parts[4])
             message_id_extracted = int(link_parts[5])
         else:
             chat_id_extracted = "@" + link_parts[3]
             message_id_extracted = int(link_parts[4])
         accounts = await accountList()
         chosen_accounts = accounts[:acc_count]
         total_reports = len(chosen_accounts) * rpt_count
         all_reports = 0
         error = 0
         done = 0
         TS = time.time()
         msg = await message.reply('<b>♻️ عملیات ریپورت بخش (spam) شروع شد ...</b>')
         for i in range(rpt_count):
             for session in chosen_accounts:
                 if evalID not in isWorking:
                     break
                 all_reports += 1
                 await asyncio.sleep(sleeping)
                 try:
                     api_id2, api_hash2 = await randomAPP()
                     cli = Client(f'sessions/{session}', api_id2, api_hash2)
                     await cli.connect()
                     await cli.invoke(functions.messages.Report(
                         peer=await cli.resolve_peer(chat_id_extracted),
                         id=[message_id_extracted],
                         reason=types.InputReportReasonSpam(),
                         message=report_text))
                     await cli.disconnect()
                 except Exception as e:
                     try:
                         await cli.disconnect()
                     except:
                         pass
                     error += 1
                 else:
                     done += 1
                 spendTime = await remainTime(TS)
                 await bot.edit_message_text(chat_id, msg.id,
                     f'''♻️ عملیات ریپورت بخش (spam)
• کل ریپورت ها : {total_reports}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
         try:
             isWorking.remove(evalID)
         except:
             pass
         spendTime = await remainTime(TS)
         await message.reply(f'''<b>♻️ عملیات ریپورت بخش (spam) با موفقیت به پایان رسید ✅</b>
• کل ریپورت ها : {total_reports}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''')
    
    # For REPORT (pornography)
    elif step == 'group_report_pornography_request_link':
         global tempReportLink_group_pornography
         tempReportLink_group_pornography = text.strip()
         step = 'group_report_pornography'
         await message.reply('<b>در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن گزارش را وارد کنید :</b>')
    elif step == 'group_report_pornography':
         evalID = await randomString()
         isWorking.append(evalID)
         parts = text.split("\n")
         if len(parts) < 3:
             await message.reply("<b>ورودی نامعتبر! لطفاً در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن گزارش را وارد کنید.</b>")
             return
         try:
             acc_count = int(parts[0].strip())
             rpt_count = int(parts[1].strip())
         except:
             await message.reply("<b>عدد وارد شده معتبر نیست!</b>")
             return
         report_text = parts[2]
         link_parts = tempReportLink_group_pornography.split('/')
         if link_parts[3] == "c":
             chat_id_extracted = int("-100" + link_parts[4])
             message_id_extracted = int(link_parts[5])
         else:
             chat_id_extracted = "@" + link_parts[3]
             message_id_extracted = int(link_parts[4])
         accounts = await accountList()
         chosen_accounts = accounts[:acc_count]
         total_reports = len(chosen_accounts) * rpt_count
         all_reports = 0
         error = 0
         done = 0
         TS = time.time()
         msg = await message.reply('<b>♻️ عملیات ریپورت بخش (pornography) شروع شد ...</b>')
         for i in range(rpt_count):
             for session in chosen_accounts:
                 if evalID not in isWorking:
                     break
                 all_reports += 1
                 await asyncio.sleep(sleeping)
                 try:
                     api_id2, api_hash2 = await randomAPP()
                     cli = Client(f'sessions/{session}', api_id2, api_hash2)
                     await cli.connect()
                     await cli.invoke(functions.messages.Report(
                         peer=await cli.resolve_peer(chat_id_extracted),
                         id=[message_id_extracted],
                         reason=types.InputReportReasonPornography(),
                         message=report_text))
                     await cli.disconnect()
                 except Exception as e:
                     try:
                         await cli.disconnect()
                     except:
                         pass
                     error += 1
                 else:
                     done += 1
                 spendTime = await remainTime(TS)
                 await bot.edit_message_text(chat_id, msg.id,
                     f'''♻️ عملیات ریپورت بخش (pornography)
• کل ریپورت ها : {total_reports}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
         try:
             isWorking.remove(evalID)
         except:
             pass
         spendTime = await remainTime(TS)
         await message.reply(f'''<b>♻️ عملیات ریپورت بخش (pornography) با موفقیت به پایان رسید ✅</b>
• کل ریپورت ها : {total_reports}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''')
    
    # For REPORT (fake)
    elif step == 'group_report_fake_request_link':
         global tempReportLink_group_fake
         tempReportLink_group_fake = text.strip()
         step = 'group_report_fake'
         await message.reply('<b>در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن ریپورت را وارد کنید :</b>')
    elif step == 'group_report_fake':
         evalID = await randomString()
         isWorking.append(evalID)
         parts = text.split("\n")
         if len(parts) < 3:
             await message.reply("<b>ورودی نامعتبر! لطفاً در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن ریپورت را وارد کنید.</b>")
             return
         try:
             acc_count = int(parts[0].strip())
             rpt_count = int(parts[1].strip())
         except:
             await message.reply("<b>عدد وارد شده معتبر نیست!</b>")
             return
         report_text = parts[2]
         link_parts = tempReportLink_group_fake.split('/')
         if link_parts[3] == "c":
             chat_id_extracted = int("-100" + link_parts[4])
             message_id_extracted = int(link_parts[5])
         else:
             chat_id_extracted = "@" + link_parts[3]
             message_id_extracted = int(link_parts[4])
         accounts = await accountList()
         chosen_accounts = accounts[:acc_count]
         total_reports = len(chosen_accounts) * rpt_count
         all_reports = 0
         error = 0
         done = 0
         TS = time.time()
         msg = await message.reply('<b>♻️ عملیات ریپورت بخش (fake) شروع شد ...</b>')
         for i in range(rpt_count):
             for session in chosen_accounts:
                 if evalID not in isWorking:
                     break
                 all_reports += 1
                 await asyncio.sleep(sleeping)
                 try:
                     api_id2, api_hash2 = await randomAPP()
                     cli = Client(f'sessions/{session}', api_id2, api_hash2)
                     await cli.connect()
                     await cli.invoke(functions.messages.Report(
                         peer=await cli.resolve_peer(chat_id_extracted),
                         id=[message_id_extracted],
                         reason=types.InputReportReasonFake(),
                         message=report_text))
                     await cli.disconnect()
                 except Exception as e:
                     try:
                         await cli.disconnect()
                     except:
                         pass
                     error += 1
                 else:
                     done += 1
                 spendTime = await remainTime(TS)
                 await bot.edit_message_text(chat_id, msg.id,
                     f'''♻️ عملیات ریپورت بخش (fake)
• کل ریپورت ها : {total_reports}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
         try:
             isWorking.remove(evalID)
         except:
             pass
         spendTime = await remainTime(TS)
         await message.reply(f'''<b>♻️ عملیات ریپورت بخش (fake) با موفقیت به پایان رسید ✅</b>
• کل ریپورت ها : {total_reports}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''')
    
    # For REPORT (Violence)
    elif step == 'group_report_violence_request_link':
         global tempReportLink_group_violence
         tempReportLink_group_violence = text.strip()
         step = 'group_report_violence'
         await message.reply('<b>در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن ریپورت را وارد کنید :</b>')
    elif step == 'group_report_violence':
         evalID = await randomString()
         isWorking.append(evalID)
         parts = text.split("\n")
         if len(parts) < 3:
             await message.reply("<b>ورودی نامعتبر! لطفاً در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن ریپورت را وارد کنید.</b>")
             return
         try:
             acc_count = int(parts[0].strip())
             rpt_count = int(parts[1].strip())
         except:
             await message.reply("<b>عدد وارد شده معتبر نیست!</b>")
             return
         report_text = parts[2]
         link_parts = tempReportLink_group_violence.split('/')
         if link_parts[3] == "c":
             chat_id_extracted = int("-100" + link_parts[4])
             message_id_extracted = int(link_parts[5])
         else:
             chat_id_extracted = "@" + link_parts[3]
             message_id_extracted = int(link_parts[4])
         accounts = await accountList()
         chosen_accounts = accounts[:acc_count]
         total_reports = len(chosen_accounts) * rpt_count
         all_reports = 0
         error = 0
         done = 0
         TS = time.time()
         msg = await message.reply('<b>♻️ عملیات ریپورت بخش (Violence) شروع شد ...</b>')
         for i in range(rpt_count):
             for session in chosen_accounts:
                 if evalID not in isWorking:
                     break
                 all_reports += 1
                 await asyncio.sleep(sleeping)
                 try:
                     api_id2, api_hash2 = await randomAPP()
                     cli = Client(f'sessions/{session}', api_id2, api_hash2)
                     await cli.connect()
                     await cli.invoke(functions.messages.Report(
                         peer=await cli.resolve_peer(chat_id_extracted),
                         id=[message_id_extracted],
                         reason=types.InputReportReasonViolence(),
                         message=report_text))
                     await cli.disconnect()
                 except Exception as e:
                     try:
                         await cli.disconnect()
                     except:
                         pass
                     error += 1
                 else:
                     done += 1
                 spendTime = await remainTime(TS)
                 await bot.edit_message_text(chat_id, msg.id,
                     f'''♻️ عملیات ریپورت بخش (Violence)
• کل ریپورت ها : {total_reports}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
         try:
             isWorking.remove(evalID)
         except:
             pass
         spendTime = await remainTime(TS)
         await message.reply(f'''<b>♻️ عملیات ریپورت بخش (Violence) با موفقیت به پایان رسید ✅</b>
• کل ریپورت ها : {total_reports}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''')
    
    # For REPORT (Illegal)
    elif step == 'group_report_illegal_request_link':
         global tempReportLink_group_illegal
         tempReportLink_group_illegal = text.strip()
         step = 'group_report_illegal'
         await message.reply('<b>در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن ریپورت را وارد کنید :</b>')
    elif step == 'group_report_illegal':
         evalID = await randomString()
         isWorking.append(evalID)
         parts = text.split("\n")
         if len(parts) < 3:
             await message.reply("<b>ورودی نامعتبر! لطفاً در خط اول تعداد اکانت، در خط دوم تعداد گزارش و در خط سوم متن ریپورت را وارد کنید.</b>")
             return
         try:
             acc_count = int(parts[0].strip())
             rpt_count = int(parts[1].strip())
         except:
             await message.reply("<b>عدد وارد شده معتبر نیست!</b>")
             return
         report_text = parts[2]
         link_parts = tempReportLink_group_illegal.split('/')
         if link_parts[3] == "c":
             chat_id_extracted = int("-100" + link_parts[4])
             message_id_extracted = int(link_parts[5])
         else:
             chat_id_extracted = "@" + link_parts[3]
             message_id_extracted = int(link_parts[4])
         accounts = await accountList()
         chosen_accounts = accounts[:acc_count]
         total_reports = len(chosen_accounts) * rpt_count
         all_reports = 0
         error = 0
         done = 0
         TS = time.time()
         msg = await message.reply('<b>♻️ عملیات ریپورت بخش (Illegal) شروع شد ...</b>')
         for i in range(rpt_count):
             for session in chosen_accounts:
                 if evalID not in isWorking:
                     break
                 all_reports += 1
                 await asyncio.sleep(sleeping)
                 try:
                     api_id2, api_hash2 = await randomAPP()
                     cli = Client(f'sessions/{session}', api_id2, api_hash2)
                     await cli.connect()
                     await cli.invoke(functions.messages.Report(
                         peer=await cli.resolve_peer(chat_id_extracted),
                         id=[message_id_extracted],
                         reason=types.InputReportReasonIllegalDrugs(),
                         message=report_text))
                     await cli.disconnect()
                 except Exception as e:
                     try:
                         await cli.disconnect()
                     except:
                         pass
                     error += 1
                 else:
                     done += 1
                 spendTime = await remainTime(TS)
                 await bot.edit_message_text(chat_id, msg.id,
                     f'''♻️ عملیات ریپورت بخش (Illegal)
• اکانت های بررسی شده : {all_reports}/{len(chosen_accounts)}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}
برای لغو این عملیات از دستور ( /stop_{evalID} ) استفاده نمایید.''')
         try:
             isWorking.remove(evalID)
         except:
             pass
         spendTime = await remainTime(TS)
         await message.reply(f'''<b>♻️ عملیات ریپورت بخش (Illegal) با موفقیت به پایان رسید ✅</b>
• کل ریپورت ها : {total_reports}
• موفق : {done}
• خطا : {error}
• زمان سپری شده : {spendTime}''')

bot.run()