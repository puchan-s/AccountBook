from flask import Flask, render_template ,request
import ocr.tesseract
import db.mysql
from logging import getLogger

logger = getLogger(__name__)
app = Flask(__name__)

#レシート購入日付の入力可能年開始
INT_START_YEAR = 2021 

@app.route("/Output" , methods=['GET' , 'POST'] )
def output():
    """[summary]
    画像を解析し、その情報を登録画面に表示する
    hostパラメータ : data -> 画像データ(Base64)
    Returns:
        [str]: 商品登録画面
    """

    ##################
    #画像データ解析
    ##################
    List2_ocrData = ocr.tesseract.ocrTesseractReceipt(request.form["data"])


    ##################
    #商品以外のデータを取得
    ##################
    #電話番号
    str_ocrTel = ""
    #日付情報([0]:年 [1]:月 [2]:日 )
    List_ocrDate = []

    for List_valueData in reversed(List2_ocrData) :
        #店舗情報取得
        if List_valueData[0].lower() == 'tel' :
            str_ocrTel = List_valueData[1]
            str_ocrTel = str_ocrTel.replace('-','')
            List2_ocrData.remove(List_valueData)

        #日付取得
        if List_valueData[0].lower() == 'date' :
            str_work = List_valueData[1].replace("年","/")
            str_work = str_work.replace("月","/")
            str_work = str_work.replace("日","")
            List_workArray = str_work.split("/")
            List_ocrDate.append(int(List_workArray[0]) - INT_START_YEAR )
            List_ocrDate.append(int(List_workArray[1]) -1 )
            List_ocrDate.append(int(List_workArray[2]) -1 )
            List2_ocrData.remove(List_valueData)

        if str_ocrTel != "" and len(List_ocrDate) == 3 :
            #店舗情報、日付を取得できたらループ終了
            break

    ##################
    #店舗情報取得
    ##################
    #DBのSHOPDATA
    List2_shopData = db.mysql.select( db.mysql.SHOPDATA_SELECT_SHOPTEL.format(str_ocrTel) )
    #画面に表示する SHOPDATA
    Dict_shopData ={}
    if len(List2_shopData) == 0 :
        Dict_shopData = {'Tel' : str_ocrTel }
    else :
        Dict_shopData = { 'name' : List2_shopData[0][1] ,'Tel' : List2_shopData[0][2] }

    ##################
    #表品分類取得
    ##################
    List2_itemType = db.mysql.select( db.mysql.ITEMTYPE_SELECT )

    ##################
    #画面表示用パラメータ
    ##################
    Dict_templateData = { 'ocrData' : List2_ocrData , 'shopData' : Dict_shopData , "ItemType" : List2_itemType , "reciptDate" : List_ocrDate ,  "reciptNo" : -1 }
    return  render_template('ReciptData.html',**Dict_templateData )

@app.route("/InputPhoto")
def inputPhoto():
    """[summary]
    画像入力画面表示
    Returns:
        [str]: 画像入力画面
    """
    return  render_template('InputPhoto.html' )

@app.route("/save", methods=['GET', 'POST'])
def save():
    """[summary]
    レシートデータ保存
    hostパラメータ : Year -> 購入年
                    Month -> 購入月
                    Day -> 購入日
                    shopName -> 店舗名
                    tel -> 店舗電話番号
                    ReciptNo -> レシート番号 ない場合「-1」
                    ItemName* -> 商品名
                    ItemType* -> 商品種類
                    ItemValue* -> 商品価格
                    注意：*は任意の数字が入り、複数パラメータが存在します。
    Returns:
        [str]: 画像入力画面
    """

    #入力データ
    Dict_ReciptData = request.form.copy()

    #店舗データ取得
    str_year = Dict_ReciptData.pop('Year')
    str_month = Dict_ReciptData.pop('Month')
    str_day = Dict_ReciptData.pop('Day')
    str_shopName = Dict_ReciptData.pop('shopName')
    str_tel = Dict_ReciptData.pop('tel')
    str_tel = str_tel.replace('-','')
    str_receiptID = Dict_ReciptData.pop('ReciptNo')

    #SHOPID取得
    str_selectSql = db.mysql.SHOPDATA_SELECT_SHOPTEL.format(str_tel)
    List2_shopData = db.mysql.select( str_selectSql )
    if len(List2_shopData) == 0 :
        #SHOPDATAが取得できない場合は新規登録
        str_shopData_insert = db.mysql.SHOPDATA_INSERT.format(
            str_shopName,
            str_tel,
            1
        )
        db.mysql.commit( str_shopData_insert)

        #登録した店舗情報を取得
        List2_shopData = db.mysql.select( str_selectSql )

    #レシートID作成
    if( str_receiptID == "-1" ):
        #新規登録の場合
        List2_receiptData = db.mysql.select( db.mysql.RECEIPT_MAXID )
        if type(List2_receiptData[0][0]) != int :
            str_receiptID = 1
        else :
            str_receiptID = List2_receiptData[0][0] + 1

        #レシート情報を登録
        str_receipt_insert = db.mysql.RECEIPT_INSERT.format(
            str_receiptID,
            str_year,
            str_month,
            str_day,
            1,List2_shopData[0][0]
            )
        db.mysql.commit( str_receipt_insert)
    else :
        #更新の場合
        #一度レシート詳細（商品情報）を全削除する
        db.mysql.commit(db.mysql.RECEIPTDETAILS_DELETE.format(str_receiptID))

        #レシートデータ更新
        str_receipt_update = db.mysql.RECEIPT_UPDATE.format(
            str_receiptID,
            str_year,
            str_month,
            str_day,1,
            List2_shopData[0][0]
            )
        db.mysql.commit( str_receipt_update )

    #レシート詳細情報を登録
    #ループ回数
    int_count = 0
    while len(Dict_ReciptData) != 0 :
        #商品データがなくなるまでループ

        try :
            #登録用SQL作成
            str_receiptDitail_insert = db.mysql.RECEIPTDETAILS_INSERT.format(
                str_receiptID,
                Dict_ReciptData.pop('ItemName' + str(int_count)),
                Dict_ReciptData.pop('ItemType' + str(int_count)),
                Dict_ReciptData.pop('ItemValue' + str(int_count)),
                1
            )

            #登録
            db.mysql.commit( str_receiptDitail_insert)
        except :
            pass

        #ループの回数を追加
        int_count += 1

    return render_template('InputPhoto.html' )

@app.route("/getShopData" , methods=['GET' , 'POST'])
def getShopData():
    """[summary]
    店舗情報取得
    GETパラメータ : SHOPTEL -> 店舗電話番号
    Returns:
        [Dict]: 店舗名
    """
    str_selectSql = db.mysql.SHOPDATA_SELECT_SHOPTEL.format(request.args.get('SHOPTEL'))
    List2_shopData = db.mysql.select( str_selectSql )

    Dict_retData = { 'ShopName' : List2_shopData[0][1]}
    return Dict_retData

@app.route("/ItemTypeAll" , methods=['GET' , 'POST'])
def getItemTypeAll():
    """[summary]
    商品種類全部取得
    Returns:
        [Dict[str:List]]: 商品種類
    """
    str_itemType = db.mysql.select( db.mysql.ITEMTYPE_SELECT )
    Dict_retData = { "ItemType" : str_itemType }
    return Dict_retData

@app.route("/getReceiptData" , methods=['GET' , 'POST'])
def getReceiptData():
    """[summary]
    レシート情報一覧画面表示
    Returns:
        [str]: レシート情報一覧
    """
    List2_receipt = db.mysql.select( db.mysql.RECEIPT_SHOP_SELECT )
    Dict_templateData = { "receipt" : List2_receipt }
    return  render_template('receiptList.html',**Dict_templateData )

@app.route("/ReceiptDetailData" , methods=['GET' , 'POST'])
def getReceiptDitailData():
    """[summary]
    登録されているレシートデータを表示する(修正可能)
    GETパラメータ : receiptID -> レシートID
    Returns:
        [str]: レシート登録情報（修正可能）
    """

    ##################
    #レシート情報
    ##################
    List2_receipt = db.mysql.select( db.mysql.RECEIPT_SELECT.format(request.args.get('receiptID') , 1 ) )
    if len(List2_receipt) == 0 :
        #取得できるレシートデータがない場合
        pass

    ##################
    #日付取得 
    ##################
    List_ReciptDate = [List2_receipt[0][1] - INT_START_YEAR ,List2_receipt[0][2] -1 ,List2_receipt[0][3] -1 ]

    ##################
    #商品情報取得
    ##################
    List2_shopData = db.mysql.select( db.mysql.SHOPDATA_SELECT_SHOPID.format(List2_receipt[0][5]) )
    Dict_shopData = {}
    if len(List2_shopData) != 0 :
        Dict_shopData = { 'name' : List2_shopData[0][1] ,'Tel' : List2_shopData[0][2] }

    ##################
    #商品詳細情報取得
    ##################
    List2_receiptdetails = db.mysql.select( db.mysql.RECEIPTDETAILS_SELECT.format(request.args.get('receiptID') , 1 ) )
    List2_ocrData = []
    for List_receiptdetail in List2_receiptdetails :
        List_workData = [List_receiptdetail[2],List_receiptdetail[4]]
        List2_ocrData.append(List_workData)

    ##################
    #表品分類取得
    ##################
    List2_itemType = db.mysql.select( db.mysql.ITEMTYPE_SELECT )

    Dict_templateData = { 'ocrData' : List2_ocrData , 'shopData' : Dict_shopData , "ItemType" : List2_itemType , "reciptDate" : List_ReciptDate , "reciptNo" : request.args.get('receiptID') }
    return  render_template('ReciptData.html',**Dict_templateData )

@app.route("/ReceiptDataMonth" , methods=['GET', 'POST'])
def getReceiptDataManth():
    """[summary]
    購入年月のレシート情報を表示（年月合計金額、種類別金額、レシートごとのデータ
    getパラメータ :   year -> 購入年
                    month -> 購入月
    Returns:
        [str]: 年月のレシート情報
    """

    #指定された年月に買ったレシート情報全て取得
    str_select_receipt_month = db.mysql.RECEIPT_MONTH_SELECT.format(
        request.args.get('year') , 
        request.args.get('month') , 
        1 
        )
    List2_receiptDetails = db.mysql.select( str_select_receipt_month )

    #表品分類取得
    List2_itemType = db.mysql.select( db.mysql.ITEMTYPE_SELECT )

    #口径金額
    int_totalMoney = 0
    #タイプ別合計([0]は空データ)
    List_typeMoneys = [0] * ( len(List2_itemType) + 1 )
    #商品個別データ
    List_receiptMoeys = []

    for List_receiptDetail in List2_receiptDetails :
        if type(List_receiptDetail[12]) is int :
            pass
        else :
            continue

        #料金
        int_money = int(List_receiptDetail[12])
        #商品種類（番号）
        int_itemTypeNo = int(List_receiptDetail[11])
        #商品名
        str_itemName = List_receiptDetail[10]
        #店舗名
        str_shopName = List_receiptDetail[17]
        #レシートID
        str_receiptID = List_receiptDetail[0]
        #購入日付
        str_date = str(List_receiptDetail[1]) + '/' + str(List_receiptDetail[2]) + '/' + str(List_receiptDetail[3])
        #合計
        int_totalMoney += int_money

        #タイプ別合計
        List_typeMoneys[int_itemTypeNo] += int_money

        #レシート個別
        detail = [ str_receiptID , str_date , str_shopName , str_itemName , int_itemTypeNo , int_money ]
        List_receiptMoeys.append(detail)

    Dict_templateData = { 'totalMoney' : int_totalMoney , 'typeMoneys' : List_typeMoneys , "ReceiptMoeys" : List_receiptMoeys , "ItemType" : List2_itemType}
    return  render_template('ReceiptMonth.html',**Dict_templateData )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
