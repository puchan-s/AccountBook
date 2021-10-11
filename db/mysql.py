'''
db.mysql.py
sqlの実行、SQL文を記載
'''
import MySQLdb
import configparser

#使用するSQL
#店舗情報
SHOPDATA_SELECT_SHOPTEL = "SELECT * FROM SHOPDATA WHERE SHOPTEL={0}"
SHOPDATA_SELECT_SHOPID = "SELECT * FROM SHOPDATA WHERE SHOPID={0}"
SHOPDATA_INSERT = "INSERT INTO SHOPDATA ( SHOPNAME , SHOPTEL , CREATEUSER , CREATEDATE , UPDATEDATE ) VALUES  ('{0}','{1}',{2},CURRENT_TIMESTAMP(),NULL)"

#商品種類
ITEMTYPE_SELECT = "SELECT * FROM ITEMTYPE"

#レシート情報
RECEIPT_SELECT = "SELECT * FROM RECEIPT WHERE RECEIPTID={0} AND USERID={1}"
RECEIPT_MONTH_SELECT = "SELECT * FROM RECEIPT" \
                         " LEFT JOIN RECEIPTDETAILS ON RECEIPT.RECEIPTID = RECEIPTDETAILS.RECEIPTID " \
                         " LEFT JOIN SHOPDATA ON RECEIPT.SHOPID = SHOPDATA.SHOPID " \
                             " WHERE DATE_YEAR={0} AND DATE_MONTH={1} AND RECEIPT.USERID={2}"
RECEIPT_SHOP_SELECT = "SELECT * FROM RECEIPT LEFT JOIN SHOPDATA ON RECEIPT.SHOPID = SHOPDATA.SHOPID "
RECEIPT_MAXID = "SELECT MAX(RECEIPTID) AS RECEIPID FROM RECEIPT"
RECEIPT_INSERT = "INSERT INTO RECEIPT ( RECEIPTID ,DATE_YEAR , DATE_MONTH,DATE_DAY ,USERID ,SHOPID , CREATEDATE , UPDATEDATE ) VALUES ({0},{1},{2},{3},{4},{5},CURDATE(),NULL)"
RECEIPT_UPDATE = "UPDATE RECEIPT SET DATE_YEAR = {1}, DATE_MONTH = {2} , DATE_DAY = {3} ,SHOPID = {5} , UPDATEDATE = CURDATE() WHERE RECEIPTID = {0} AND USERID = {4} "

#レシート商品情報
RECEIPTDETAILS_SELECT = "SELECT * FROM RECEIPTDETAILS WHERE RECEIPTID={0} AND USERID={1}"
RECEIPTDETAILS_INSERT = "INSERT INTO RECEIPTDETAILS ( RECEIPTID ,ITEMNAME ,ITEMTYPE ,ITEMMONEY , USERID , CREATEDATE  , UPDATEDATE ) VALUES ({0},'{1}',{2},{3},{4},CURRENT_TIMESTAMP(),NULL)"
RECEIPTDETAILS_DELETE = "DELETE FROM RECEIPTDETAILS WHERE RECEIPTID = {0}"

#DB接続用変数 項目設定
CONFIGPATH = "config.ini" 
config_ini = configparser.ConfigParser()
config_ini.read(CONFIGPATH, encoding='utf-8')
read_DB = config_ini['DBSettings']
DB_User = read_DB.get('User')
DB_User = config_ini['DBSettings']['User']
DB_Passwd = config_ini['DBSettings']['Passwd']
DB_Host = config_ini['DBSettings']['Host']
DB_DBName = config_ini['DBSettings']['DBName']
DB_Sock = config_ini['DBSettings']['Sock']

def select(str_sql):
    """[summary]
        DBからSELECTした値を取得する
    Args:
        str_sql (str): 実行するSQL文

    Returns:
        str[str[]]: DBより取得したデータの2次元配列
    """
    cls_conn = None

    try:
        # 接続する
        cls_conn = MySQLdb.connect(
            user=DB_User,
            passwd=DB_Passwd,
            unix_socket=DB_Sock,
            host=DB_Host,
            db=DB_DBName,
        )

        # カーソルを取得する
        cls_cur = cls_conn.cursor()

        # SQL（データベースを操作するコマンド）を実行する
        cls_cur.execute(str_sql)

        # 実行結果を取得する
        List2_rows = cls_cur.fetchall()

        #取得情報の返却
        return List2_rows

    except Exception as e:
        return None
    finally :
        #接続を破棄
        cls_cur.close
        cls_conn.close

def commit(str_sql):
    """[summary]
      INSERT,UPDATE,DELETEを実行する
    Args:
        str_sql (str): 実行するSQL
    """
    cls_conn = None

    try:
        #接続
        cls_conn = MySQLdb.connect(
            user=DB_User,
            passwd=DB_Passwd,
            unix_socket=DB_Sock,
            host=DB_Host,
            db=DB_DBName,
        )

        #カーソル取得
        cls_cur = cls_conn.cursor()

        #実行
        cls_cur.execute(str_sql)
        cls_conn.commit()

    except Exception as e:
        print(f"Error Occurred: {e}")

    finally:
        #接続を破棄
        cls_cur.close()
        cls_conn.close()
