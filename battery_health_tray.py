import os
import subprocess
import threading
from datetime import datetime
from typing import Any

import pystray
import wmi
from PIL import Image, ImageDraw, ImageFont
from pystray import MenuItem as item  # noqa: N813


UPDATE_SECONDS = 3600
ICON_SIZE = 32
FONTS = (
    r'C:\Windows\Fonts\segoeui.ttf',
    r'C:\Windows\Fonts\SegoeUI.ttf',
    r'C:\Windows\Fonts\arial.ttf',
)


def battery() -> tuple[int | None, int | None, int | None]:
    try:
        c = wmi.WMI(namespace=r'root\wmi')
        design: int = sum(
            int(s.DesignedCapacity)
            for s in c.BatteryStaticData()
            if getattr(s, 'DesignedCapacity', None) is not None
        )
        full: int = sum(
            int(f.FullChargedCapacity)
            for f in c.BatteryFullChargedCapacity()
            if getattr(f, 'FullChargedCapacity', None) is not None
        )
        if not design or not full or design <= 0:
            return None, None, None
        h = max(0, min(round(full / design * 100), 999))
        return h, full, design
    except Exception:
        return None, None, None


def icon_img(text: str) -> Image.Image:
    img = Image.new('RGBA', (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(
        [1, 1, ICON_SIZE - 1, ICON_SIZE - 1], radius=6, fill=(20, 20, 20, 255)
    )
    font = next(
        (
            ImageFont.truetype(p, 16 if len(text) <= 2 else 13)
            for p in FONTS
            if os.path.exists(p)
        ),
        ImageFont.load_default(),
    )
    b = d.textbbox((0, 0), text, font=font)
    d.text(
        ((ICON_SIZE - (b[2] - b[0])) // 2, (ICON_SIZE - (b[3] - b[1])) // 2 - 1),
        text,
        font=font,
        fill=(255, 255, 255, 255),
    )
    return img


class Tray:
    def __init__(self) -> None:
        self.stop = threading.Event()
        self.icon = pystray.Icon('BatteryHealth')
        self.icon.menu = pystray.Menu(
            item('立即更新', self.update),
            item('產生 battery-report.html', self.report),
            item('離開', self.quit),
        )

    def update(self, *_: Any) -> None:
        h, full, design = battery()
        text = '??' if h is None else str(h)
        tip = (
            'Battery health unavailable'
            if h is None
            else (
                f'Battery health: {h}%\nFull Charge: {full} mWh\nDesign: {design} mWh\nUpdated: {datetime.now():%Y-%m-%d %H:%M:%S}'
            )
        )
        self.icon.icon, self.icon.title = icon_img(text), tip

    def loop(self) -> None:
        self.update()
        while not self.stop.wait(UPDATE_SECONDS):
            self.update()

    def report(self, *_: Any) -> None:
        try:
            out = os.path.join(os.path.expanduser('~'), 'battery-report.html')
            subprocess.run(['powercfg', '/batteryreport', '/output', out], check=False)
            os.startfile(out)
        except Exception as e:
            self.icon.title = str(e)

    def quit(self, *_: Any) -> None:
        self.stop.set()
        self.icon.stop()

    def run(self) -> None:
        threading.Thread(target=self.loop, daemon=True).start()
        self.icon.run()


if __name__ == '__main__':
    Tray().run()
