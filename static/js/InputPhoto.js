
/**
 * 画像読み込み処理（画像サイズ変更）
 * @param {Element} e //ファイルロードエレメント
 */
const fileup = (e) => {
  const img = document.getElementById('img');
  const reader = new FileReader();
  const imgReader = new Image();
  const imgWidth = 400;
  reader.onloadend = () => {
    imgReader.onload = () => {
    const imgType = imgReader.src.substring(5, imgReader.src.indexOf(';'));
    const imgHeight = imgReader.height * (imgWidth / imgReader.width);
    const canvas = document.createElement('canvas');
    canvas.width = imgWidth;
    canvas.height = imgHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(imgReader,0,0,imgWidth,imgHeight);
    img.src = canvas.toDataURL(imgType);
    }
    imgReader.src = reader.result;
  }
  reader.readAsDataURL(e.files[0]);
}

/**
 * 画像送信
 */
function submitImage(){

  const img = document.querySelector("#img");

  var work_canvas = document.createElement('canvas');
  work_canvas.width  = img.width;
  work_canvas.height = img.height;

  // Draw Image
  var ctx = work_canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);
  // To Base64

  // Canvasのデータを取得
  const canvas = work_canvas.toDataURL("image/png");  // DataURI Schemaが返却される

  // POST先
  var url = "/Output";

  // パラメータを付与する場合
  var inputs = '';
  var params = [["data", canvas]];
  for(var i = 0, n = params.length; i < n; i++) {
    inputs += '<input type="hidden" name="' + params[i][0] + '" value="' + params[i][1] + '" />';
  }

  // POST遷移
  $("body").append('<form action="'+url+'" method="post" id="post">'+inputs+'</form>');
  $("#post").submit();

}