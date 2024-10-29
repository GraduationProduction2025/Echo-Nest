//新規追加ボタンを非表示にして質問タイプ選択ボタンを表示
function showInputOptions(event) {
    event.preventDefault();
    document.getElementById("inputOptions").style.display = "block";
    document.getElementById("input-cre").style.display = "none";
}

//質問タイプを選択
function createInputField(event, inputType) {
    event.preventDefault();
    var newDiv = document.createElement("div");
    newDiv.classList.add("ques-container");
    var addQuesDiv = document.querySelector(".add-ques");
    addQuesDiv.parentNode.insertBefore(newDiv, addQuesDiv);
    var newInputField;

    newInputField = '<div class="ques-lane">' +
                        '<input type="text" name="ques-title" class="ques-title" placeholder="質問のタイトルを入力">' +
                        '<img src="/static/img/delbox.png" class="ques-del">' +
                    '</div>';
    newDiv.innerHTML += newInputField;

    if (inputType === "text") { //テキストを選択
        newInputField = '<div>' +
                            '<textarea rows="3" name="ques-text" class="ques-text" placeholder="回答を入力してください" disabled></textarea> ' +
                        '</div>';
    }
    newDiv.innerHTML += newInputField; //選択されたタイプをhtmlに追加
    document.getElementById("inputOptions").style.display = "none"; //タイプ選択ボタンを非表示
    document.getElementById("input-cre").style.display = ""; //新規追加ボタンを表示
}

