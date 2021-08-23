from cfg import configs
import wifi
import ntptime

print(configs)


wifi.do_create()
if configs["STA_essid"]:
    wifi.do_connect(configs["STA_essid"], configs["STA_password"])


ntptime.host = "time.google.com"
ntptime.settime()
