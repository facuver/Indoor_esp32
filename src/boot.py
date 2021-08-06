# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
# esp.osdebug(None)
#import webrepl
# webrepl.start()


from cfg import configs, ip
import wifi


print(configs)


if configs["STA_essid"]:

    ip = wifi.do_connect(configs["STA_essid"], configs["STA_password"])
    print(ip)
