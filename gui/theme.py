# gui/theme.py
"""Thiết lập theme và style cho ứng dụng"""
from tkinter import ttk

class AppTheme:
    """Quản lý theme và styling cho ứng dụng"""
    
    # Màu sắc
    PRIMARY_COLOR = "#2196F3"
    PRIMARY_DARK = "#1976D2"
    SUCCESS_COLOR = "#4CAF50"
    WARNING_COLOR = "#FFC107"
    DANGER_COLOR = "#F44336"
    
    BG_PRIMARY = "#FFFFFF"
    BG_SECONDARY = "#F5F5F5"
    BG_LIGHT = "#FAFAFA"
    BG_DARK = "#2C3E50"
    
    TEXT_PRIMARY = "#212121"
    TEXT_SECONDARY = "#757575"
    TEXT_LIGHT = "#FFFFFF"
    
    BORDER_COLOR = "#E0E0E0"
    SHADOW_COLOR = "#0000001A"
    
    # Font
    FONT_FAMILY = "Segoe UI"
    FONT_SMALL = (FONT_FAMILY, 9)
    FONT_NORMAL = (FONT_FAMILY, 10)
    FONT_MEDIUM = (FONT_FAMILY, 11)
    FONT_LARGE = (FONT_FAMILY, 12, "bold")
    FONT_TITLE = (FONT_FAMILY, 14, "bold")
    FONT_HEADER = (FONT_FAMILY, 16, "bold")
    
    @staticmethod
    def configure_styles(root):
        """Cấu hình tất cả các style cho ứng dụng"""
        style = ttk.Style()
        
        # Set theme
        try:
            style.theme_use('clam')
        except:
            pass
        
        # ===== TTKBOOTSTRAP STYLE =====
        
        # Main Frame
        style.configure('Main.TFrame', background=AppTheme.BG_SECONDARY)
        
        # Header Frame
        style.configure('Header.TFrame', 
                       background=AppTheme.BG_DARK,
                       relief='flat')
        
        # Header Label
        style.configure('Header.TLabel',
                       background=AppTheme.BG_DARK,
                       foreground=AppTheme.TEXT_LIGHT,
                       font=AppTheme.FONT_MEDIUM)
        
        # Title Label
        style.configure('Title.TLabel',
                       background=AppTheme.BG_SECONDARY,
                       foreground=AppTheme.TEXT_PRIMARY,
                       font=AppTheme.FONT_HEADER)
        
        style.configure('Title2.TLabel',
                       background=AppTheme.BG_SECONDARY,
                       foreground=AppTheme.TEXT_PRIMARY,
                       font=AppTheme.FONT_LARGE)
        
        # Button Styles
        style.configure('Primary.TButton',
                       font=AppTheme.FONT_NORMAL,
                       relief='flat',
                       padding=10)
        
        style.map('Primary.TButton',
                 background=[('pressed', AppTheme.PRIMARY_DARK),
                           ('active', AppTheme.PRIMARY_COLOR)],
                 foreground=[('pressed', AppTheme.TEXT_LIGHT),
                           ('active', AppTheme.TEXT_LIGHT)])
        
        style.configure('Success.TButton',
                       font=AppTheme.FONT_NORMAL,
                       relief='flat',
                       padding=10)
        
        style.map('Success.TButton',
                 background=[('pressed', '#388E3C'),
                           ('active', AppTheme.SUCCESS_COLOR)],
                 foreground=[('pressed', AppTheme.TEXT_LIGHT),
                           ('active', AppTheme.TEXT_LIGHT)])
        
        style.configure('Danger.TButton',
                       font=AppTheme.FONT_NORMAL,
                       relief='flat',
                       padding=10)
        
        style.map('Danger.TButton',
                 background=[('pressed', '#D32F2F'),
                           ('active', AppTheme.DANGER_COLOR)],
                 foreground=[('pressed', AppTheme.TEXT_LIGHT),
                           ('active', AppTheme.TEXT_LIGHT)])
        
        style.configure('Accent.TButton',
                       font=AppTheme.FONT_NORMAL,
                       relief='flat',
                       padding=8)
        
        style.map('Accent.TButton',
                 background=[('pressed', AppTheme.PRIMARY_DARK),
                           ('active', AppTheme.PRIMARY_DARK)],
                 foreground=[('pressed', AppTheme.TEXT_LIGHT),
                           ('active', AppTheme.TEXT_LIGHT)])
        
        # Label Styles
        style.configure('TLabel',
                       background=AppTheme.BG_SECONDARY,
                       foreground=AppTheme.TEXT_PRIMARY,
                       font=AppTheme.FONT_NORMAL)
        
        style.configure('Secondary.TLabel',
                       background=AppTheme.BG_SECONDARY,
                       foreground=AppTheme.TEXT_SECONDARY,
                       font=AppTheme.FONT_SMALL)
        
        # Entry Styles
        style.configure('TEntry',
                       fieldbackground=AppTheme.BG_PRIMARY,
                       background=AppTheme.BG_PRIMARY,
                       foreground=AppTheme.TEXT_PRIMARY,
                       font=AppTheme.FONT_NORMAL,
                       relief='solid',
                       borderwidth=1)
        
        # Combobox Styles
        style.configure('TCombobox',
                       fieldbackground=AppTheme.BG_PRIMARY,
                       background=AppTheme.BG_PRIMARY,
                       foreground=AppTheme.TEXT_PRIMARY,
                       font=AppTheme.FONT_NORMAL)
        
        # Notebook (Tab) Styles
        style.configure('Custom.TNotebook',
                       background=AppTheme.BG_SECONDARY,
                       borderwidth=0)
        
        style.configure('Custom.TNotebook.Tab',
                       background=AppTheme.BG_LIGHT,
                       foreground=AppTheme.TEXT_PRIMARY,
                       font=AppTheme.FONT_NORMAL,
                       padding=[15, 12])
        
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', AppTheme.PRIMARY_COLOR)],
                 foreground=[('selected', AppTheme.TEXT_LIGHT)])
        
        # Section Button
        style.configure('Section.TButton',
                       background=AppTheme.BG_LIGHT,
                       foreground=AppTheme.TEXT_PRIMARY,
                       font=AppTheme.FONT_MEDIUM,
                       relief='flat',
                       padding=10,
                       borderwidth=0)
        
        style.map('Section.TButton',
                 background=[('active', AppTheme.BG_SECONDARY),
                           ('pressed', AppTheme.BG_SECONDARY)],
                 foreground=[('active', AppTheme.PRIMARY_COLOR)])
        
        # LabelFrame Styles
        style.configure('TLabelframe',
                       background=AppTheme.BG_SECONDARY,
                       foreground=AppTheme.TEXT_PRIMARY,
                       font=AppTheme.FONT_MEDIUM,
                       relief='flat',
                       borderwidth=1)
        
        style.configure('TLabelframe.Label',
                       background=AppTheme.BG_SECONDARY,
                       foreground=AppTheme.TEXT_PRIMARY,
                       font=AppTheme.FONT_MEDIUM)
        
        # Frame Styles
        style.configure('TFrame',
                       background=AppTheme.BG_SECONDARY,
                       relief='flat')
        
        style.configure('Card.TFrame',
                       background=AppTheme.BG_PRIMARY,
                       relief='flat',
                       borderwidth=1)
        
        # Progressbar
        style.configure('TProgressbar',
                       background=AppTheme.PRIMARY_COLOR)
        
        # Separator
        style.configure('TSeparator',
                       background=AppTheme.BORDER_COLOR)


class WidgetHelper:
    """Hỗ trợ tạo các widget với style đẹp"""
    
    @staticmethod
    def create_card(parent, padding="15"):
        """Tạo một card (frame với background trắng)"""
        from tkinter import ttk
        card = ttk.Frame(parent, style='Card.TFrame')
        card.configure(padding=padding)
        return card
    
    @staticmethod
    def create_info_label(parent, text, style='Secondary.TLabel'):
        """Tạo label text nhỏ"""
        from tkinter import ttk
        return ttk.Label(parent, text=text, style=style)
    
    @staticmethod
    def create_button(parent, text, command, style='Primary.TButton', width=None):
        """Tạo button với style"""
        from tkinter import ttk
        btn = ttk.Button(parent, text=text, command=command, style=style, width=width)
        return btn
