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
    )
    special_move = forms.CharField(
        label='得意技',
        max_length=30,
        required=False,
        empty_value=DEFAULT_SPECIAL_MOVE
    )
    favorite_weapon = forms.CharField(
        label='愛用の武器',
        max_length=30,
        required=False,
        empty_value=DEFAULT_FAVORITE_WEAPON
    )
    job_after = forms.ChoiceField(
        label='変化後の職業',
        choices=JOB_CHOICE,
        required=True
    )
