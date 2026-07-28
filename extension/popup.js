const askButton = document.getElementById("askBtn");

askButton.addEventListener("click", async () => {

    // Get the currently active tab
    const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    // Send a message to content.js
    chrome.tabs.sendMessage(
        tab.id,
        {
            type: "GET_PAGE_TEXT"
        },
        (response) => {

            console.clear();

            console.log("========== PAGE TEXT ==========\n");

            console.log(response.text);

        }
    );

});