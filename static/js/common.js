//新規追加ボタンを非表示にして質問タイプ選択ボタンを表示
function showInputOptions(event) {
    event.preventDefault();
    document.getElementById("inputOptions").style.display = "block";
    document.getElementById("input-cre").style.display = "none";
}

// インデックスを管理するオブジェクト
let optionCounters = {}; // 各質問ごとのオプション数を保持
let questionIndex = 1;  // 質問ごとのインデックス

// 質問タイプを選択
function createInputField(event, inputType) {
    event.preventDefault();
    const newDiv = document.createElement("div");
    newDiv.classList.add("ques-container");
    newDiv.dataset.index = questionIndex; // 質問ごとのインデックスを設定
    const addQuesDiv = document.querySelector(".add-ques");
    addQuesDiv.parentNode.insertBefore(newDiv, addQuesDiv);
    let newInputField;

    newInputField = `<div class="ques-lane">
                    <input type="text" name="ques-title" class="ques-title" placeholder="質問のタイトルを入力">
                    <img src="/static/img/delbox.png" class="ques-del" onclick="ques_del(this)">
                    </div>`;
    newDiv.innerHTML += newInputField;

    // optionCountersに新しい質問用のカウンタを追加し初期化
    optionCounters[questionIndex] = 1;

    if (inputType === "text") { // テキストを選択
        newInputField = '<input type="hidden" name="ques-type" value="1">'+
                        '<div>' +
                        '<textarea rows="3" name="ques-text" class="ques-text" placeholder="回答を入力してください" disabled></textarea> ' +
                        '</div>';
    } else if (inputType === "checkbox") { // チェックボックスを選択
        newInputField = `<input type="hidden" name="ques-type" value="2">
                         <div id="options-container-${questionIndex}">
                            <div><input type="checkbox">
                            <input type="text" name="option-text-${questionIndex}-1" class="option-text" placeholder="オプション名を入力">
                            <button type="button" class="option-del" onclick="option_del(this, ${questionIndex})">✕</button>
                            </div>
                            <div><input type="checkbox">
                            <input type="text" name="option-text-${questionIndex}-2" class="option-text" placeholder="オプション名を入力">
                            <button type="button" class="option-del" onclick="option_del(this, ${questionIndex})">✕</button>
                            </div>
                         </div>
                         <div id="options-add-${questionIndex}">
                            <button type="button" class="option-add" onclick="option_add(this, ${questionIndex})">＋ オプションを追加</button>
                         </div>`;
    }
    newDiv.innerHTML += newInputField; 
    questionIndex++; 
    document.getElementById("input-cre").style.display = ""; 
    document.getElementById("inputOptions").style.display = "none"; 
}

// オプションを追加する関数
function option_add(button, questionIndex) {
    const optionsContainer = document.getElementById(`options-container-${questionIndex}`);
    let optionCount = optionCounters[questionIndex]++;
    const newOption = `<div><input type="checkbox">
                       <input type="text" name="option-text-${questionIndex}-${optionCount}" class="option-text" placeholder="オプション名を入力">
                       <button type="button" class="option-del" onclick="option_del(this, ${questionIndex})">✕</button></div>`;
    optionsContainer.insertAdjacentHTML('beforeend', newOption);
}

// オプション削除の関数
function option_del(button, questionIndex) {
    button.parentElement.remove();
    updateOptionIndices(questionIndex);
}

// インデックスを再設定
function updateOptionIndices(questionIndex) {
    const optionsContainer = document.getElementById(`options-container-${questionIndex}`);
    const options = optionsContainer.querySelectorAll('.option-text');
    options.forEach((option, index) => {
        option.name = `option-text-${questionIndex}-${index + 1}`;
    });
    optionCounters[questionIndex] = options.length + 1;
}

// 質問削除の関数
function ques_del(button) {
    const container = button.closest('.ques-container');
    if (container) { // containerがnullでないことを確認
        const questionIndex = parseInt(container.dataset.index, 10);
        delete optionCounters[questionIndex];
        container.remove();
        updateQuestionIndices();
    }
}

// 質問インデックスを詰める関数
function updateQuestionIndices() {
    const questionContainers = document.querySelectorAll('.ques-container');
    questionContainers.forEach((container, index) => {
        const newIndex = index + 1;

        // optionsContainerが存在する場合、オプションのインデックスを更新
        const optionsContainer = container.querySelector(`#options-container-${container.dataset.index}`);
        if (optionsContainer) {
            optionsContainer.id = `options-container-${newIndex}`;
            const options = optionsContainer.querySelectorAll('.option-text');
            options.forEach((option, optionIndex) => {
                if (option) {
                    option.name = `option-text-${newIndex}-${optionIndex + 1}`;
                }
            });
            optionCounters[newIndex] = options.length + 1;
        } else {
            optionCounters[newIndex] = 1;
        }

        // optionsAddが存在する場合、オプションのインデックスを更新
        const optionsAdd = container.querySelector(`#options-add-${container.dataset.index}`);
        if (optionsAdd) {
            optionsAdd.id = `options-add-${newIndex}`;
            const optionAddButton = container.querySelector('.option-add');
            optionAddButton.setAttribute('onclick', `option_add(this, ${newIndex})`);
        }        
        container.dataset.index = newIndex;
    });

    // 全体の質問インデックスもリセット
    questionIndex = questionContainers.length + 1;
}

// フォーム送信前のバリデーション関数
function validateForm() {
    // 全てのoption-textフィールドを取得
    const optionFields = document.querySelectorAll('.option-text');
    let isValid = true;
    
    // 各option-textが入力されているか確認
    optionFields.forEach((field) => {
        if (field.value.trim() === '') {
            isValid = false;
            field.classList.add('error'); // 空欄のフィールドにエラースタイルを追加
        } else {
            field.classList.remove('error'); // 入力されている場合はエラーを削除
        }
    });

    // バリデーション結果に基づいて処理を分岐
    if (!isValid) {
        alert('入力されていないオプションがあります。');
        return false; // フォーム送信を中断
    }
    return true; // バリデーションを通過
}

document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.getElementById('create-ques-btn');
    
    // ボタンが存在する場合のみイベントリスナーを追加
    if (submitButton) {
        submitButton.addEventListener('click', (event) => {
            if (!validateForm()) {
                event.preventDefault(); // バリデーションエラーがある場合は送信を中止
            }
        });
    }
});

