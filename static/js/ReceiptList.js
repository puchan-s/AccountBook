
/**
 * 登録されたレシートデータ全てを取得
 * @param {Array} receiptData //レシートデータ配列
 */
function getReceiptData(receiptData){
    let items = document.getElementById("items");

    var itemCount = 0 ;
    receiptData.forEach( (value,index,receiptData) => {
        let addElement = document.createElement("div");
        addElement.id = "receiptData" + itemCount

        let link = document.createElement("a");
        link.href = "/ReceiptDetailData?receiptID=" + value[0] ;
        link.textContent = value[1] + "-" + value[2] + "-" + value[3] + " " + value[9] ;
        addElement.appendChild(link);

        items.appendChild(addElement);

        itemCount++ ;
    });
} 