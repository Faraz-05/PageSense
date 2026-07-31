const modelDropdown = document.getElementById("model");
const askButton = document.getElementById("askBtn");
const compareButton = document.getElementById("compareBtn");

const questionInput = document.getElementById("question");
const responseBox = document.getElementById("response");
const loading = document.getElementById("loading");

// =====================================
// Load Models
// =====================================

async function loadModels() {

    try {

        const response = await fetch("http://127.0.0.1:8000/models");

        const data = await response.json();

        modelDropdown.innerHTML = "";

        data.models.forEach(model => {

            const option = document.createElement("option");

            option.value = model.id;

            option.textContent = model.name;

            modelDropdown.appendChild(option);

        });

    }

    catch (error) {

        responseBox.textContent = error.message;

    }

}

// =====================================
// Get Page Text
// =====================================

async function getPageText() {

    const [tab] = await chrome.tabs.query({

        active: true,

        currentWindow: true

    });

    return new Promise((resolve, reject) => {

        chrome.tabs.sendMessage(

            tab.id,

            {

                type: "GET_PAGE_TEXT"

            },

            (response) => {

                if (chrome.runtime.lastError) {

                    reject(chrome.runtime.lastError.message);

                    return;

                }

                resolve(response.text);

            }

        );

    });

}

// =====================================
// Ask AI
// =====================================

askButton.addEventListener("click", async () => {

    const question = questionInput.value.trim();

    if (!question) {

        alert("Enter a question");

        return;

    }

    loading.hidden = false;

    responseBox.textContent = "";

    try {

        const pageText = await getPageText();

        const apiResponse = await fetch(

            "http://127.0.0.1:8000/chat",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    question: question,

                    page_text: pageText,

                    model: modelDropdown.value

                })

            }

        );

        const data = await apiResponse.json();

        responseBox.textContent = data.answer;

    }

    catch (error) {

        responseBox.textContent = error;

    }

    loading.hidden = true;

});

// =====================================
// Compare Models
// =====================================

compareButton.addEventListener("click", async () => {

    const question = questionInput.value.trim();

    if (!question) {

        alert("Enter a question");

        return;

    }

    loading.hidden = false;

    responseBox.textContent = "";

    try {

        const pageText = await getPageText();

        const apiResponse = await fetch(

            "http://127.0.0.1:8000/compare",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    question: question,

                    page_text: pageText,

                    model: ""

                })

            }

        );

        const data = await apiResponse.json();

        responseBox.textContent =

`🟢 Gemini

${data.gemini}

--------------------------------------------------

🦙 Llama 3.3

${data.llama}

--------------------------------------------------

🤖 GPT OSS

${data.gptoss}

--------------------------------------------------

💜 Qwen

${data.qwen}`;

    }

    catch (error) {

        responseBox.textContent = error;

    }

    loading.hidden = true;

});

loadModels();