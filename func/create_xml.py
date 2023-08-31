
XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
 <package>
  <info>
   <GUID>{A4F6D1E0-909A-11D5-B08F-000021EF6307}</GUID>
   <versionStat>404072</versionStat>
   <version>404072</version>
  </info>
  <dataset id="CaptionDB">
   <fields>
    <f id="1" name="id" t="Integer"></f>
    <f id="2" name="NUMNOTICE" t="String" s="50"></f>
    <f id="3" name="NAME" t="String" s="50" r="True"></f>
    <f id="4" name="C_Gender" t="Integer"></f>
    <f id="5" name="Age" t="Integer"></f>
    <f id="6" name="C_Social" t="Integer"></f>
    <f id="7" name="C_Region" t="Integer"></f>
    <f id="8" name="Note" t="String" s="255"></f>
    <f id="9" name="C_PlaceIncident" t="Integer"></f>
    <f id="10" name="Note3" t="String" s="255"></f>
    <f id="11" name="DatePoison" t="Integer"></f>
    <f id="12" name="DateFirstRecourse" t="Integer"></f>
    <f id="13" name="DateAffFirst" t="Integer"></f>
    <f id="14" name="C_Diagnosis" t="Integer"></f>
    <f id="15" name="C_BooleanAlc" t="Integer"></f>
    <f id="16" name="C_SetDiagnosis" t="Integer"></f>
    <f id="17" name="C_MedicalHelp" t="Integer"></f>
    <f id="18" name="C_PlaceMortality" t="Integer"></f>
    <f id="19" name="Note5" t="String" s="255"></f>
    <f id="20" name="C_TypePoison" t="Integer"></f>
    <f id="21" name="ValPoison" t="Float"></f>
    <f id="22" name="C_AimPoison" t="Integer"></f>
    <f id="23" name="Note7" t="String" s="255"></f>
    <f id="24" name="C_PlacePoison" t="Integer"></f>
    <f id="25" name="Note8" t="String" s="255"></f>
    <f id="26" name="DateDocument" t="Integer"></f>
    <f id="27" name="NAMEPEOPLEGET" t="String" s="50"></f>
    <f id="28" name="CREATEUSER" t="String" s="50"></f>
    <f id="29" name="CREATEDATE" t="DateTime"></f>
    <f id="30" name="UPDATEUSER" t="String" s="50"></f>
    <f id="31" name="UPDATEDATE" t="DateTime"></f>
    <f id="32" name="FlagColor" t="Integer"></f>
    <f id="33" name="C_GSEN" t="Integer"></f>
    <f id="34" name="S_OBJECTMESS" t="Integer"></f>
    <f id="35" name="S_OBJECTMESSNAME" t="String" s="255"></f>
    <f id="36" name="S_STREET" t="Integer"></f>
    <f id="37" name="S_STREETNAME" t="String" s="255"></f>
    <f id="38" name="HOUSE" t="String" s="50"></f>
    <f id="39" name="FLAT" t="String" s="50"></f>
    <f id="40" name="DateLock" t="Integer"></f>
    <f id="41" name="S_ObjectMedicalHelp" t="Integer"></f>
    <f id="42" name="S_ObjectMedicalHelpName" t="String" s="50"></f>
    <f id="43" name="errorfontcolor" t="Integer"></f>
    <f id="44" name="errorfontstyle" t="Integer"></f>
    <f id="45" name="errorcolor" t="Integer"></f>
    <f id="46" name="errorcolfontcolor" t="Integer"></f>
    <f id="47" name="errorcolfontstyle" t="Integer"></f>
    <f id="48" name="errorcolcolor" t="Integer"></f>
    <f id="48" name="errortext" t="String" s="254"></f>
    <f id="50" name="errorcolumns" t="String" s="254"></f>
    <f id="51" name="CANREADONLY" t="SmallInt"></f>
    <f id="52" name="CANEDITONLY" t="SmallInt"></f>
    <f id="53" name="CANDELETEONLY" t="SmallInt"></f>
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
        '\n      <v f="8"></v>',
        '\n      <v f="9">', row['o_1101'], '</v>',
        '\n      <v f="10">', row['o_1103'], '</v>',
        '\n      <v f="11">', row['o_1104'].strftime('%Y%m%d'), '</v>',
        '\n      <v f="12">', row['o_1105'].strftime('%Y%m%d'), '</v>',
        '\n      <v f="13">', row['o_303'].strftime('%Y%m%d'), '</v>',
        '\n      <v f="14">', row['mkb_rpn'], '</v>',
        '\n      <v f="15">', row['o_1108'], '</v>',
        '\n      <v f="16">', row['o_1109'], '</v>',
        '\n      <v f="17">', row['o_1110'], '</v>',
        '\n      <v f="18"></v>',
        '\n      <v f="20">', row['o_1113'], '</v>',
        '\n      <v f="21">1</v>',
        '\n      <v f="22">', row['o_1115'], '</v>',
        '\n      <v f="24">', row['o_1117'], '</v>',
        '\n      <v f="26">', row['o_303'].strftime('%Y%m%d'), '</v>',
        '\n      <v f="37">', row['street'], '</v>',
        '\n      <v f="38">', row['house'], '</v>',
        '\n      <v f="39">', row['flat'], '</v>',
        '\n      <v f="42">',
        row['org_name'].replace('НИИ СП', 'НИИ СП Джанелидзе'),
        '</v>',
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
