// Listen for messages from the extension
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

    // Check if the popup requested the page text
    if (request.type === "GET_PAGE_TEXT") {

        // Extract all visible text from the webpage
        const pageText = document.body.innerText;

        // Send the extracted text back
        sendResponse({
            text: pageText
        });
    }

});