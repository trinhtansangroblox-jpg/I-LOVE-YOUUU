import platform
import random
import subprocess
import sys

BANG_MAU = [
    ("#FFE4E6", "#FFF1F2", "#FB7185"),
    ("#FCE7F3", "#FDF2F8", "#F472B6"),
    ("#F3E8FF", "#FAF5FF", "#C084FC"),
    ("#E0E7FF", "#EEF2FF", "#818CF8"),
    ("#E0F2FE", "#F0F9FF", "#38BDF8"),
    ("#DCFCE7", "#F0FDF4", "#4ADE80"),
    ("#FEF3C7", "#FFFBEB", "#FBBF24"),
    ("#FFEDD5", "#FFF7ED", "#FB923C"),
]

LOI_NHAN = ["I LOVE YOUU ✨"]
GIOI_HAN_CUA_SO = 85
danh_sach_thu = []


def tu_dong_cai_thu_vien_linux():
  try:
    import cairo
    import gi
  except ImportError:
    try:
      subprocess.check_call([
          sys.executable,
          "-m",
          "pip",
          "install",
          "PyGObject",
          "pycairo",
          "--quiet",
      ])
    except Exception:
      subprocess.call([
          "sudo",
          "apt",
          "install",
          "-y",
          "python3-gi",
          "python3-gi-cairo",
          "gir1.2-gtk-3.0",
      ])


def tu_dong_cai_thu_vien_windows():
  try:
    import tkinter
  except ImportError:
    try:
      subprocess.check_call(
          [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--quiet"]
      )
      subprocess.check_call(
          [sys.executable, "-m", "pip", "install", "tk", "--quiet"]
      )
    except Exception:
      try:
        subprocess.check_call([
            "winget",
            "install",
            "-e",
            "--id",
            "Python.Python.3.12",
            "--silent",
            "--accept-package-agreements",
            "--accept-source-agreements",
        ])
      except Exception:
        pass

  for goi in ["customtkinter", "pywinstyles", "darkdetect", "packaging"]:
    try:
      __import__(goi)
    except ImportError:
      try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", goi, "--quiet"]
        )
      except Exception:
        pass


def chay_tren_linux():
  tu_dong_cai_thu_vien_linux()
  import cairo
  import gi

  gi.require_version("Gtk", "3.0")
  gi.require_version("Gdk", "3.0")
  from gi.repository import Gdk, GLib, Gtk

  css_provider = Gtk.CssProvider()
  css_provider.load_from_data(b"""
        .btn-metoo {
            background-image: linear-gradient(135deg, #FF5E8E, #FF2A6D);
            color: #FFFFFF;
            border-radius: 14px;
            border: none;
            padding: 5px 15px;
            font-weight: bold;
            box-shadow: 0 3px 8px rgba(255, 42, 109, 0.35);
        }
        .btn-metoo:hover {
            background-image: linear-gradient(135deg, #FF477E, #E01E5A);
        }
        .btn-khong {
            background-color: rgba(255, 255, 255, 0.85);
            color: #4A4A4A;
            border-radius: 14px;
            border: 1px solid rgba(0, 0, 0, 0.08);
            padding: 5px 14px;
            font-weight: 600;
        }
        .btn-close {
            color: #666666;
            border-radius: 50%;
            padding: 2px 6px;
        }
        .btn-close:hover {
            background-color: rgba(255, 94, 142, 0.2);
            color: #E01E5A;
        }
    """)
  Gtk.StyleContext.add_provider_for_screen(
      Gdk.Screen.get_default(),
      css_provider,
      Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
  )

  def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) / 255.0 for i in (0, 2, 4))

  class LaThuGTK(Gtk.Window):

    def __init__(self, screen_w, screen_h):
      super().__init__(type=Gtk.WindowType.TOPLEVEL)
      self.pad = 14
      self.card_w, self.card_h = 330, 195
      self.w = self.card_w + self.pad * 2
      self.h = self.card_h + self.pad * 2

      c1, c2, border_c = random.choice(BANG_MAU)
      self.rgb1 = hex_to_rgb(c1)
      self.rgb2 = hex_to_rgb(c2)
      self.rgb_border = hex_to_rgb(border_c)
      self.noi_dung = random.choice(LOI_NHAN)

      screen = self.get_screen()
      visual = screen.get_rgba_visual()
      if visual and screen.is_composited():
        self.set_visual(visual)

      self.set_app_paintable(True)
      self.set_decorated(False)
      self.set_keep_above(True)
      self.set_skip_taskbar_hint(True)
      self.set_default_size(self.w, self.h)

      x = random.randint(0, max(20, screen_w - self.w))
      y = random.randint(0, max(20, screen_h - self.h))
      self.move(x, y)

      self.connect("draw", self.ve_thiep_nghe_thuat)
      self.connect("key-press-event", self.kiem_tra_phim_thoat)

      self.fixed = Gtk.Fixed()
      self.add(self.fixed)

      lbl_to = Gtk.Label()
      lbl_to.set_markup(
          '<span foreground="#4B5563" size="8500"><i><b>💌 to the person I'
          " have a crush on</b></i></span>"
      )
      self.fixed.put(lbl_to, self.pad + 16, self.pad + 16)

      btn_close = Gtk.Button(label="✕")
      btn_close.set_relief(Gtk.ReliefStyle.NONE)
      btn_close.get_style_context().add_class("btn-close")
      btn_close.connect("clicked", self.on_close_clicked)
      self.fixed.put(btn_close, self.pad + self.card_w - 34, self.pad + 9)

      self.lbl_msg = Gtk.Label()
      self.lbl_msg.set_markup(
          f'<span foreground="#1F2937" size="13500"><b>{self.noi_dung}</b></span>'
      )
      self.lbl_msg.set_size_request(self.card_w - 40, 48)
      self.lbl_msg.set_justify(Gtk.Justification.CENTER)
      self.fixed.put(self.lbl_msg, self.pad + 20, self.pad + 56)

      self.btn_metoo = Gtk.Button(label="Me too 💖")
      self.btn_metoo.get_style_context().add_class("btn-metoo")
      self.btn_metoo.connect("clicked", self.on_metoo_clicked)
      self.fixed.put(self.btn_metoo, self.pad + 64, self.pad + 116)

      self.btn_khong = Gtk.Button(label="Không")
      self.btn_khong.get_style_context().add_class("btn-khong")
      self.btn_khong.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)
      self.btn_khong.connect("enter-notify-event", self.on_khong_hover)
      self.fixed.put(self.btn_khong, self.pad + 186, self.pad + 116)

      lbl_footer = Gtk.Label()
      lbl_footer.set_markup(
          '<span foreground="#6B7280" size="8000"><i>— From Sang —</i></span>'
      )
      lbl_footer.set_size_request(self.card_w - 40, 20)
      self.fixed.put(lbl_footer, self.pad + 20, self.pad + self.card_h - 27)

      self.show_all()

    def ve_duong_bo_goc(self, cr, x, y, w, h, radius):
      pi = 3.141592653589793
      cr.new_sub_path()
      cr.arc(x + w - radius, y + radius, radius, -pi / 2, 0)
      cr.arc(x + w - radius, y + h - radius, radius, 0, pi / 2)
      cr.arc(x + radius, y + h - radius, radius, pi / 2, pi)
      cr.arc(x + radius, y + radius, radius, pi, 3 * pi / 2)
      cr.close_path()

    def ve_thiep_nghe_thuat(self, widget, cr):
      cr.set_operator(cairo.OPERATOR_CLEAR)
      cr.paint()
      cr.set_operator(cairo.OPERATOR_OVER)

      for i in range(6, 0, -1):
        self.ve_duong_bo_goc(
            cr,
            self.pad - i * 0.8,
            self.pad - i * 0.4 + 2.5,
            self.card_w + i * 1.6,
            self.card_h + i * 1.6,
            24 + i,
        )
        cr.set_source_rgba(
            self.rgb_border[0],
            self.rgb_border[1],
            self.rgb_border[2],
            0.045 * (7 - i),
        )
        cr.fill()

      grad = cairo.LinearGradient(
          self.pad, self.pad, self.pad + self.card_w, self.pad + self.card_h
      )
      grad.add_color_stop_rgb(0.0, *self.rgb1)
      grad.add_color_stop_rgb(1.0, *self.rgb2)

      self.ve_duong_bo_goc(cr, self.pad, self.pad, self.card_w, self.card_h, 24)
      cr.set_source(grad)
      cr.fill_preserve()

      cr.set_source_rgba(
          self.rgb_border[0], self.rgb_border[1], self.rgb_border[2], 0.85
      )
      cr.set_line_width(1.6)
      cr.stroke()

      self.ve_duong_bo_goc(
          cr, self.pad + 5, self.pad + 5, self.card_w - 10, self.card_h - 10, 20
      )
      cr.set_source_rgba(1.0, 1.0, 1.0, 0.65)
      cr.set_line_width(1.0)
      cr.stroke()

    def on_khong_hover(self, widget, event):
      nx = random.randint(self.pad + 16, self.pad + self.card_w - 92)
      ny = random.randint(self.pad + 42, self.pad + self.card_h - 58)
      self.fixed.move(self.btn_khong, nx, ny)

    def on_metoo_clicked(self, button):
      self.lbl_msg.set_markup(
          '<span foreground="#E11D48" size="13500"><b>Yêu thế! 🥰</b></span>'
      )
      self.btn_khong.hide()
      self.btn_metoo.hide()
      GLib.timeout_add(900, self.dong_nhe_nhang)

    def dong_nhe_nhang(self):
      if self in danh_sach_thu:
        danh_sach_thu.remove(self)
      self.destroy()
      return False

    def on_close_clicked(self, button):
      if self in danh_sach_thu:
        danh_sach_thu.remove(self)
      self.destroy()
      for _ in range(2):
        if len(danh_sach_thu) < GIOI_HAN_CUA_SO:
          sinh_mot_la_thu()

    def kiem_tra_phim_thoat(self, widget, event):
      if event.keyval == Gdk.KEY_Escape:
        Gtk.main_quit()

  display = Gdk.Display.get_default()
  monitor = display.get_primary_monitor() or display.get_monitor(0)
  geo = monitor.get_geometry()
  screen_w, screen_h = geo.width, geo.height

  def sinh_mot_la_thu():
    if len(danh_sach_thu) < GIOI_HAN_CUA_SO:
      thu = LaThuGTK(screen_w, screen_h)
      danh_sach_thu.append(thu)
    return True

  def chay_ngau_nhien():
    sinh_mot_la_thu()
    delay = random.randint(70, 350)
    GLib.timeout_add(delay, chay_ngau_nhien)
    return False

  GLib.timeout_add(100, chay_ngau_nhien)
  Gtk.main()


def chay_tren_windows():
  tu_dong_cai_thu_vien_windows()
  import customtkinter as ctk
  import pywinstyles

  ctk.set_appearance_mode("light")
  CHROMA_KEY = "#000001"

  def dong_mot_thu(cua_so):
    if cua_so in danh_sach_thu:
      danh_sach_thu.remove(cua_so)
    cua_so.destroy()
    for _ in range(2):
      if len(danh_sach_thu) < GIOI_HAN_CUA_SO:
        tao_la_thu()

  def tao_la_thu():
    if len(danh_sach_thu) >= GIOI_HAN_CUA_SO:
      return

    thu = ctk.CTkToplevel(root)
    danh_sach_thu.append(thu)

    mau_nen, mau_trong, mau_vien = random.choice(BANG_MAU)
    noi_dung = random.choice(LOI_NHAN)

    w, h = 340, 205
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = random.randint(10, max(50, screen_w - w - 10))
    y = random.randint(10, max(50, screen_h - h - 10))

    thu.geometry(f"{w}x{h}+{x}+{y}")
    thu.overrideredirect(True)
    thu.attributes("-topmost", True)
    thu.configure(fg_color=CHROMA_KEY)

    try:
      pywinstyles.set_opacity(thu, color=CHROMA_KEY)
    except Exception:
      try:
        thu.wm_attributes("-transparentcolor", CHROMA_KEY)
      except Exception:
        pass

    outer_card = ctk.CTkFrame(
        thu,
        width=w,
        height=h,
        corner_radius=26,
        fg_color=mau_nen,
        border_width=2,
        border_color=mau_vien,
        bg_color=CHROMA_KEY,
    )
    outer_card.pack(fill="both", expand=True)

    inner_card = ctk.CTkFrame(
        outer_card,
        width=w - 12,
        height=h - 12,
        corner_radius=21,
        fg_color=mau_trong,
        border_width=1,
        border_color="#FFFFFF",
    )
    inner_card.place(x=6, y=6)

    lbl_to = ctk.CTkLabel(
        inner_card,
        text="💌 to the person I have a crush on",
        text_color="#4B5563",
        font=("Segoe UI", 11, "bold italic"),
    )
    lbl_to.place(x=14, y=10)

    btn_x = ctk.CTkButton(
        inner_card,
        text="✕",
        width=24,
        height=24,
        corner_radius=12,
        fg_color="transparent",
        hover_color="#FFE4E6",
        text_color="#6B7280",
        font=("Segoe UI", 11, "bold"),
        command=lambda w=thu: dong_mot_thu(w),
    )
    btn_x.place(x=w - 44, y=9)

    lbl_msg = ctk.CTkLabel(
        inner_card,
        text=noi_dung,
        text_color="#1F2937",
        font=("Segoe UI", 18, "bold"),
        width=w - 52,
    )
    lbl_msg.place(x=20, y=54)

    def bam_metoo():
      lbl_msg.configure(text="Yêu thế! 🥰", text_color="#E11D48")
      btn_metoo.place_forget()
      btn_khong.place_forget()
      thu.after(
          900,
          lambda: (
              danh_sach_thu.remove(thu) if thu in danh_sach_thu else None,
              thu.destroy(),
          ),
      )

    btn_metoo = ctk.CTkButton(
        inner_card,
        text="Me too 💖",
        width=102,
        height=34,
        corner_radius=17,
        fg_color="#FF477E",
        hover_color="#E01E5A",
        text_color="#FFFFFF",
        font=("Segoe UI", 12, "bold"),
        command=bam_metoo,
    )
    btn_metoo.place(x=58, y=112)

    def tron_chuot(event):
      nx = random.randint(18, w - 115)
      ny = random.randint(42, h - 75)
      btn_khong.place(x=nx, y=ny)

    btn_khong = ctk.CTkButton(
        inner_card,
        text="Không",
        width=88,
        height=34,
        corner_radius=17,
        fg_color="#F3F4F6",
        hover_color="#E5E7EB",
        border_width=1,
        border_color="#D1D5DB",
        text_color="#374151",
        font=("Segoe UI", 12, "bold"),
    )
    btn_khong.place(x=180, y=112)
    btn_khong.bind("<Enter>", tron_chuot)

    lbl_footer = ctk.CTkLabel(
        inner_card,
        text="— From Sang —",
        text_color="#6B7280",
        font=("Segoe UI", 10, "italic"),
        width=w - 52,
    )
    lbl_footer.place(x=20, y=h - 38)

  def chay_ngau_nhien():
    tao_la_thu()
    delay = random.randint(70, 350)
    root.after(delay, chay_ngau_nhien)

  def thoat_tat_ca(event=None):
    root.destroy()

  root = ctk.CTk()
  root.withdraw()
  root.bind_all("<Escape>", thoat_tat_ca)

  chay_ngau_nhien()
  root.mainloop()


if __name__ == "__main__":
  if platform.system() == "Linux":
    chay_tren_linux()
  else:
    chay_tren_windows()