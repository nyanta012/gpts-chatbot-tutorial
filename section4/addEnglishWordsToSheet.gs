/**
 * スプレッドシートの最初のシートを取得する
 */
function getFirstSheet() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  return spreadsheet.getSheets()[0];
}

/**
 * 単語をスプレッドシートに追加する
 */
function addWord(word) {
  var sheet = getFirstSheet();
  var lastRow = sheet.getLastRow();
  sheet.getRange(lastRow + 1, 1).setValue(word);
}

/**
 * HTTP POST リクエストを処理する
 */
function doPost(e) {
  try {
    var postData = JSON.parse(e.postData.contents);
    var word = postData.word;
    addWord(word);
    return createJsonResponse(200, "Word added: " + word);
  } catch (error) {
    Logger.log("Error in doPost: " + error.message);
    return createJsonResponse(500, "Error: " + error.message);
  }
}

/**
 * JSON形式のレスポンスを生成する
 */
function createJsonResponse(status, message) {
  var response = {
    status: status,
    message: message
  };
  return ContentService.createTextOutput(JSON.stringify(response))
                        .setMimeType(ContentService.MimeType.JSON);
}

/**
 * doPost関数のテストを行う
 */
function testDoPost() { 
  try {
    var response = doPost({postData: {contents: JSON.stringify({word: "example"})}});
    var content = response.getContent();
    Logger.log("Response: " + content);
  } catch (error) {
    Logger.log("Error in testDoPost: " + error.message);
  }
}
