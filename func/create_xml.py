
XML = """<package>
    <info>
        <GUID>{A4F6D1E0-909A-11D5-B08F-000021EF6307}</GUID>
        <versionStat>405037</versionStat>
        <version>405037</version>
    </info>
<dataset id="CaptionDB">
    <fields>
        <f id="1" name="id" t="Integer" c="Код"/>
        <f id="2" name="NUMNOTICE" t="String" s="50" c="Номер извещения"/>
        <f id="3" name="NAME" t="String" s="50" r="True" c="Ф.И.О."/>
        <f id="4" name="C_Gender" t="Integer" c="Пол (код)"/>
        <f id="5" name="Age" t="Integer" c="Возраст (код)"/>
        <f id="6" name="C_Social" t="Integer" c="Социальная группа (код)"/>
        <f id="7" name="C_Region" t="Integer" c="Район (код)"/>
        <f id="8" name="Note" t="String" s="255" c="Адрес происшествия"/>
        <f id="9" name="C_PlaceIncident" t="Integer" c="Место происшествия (код)"/>
        <f id="10" name="Note3" t="String" s="255" c="Наименование места происшествия"/>
        <f id="11" name="DatePoison" t="Integer" c="Дата отравления"/>
        <f id="12" name="DateFirstRecourse" t="Integer" c="Дата первого обращения"/>
        <f id="13" name="DateAffFirst" t="Integer" c="Дата установления первичного диагноза"/>
        <f id="14" name="C_Diagnosis" t="Integer" c="Диагноз (код)"/>
        <f id="15" name="Note1" t="String" s="255" c="Примечание (диагноз)"/>
        <f id="16" name="C_BooleanAlc" t="Integer" c="Сочетание с алкоголем (код)"/>
        <f id="17" name="C_SetDiagnosis" t="Integer" c="Диагноз установил (код)"/>
        <f id="18" name="C_MedicalHelp" t="Integer" c="Медицинская помощь (код)"/>
        <f id="19" name="C_PlaceMortality" t="Integer" c="Исход заболевания (код)"/>
        <f id="20" name="Note5" t="String" s="255" c="Примечание (где и когда наступила смерть)"/>
        <f id="21" name="C_TypePoison" t="Integer" c="Характер отравления (код)"/>
        <f id="22" name="ValPoison" t="Float" c="Количество отравившихся"/>
        <f id="23" name="C_AimPoison" t="Integer" c="Обстоятельство отравления (код)"/>
        <f id="24" name="Note7" t="String" s="255" c="Примечание (обстоятельства отравления)"/>
        <f id="25" name="C_PlacePoison" t="Integer" c="Место приобретения яда (код)"/>
        <f id="26" name="Note8" t="String" s="255" c="Примечание (место приобретения яда)"/>
        <f id="27" name="DateDocument" t="Integer" c="Дата документа"/>
        <f id="28" name="NAMEPEOPLEGET" t="String" s="50" c="ФИО получившего извещение"/>
        <f id="29" name="CREATEUSER" t="String" s="50" c="Пользователь, создавший запись"/>
        <f id="30" name="CREATEDATE" t="DateTime" c="Дата создания записи"/>
        <f id="31" name="UPDATEUSER" t="String" s="50" c="Пользователь, изменивший запись"/>
        <f id="32" name="UPDATEDATE" t="DateTime" c="Дата изменения записи"/>
        <f id="33" name="FlagColor" t="Integer"/>
        <f id="34" name="C_GSEN" t="Integer" c="Учреждение РПН (код)"/>
        <f id="35" name="S_OBJECTMESS" t="Integer" c="ЛПУ сообщившее о заболевании"/>
        <f id="36" name="S_OBJECTMESSNAME" t="String" s="255" c="ЛПУ сообщившее о заболевании"/>
        <f id="37" name="S_STREET" t="Integer" c="Улица"/>
        <f id="38" name="S_STREETNAME" t="String" s="255" c="Улица"/>
        <f id="39" name="HOUSE" t="String" s="50" c="Номер дома"/>
        <f id="40" name="FLAT" t="String" s="50" c="Квартира"/>
        <f id="41" name="DateLock" t="Integer" c="Дата закрытия документа"/>
        <f id="42" name="S_ObjectMedicalHelp" t="Integer" c="Медицинская помощь (ЛПУ)"/>
        <f id="43" name="S_ObjectMedicalHelpName" t="String" s="255" c="Медицинская помощь (ЛПУ)"/>
        <f id="44" name="datereceipt" t="Integer" c="Дата получения"/>
        <f id="45" name="errorfontcolor" t="Integer" c=" "/>
        <f id="46" name="errorfontstyle" t="Integer" c=" "/>
        <f id="47" name="errorcolor" t="Integer" c=" "/>
        <f id="48" name="errorcolfontcolor" t="Integer" c=" "/>
        <f id="49" name="errorcolfontstyle" t="Integer" c=" "/>
        <f id="50" name="errorcolcolor" t="Integer" c=" "/>
        <f id="51" name="errortext" t="String" s="254" c=" "/>
        <f id="52" name="errorcolumns" t="String" s="254" c=" "/>
        <f id="53" name="CANREADONLY" t="SmallInt" c=" "/>
        <f id="54" name="CANEDITONLY" t="SmallInt" c=" "/>
        <f id="55" name="CANDELETEONLY" t="SmallInt" c=" "/>
    </fields>
<data>"""


def find_street(STRING: str) -> str:
    list_ = [
        'проспект', 'пр.', 'бульвар',
        'аллея', 'улица', 'переулок', 'дорога',
        'шоссе', 'набережная', 'наб.', 'пер.', 'ул.',
        'ал.', 'бул.', 'площадь', 'пр-т', 'ул '
        ]
    for part in STRING.replace(';', ',').split(','):
        for key in list_:
            if key in part.lower():
                return part
    return STRING


def find_dom(STRING: str) -> str:
    for part in STRING.split(','):
        for key in ['д.', 'дом']:
            if key in part.lower():
                return part
    return ''


def find_kv(STRING: str) -> str:
    for part in STRING.split(','):
        for key in ['кв.', 'квартира']:
            if key in part.lower():
                return part
    return ''


def generate_row(row: dict) -> str:
    LIST = (
        '\n   <r>',
        '\n      <v f="2">', row['history_number'], '</v>',  # номер ИБ
        '\n      <v f="3">', row['case_biz_key'], '</v>',  # вместо ФИО
        '\n      <v f="4">', row['sex'], '</v>',  # пол
        '\n      <v f="5">', row['age'], '</v>',  # возраст
        '\n      <v f="6">', row['o_1119'], '</v>',
        '\n      <v f="7">', row['o_1123'], '</v>',
        '\n      <v f="8">', row['o_1102'], '</v>',
        '\n      <v f="9">', row['o_1101'], '</v>',
        '\n      <v f="10">', row['o_1103'], '</v>',
        '\n      <v f="11">', row['o_1104'].strftime('%Y%m%d'), '</v>',
        '\n      <v f="12">', row['o_1105'].strftime('%Y%m%d'), '</v>',
        '\n      <v f="13">', row['o_303'].strftime('%Y%m%d'), '</v>',
        '\n      <v f="14">', row['mkb_rpn'], '</v>',
#        '\n      <v f="15"></v>',
        '\n      <v f="16">', row['o_1108'], '</v>',
        '\n      <v f="17">', row['o_1109'], '</v>',
        '\n      <v f="18">', row['o_1110'], '</v>',
        '\n      <v f="19">0</v>',
        '\n      <v f="21">', row['o_1113'], '</v>',
        '\n      <v f="22">1</v>',
        '\n      <v f="23">', row['o_1115'], '</v>',
        '\n      <v f="25">', row['o_1117'], '</v>',
        '\n      <v f="27">', row['o_303'].strftime('%Y%m%d'), '</v>',
        '\n      <v f="34">0</v>',
        '\n      <v f="38">', row['street'], '</v>',
        '\n      <v f="39">', row['house'], '</v>',
        '\n      <v f="40">', row['flat'], '</v>',
        '\n      <v f="43">', row['org_name'].replace('НИИ СП', 'НИИ СП Джанелидзе'), '</v>',
        '\n   </r>'
        )
    return ''.join(str(x) for x in LIST)


def create_xml(JSON: list, NAME: str) -> str:
    "Генерируем файлик и возвращаем путь до него"

    STRING = XML
    for row in JSON:
        for k, v in row.items():
            if row[k] is None or row[k] == '-1':
                row[k] = ''
        STRING += generate_row(row)

    STRING += "\n</data>\n</dataset>\n</package>"

    FILE = f'/tmp/{NAME}.xml'

    with open(FILE, 'w') as f:
        f.write(STRING)
    return FILE
