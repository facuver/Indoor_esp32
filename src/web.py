from microdot_asyncio import Microdot, send_file
from wifi import interface, get_scans
from cfg import configs, update_configs, update_automation, automation
from periferics import get_status

app = Microdot()


@app.get("/")
async def index(request):
    return send_file("/public/index.html")


@app.get("/public/<fn>")
async def get_public(request, fn):
    return send_file("/public/{}".format(fn))


@app.get("/api/ifconfig")
async def ifconfig(request):
    return {"status": list(interface.ifconfig())}


@app.get("/api/scans")
async def scan(request):
    return {"net": get_scans()}


@app.get("/api/log")
async def log(request):
    return send_file("/log.txt")


@app.get("/api/clear_log")
async def clear_log(request):
    with open("/log.txt", "w") as f:
        f.write("")
    return "Log Cleared"


@app.post("/api/connect")
async def post_connect(request):
    net = request.json
    print(net)
    configs["STA_essid"] = net["essid"]
    configs["STA_password"] = net["password"]
    update_configs(configs)
    from machine import reset

    reset()


@app.get("/api/home")
async def home(request):
    return get_status()


@app.post("/api/update_automation")
async def update_auto(request):
    res = request.json
    print(res)
    automation["ligth"]["time_on"] = int(res["ligth"]["time_on"])
    automation["ligth"]["time_off"] = int(res["ligth"]["time_off"])
    automation["soil_target"] = int(res["soil_target"])
    automation["humidity_target"] = int(res["humidity_target"])
    update_automation(automation)
    return "OK"
