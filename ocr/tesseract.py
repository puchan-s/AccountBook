'''
ocr.tesseract.py
tesseractを使用し画像解析、レシートデータの作成
'''
from PIL import Image
from io import BytesIO
import re
import base64

#事前に設定する読み込む環境
#sudo pip3 install pil
#sudo pip3 install pyocr

import pyocr
import pyocr.builders

def ocrTesseractReceipt(str_base64) :
    """[summary]
        画像をレシート用データに変換する
    Args:
        str_base64 (Str): Base64のString
    Returns:
        List[List[]] : レシートデータを以下の形式の配列で返す
                        電話番号 :['Tel',電話番号]
                        日付　　 :['Date',日付()]
                        商品　　 :[商品名,料金]
    """
    try:
        #Tesseractの事前準備
        tools = pyocr.get_available_tools()
        tool = tools[0]

        #Baseg4のヘッダーを消す
        dec_data = base64.b64decode( str_base64.split(',')[1] )

        #Base64を画像として開く
        img_recipt = Image.open(BytesIO(dec_data))

        #画像の解析
        str_txt = tool.image_to_string(
            img_recipt,
            lang='jpn',
            builder=pyocr.builders.TextBuilder()
        )

        #行に分割
        List_line = str_txt.split("\n")

        #電話番号パターン
        List_telPattern = [
                "0\d-\d{4}-\d{4}",
                "0\d{3}-\d{2}-\d{4}",
        #       "(0\d\)\d{4}-\d{4}",
        #       "(0\d{3}\)\d{2}-\d{4}"
            ]

        #日付パターン
        List_datePattern = [
                "(\d+)年(\d+)月(\d+)日" 
                #r"(\d+)年(\d+)月(\d+)日（.）(.*)"
                #r'[12]\d{3}[/\-年](0?[1-9]|1[0-2])[/\-月](0?[1-9]|[12][0-9]|3[01])日?$'
                #,r'(明治|大正|昭和|平成|令和)(0?[1-9]|[0-9][0-9])年(0?[1-9]|1[0-2])月(0?[1-9]|[12][0-9]|3[01])日'
            ]

        #除外文言(この文字が含まれた行のデータは格納されない)
        List_exclusionWords = ['税','合計','点数']

        #解析したデータの格納変数
        List2_getData = []
        #電話番号が見つかった場合True
        is_Tel = False
        #日付が見つかった場合True
        is_Date = False


        for str_line in List_line :

            #除外対象文字検査
            is_ExclusionWord = False
            for str_exclusionWord in List_exclusionWords :
                cls_exWordMatch = re.search(str_exclusionWord , str_line)
                if cls_exWordMatch is None:
                    pass
                else :
                    is_ExclusionWord = True
                    break

            if is_ExclusionWord == True :
                #除外文字があった場合、次の行に行く
                continue

            #日付、電話検査対象文字列を作成
            str_checkLine = str_line.replace(' ','')

            if is_Tel == False :
                #電話番号を検索
                for str_TelP in List_telPattern :
                    cls_telMatch = re.search(str_TelP , str_checkLine)
                    if cls_telMatch is None:
                        pass
                    else :
                        #電話番号が見つかった場合
                        List_telData = ["Tel",cls_telMatch.group()]
                        List2_getData.append(List_telData)
                        is_Tel = True
                        break

                if is_Tel == True :
                    continue

            if is_Date == False :
                #日付を検索
                for str_dateP in List_datePattern :
                    cls_DateMatch = re.search(str_dateP, str_checkLine)
                    if cls_DateMatch is None:
                        pass
                    else :
                        #日付が見つかった場合
                        List_dateData = ["Date",cls_DateMatch.group()]
                        List2_getData.append(List_dateData)
                        is_Date = True
                        break

                if is_Date == True :
                    continue

            #データ取得
            #末尾の空白で2つに分割
            int_splitIndex = str_line.rfind(' ')
            str_indexName = str_line[:int_splitIndex].replace(' ','')
            #後ろのデータを数字に変換
            str_value = str_line[int_splitIndex:]
            int_value = str(re.sub(r"\D", "",str_value))
            #数字に変換できた場合に登録
            if int_value != "" :
                List2_getData.append([str_indexName,int_value])

        return List2_getData
    except Exception as e:
        print(e)
        return None
