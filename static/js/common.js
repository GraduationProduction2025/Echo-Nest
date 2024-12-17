// 質問のインデックス管理
let questionCounter = 0;

// 質問作成
function createInputField(event, inputType) {
    event.preventDefault();

    const form = document.querySelector("form");
    const existingContainers = form.querySelectorAll(".ques-container");
    questionCounter = existingContainers.length;

    const newDiv = document.createElement("div");
    newDiv.classList.add("ques-container");
    newDiv.dataset.index = ++questionCounter;

    const addQuesDiv = document.querySelector(".add-ques");
    addQuesDiv.parentNode.insertBefore(newDiv, addQuesDiv);

    const newInputField = `
        <div class="ques-lane">
            <div class="image-upload-container">
                <input type="file" name="ques-image-${questionCounter}" id="file-input-${questionCounter}" class="ques-image" accept="image/*" onchange="previewImage(this, ${questionCounter})" style="display: none;">
                <div class="image-preview" id="image-preview-${questionCounter}">
                    <img src="/static/img/def-img.png" alt="画像を選択" class="preview-img" id="upload-btn-${questionCounter}" onclick="triggerFileInput(${questionCounter})" style="cursor: pointer;">
                    <button type="button" class="image-del-btn" onclick="removeImage(${questionCounter})" style="display: none;">✕</button>
                </div>
            </div>
            <input type="text" name="ques-title" class="ques-title" placeholder="質問のタイトルを入力">
            <img src="/static/img/delbox.png" class="ques-del" onclick="deleteQuestion(this)">
        </div>
        <div class="select-right">
            <select name="ques-change" class="ques-change" onchange="updateInputField(this)">
                <option value="text">テキスト</option>
                <option value="checkbox">チェックボックス</option>
                <option value="radio">ラジオボタン</option>
                <option value="select">プルダウン</option>
            </select>
        </div>
        <div class="input-container"></div>
    `;

    newDiv.innerHTML = newInputField;
    updateInputField(newDiv.querySelector("select"), inputType);
}

// 質問タイプを変更
function updateInputField(selectElement, inputType = null) {
    const container = selectElement.closest('.ques-container');
    const inputContainer = container.querySelector('.input-container');
    inputContainer.innerHTML = ""; // 既存のフィールドをクリア

    const selectedInputType = inputType || selectElement.value; // 明示的指定があればそれを優先
    changeQuestionType(container, selectedInputType);
}

// 質問フィールドを変更
function changeQuestionType(container, inputType) {
    const inputContainer = container.querySelector('.input-container');
    const questionIndex = container.dataset.index;

    let inputHtml = "";

    switch (inputType) {
        case "text":
            inputHtml = `
                <input type="hidden" name="ques-type" value="textarea">
                <textarea rows="3" name="ques-text" class="ques-text" placeholder="回答を入力してください" disabled></textarea>
            `;
            break;
        case "checkbox":
        case "radio":
        case "select":
            const inputTypeLabel = inputType === "checkbox" ? "チェックボックス" :
                inputType === "radio" ? "ラジオボタン" : "プルダウン";
            inputHtml = `
                <input type="hidden" name="ques-type" value="${inputType}">
                <div id="options-container-${questionIndex}" class="options-container">
                    ${generateOption(questionIndex, 1, inputType)}
                    ${generateOption(questionIndex, 2, inputType)}
                </div>
                <button type="button" class="option-add" onclick="addOption(this)">＋ ${inputTypeLabel}を追加</button>
            `;
            break;
    }

    inputContainer.innerHTML = inputHtml;
}

// オプション生成関数
function generateOption(questionIndex, optionIndex, inputType) {
    const inputTag = inputType === "checkbox" ? `<input type="checkbox" disabled>` :
        inputType === "radio" ? `<input type="radio" name="radio${questionIndex}" disabled>` :
            `<label>${optionIndex}.</label>`;
    return `
        <div class="option">
            ${inputTag}
            <input type="text" name="option-text-${questionIndex}-${optionIndex}" class="option-text" placeholder="オプション名を入力">
            <button type="button" class="option-del" onclick="deleteOption(this,${questionIndex})">✕</button>
        </div>
    `;
}

// オプションを追加
function addOption(button) {
    const container = button.previousElementSibling;
    const questionIndex = container.id.split('-').pop();
    const optionIndex = container.children.length + 1;
    const inputType = container.closest('.ques-container').querySelector('input[name="ques-type"]').value;

    const newOption = generateOption(questionIndex, optionIndex, inputType);
    container.insertAdjacentHTML("beforeend", newOption);
}

// オプションを削除
function deleteOption(button, Index) {
    const container = button.closest(".options-container");
    button.parentElement.remove();
    updateOptionIndices(container, Index);
}

// 質問を削除
function deleteQuestion(button) {
    const container = button.closest('.ques-container');
    if (container) {
        container.remove(); // 対象の質問を削除
        updateQuestionIndices(); // 削除後、インデックスを再割り当て
    }
}

// 質問インデックスを更新
function updateQuestionIndices() {
    const containers = document.querySelectorAll('.ques-container');
    containers.forEach((container, newIndex) => {
        const oldIndex = container.dataset.index;
        const optionsContainer = container.querySelector(`#options-container-${oldIndex}`);
        const optionsAddButton = container.querySelector(`#options-add-${oldIndex}`);

        // 新しいインデックスを割り当て
        container.dataset.index = newIndex + 1;

        // options-container の ID を更新
        if (optionsContainer) {
            optionsContainer.id = `options-container-${newIndex + 1}`;
            updateOptionIndices(optionsContainer, newIndex + 1);
        }

        // オプション追加ボタンの ID と onclick 属性を更新
        if (optionsAddButton) {
            optionsAddButton.id = `options-add-${newIndex + 1}`;
            const optionAddButton = container.querySelector('.option-add');
            optionAddButton.setAttribute('onclick', `addOption(this, ${newIndex + 1})`);
        }

        // セレクトボックスの onchange 属性を更新
        const selectElement = container.querySelector('select[name="ques-change"]');
        if (selectElement) {
            selectElement.setAttribute('onchange', `updateInputField(this)`);
        }
    });

    questionCounter = containers.length; // 質問数を更新
}

// オプションインデックスを更新
function updateOptionIndices(container, questionIndex) {
    const options = container.querySelectorAll('.option');
    options.forEach((option, newIndex) => {
        const input = option.querySelector(".option-text");
        input.name = `option-text-${questionIndex}-${newIndex + 1}`;

        const label = option.querySelector("label");
        if (label) label.textContent = `${newIndex + 1}.`;

        const deleteButton = option.querySelector(".option-del");
        if (deleteButton) {
            deleteButton.setAttribute("onclick", `deleteOption(this,${questionIndex})`);
        }
    });
}

//画像添付
function triggerFileInput(editid) {
    const fileInput = document.getElementById(`file-input-${editid}`);
    fileInput.click();
}

function previewImage(input, editid) {
    const file = input.files[0];
    const previewContainer = document.getElementById(`image-preview-${editid}`);
    const previewImage = previewContainer.querySelector('.preview-img');
    const deleteButton = previewContainer.querySelector('.image-del-btn');

    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            previewImage.src = e.target.result;
            deleteButton.style.display = 'block'; // 削除ボタンを表示
        };

        reader.readAsDataURL(file);
    }
}

function removeImage(editid) {
    const previewContainer = document.getElementById(`image-preview-${editid}`);
    const previewImage = previewContainer.querySelector('.preview-img');
    const fileInput = document.getElementById(`file-input-${editid}`);
    const deleteButton = previewContainer.querySelector('.image-del-btn');

    // プレビュー画像とファイル入力をリセット
    previewImage.src = "/static/img/def-img.png";
    deleteButton.style.display = 'none';
    fileInput.value = '';
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {
        const errors = validateForm();
        if (errors.length > 0) {
            event.preventDefault(); // フォームの送信を防止
            alert(errors.join("\n")); // エラー内容をまとめてアラートで表示
        }
    });
});

function validateForm() {
    const errors = new Set(); // 重複を防ぐために Set を使用

    // タイトルの検証
    const titleText = document.querySelector(".title-text");
    if (!titleText || titleText.value.trim() === "") {
        errors.add("タイトルが入力されていません。");
        titleText.classList.add("error");
    } else {
        titleText.classList.remove("error");
    }

    // 各質問の検証
    const questionContainers = document.querySelectorAll(".ques-container");
    let questionTitleError = false;
    let optionTextError = false;

    questionContainers.forEach(container => {
        const questionTitle = container.querySelector(".ques-title");
        if (!questionTitle || questionTitle.value.trim() === "") {
            questionTitleError = true;
            questionTitle.classList.add("error");
        } else {
            questionTitle.classList.remove("error");
        }

        const optionTexts = container.querySelectorAll(".option-text");
        optionTexts.forEach(option => {
            if (!option || option.value.trim() === "") {
                optionTextError = true;
                option.classList.add("error");
            } else {
                option.classList.remove("error");
            }
        });
    });

    //質問が一つもないエラーを追加
    if (questionCounter == 0) {
        errors.add("質問を作成してください。");
    }

    // 質問タイトルのエラーを追加
    if (questionTitleError) {
        errors.add("未入力の質問タイトルがあります。");
    }

    // 選択肢のエラーを追加
    if (optionTextError) {
        errors.add("未入力のオプションがあります。");
    }

    return Array.from(errors); // Set を配列に変換して返す
}

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
