# Modern menu redesign - paste this into _build_menu_screen method
def _build_menu_screen_modern(self):
    """Build ultra-modern menu screen with glassmorphism, gradients, and animations."""
    screen = MenuScreen(name="menu")
    
    # Root layout
    root_layout = BoxLayout(orientation="vertical", padding=0, spacing=0)
    
    # Animated gradient background (dark to darker gradient)
    with root_layout.canvas.before:
        # Base dark background
        Color(0.05, 0.06, 0.10, 1.0)
        Rectangle(size=root_layout.size, pos=root_layout.pos)
        
        # Gradient overlay (cyan to purple)
        Color(0.0, 0.5, 0.8, 0.08)
        Rectangle(size=root_layout.size, pos=root_layout.pos)
    
    # ====== TOP SECTION: LOGO & TITLE ======
    top_section = BoxLayout(orientation="vertical", size_hint_y=0.20, padding=[10, 15], spacing=5)
    
    # "SNAKE GAME PRO" Title with glow effect
    title_main = Label(
        text="[b]🐍 SNAKE GAME[/b]",
        markup=True,
        font_size="48sp",
        color=(0.0, 1.0, 0.85, 1.0),  # Bright cyan
        bold=True,
        size_hint_y=0.65,
        outline_width=2,
        outline_color=(0.0, 0.6, 0.8, 0.5)
    )
    
    # Subtitle with animated-look text
    title_sub = Label(
        text="[color=ffaa00]★[/color] [i]Pro Edition[/i] [color=ffaa00]★[/color]",
        markup=True,
        font_size="14sp",
        color=(1.0, 0.85, 0.3, 0.95),
        size_hint_y=0.35,
        bold=True
    )
    
    top_section.add_widget(title_main)
    top_section.add_widget(title_sub)
    root_layout.add_widget(top_section)
    
    # ====== MIDDLE SECTION: CARDS & CONTROLS ======
    cards_section = BoxLayout(orientation="vertical", size_hint_y=0.72, padding=[12, 10], spacing=12)
    
    # Mode Card (Glassmorphic card design)
    mode_card = BoxLayout(
        orientation="vertical",
        size_hint_y=0.18,
        padding=[12, 8],
        spacing=3
    )
    with mode_card.canvas.before:
        Color(0.12, 0.14, 0.18, 0.6)  # Glassmorphic base
        RoundedRectangle(pos=mode_card.pos, size=mode_card.size, radius=[15])
        # Glow border effect
        Color(0.0, 0.8, 0.6, 0.3)
        Line(rounded_rectangle=(mode_card.pos[0], mode_card.pos[1], mode_card.size[0], mode_card.size[1], 15), width=2)
    
    mode_label = Label(
        text="[b][color=00ff88]⚙ GAME MODE[/color][/b]",
        markup=True,
        font_size="11sp",
        size_hint_y=0.35,
        bold=True
    )
    
    spinner = Spinner(
        text='Classic',
        values=('Classic', 'No Wall', 'Time Attack', 'Hardcore'),
        size_hint_y=0.65,
        background_color=(0.1, 0.12, 0.15, 0.9),
        color=(0.0, 1.0, 0.85, 1.0)
    )
    spinner.id = 'mode_spinner'
    
    mode_card.add_widget(mode_label)
    mode_card.add_widget(spinner)
    cards_section.add_widget(mode_card)
    
    # Player Name Card
    name_card = BoxLayout(
        orientation="vertical",
        size_hint_y=0.16,
        padding=[12, 8],
        spacing=3
    )
    with name_card.canvas.before:
        Color(0.12, 0.14, 0.18, 0.6)
        RoundedRectangle(pos=name_card.pos, size=name_card.size, radius=[15])
        Color(0.8, 0.5, 0.0, 0.3)
        Line(rounded_rectangle=(name_card.pos[0], name_card.pos[1], name_card.size[0], name_card.size[1], 15), width=2)
    
    name_label = Label(
        text="[b][color=ffaa00]👤 YOUR NAME[/color][/b]",
        markup=True,
        font_size="11sp",
        size_hint_y=0.35,
        bold=True
    )
    
    name_input_box = BoxLayout(size_hint_y=0.65, spacing=8)
    name_input = TextInput(
        text="Player",
        multiline=False,
        size_hint_x=0.75,
        background_color=(0.08, 0.09, 0.12, 1.0),
        foreground_color=(0.0, 1.0, 0.85, 1.0),
        cursor_color=(0.0, 1.0, 0.85, 1.0)
    )
    name_input.id = 'name_input'
    
    save_name_btn = Button(
        text="✓",
        size_hint_x=0.25,
        background_color=(0.0, 0.85, 0.55, 1.0),
        font_size="22sp"
    )
    save_name_btn.bind(on_press=lambda x: screen.save_player_name())
    
    name_input_box.add_widget(name_input)
    name_input_box.add_widget(save_name_btn)
    name_card.add_widget(name_label)
    name_card.add_widget(name_input_box)
    cards_section.add_widget(name_card)
    
    # ====== PRIMARY ACTION BUTTON: PLAY NOW ======
    play_button = Button(
        text="[b]▶ PLAY NOW[/b]",
        markup=True,
        size_hint_y=0.20,
        background_color=(0.0, 0.95, 0.65, 1.0),
        font_size="20sp",
        bold=True
    )
    with play_button.canvas.before:
        Color(0.0, 1.0, 0.7, 0.4)
        Ellipse(pos=(play_button.pos[0] - 30, play_button.pos[1] - 30), size=(play_button.size[0] + 60, play_button.size[1] + 60))
    play_button.bind(on_press=lambda x: screen.start_game())
    cards_section.add_widget(play_button)
    
    # Menu button grid (3 buttons)
    menu_grid_row1 = BoxLayout(size_hint_y=0.18, spacing=10)
    
    btn_progress = Button(
        text="[b]📊\nPROGRESS[/b]",
        markup=True,
        background_color=(0.15, 0.4, 1.0, 0.9),
        font_size="13sp"
    )
    with btn_progress.canvas.before:
        Color(0.15, 0.4, 1.0, 0.3)
        RoundedRectangle(pos=btn_progress.pos, size=btn_progress.size, radius=[12])
    btn_progress.bind(on_press=lambda x: screen.show_progression())
    
    btn_scores = Button(
        text="[b]🏆\nSCORES[/b]",
        markup=True,
        background_color=(1.0, 0.3, 0.5, 0.9),
        font_size="13sp"
    )
    with btn_scores.canvas.before:
        Color(1.0, 0.3, 0.5, 0.3)
        RoundedRectangle(pos=btn_scores.pos, size=btn_scores.size, radius=[12])
    btn_scores.bind(on_press=lambda x: screen.show_leaderboard())
    
    btn_settings = Button(
        text="[b]⚡\nSETTINGS[/b]",
        markup=True,
        background_color=(0.8, 0.4, 1.0, 0.9),
        font_size="13sp"
    )
    with btn_settings.canvas.before:
        Color(0.8, 0.4, 1.0, 0.3)
        RoundedRectangle(pos=btn_settings.pos, size=btn_settings.size, radius=[12])
    btn_settings.bind(on_press=lambda x: screen.show_settings())
    
    menu_grid_row1.add_widget(btn_progress)
    menu_grid_row1.add_widget(btn_scores)
    menu_grid_row1.add_widget(btn_settings)
    cards_section.add_widget(menu_grid_row1)
    
    # Daily reward card
    daily_card = BoxLayout(
        orientation="vertical",
        size_hint_y=0.14,
        padding=[10, 6],
        spacing=3
    )
    with daily_card.canvas.before:
        Color(1.0, 0.85, 0.0, 0.15)
        RoundedRectangle(pos=daily_card.pos, size=daily_card.size, radius=[12])
        Color(1.0, 0.85, 0.0, 0.4)
        Line(rounded_rectangle=(daily_card.pos[0], daily_card.pos[1], daily_card.size[0], daily_card.size[1], 12), width=2)
    
    daily_label = Label(
        text="🎁 Daily Reward Ready!",
        font_size="11sp",
        color=(1.0, 0.95, 0.2, 1.0),
        bold=True,
        size_hint_y=0.45
    )
    daily_label.id = 'daily_label'
    
    btn_daily = Button(
        text="[b]CLAIM REWARD[/b]",
        markup=True,
        background_color=(1.0, 0.85, 0.0, 0.95),
        font_size="12sp",
        size_hint_y=0.55,
        color=(0.0, 0.0, 0.0, 1.0)
    )
    btn_daily.bind(on_press=lambda x: screen.claim_daily_reward())
    
    daily_card.add_widget(daily_label)
    daily_card.add_widget(btn_daily)
    cards_section.add_widget(daily_card)
    
    root_layout.add_widget(cards_section)
    
    # ====== BOTTOM SECTION: STATS ======
    stats_section = BoxLayout(size_hint_y=0.08, padding=[10, 4], spacing=12)
    
    high_score_label = Label(
        text="🏅 Score: 0",
        font_size="10sp",
        color=(0.0, 1.0, 0.8, 1.0),
        bold=True,
        size_hint_x=0.5
    )
    high_score_label.id = 'high_score_label'
    
    level_label = Label(
        text="⭐ Level: 1",
        font_size="10sp",
        color=(1.0, 0.85, 0.2, 1.0),
        bold=True,
        size_hint_x=0.5
    )
    level_label.id = 'level_label'
    
    stats_section.add_widget(high_score_label)
    stats_section.add_widget(level_label)
    root_layout.add_widget(stats_section)
    
    screen.add_widget(root_layout)
    screen.ids = {
        'mode_spinner': spinner,
        'name_input': name_input,
        'daily_label': daily_label,
        'high_score_label': high_score_label,
        'level_label': level_label,
    }
    return screen
