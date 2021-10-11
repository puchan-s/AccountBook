
/**
 * 月のデータを表示する
 * @param {int} totalMoney      //月合計金額
 * @param {Array} typeMoneys    //種類別合計金額
 * @param {Array} itemTypes     //種類名
 * @param {Array} ReceiptMoneys //レシートごとのデータ
 */
function getMonthReceiptData(totalMoney ,typeMoneys ,  itemTypes ,ReceiptMoneys){

    //月合計
    let totalMoneyElement = document.getElementById("TotalMoney") ;
    totalMoneyElement.rows[0].cells[1].innerHTML = totalMoney + "円" ;

    //分類合計
    let typeMoneysElement = document.getElementById("typeMoneys") ;
    console.log(typeMoneys)
    itemTypes.forEach( (value,index,itemTypes) => {
        let trElement = document.createElement("tr");
        let typeNameElement = document.createElement("th");
        typeNameElement.textContent = value[1] ;
        let typeMoneyElement = document.createElement("th");
        typeMoneyElement.textContent = typeMoneys[index + 1] ;  //typeIDが1から始まるため、1を加算
        trElement.appendChild(typeNameElement);
        trElement.appendChild(typeMoneyElement);
        typeMoneysElement.appendChild(trElement);
    });
    
    //詳細 
    let ReceiptMoneyElement = document.getElementById("ReceiptMoneys");
    let ReceiptTitleElement = document.createElement("td");
    var ReceiptID = -1 ;
    var DataCount = 0 ;
    ReceiptMoneys.forEach( (value,index,ReceiptMoneys) => {
        let trElement = document.createElement("tr");

        if(ReceiptID != value[0]){
            //レシートデータが変わった場合
            //rowSpanの設定
            ReceiptTitleElement.rowSpan = DataCount ;

            //新しいデータ
            ReceiptID = value[0] ;
            ReceiptTitleElement = document.createElement("td");
            ReceiptTitleElement.innerHTML = value[2] + "<br>" + value[1] ;
            trElement.append(ReceiptTitleElement);
            DataCount = 0 ;
        }

        let ItemName = document.createElement("td");
        ItemName.textContent = value[3];
        let ItemMoney = document.createElement("td");
        ItemMoney.textContent = value[5] + "円";

        trElement.append(ItemName);
        trElement.append(ItemMoney);

        ReceiptMoneyElement.appendChild(trElement);

        DataCount++ ;
    });
    ReceiptTitleElement.rowSpan = DataCount ;
}
 