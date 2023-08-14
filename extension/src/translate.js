window.addEventListener("load", () => {
    translate()
})

async function translate() {
    const elements = document.querySelectorAll(".translate")
    for(let i=0; i < elements.length; i++) {
        let content = "Err: No translation" 
        if (elements[i].hasAttribute("key")) { 
            content = await chrome.i18n.getMessage(elements[i].getAttribute("key"))
        }
        elements[i].innerText = content
    }
}