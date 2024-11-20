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
    let newInputField = `<div class="ques-lane">
                    <input type="text" name="ques-title" class="ques-title" placeholder="質問のタイトルを入力">
                    <img src="/static/img/delbox.png" class="ques-del" onclick="ques_del(this)">
                    </div>
                    <select name="ques-change" onchange="updateInputField(this, ${questionIndex})">
                        <option value="text">テキスト</option>
                        <option value="checkbox">チェックボックス</option>
                        <option value="radio">ラジオボタン</option>
                    </select>`;
    newDiv.innerHTML += newInputField;

    // 初期オプション数を設定
    optionCounters[questionIndex] = 3;

    // 初期の inputType に応じたフィールドを追加
    addInputField(newDiv, inputType, questionIndex);
    questionIndex++;
}

// 質問タイプに応じて入力フィールドを追加
function addInputField(container, inputType, index) {
    let inputFieldHtml;
    if (inputType === "text") {
        inputFieldHtml = `<input type="hidden" name="ques-type" value="textarea">
                        <div>
                            <textarea rows="3" name="ques-text" class="ques-text" placeholder="回答を入力してください" disabled></textarea>
                        </div>`;
    } else if (inputType === "checkbox") {
        inputFieldHtml = `<input type="hidden" name="ques-type" value="checkbox">
                         <div id="options-container-${index}">
                            <div><input type="checkbox">
                            <input type="text" name="option-text-${index}-1" class="option-text" placeholder="オプション名を入力">
                            <button type="button" class="option-del" onclick="option_del(this, ${index})">✕</button>
                            </div>
                            <div><input type="checkbox">
                            <input type="text" name="option-text-${index}-2" class="option-text" placeholder="オプション名を入力">
                            <button type="button" class="option-del" onclick="option_del(this, ${index})">✕</button>
                            </div>
                         </div>
                         <div id="options-add-${index}">
                            <button type="button" class="option-add" onclick="option_add(this, ${index} ,1)">＋ オプションを追加</button>
                         </div>`;
    } else if (inputType === "radio") {
        inputFieldHtml = `<input type="hidden" name="ques-type" value="radio">
                         <div id="options-container-${index}">
                            <div><input type="radio" name="radio${index}">
                            <input type="text" name="option-text-${index}-1" class="option-text" placeholder="オプション名を入力">
                            <button type="button" class="option-del" onclick="option_del(this, ${index})">✕</button>
                            </div>
                            <div><input type="radio" name="radio${index}">
                            <input type="text" name="option-text-${index}-2" class="option-text" placeholder="オプション名を入力">
                            <button type="button" class="option-del" onclick="option_del(this, ${index})">✕</button>
                            </div>
                         </div>
                         <div id="options-add-${index}">
                            <button type="button" class="option-add" onclick="option_add(this, ${index} , 2)">＋ オプションを追加</button>
                         </div>`;
    } 
    container.querySelector('.ques-lane').insertAdjacentHTML('afterend', inputFieldHtml);
}

// オプションの更新処理
function updateInputField(selectElement, questionIndex) {
    const selectedType = selectElement.value;
    const container = selectElement.closest('.ques-container');
    const existingField = container.querySelector('[name="ques-type"]').nextElementSibling; // 入力フィールドのみ取得

    // 既存の入力フィールドを削除
    if (existingField) {
        existingField.remove();
    }

    // hidden ques-type フィールドがある場合に削除
    const quesTypeField = container.querySelector('input[name="ques-type"]');
    if (quesTypeField) {
        quesTypeField.remove();
    }

    // options-add が存在する場合削除する
    const optionsAdd = container.querySelector(`#options-add-${questionIndex}`);
    if (optionsAdd) {
        optionsAdd.remove();
    }

    //オプション数をリセット
    optionCounters[questionIndex] = 3;

    // 新しいタイプに応じてフィールドを追加
    addInputField(container, selectedType, questionIndex);
}

// オプションを追加する関数
function option_add(button, Index , Type_num) {
    const optionsContainer = document.getElementById(`options-container-${Index}`);
    let optionCount = optionCounters[Index]++;

    if (Type_num == 1) {
        newOption = `<div><input type="checkbox">
               <input type="text" name="option-text-${Index}-${optionCount}" class="option-text" placeholder="オプション名を入力">
               <button type="button" class="option-del" onclick="option_del(this, ${Index})">✕</button></div>`;
    } else if (Type_num == 2) {
        newOption = `<div><input type="radio" name="radio${Index}">
               <input type="text" name="option-text-${Index}-${optionCount}" class="option-text" placeholder="オプション名を入力">
               <button type="button" class="option-del" onclick="option_del(this, ${Index})">✕</button></div>`;
    }
    
    optionsContainer.insertAdjacentHTML('beforeend', newOption);
}

// オプション削除の関数
function option_del(button, Index) {
    button.parentElement.remove();
    updateOptionIndices(Index);
}

// インデックスを再設定
function updateOptionIndices(Index) {
    const optionsContainer = document.getElementById(`options-container-${Index}`);
    const options = optionsContainer.querySelectorAll('.option-text');
    options.forEach((option, index) => {
        option.name = `option-text-${Index}-${index + 1}`;
    });
    optionCounters[Index] = options.length + 1;
}

// 質問削除の関数
function ques_del(button) {
    const container = button.closest('.ques-container');
    if (container) {
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
                option.name = `option-text-${newIndex}-${optionIndex + 1}`;
            });
            optionCounters[newIndex] = options.length + 1;
        } else {
            optionCounters[newIndex] = 1;
        }

        const optionsAdd = container.querySelector(`#options-add-${container.dataset.index}`);
        if (optionsAdd) {
            optionsAdd.id = `options-add-${newIndex}`;
            const optionAddButton = container.querySelector('.option-add');
            optionAddButton.setAttribute('onclick', `option_add(this, ${newIndex})`);
        }
        container.dataset.index = newIndex;
    });

    questionIndex = questionContainers.length + 1;
}
