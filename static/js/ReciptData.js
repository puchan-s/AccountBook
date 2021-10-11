/********************
 * グローバル変数
 ********************/

/**
 * 表示した商品情報の数（追加された分は加算され、削除された分はそのまま残る）
 */
var g_itemCount = 0 ;

/**
 * ItemType配列　全ての商品種類をしている
 */
var g_ItemType = null ;

/*****************
 * メソッド宣言
 *****************/

/**
 * ショップ名取得
 */
function getShopName(){

    var shopTel = "";
    var inputShopTel = document.getElementById("Tel")

    var request = new XMLHttpRequest();

    request.open('GET', '/getShopData?SHOPTEL=' + inputShopTel.value , true);
    request.responseType = 'json';

    request.onload = function () {
        var data = this.response;
        var ShopNameElement = document.getElementById('ShopName')
        ShopNameElement.value = data['ShopName'];
    };

    request.send();
}

/**
 * xボタン押下時の削除処理
 * @param {Element} e  //削除する商品のelement
 */
function deleteItem(e){
    itemName = "item" + e.name
    const element = document.getElementById(itemName); 
    element.remove();
}

/**
 * レシートデータ初期表示処理
 * @param {Array} ShopData      //店舗情報の連想配列 
 * @param {Array} ImageTextData //商品データ
 * @param {Array} ItemType      //商品種類
 */
function ReciptDataShow(ShopData,ImageTextData,ItemType){
    //店舗データ設定
    var inputShopTel = document.getElementById("Tel");
    inputShopTel.value = ShopData["Tel"];
    var ShopNameElement = document.getElementById('ShopName');
    ShopNameElement.value = ShopData['name'];
    
    let items = document.getElementById("items");

    g_ItemType = ItemType ;

    var itemCount = 0 ;
    ImageTextData.forEach( (value,index,ImageTextData) => {
        ReciptDataAdd(itemCount,ItemType,value);
        
        itemCount++ ;
    });
    
    g_itemCount = itemCount ;
}

/**
 * 商品情報を追加する
 * @param {*} itemCount //Element.idの番号
 * @param {*} ItemType  //商品種類
 * @param {*} value     //商品情報 [0]:商品名 [1]:商品価格
 */
function ReciptDataAdd(itemCount , ItemType , value = null ){

    if(value == null){
        value = ['',''];
    }

    let addElement = document.createElement("div");
        addElement.id = "item" + itemCount
        //商品名
        let ItemNameDiv = document.createElement("div");
        ItemNameDiv.style.setProperty("display","inline-block");
        ItemNameDiv.style.setProperty("padding","5px");
        ItemNameDiv.className = "col-sm-3";
        let spanItemNameTitle = document.createElement("span");
        spanItemNameTitle.textContent = "商品名";
        let InputItemNameValue = document.createElement("input");
        InputItemNameValue.name = "ItemName" + itemCount;
        InputItemNameValue.value = value[0] ;
        ItemNameDiv.appendChild(spanItemNameTitle);
        ItemNameDiv.appendChild(InputItemNameValue);

        //分類
        let ItemTypeDiv = document.createElement("div");
        ItemTypeDiv.style.setProperty("display","inline-block");
        ItemTypeDiv.style.setProperty("padding","5px");
        ItemTypeDiv.className = "col-sm-3";
        let spanItemTypeTitle = document.createElement("span");
        spanItemTypeTitle.textContent = "分類";
        ItemTypeDiv.appendChild(spanItemTypeTitle);
        let ItemTypeSelect = document.createElement("select");
        ItemTypeSelect.name = "ItemType" + itemCount;
        ItemType.forEach( (ItemTypeValue,ItemTypeIndex,ItemType) => {
            let optionElement = document.createElement("option");
            optionElement.value=ItemTypeValue[0];
            optionElement.textContent = ItemTypeValue[1];
            ItemTypeSelect.appendChild(optionElement);
        });
        ItemTypeDiv.appendChild(ItemTypeSelect);


        //価格
        let ItemValueDiv = document.createElement("div");
        ItemValueDiv.style.setProperty("display","inline-block");
        ItemValueDiv.style.setProperty("padding","5px");
        ItemValueDiv.className = "col-sm-3";
        let spanItemValueTitle = document.createElement("span");
        spanItemValueTitle.textContent = "価格";
        let InputItemValueValue = document.createElement("input");
        InputItemValueValue.name = "ItemValue" + itemCount;
        InputItemValueValue.value = value[1] ;
        ItemValueDiv.appendChild(spanItemValueTitle);
        ItemValueDiv.appendChild(InputItemValueValue);

        //削除ボタン
        let deleteButton = document.createElement("button");
        deleteButton.className = "col-sm-1";
        deleteButton.name = itemCount ;
        deleteButton.textContent = "x";
        deleteButton.setAttribute('onclick', 'deleteItem(this)');
        deleteButton.type="button";

        addElement.appendChild(ItemNameDiv);
        addElement.appendChild(ItemTypeDiv);
        addElement.appendChild(ItemValueDiv);
        addElement.append(deleteButton);

        items.appendChild(addElement);
}

/**
 * 追加ボタン処理
 */
function addReciptDataClick(){
    ReciptDataAdd(g_itemCount,g_ItemType);
    g_itemCount = g_itemCount + 1 ;
}