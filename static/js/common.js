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
                        <option value="select">プルダウン</option>
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
    } else if (inputType === "select") {
        inputFieldHtml = `<input type="hidden" name="ques-type" value="select">
                         <div id="options-container-${index}">
                            <div><label id="select-num">1.</label>
                            <input type="text" name="option-text-${index}-1" class="option-text" placeholder="オプション名を入力">
                            <button type="button" class="option-del" onclick="option_del(this, ${index})">✕</button>
                            </div>
                            <div><label id="select-num">2.</label>
                            <input type="text" name="option-text-${index}-2" class="option-text" placeholder="オプション名を入力">
                            <button type="button" class="option-del" onclick="option_del(this, ${index})">✕</button>
                            </div>
                         </div>
                         <div id="options-add-${index}">
                            <button type="button" class="option-add" onclick="option_add(this, ${index} , 3)">＋ オプションを追加</button>
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
    } else if (Type_num == 3) {
        newOption = `<div><label id="select-num">${optionCount}.</label>
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

        const label = option.previousElementSibling;
        if (label && label.id === "select-num") {
            label.textContent = `${index + 1}.`;
        }
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

//タイトルやオプションが空欄で送信される際にメッセージを出す処理
document.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('create-ques-btn')) {
        return;
    }
    const createBtn = document.getElementById('create-ques-btn');
    const tempBtn = document.getElementById('tem-ques-btn');

    function validateInputs() {
        const titleText = document.querySelector('.title-text');
        const quesTitles = document.querySelectorAll('.ques-title');
        const optionTexts = document.querySelectorAll('.option-text');

        let errors = [];
        let check = true;

        // タイトルのチェック
        if (!titleText.value.trim()) {
            errors.push('タイトルが入力されていません。');
        }

        // 質問タイトルのチェック
        quesTitles.forEach((quesTitle) => {
            if (!quesTitle.value.trim()) {
                check = false; 
            }
        });
        if(check != true){
            errors.push('未入力の質問タイトルがあります。');
            check = true
        }

        // オプション名のチェック
        optionTexts.forEach((optionText) => {
            if (!optionText.value.trim()) {
                check = false;
            }
        });
        if(check != true){
            errors.push('未入力のオプションがあります。');
            check = true
        }

        // エラーがあれば警告表示
        if (errors.length > 0) {
            alert(errors.join('\n'));
            return false;
        }

        return true;
    }

    createBtn.addEventListener('click', (e) => {
        if (!validateInputs()) {
            e.preventDefault(); // フォームの送信を防ぐ
        }
    });

    tempBtn.addEventListener('click', (e) => {
        if (!validateInputs()) {
            e.preventDefault(); // フォームの送信を防ぐ
        }
    });
});

//横スクロールを可能にする
document.addEventListener('DOMContentLoaded', function () {
    const scrollContainer = document.querySelector('.scrollable-card-container');

    scrollContainer.addEventListener('wheel', function (event) {
        event.preventDefault(); // 縦スクロールを無効化
        scrollContainer.scrollLeft += event.deltaY; // ホイールの動きを横スクロールに変換
    });
});

//自動でループしながら徐々にスクロールさせる
document.addEventListener('DOMContentLoaded', function () {
    const scrollContainer = document.querySelector('.scrollable-card-container');
    const cardWrapper = document.querySelector('.card-wrapper');
    
    let cardWidth = 0; // カードの幅を保持
    let isScrolling = false; // スクロールが進行中かどうか

    // 最初の要素の幅を取得
    if (cardWrapper && cardWrapper.children.length > 0) {
        cardWidth = cardWrapper.children[0].offsetWidth;
    }

    // スクロール可能かどうかを判定
    function isScrollable() {
        if (!scrollContainer || !cardWrapper) return false;

        const totalCardWidth = cardWidth * cardWrapper.children.length; // 全カードの幅
        const containerWidth = scrollContainer.clientWidth; // コンテナの幅

        // 要素がコンテナ内に収まりきる場合、スクロールは不要
        return totalCardWidth > containerWidth;
    }

    // スクロール処理
    function autoScroll() {
        if (!isScrollable()) return; // スクロール可能でない場合は処理を実行しない

        if (!scrollContainer || !cardWrapper) return;

        // スクロール位置を少し進める
        scrollContainer.scrollLeft += 1;

        // 横スクロールが終了したときに最初の要素を最後に移動
        if (scrollContainer.scrollLeft >= (cardWrapper.scrollWidth - scrollContainer.clientWidth) && !isScrolling) {
            isScrolling = true;  // スクロール中フラグを立てる

            // 最初の要素を最後に移動
            const firstCard = cardWrapper.firstElementChild;
            cardWrapper.appendChild(firstCard); // 最初の要素を最後に追加

            // 再度スクロール位置を調整
            scrollContainer.scrollLeft -= cardWidth; // 少し戻して繋がり感を持たせる

            // スクロール終了後フラグをリセット
            setTimeout(() => {
                isScrolling = false;
            }, 100);
        }
    }

    // 自動スクロールを一定間隔で実行
    const scrollInterval = setInterval(autoScroll, 20); // 20msごとにスクロール
});

