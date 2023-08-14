const idButton = "hrSendButton"
const idButtonTitle = "hrSendButtonTitle"
const timeRestoreButtonTitle = 5

window.addEventListener("load", () => {
    insertSendButton()
})

async function getServerUrl() {
    return await chrome.storage.local.get("url")
}

function insertSendButton() {
    const container = document.querySelector(".cover-column.lillie")
    const title = document.createElement("h1")
    title.id = idButtonTitle
    const button = document.createElement("a")
    button.append(title)
    button.id = idButton
    button.href = "javascript: void(0)"
    button.onclick = sendRequest
    container.append(button)
    setButtonTitle()
}

function setButtonTitle(title) {
    if (title === null || title === undefined || title === "") {
        title = chrome.i18n.getMessage("messageSendRequest")
    }
    const buttonTitle = document.querySelector(`#${idButtonTitle}`)
    buttonTitle.innerText = title
}

async function sendRequest() {
    const url = (await getServerUrl()).url
    if (url === null || url === undefined || url === "") {
        onRequestFailed(`URL is invalid: ${url}`)
        return false
    }
    setButtonTitle(chrome.i18n.getMessage("messageRequested"))
    const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "url": document.URL
        })
    })
    if (!response.ok) {
        onRequestFailed(`Response: ${response.body}`)
        return false
    }
    onRequestSucceful(`Request successful`)
    return false

}

async function onRequestSucceful(message) {
    setButtonTitle(chrome.i18n.getMessage("messageRequestSuccessful"))
    console.debug(message)
}

async function onRequestFailed(message) {
    setButtonTitle(chrome.i18n.getMessage("messageRequestFailed"))
    setTimeout(setButtonTitle(), timeRestoreButtonTitle * 1000)
    console.warn(message)
}