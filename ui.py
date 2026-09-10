"""AutoTTS stüdyo görünümü: yerleşim, renkler ve görsel bileşenler."""
import tkinter as tk
import customtkinter as ctk

BG = '#F3F5F7'
SURFACE = '#FFFFFF'
INK = '#182932'
MUTED = '#697A85'
BORDER = '#E2E8EC'
ACCENT = '#087F73'
HOVER = '#06695F'
DARK = '#172C35'
FONT = 'Helvetica Neue'


def label(parent, text, size=13, color=INK, bold=False, **kwargs):
    kwargs.setdefault('height', max(18, size + 6))
    return ctk.CTkLabel(parent, text=text, font=(FONT, size, 'bold' if bold else 'normal'),
                       text_color=color, **kwargs)


def card(parent):
    return ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=18,
                       border_width=1, border_color=BORDER)


def button(parent, text, command, primary=False, **kwargs):
    return ctk.CTkButton(parent, text=text, command=command, height=38, corner_radius=10,
                        font=(FONT, 13, 'bold'), fg_color=ACCENT if primary else '#EDF3F4',
                        hover_color=HOVER if primary else '#DFE9EC',
                        text_color='white' if primary else INK, text_color_disabled='#8B9BA4', **kwargs)


def menu(parent, values, width=240):
    return ctk.CTkOptionMenu(parent, values=values, width=width, height=36,
                             corner_radius=9, font=(FONT, 13), dropdown_font=(FONT, 13),
                             fg_color='#F0F4F6', button_color='#F0F4F6', button_hover_color='#DDE8EB',
                             text_color=INK, text_color_disabled=MUTED, dropdown_fg_color=SURFACE,
                             dropdown_text_color=INK, dropdown_hover_color='#E3F2EE',
                             dynamic_resizing=False)


def slider(parent, command, **kwargs):
    return ctk.CTkSlider(parent, command=command, height=18, border_width=5,
                         fg_color=BORDER, progress_color=ACCENT, button_color=ACCENT,
                         button_hover_color=HOVER, button_length=14, **kwargs)


class Waveform(tk.Canvas):
    """Üretilen gerçek örnekleri özetler; oynatılan bölümü renklendirir."""
    def __init__(self, parent):
        super().__init__(parent, height=35, bg=DARK, highlightthickness=0, bd=0)
        self.samples = None
        self.fraction = 0
        self.bind('<Configure>', lambda _: self.redraw())

    def set_audio(self, samples):
        self.samples = samples
        self.redraw()

    def set_position(self, fraction):
        fraction = max(0, min(1, fraction))
        if abs(fraction - self.fraction) > .002:
            self.fraction = fraction
            self.redraw()

    def redraw(self):
        self.delete('all')
        width, height = self.winfo_width(), self.winfo_height()
        if self.samples is None or len(self.samples) == 0:
            self.create_line(0, height / 2, width, height / 2, fill='#37505A', width=2)
            return
        import numpy as np
        # Geniş girdilerde çizim maliyeti ekran genişliğiyle sınırlı tutulur.
        count = max(1, width // 5)
        stride = max(1, len(self.samples) // 12000)
        sampled = np.abs(self.samples[::stride])
        peak = max(float(sampled.max()), .001)
        for i, chunk in enumerate(np.array_split(sampled, count)):
            magnitude = float(chunk.max()) / peak if chunk.size else 0
            bar = max(2, magnitude * (height - 4))
            x = i * 5 + 2
            self.create_line(x, (height - bar) / 2, x, (height + bar) / 2,
                             fill='#66D7BF' if i / count <= self.fraction else '#58727D',
                             width=2, capstyle=tk.ROUND)


def build_interface(app):
    """Widget referansları kontrolcü üzerinde kalır; iş mantığı burada bulunmaz."""
    ctk.set_appearance_mode('light')
    app.configure(fg_color=BG)
    app.geometry('1180x840')
    app.minsize(980, 760)
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(2, weight=1)

    header = ctk.CTkFrame(app, fg_color=SURFACE, corner_radius=0, height=70)
    header.grid(row=0, column=0, sticky='ew')
    header.grid_columnconfigure(2, weight=1)
    label(header, '≋', 30, 'white', True, width=42, height=42, fg_color=ACCENT,
          corner_radius=12).grid(row=0, column=0, padx=(28, 12), pady=11)
    label(header, 'AutoTTS', 23, bold=True).grid(row=0, column=1)
    label(header, 'SES STÜDYOSU', 10, MUTED, True).grid(row=0, column=2, padx=20, sticky='w')
    label(header, '●  Yerel ses üretimi', 12, ACCENT, fg_color='#E8F5EF',
          corner_radius=12, width=165, height=32).grid(row=0, column=3, padx=28)

    intro = ctk.CTkFrame(app, fg_color='transparent')
    intro.grid(row=1, column=0, padx=30, pady=(16, 14), sticky='ew')
    label(intro, 'Metninize ses verin.', 28, bold=True).pack(anchor='w')
    label(intro, 'Yazın, bir ses seçin ve dinleyin. Her şey tek bir çalışma alanında.',
          13, MUTED).pack(anchor='w', pady=(3, 0))

    workspace = ctk.CTkFrame(app, fg_color='transparent')
    workspace.grid(row=2, column=0, padx=28, sticky='nsew')
    workspace.grid_columnconfigure(0, weight=1)
    workspace.grid_columnconfigure(1, minsize=310)
    workspace.grid_rowconfigure(0, weight=1)
    editor = card(workspace)
    editor.grid(row=0, column=0, sticky='nsew', padx=(0, 18))
    editor.grid_columnconfigure(0, weight=1)
    editor.grid_rowconfigure(1, weight=1)
    editor_header = ctk.CTkFrame(editor, fg_color='transparent')
    editor_header.grid(row=0, column=0, padx=22, pady=(18, 8), sticky='ew')
    label(editor_header, 'Metin editörü', 16, bold=True).pack(side='left')
    label(editor_header, 'İNGİLİZCE', 10, MUTED, True, fg_color=BG,
          corner_radius=7, width=80, height=25).pack(side='right')
    app.text = ctk.CTkTextbox(editor, font=(FONT, 17), wrap='word', fg_color=SURFACE,
                             text_color=INK, corner_radius=0, border_width=0,
                             scrollbar_button_color='#D8E2E6', scrollbar_button_hover_color='#B8CBD2')
    app.text.grid(row=1, column=0, padx=18, pady=4, sticky='nsew')
    app.text._textbox.configure(spacing1=3, spacing3=5, insertbackground=ACCENT)
    app.placeholder = label(app.text, 'İngilizce metninizi buraya yazın\nveya yapıştırın…',
                            17, '#93A0A8', justify='left')
    app.placeholder.place(x=8, y=8)
    app.placeholder.bind('<Button-1>', lambda _: app.text.focus_set())
    editor_footer = ctk.CTkFrame(editor, fg_color='transparent')
    editor_footer.grid(row=2, column=0, padx=22, pady=(6, 18), sticky='ew')
    app.word_count = label(editor_footer, '0 kelime · 0 karakter', 11, MUTED)
    app.word_count.pack(side='left')
    label(editor_footer, '⌘ + Enter  seslendir', 11, MUTED).pack(side='right')

    side = ctk.CTkFrame(workspace, fg_color='transparent', width=310)
    side.grid(row=0, column=1, sticky='nsew')
    side.grid_columnconfigure(0, weight=1)
    settings = card(side)
    settings.grid(row=0, column=0, sticky='ew')
    settings.grid_columnconfigure(0, weight=1)
    label(settings, 'Ses ayarları', 16, bold=True).grid(row=0, column=0, padx=20, pady=(17, 12), sticky='w')
    label(settings, 'SES', 10, MUTED, True).grid(row=1, column=0, padx=20, sticky='w')
    app.voice = menu(settings, list(app.voice_map), 270)
    app.voice.grid(row=2, column=0, padx=20, pady=(5, 13), sticky='ew')
    speed_header = ctk.CTkFrame(settings, fg_color='transparent')
    speed_header.grid(row=3, column=0, padx=20, sticky='ew')
    label(speed_header, 'KONUŞMA HIZI', 10, MUTED, True).pack(side='left')
    app.speed_label = label(speed_header, '1.00x', 12, ACCENT, True)
    app.speed_label.pack(side='right')
    app.speed = slider(settings, app._speed_changed, from_=0.5, to=2, number_of_steps=30)
    app.speed.set(1)
    app.speed.grid(row=4, column=0, padx=18, pady=(7, 0), sticky='ew')
    endpoints = ctk.CTkFrame(settings, fg_color='transparent')
    endpoints.grid(row=5, column=0, padx=20, sticky='ew')
    label(endpoints, '0.5x', 10, MUTED).pack(side='left')
    label(endpoints, '2.0x', 10, MUTED).pack(side='right')
    app.generate = button(settings, 'Seslendir  →', app._generate, primary=True)
    app.generate.grid(row=6, column=0, padx=20, pady=(10, 18), sticky='ew')

    batch = card(side)
    batch.grid(row=1, column=0, pady=(14, 0), sticky='new')
    batch.grid_columnconfigure(0, weight=1)
    label(batch, 'Toplu seslendirme', 15, bold=True).grid(row=0, column=0, columnspan=2,
                                                     padx=20, pady=(14, 0), sticky='w')
    app.batch_label = label(batch, 'Birden fazla TXT dosyasını sırayla işleyin.', 11, MUTED,
                            wraplength=265, justify='left')
    app.batch_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(3, 10), sticky='w')
    app.pick = button(batch, '+  TXT dosyaları', app._pick, width=150)
    app.pick.grid(row=2, column=0, padx=(20, 8), sticky='ew')
    app.batch_format = menu(batch, ['WAV', 'MP3'], 90)
    app.batch_format.grid(row=2, column=1, padx=(0, 20))
    app.batch_button = button(batch, 'Toplu seslendir  →', app._batch)
    app.batch_button.grid(row=3, column=0, columnspan=2, padx=20, pady=(8, 16), sticky='ew')

    player = ctk.CTkFrame(app, fg_color=DARK, corner_radius=18)
    player.grid(row=3, column=0, padx=28, pady=(18, 0), sticky='ew')
    player.grid_columnconfigure(1, weight=1)
    app.play = button(player, '▶ Oynat', app._play, primary=True, width=118, state='disabled')
    app.play.grid(row=0, column=0, rowspan=2, padx=(20, 18), pady=(18, 6))
    app.audio_title = label(player, 'Ses önizlemesi', 14, '#F3F7F8', True)
    app.audio_title.grid(row=0, column=1, pady=(14, 0), sticky='w')
    app.waveform = Waveform(player)
    app.waveform.grid(row=1, column=1, padx=(0, 18), sticky='ew')
    export = ctk.CTkFrame(player, fg_color='transparent')
    export.grid(row=0, column=2, rowspan=2, padx=(0, 20), pady=(14, 0))
    label(export, 'DIŞA AKTAR', 9, '#A3B8C2', True).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
    app.export_format = menu(export, ['WAV', 'MP3'], 90)
    app.export_format.grid(row=1, column=0, padx=(0, 8))
    app.save = button(export, 'Kaydet ↗', app._save, width=96, state='disabled')
    app.save.grid(row=1, column=1)
    transport = ctk.CTkFrame(player, fg_color='transparent')
    transport.grid(row=2, column=0, columnspan=3, padx=20, pady=(4, 15), sticky='ew')
    transport.grid_columnconfigure(1, weight=1)
    app.rewind = ctk.CTkButton(transport, text='−10 sn', command=lambda: app._skip(-10),
                              width=65, height=28, fg_color='#28414C', hover_color='#385763', state='disabled')
    app.rewind.grid(row=0, column=0, padx=(0, 12))
    app.timeline = slider(transport, app._seek, from_=0, to=1, state='disabled')
    app.timeline.configure(fg_color='#37505A', progress_color='#66D7BF', button_color='#66D7BF')
    app.timeline.set(0)
    app.timeline.grid(row=0, column=1, sticky='ew')
    app.forward = ctk.CTkButton(transport, text='+10 sn', command=lambda: app._skip(10),
                               width=65, height=28, fg_color='#28414C', hover_color='#385763', state='disabled')
    app.forward.grid(row=0, column=2, padx=12)
    app.time_label = label(transport, '00:00 / 00:00', 12, '#BFD0D7', width=105)
    app.time_label.grid(row=0, column=3)

    footer = ctk.CTkFrame(app, fg_color='transparent')
    footer.grid(row=4, column=0, padx=30, pady=(10, 13), sticky='ew')
    footer.grid_columnconfigure(0, weight=1)
    app.status = label(footer, 'Hazır · İlk seslendirmede model indirilir.', 11, MUTED, anchor='w')
    app.status.grid(row=0, column=0, sticky='ew')
    app.progress = ctk.CTkProgressBar(footer, width=125, height=4, fg_color=BORDER, progress_color=ACCENT)
    app.progress.grid(row=0, column=1, padx=(15, 0))
    app.progress.set(0)
    app.playback_controls = [app.play, app.timeline, app.rewind, app.forward]
    app.controls = [app.generate, app.voice, app.speed, app.pick, app.batch_button,
                    app.batch_format, app.export_format]
