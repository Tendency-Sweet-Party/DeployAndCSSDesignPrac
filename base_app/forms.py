from django import forms

DEFAULT_SPECIAL_MOVE = '光の一撃'
DEFAULT_FAVORITE_WEAPON = '光の剣'
JOB_CHOICE = (
    ('', '-' * 10),
    ('princess', "プリンセス"),
    ('bunny', "バニーガール"),
    ('sex_doll', "セックスドール"),
)


class InitialSettingForm(forms.Form):
    main_character_name = forms.CharField(
        label='主人公の名前',
        max_length=30,
        required=True,
        help_text="<span class='text_emphasize'>主人公の名前</span> を入力してください。",
        widget=forms.TextInput(attrs={'class': 'initial_setting_control'}, ),
    )
    special_move = forms.CharField(
        label='得意技',
        max_length=30,
        required=False,
        empty_value=DEFAULT_SPECIAL_MOVE,
        help_text="<span class='text_emphasize'>得意技</span>を入力してください。<br>空欄の場合はデフォルトが選択させます。",
        widget=forms.TextInput(attrs={'class': 'initial_setting_control'}, ),
    )
    # favorite_weapon = forms.CharField(
    #     label='愛用の武器',
    #     max_length=30,
    #     required=False,
    #     empty_value=DEFAULT_FAVORITE_WEAPON,
    #     help_text="主人公の愛用の武器を入力してくだいさい。",
    # )
    job_after = forms.ChoiceField(
        label='変化後の職業',
        choices=JOB_CHOICE,
        required=True,
        help_text="下の選択肢から<span class='text_emphasize'>好きなジョブ</span>を一つ選択してください。",
    )
