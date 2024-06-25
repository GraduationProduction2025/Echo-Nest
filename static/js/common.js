//新規追加ボタンを非表示にして質問タイプ選択ボタンを表示
function showInputOptions() {
    document.getElementById("inputOptions").style.display = "block";
    document.getElementById("input-cre").style.display = "none";
}

//質問タイプを選択
function createInputField(inputType) {
    var newDiv = document.createElement("div");
    newDiv.classList.add("ques-container");
    var addQuesDiv = document.querySelector(".add-ques");
    addQuesDiv.parentNode.insertBefore(newDiv, addQuesDiv);
    var newInputField;

    newInputField = '<div class="ques-lane">' +
                        '<input type="text" class="ques-name" placeholder="質問のタイトルを入力">' +
                        '<img src="/static/img/delbox.png" class="ques-del">' +
                    '</div>';
    newDiv.innerHTML += newInputField;

    if (inputType === "text") { //テキストを選択
        newInputField = '<div>' +
                            '<textarea rows="3" class="ques-text" placeholder="回答を入力してください" disabled></textarea> ' +
                        '</div>';
    } else if (inputType === "radio") { //ラジオボタンを選択
        newInputField = '<div>'+
                            '<div class="radio">'+
                                '<input type="radio" name="radio">'+
                                '<input type="text" class="option-text" placeholder="オプション名を入力">'+
                                '<button class="option-del">✕</button>'+
                            '</div>'+
                            '<div class="radio">'+
                                '<input type="radio" name="radio">'+
                                '<input type="text" class="option-text" placeholder="オプション名を入力">'+
                                '<button class="option-del">✕</button>'+
                            '</div>'+
                            '<button class="option-add">＋ オプションを追加</button>'+
                        '</div>';
    } else if (inputType === "checkbox") { //チェックボックスを選択
        newInputField = '<div>'+
                            '<div>'+
                                '<input type="checkbox">'+
                                '<input type="text" class="option-text" placeholder="オプション名を入力">'+
                                '<button class="option-del">✕</button>'+
                            '</div>'+
                            '<div>'+
                                '<input type="checkbox">'+
                                '<input type="text" class="option-text" placeholder="オプション名を入力">'+
                                '<button class="option-del">✕</button>'+
                            '</div>'+
                            '<button class="option-add">＋ オプションを追加</button>'+
                        '</div>';
    } else if (inputType === "select") { //プルダウンを選択
        newInputField = '<div>'+
                            '<input type="text" class="ques-text" placeholder="(要素1,要素2,要素3)と入力">'+
                        '</div>';
    }
    newDiv.innerHTML += newInputField; //選択されたタイプをhtmlに追加
    document.getElementById("inputOptions").style.display = "none"; //タイプ選択ボタンを非表示
    document.getElementById("input-cre").style.display = ""; //新規追加ボタンを表示
}