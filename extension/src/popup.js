window.addEventListener("load", () => {
    const input = document.querySelector("#inputUrl")
    input.addEventListener("change", () => {
        saveUrl()
    })
    const button = document.querySelector("#btnSave")
    button.addEventListener("click", () => {
        saveUrl()
    })
})

function getInputContent() {
    const box = document.querySelector("#inputUrl")
    return box.value
}

async function saveUrl() {
    const url = getInputContent()
    await chrome.storage.local.set({"url": url})
}