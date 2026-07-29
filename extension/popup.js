const modelDropdown = document.getElementById("model");
const askButton = document.getElementById("askBtn");

const questionInput = document.getElementById("question");
const responseBox = document.getElementById("response");
const loading = document.getElementById("loading");

// --------------------
// Load Models
// --------------------

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

    catch(error){

        responseBox.textContent = error.message;

    }

}

// --------------------
// Ask AI
// --------------------

askButton.addEventListener("click", async ()=>{

    const question = questionInput.value.trim();

    if(question===""){

        alert("Enter a question");

        return;

    }

    loading.hidden=false;

    responseBox.textContent="";

    const [tab]=await chrome.tabs.query({

        active:true,

        currentWindow:true

    });

    chrome.tabs.sendMessage(

        tab.id,

        {

            type:"GET_PAGE_TEXT"

        },

        async(response)=>{

            if(chrome.runtime.lastError){

                responseBox.textContent=chrome.runtime.lastError.message;

                loading.hidden=true;

                return;

            }

            try{

                const apiResponse=await fetch("http://127.0.0.1:8000/chat",{

                    method:"POST",

                    headers:{

                        "Content-Type":"application/json"

                    },

                    body:JSON.stringify({

                        question:question,

                        page_text:response.text,

                        model:modelDropdown.value

                    })

                });

                const data=await apiResponse.json();

                responseBox.textContent=data.answer;

            }

            catch(error){

                responseBox.textContent=error.message;

            }

            loading.hidden=true;

        }

    );

});

loadModels();